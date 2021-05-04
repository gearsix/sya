#!/usr/bin/env python3

import argparse
import subprocess
import re
import os

Timestamp = re.compile(':?\d\d')

class TracklistItem:
    def __init__(self, timestamp, title):
        self.timestamp = timestamp
        self.title = title

def parse_args():
    parser = argparse.ArgumentParser(
        description='download & split audio tracks long youtube videos')
    # arguments
    parser.add_argument('tracklist', metavar='TRACKLIST',
        help='tracklist to split audio by')
    # options
    parser.add_argument('-o', '--output', metavar='PATH', type=str, nargs='?', default='out',
        help='specify the directory to write output files to (default: ./out)')
    parser.add_argument('-f', '--format', type=str, nargs='?', default='mp3',
        help='specify the --audio-format argument to pass to youtube-dl (default: mp3)')
    parser.add_argument('-q', '--quality', type=str, nargs='?', default='320K',
        help='specify the --audio-quality argument to pass to youtube-dl (default: 320K)')
    parser.add_argument('--youtube-dl', metavar='PATH', type=str, nargs='?',
        default='youtube-dl', dest='youtubedl',
        help='path of the "youtube-dl" binary to use')
    parser.add_argument('--ffmpeg', metavar='PATH', type=str, nargs='?',
        default='ffmpeg', dest='ffmpeg',
        help='path of the "ffmpeg" binary to use')
    parser.add_argument('-k', '--keep', action='store_true',
        help='keep any files removed during processing (full video/audio file)')
    return parser.parse_args()

def check_bin(*binaries):
    for b in binaries:
        try:
            subprocess.call([b], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            print(b, 'failed to execute, check it exists in your $PATH.\n'
            'Otherwise you can point to the binary using the relevant optional argument.')

def get_audio(youtubedl, url, format='mp3', quality='320K', keep=True, ffmpeg='ffmpeg'):
    cmd = [youtubedl, url, '--extract-audio', '--audio-format', format,
        '--audio-quality', quality, '-o', 'audio.%(ext)s', '--prefer-ffmpeg']
    if keep == True:
        cmd.append('-k')
    if ffmpeg != 'ffmpeg':
        cmd.append('--ffmpeg-location ', ffmpeg)
    subprocess.call(cmd)
    return './audio.mp3'

def load_tracklist(path):
    tracklist = []
    tracklist_file = open(path, mode = 'r')
    for t in tracklist_file.readlines():
        tracklist.append(t.strip('\n'))
    tracklist_file.close()
    return tracklist

def parse_tracks(tracklist):
    tracks = []
    for lcount, line in enumerate(tracklist):
        sline = line.split(' ', maxsplit=1)
        if Timestamp.match(sline[0]):
            tracks.append(TracklistItem(sline[0], sline[1]))
        else: # assume there's no timestamp, whole line = track title
            tracks.append(TracklistItem(None, line))
    return tracks

def missing_times(tracks):
    missing = []
    for i, t in enumerate(tracks):
        if t.timestamp == None:
            missing.append(i)
    return missing

def find_times(tracks, missing):
    j = 0
    for i, t in enumerate(tracks):
        if i == missing[j]:
            # TODO
            j += 1
    return tracks

def split_tracks(ffmpeg, audio_fpath, tracks, outpath):
    ret = subprocess.run(['ffmpeg', '-v', 'quiet', '-stats', '-i', 'audio.mp3',
        '-f', 'null', '-'], stdout=subprocess.PIPE)
    print(ret)
    for i, t in enumerate(tracks):
        end = 'END'
        if i < len(tracks)-1:
            end = tracks[i+1].timestamp
        subprocess.call(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error',
            '-i', audio_fpath, '-ss', t.timestamp, '-to', end, '-acodec', 'copy',
            '{}/{} - {}.mp3'.format(outpath, str(i).zfill(2), t.title)])
    return

if __name__ == '__main__':
    args = parse_args()
    check_bin(args.youtubedl, args.ffmpeg)
    tracklist = load_tracklist(args.tracklist)
    audio_fpath = get_audio(args.youtubedl, tracklist[0],
            args.format, args.quality, args.keep, args.ffmpeg)
    tracks = parse_tracks(tracklist[1:])
    missing = missing_times(tracks)
    if len(missing) > 0:
        tracks = find_times(tracks, missing)
    os.makedirs(args.output, exist_ok=True)
    split_tracks(args.ffmpeg, audio_fpath, tracks, args.output)

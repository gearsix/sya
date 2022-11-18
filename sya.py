#!/usr/bin/env python3

# std
import argparse
import subprocess
import re
import os
import sys

Shell = False if sys.platform is "win32" else True
Timestamp = re.compile('[\[\(]?((\d+:)+(\d+))[\]\)]?')

class TracklistItem:
    def __init__(self, timestamp, title):
        self.timestamp = timestamp
        self.title = title

# utilities
def error_exit(msg):
    print('exit failure "{}"'.format(msg))
    sys.exit()

def check_bin(*binaries):
    for b in binaries:
        try:
            subprocess.call([b], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=Shell)
        except:
            error_exit('failed to execute {}'.format(b))

# functions
def get_audio(youtubedl, url, outdir, format='mp3', quality='320K', keep=True, ffmpeg='ffmpeg'):
    print('Downloading {} ({}, {})...'.format(url, format, quality))
    fname = '{}/{}'.format(outdir, os.path.basename(outdir), format)
    cmd = [youtubedl, '--newline', '--extract-audio', '--audio-format', format,
        '--audio-quality', quality, '--prefer-ffmpeg', '--ffmpeg-location', ffmpeg,
        '-o', fname + '.%(ext)s']
    if keep == True:
        cmd.append('-k')
    cmd.append(url)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=Shell)
    for line in p.stdout.readlines():
        print('    {}'.format(line.decode('utf-8', errors='ignore').strip()))
    return '{}.{}'.format(fname, format)

def load_tracklist(path):
    tracklist = []
    tracklist_file = open(path, mode = 'r')
    for t in tracklist_file.readlines():
        t = t.strip('\n\t ')
        if len(t) > 0:
            tracklist.append(t)
    tracklist_file.close()
    return tracklist

def parse_tracks(tracklist):
    tracks = []
    for lcount, line in enumerate(tracklist):
        sline = line.split(' ')
        
        timestamp = None
        for l in sline:
            if Timestamp.match(l):
                timestamp = l.strip('[()]')
                sline.remove(l)
        if timestamp == None:
            print('line {}, missing timestamp: "{}"'.format(lcount, line))
        
        title = ' '.join(sline).strip(' ')
        title = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", '', title)
        
        tracks.append(TracklistItem(timestamp, title))
    return tracks

def missing_times(tracks):
    missing = []
    for i, t in enumerate(tracks):
        if t.timestamp == None:
            missing.append(i)
    return missing

def read_tracklen(ffmpeg, track_fpath):
    cmd = [ffmpeg, '-v', 'quiet', '-stats', '-i', track_fpath, '-f', 'null', '-']
    length = '00:00'
    try:
        ret = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=Shell)
        length = str(ret).split('\\r')
        # some nasty string manip. to extract length (printed to stderr)
        if sys.platform == 'win32':
            length = length[len(length)-2].split(' ')[1].split('=')[1][:-3]
        else:
            length = length[len(length)-1].split(' ')[1].split('=')[1][:-3]
        print('Track length: {}'.format(length))
    except:
        error_exit('Failed to find track length, aborting.')
    return length

def split_tracks(ffmpeg, audio_fpath, audio_len, tracks, format='mp3', outpath='out'):    
    print('Splitting...')
    for i, t in enumerate(tracks):
        outfile = '{}/{} - {}.{}'.format(outpath, str(i+1).zfill(2), t.title.strip(' - '), format)
        end = audio_len
        if i < len(tracks)-1:
            end = tracks[i+1].timestamp
        print('     {} ({} - {})'.format(outfile, t.timestamp, end))
        cmd = ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', 
            '-i', audio_fpath, '-ss', t.timestamp, '-to', end,
            '-acodec', 'copy', outfile]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=Shell)
        for line in p.stdout.readlines():
            print('    {}'.format(line.decode('utf-8', errors='ignore').strip()))
    return

# runtime
def parse_args():
    parser = argparse.ArgumentParser(
        description='download & split audio tracks long youtube videos')
    # arguments
    parser.add_argument('tracklist', metavar='TRACKLIST', nargs='?',
        help='tracklist to split audio by')
    # options
    parser.add_argument('-o', '--output',
        metavar='PATH', type=str, nargs='?', dest='output',
        help='specify the directory to write output files to (default: ./out)')
    parser.add_argument('-f', '--format',
        type=str, nargs='?', default='mp3', dest='format',
        help='specify the --audio-format argument to pass to yt-dlp (default: mp3)')
    parser.add_argument('-q', '--quality',
        type=str, nargs='?', default='320K', dest='quality',
        help='specify the --audio-quality argument to pass to yt-dlp (default: 320K)')
    parser.add_argument('--yt-dlp',
        metavar='PATH', type=str, nargs='?', dest='youtubedl',
        help='path of the "yt-dlp" binary to use')
    parser.add_argument('--ffmpeg',
        metavar='PATH', type=str, nargs='?', dest='ffmpeg',
        help='path of the "ffmpeg" binary to use')
    parser.add_argument('-k', '--keep',
        action='store_true', default=False, dest='keep',
        help='keep any files removed during processing (full video/audio file)')
    return parser.parse_args()

def sya(args):
    if args.youtubedl == None:
        args.youtubedl = 'yt-dlp.exe' if sys.platform == 'win32' else 'yt-dlp'
    if args.ffmpeg == None:
        args.ffmpeg = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'

    if check_bin(args.youtubedl, args.ffmpeg) == False:
        error_exit('required binaries are missing')
    if args.tracklist == None or os.path.exists(args.tracklist) == False:
        error_exit('missing tracklist')
    if args.output == None:
        args.output = os.path.splitext(args.tracklist)[0]

    tracklist = load_tracklist(args.tracklist)
    
    audio_fpath = get_audio(args.youtubedl, tracklist[0], args.output,
            args.format, args.quality, args.keep, args.ffmpeg)
    if os.path.exists(audio_fpath) == False:
        error_exit('download failed, aborting')

    
    tracks = parse_tracks(tracklist[1:])
    
    missing = missing_times(tracks)
    if len(missing) > 0:
        error_exit('some tracks are missing timestamps')

    length = read_tracklen(args.ffmpeg, audio_fpath)
    os.makedirs(args.output, exist_ok=True)
    split_tracks(args.ffmpeg, audio_fpath, length, tracks, args.format, args.output)

    if args.keep is False:
        os.remove(audio_fpath)

    print('Success')

if __name__ == '__main__':
    sya(parse_args())

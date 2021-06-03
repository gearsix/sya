#!/usr/bin/env python3

# std
import argparse
import subprocess
import re
import os
import sys
# sya
import gui
# pip
import PyQt5.QtWidgets as pyqt_widgets

Timestamp = re.compile('[\[,\(]?(:?\d{1,2}){3}[\],\)]?')

class TracklistItem:
    def __init__(self, timestamp, title):
        self.timestamp = timestamp
        self.title = title

def log(msg):
    msg = 'sya: ' + msg
    print(msg)

def error_exit(msg):
    log('exit failure "{}"'.format(msg))
    exit()

def parse_args():
    parser = argparse.ArgumentParser(
        description='download & split audio tracks long youtube videos')
    # arguments
    parser.add_argument('tracklist', metavar='TRACKLIST', nargs='?',
        help='tracklist to split audio by')
    # options
    parser.add_argument('-o', '--output', metavar='PATH', type=str, nargs='?',
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
    parser.add_argument('-g', '--gui', action='store_true',
        help='run the gui for configuring options')
    return parser.parse_args()

def check_bin(*binaries):
    for b in binaries:
        try:
            subprocess.call([b], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            print(b, 'failed to execute, check it exists in your $PATH.\n'
            'Otherwise you can point to the binary using the relevant optional argument.')

def get_audio(youtubedl, url, outdir, format='mp3', quality='320K', keep=True, ffmpeg='ffmpeg'):
    log('{} getting {}, {} ({})'.format(youtubedl, format, quality, url))
    fname = '{}/{}'.format(outdir, os.path.basename(outdir), format)
    cmd = [youtubedl, url, '--newline', '--extract-audio', '--audio-format', format,
        '--audio-quality', quality, '--prefer-ffmpeg', '-o', fname + '.%(ext)s']
    if keep == True:
        cmd.append('-k')
    if ffmpeg != 'ffmpeg':
        cmd.append('--ffmpeg-location')
        cmd.append(ffmpeg)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        log(line.decode('utf-8').rstrip('\n'))
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
        timestamp = sline[0]
        for l in sline: # check line in case timestamp is in another element
            if Timestamp.match(l):
                timestamp = l.strip('[()]')
                sline.remove(l)
        title = ' '.join(sline).strip(' ')
        if Timestamp.match(timestamp) == None:
            log('line {}, missing timestamp: "{}"'.format(lcount, line))
            timestamp = None
        tracks.append(TracklistItem(timestamp, title))
    return tracks

def missing_times(tracks):
    missing = []
    for i, t in enumerate(tracks):
        if t.timestamp == None:
            missing.append(i)
    return missing

def split_tracks(ffmpeg, audio_fpath, tracks, format='mp3', outpath='out'):
    log('splitting tracks...')
    cmd = ['ffmpeg', '-v', 'quiet', '-stats', '-i', 'audio.mp3',
        '-f', 'null', '-']
    ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    length = str(ret.stderr).split('\\r')
    # some nasty string manip. to extract length (printed to stderr)
    try:
        length = length[len(length)-1].split(' ')[1].split('=')[1][:-3]
    except:
        log('Failed to find track length, {}'.format(length))
        return
        
    for i, t in enumerate(tracks):
        outfile = '{}/{} - {}.{}'.format(outpath, str(i).zfill(2), t.title, format)
        end = length
        if i < len(tracks)-1:
            end = tracks[i+1].timestamp
        log('\t{} ({} - {})'.format(outfile, t.timestamp, end))
        cmd = ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', 
            '-i', audio_fpath, '-ss', t.timestamp, '-to', end,
            '-acodec', 'copy', outfile]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, b''):
            log(line.decode('utf-8').rstrip('\n'))
    return

def sya(args):
    # validate args
    if check_bin(args.youtubedl, args.ffmpeg) == False:
        error_exit('required binaries are missing')
    if args.tracklist == None or os.path.exists(args.tracklist) == False:
        error_exit('missing tracklist')
    if args.output == None:
        args.output = os.path.splitext(args.tracklist)[0]

    tracklist = load_tracklist(args.tracklist)
    audio_fpath = get_audio(args.youtubedl, tracklist[0], args.output,
            args.format, args.quality, args.keep, args.ffmpeg)
    tracks = parse_tracks(tracklist[1:])

    missing = missing_times(tracks)
    if len(missing) > 0:
        error_exit('some tracks are missing timestamps')

    os.makedirs(args.output, exist_ok=True)
    split_tracks(args.ffmpeg, audio_fpath, tracks, args.format, args.output)
    log('success')

if __name__ == '__main__':
    args = parse_args()
    if args.gui:
        app = pyqt_widgets.QApplication(sys.argv)
        options = gui.SyaGui(sya, args)
        sys.exit(app.exec())
    else:
        sya(args)

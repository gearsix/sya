#!/usr/bin/env python3

import argparse
import subprocess

class TracklistItem:
    def __init__(self, timestamp, title):
        self.timestamp = timestamp
        self.title = title

def parseargs():
    parser = argparse.ArgumentParser(
        description='download & split audio tracks long youtube videos')
    # arguments
    parser.add_argument('tracklist', metavar='TRACKLIST',
        help='tracklist to split audio by')
    # options
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
    parser.add_argument('-k', '--keep-full', action='store_true',
        help='don\'t remove the full audio file after splitting')
    return parser.parse_args()

def checkbin(*binaries):
    for b in binaries:
        try:
            subprocess.call([b], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            print(b, 'failed to execute, check it exists in your $PATH.\n'
            'Otherwise you can point to the binary using the relevant optional argument.')

def getaudio(youtubedl, url, format, quality):
    subprocess.call([youtubedl, url, '-x', '--audio-format', format, '--audio-quality', quality, '-k'])

def readtracks(tracklist_path):
    tracklist_file = open(tracklist_path, mode = 'r')
    tracklist_lines = tracklist.readlines()
    tracklist_file.close()

    tracklist = []
    for line_count, line in enumerate(tracklist_lines):
        if line_count == 0:
            getaudio(args.youtubedl, line, args.format, args.quality)
            continue
        sline = line.split(' ', maxsplit=1)
        tracklist.append(TracklistItem(sline[0], sline[1]))
    return tracklist

if __name__ == '__main__':
    args = parseargs()
    checkbin(args.youtubedl, args.ffmpeg)
    tracklist = readtracks(args.tracklist)

#!/usr/bin/env python3

import argparse
import subprocess
import re
import os
import sys
import PyQt5.QtWidgets as pyqt

Timestamp = re.compile('[\[,\(]?(:?\d{1,2}){3}[\],\)]?')

class TracklistItem:
    def __init__(self, timestamp, title):
        self.timestamp = timestamp
        self.title = title

class GUI:
    def __init__(self, widget):
        self.widget = widget
        self.init_widget()
        self.filepickerbtn = pyqt.QPushButton(widget)
        self.pathlabel = pyqt.QLabel('Tracklist:', widget)
        self.textbox = pyqt.QTextEdit(widget)
        self.init_tracklist()
        self.init_readme()

    def filepicker(self, signal):
        file = pyqt.QFileDialog.getOpenFileName(self.widget, 'Select a tracklist', os.path.expanduser("~"), "text file (*.txt)")
        if file[1] == 'text file (*.txt)':
            self.pathlineditor.setText(file[0])

    def init_widget(self):
        widget.setWindowTitle('sya')
        widget.resize(500, 500)
        #widget.setWindowIcon(pyqt.QIcon('icon.png'))

    def init_tracklist(self):
        #self.filepickerbtn.setIcon(QIcon('logo.png'))
        self.filepickerbtn.move(25, 25)
        self.filepickerbtn.resize(40, 40)
        self.filepickerbtn.clicked.connect(self.filepicker)
        
        self.pathlabel.move(75, 23)
        
        self.pathlineditor = pyqt.QLineEdit(widget)
        self.pathlineditor.move(75, 38)
        self.pathlineditor.resize(400, 25)

    def init_readme(self):
        self.textbox.resize(450, 330)
        self.textbox.move(25, 120)
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText('''
    DESCRIPTION
      sya downloads, converts and splits youtube videos using `youtube-dl` and `ffmpeg`.
      while intended for long audio mixtapes, the tools it uses are quite flexible so
      you could use it to download & split long videos as well.

    TRACKLIST
      TRACKLIST files should be text file that has the URL/v=code of the youtube video to
      download on the first line and the starting timestamp of each section to split, followed
      by the title of that section section.
      Here is an example:

        https://www.youtube.com/watch?v=ors0wpcVDcc
        Los Natas - Brisa Del Desierto [00:00]
        Sleeping Pandora - Through The Maze [02:05]
        Fluidage - Feel Like I Do [12:43]
        My Sleeping Karma - Psilocybe [18:11]
        Daisy Pusher - While Wailing (Only a Part) [26:01]
        The Whirlings - Worries on a Shelf [30:49]
        Arenna - Move Through Figurehead Lights [36:28]
        Ten East - Skyline Pressure [43:32]
        Wooden Shjips - These Shadows [49:24]
        ...etc
    ''')

def log(msg):
    print('sya:', msg)

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
    return parser.parse_args()

def check_bin(*binaries):
    for b in binaries:
        try:
            subprocess.call([b], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            print(b, 'failed to execute, check it exists in your $PATH.\n'
            'Otherwise you can point to the binary using the relevant optional argument.')

def get_audio(youtubedl, url, format='mp3', quality='320K', keep=True, ffmpeg='ffmpeg'):
    log('{} getting {}, {} ({})'.format(youtubedl, format, quality, url))
    cmd = [youtubedl, url, '--extract-audio', '--audio-format', format,
        '--audio-quality', quality, '-o', 'audio.%(ext)s', '--prefer-ffmpeg']
    if keep == True:
        cmd.append('-k')
    if ffmpeg != 'ffmpeg':
        cmd.append('--ffmpeg-location')
        cmd.append(ffmpeg)
    subprocess.call(cmd)
    return './audio.mp3'

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

def split_tracks(ffmpeg, audio_fpath, tracks, outpath):
    log('splitting tracks...')
    cmd = ['ffmpeg', '-v', 'quiet', '-stats', '-i', 'audio.mp3',
        '-f', 'null', '-']
    ret = subprocess.run(cmd, stderr=subprocess.PIPE)
    length = str(ret.stderr).split('\\r')
    # some nasty string manip. to extract length (printed to stderr)
    length = length[len(length)-1].split(' ')[1].split('=')[1][:-3]
        
    for i, t in enumerate(tracks):
        outfile = '{}/{} - {}.mp3'.format(outpath, str(i).zfill(2), t.title)
        end = length
        if i < len(tracks)-1:
            end = tracks[i+1].timestamp
        log('\t{} ({} - {})'.format(outfile, t.timestamp, end))
        cmd = ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error',
            '-i', audio_fpath, '-ss', t.timestamp, '-to', end,
            '-acodec', 'copy', outfile]
        subprocess.call(cmd)
    return

if __name__ == '__main__':
    args = parse_args()
    if len(sys.argv) == 1:
        app = pyqt.QApplication([])
        widget = pyqt.QWidget()
        gui = GUI(widget)
        widget.show()
        sys.exit(app.exec_())
    if check_bin(args.youtubedl, args.ffmpeg) == False:
        error_exit('required binaries are missing')
    tracklist = load_tracklist(args.tracklist)
    audio_fpath = get_audio(args.youtubedl, tracklist[0],
            args.format, args.quality, args.keep, args.ffmpeg)
    tracks = parse_tracks(tracklist[1:])
    missing = missing_times(tracks)
    if len(missing) > 0:
        error_exit('some tracks are missing timestamps')
    if args.output == None:
        args.output = os.path.splitext(args.tracklist)[0]
    os.makedirs(args.output, exist_ok=True)
    split_tracks(args.ffmpeg, audio_fpath, tracks, args.output)
    log('success')

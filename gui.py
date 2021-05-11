
import os
import PyQt5.QtWidgets as pyqt

class Args:
    def __init__(self, args):
        # arg values
        self.tracklist = args.tracklist
        self.format = args.format
        self.quality = args.quality
        self.youtubedl = args.youtubedl
        self.ffmpeg = args.ffmpeg
        self.keep = args.keep
        self.output = args.output
        # static shared values
        self._sizex_btn = 35
        self._sizey_btn = 35
        # widget
        self._widget = pyqt.QWidget()
        # INFO
        self._info_label = pyqt.QLabel('INFO:', self._widget)
        self._info_textedit = pyqt.QTextEdit(self._widget)
        # Tracklist
        self._tracklist_pbtn = pyqt.QPushButton(self._widget)
        self._tracklist_label = pyqt.QLabel('Tracklist:', self._widget)
        self._tracklist_edit = pyqt.QLineEdit(self._widget)
        # youtube-dl
        self._youtube_pbtn = pyqt.QPushButton(self._widget)
        self._youtube_label = pyqt.QLabel('youtube-dl:', self._widget)
        self._youtube_edit = pyqt.QLineEdit(self._widget)
        # ffmpeg
        self._ffmpeg_pbtn = pyqt.QPushButton(self._widget)
        self._ffmpeg_label = pyqt.QLabel('ffmpeg:', self._widget)
        self._ffmpeg_edit = pyqt.QLineEdit(self._widget)
        # misc. options
        self._keep_checkbox = pyqt.QCheckBox('keep whole track', self._widget)
        self._format_label = pyqt.QLabel('Format:', self._widget)
        self._format_combobox = pyqt.QComboBox(self._widget)
        self._quality_label = pyqt.QLabel('Quality:', self._widget)
        self._quality_combobox = pyqt.QComboBox(self._widget)
        # output path
        self._output_pbtn = pyqt.QPushButton(self._widget)
        self._output_label = pyqt.QLabel('Output directory:', self._widget)
        self._output_edit = pyqt.QLineEdit(self._widget)
        # init gui elements
        self._init_widget()
        self._init_readme()
        self._init_tracklist()
        self._init_youtubedl()
        self._init_ffmpeg()
        self._init_keep()
        self._init_format()
        self._init_quality()
        self._init_output()
        # run
        self._widget.show()

    def _getx_btn(self, base):
        return base + 2.5

    def _gety_btn(self, base):
        return base + 5

    def _getx_label(self, base):
        return base + 45
   
    def _gety_label(self, base):
        return base - 1

    def _getx_edit(self, base):
        return base + 45

    def _gety_edit(self, base):
        return base + 16
    
    def _filepicker_tracklist(self, signal):
        file = pyqt.QFileDialog.getOpenFileName(self._widget, 'Select a tracklist',
            os.path.expanduser("~"), "Plain-Text file (*.txt)")
        if file[1] == 'text file (*.txt)':
            self.path_edit.setText(file[0])
    
    def _filepicker_youtubedl(self, signal):
        file = pyqt.QFileDialog.getOpenFileName(self._widget, 'Select youtube-dl executable',
            os.path.expanduser("~"), "Executable file (*)")
        self.youtubedl = file[0]
        self._youtube_edit.setText(file[0])
    
    def _filepicker_ffmpeg(self, signal):
        file = pyqt.QFileDialog.getOpenFileName(self._widget, 'Select ffmpeg executable',
            os.path.expanduser("~"), "Executable file (*)")
        self.ffmpeg = file[0]
        self._ffmpeg_edit.setText(file[0])

    def _filepicker_output(sef, signal):
        file = pyqt.QFileDialog.getOpenFileName(self._widget, 'Select output directory',
            os.path.expanduser("~"), "Directory (*)")
        self.output = file[0]
        self._output_edit.setText(file[0])

    def _keep_toggle(self, signal):
        self.keep = not self.keep

    def _format_change(self, signal):
        self.format = signal

    def _quality_change(self, signal):
        self.quality = signal

    def _init_widget(self):
        self._widget.setWindowTitle('sya')
        #self._widget.setWindowIcon(pyqt.QIcon('icon.png'))
        self._widget.resize(500, 600)

    def _init_tracklist(self):
        y = 375
        x = 25
        #self.filepicker_btn.setIcon(QIcon('logo.png'))
        self._tracklist_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._tracklist_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._tracklist_pbtn.clicked.connect(self._filepicker_tracklist)
        self._tracklist_label.move(self._getx_label(x), self._gety_label(y))
        self._tracklist_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._tracklist_edit.resize(400, 25)
    
    def _init_youtubedl(self):
        y = 420
        x = 25
        self._youtube_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._youtube_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._youtube_pbtn.clicked.connect(self._filepicker_youtubedl)
        self._youtube_label.move(self._getx_label(x), self._gety_label(y))
        self._youtube_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._youtube_edit.resize(165, 25)
        self._youtube_edit.setText(self.youtubedl)

    def _init_ffmpeg(self):
        y = 420
        x = 260
        self._ffmpeg_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._ffmpeg_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._ffmpeg_pbtn.clicked.connect(self._filepicker_ffmpeg)
        self._ffmpeg_label.move(self._getx_label(x), self._gety_label(y))
        self._ffmpeg_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._ffmpeg_edit.resize(165, 25)
        self._ffmpeg_edit.setText(self.ffmpeg)

    def _init_keep(self):
        y = 480
        x = 320
        self._keep_checkbox.move(x, y)
        self._keep_checkbox.toggled.connect(self._keep_toggle)

    def _init_format(self):
        y = 480
        x = 25
        self._format_label.move(x, y+3)
        self._format_combobox.move(x + 70, y)
        self._format_combobox.activated[str].connect(self._format_change)
        self._format_combobox.addItem('mp3')
        self._format_combobox.addItem('mp4')
        self._format_combobox.addItem('wav')
        self._format_combobox.addItem('webm')
        self._format_combobox.addItem('wav')
        self._format_combobox.addItem('m4a')
        self._format_combobox.addItem('ogg')
        self._format_combobox.addItem('aac')
        self._format_combobox.addItem('flv')

    def _init_quality(self):
        y = 510
        x = 25
        self._quality_label.move(x, y+3)
        self._quality_combobox.move(x + 70, y)
        self._quality_combobox.activated[str].connect(self._format_change)
        self._quality_combobox.addItem('0 (better)')
        self._quality_combobox.addItem('1')
        self._quality_combobox.addItem('2')
        self._quality_combobox.addItem('3')
        self._quality_combobox.addItem('4')
        self._quality_combobox.addItem('5')
        self._quality_combobox.addItem('6')
        self._quality_combobox.addItem('7')
        self._quality_combobox.addItem('8')
        self._quality_combobox.addItem('9 (worse)')

    def _init_output(self):
        y = 545
        x = 25
        self._output_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._output_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._output_pbtn.clicked.connect(self._filepicker_output)
        self._output_label.move(self._getx_label(x), self._gety_label(y))
        self._output_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._output_edit.resize(400, 25)
        self._output_edit.setText(self.output)

    def _init_readme(self):
        self._info_label.move(25, 45)
        self._info_textedit.resize(450, 300)
        self._info_textedit.move(25, 65)
        self._info_textedit.setReadOnly(True)
        self._info_textedit.setPlainText(
'''sya uses the tools "youtube-dl" and "ffmpeg" to download videos from youtube, extract & converts their audio them to an audio file, then splits that file based on set timestamps set in a "tracklist" text file (see below).

Select a file to use as the "tracklist" and various options below.

Tracklist files should be text file that has the URL/v=code of the youtube video to
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
    ...etc''')

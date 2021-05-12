
import os
import PyQt5.QtWidgets as pyqt_widgets
import PyQt5.QtGui as pyqt_gui

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
        self._sizex_btn = 30
        self._sizey_btn = 30
        # container widget
        self._widget = pyqt_widgets.QWidget()
        # INFO
        self._info_label = pyqt_widgets.QLabel('INFO:', self._widget)
        self._info_textedit = pyqt_widgets.QTextEdit(self._widget)
        # Tracklist
        self._tracklist_pbtn = pyqt_widgets.QPushButton(self._widget)
        self._tracklist_label = pyqt_widgets.QLabel('Tracklist:', self._widget)
        self._tracklist_edit = pyqt_widgets.QLineEdit(self._widget)
        self._tracklist_help = pyqt_widgets.QPushButton(self._widget)
        # youtube-dl
        #self._youtube_pbtn = pyqt_widgets.QPushButton(self._widget)
        #self._youtube_label = pyqt_widgets.QLabel('youtube-dl:', self._widget)
        #self._youtube_edit = pyqt_widgets.QLineEdit(self._widget)
        # ffmpeg
        #self._ffmpeg_pbtn = pyqt_widgets.QPushButton(self._widget)
        #self._ffmpeg_label = pyqt_widgets.QLabel('ffmpeg:', self._widget)
        #self._ffmpeg_edit = pyqt_widgets.QLineEdit(self._widget)
        # misc. options
        self._keep_checkbox = pyqt_widgets.QCheckBox('keep whole track', self._widget)
        self._format_label = pyqt_widgets.QLabel('Format:', self._widget)
        self._format_combobox = pyqt_widgets.QComboBox(self._widget)
        self._quality_label = pyqt_widgets.QLabel('Quality:', self._widget)
        self._quality_combobox = pyqt_widgets.QComboBox(self._widget)
        # output path
        self._output_pbtn = pyqt_widgets.QPushButton(self._widget)
        self._output_label = pyqt_widgets.QLabel('Output directory:', self._widget)
        self._output_edit = pyqt_widgets.QLineEdit(self._widget)
        # init gui elements
        self._init_widget()
        self._init_readme()
        self._init_tracklist()
        #self._init_youtubedl()
        #self._init_ffmpeg()
        self._init_keep()
        self._init_format()
        self._init_quality()
        self._init_output()
        # run
        self._widget.show()

    def _getx_btn(self, base):
        return base + 2

    def _gety_btn(self, base):
        return base + 10

    def _getx_label(self, base):
        return base + 45
   
    def _gety_label(self, base):
        return base - 1

    def _getx_edit(self, base):
        return base + 45

    def _gety_edit(self, base):
        return base + 20
    
    def _filepicker_tracklist(self, signal):
        file = pyqt_widgets.QFileDialog.getOpenFileName(self._widget, 'Select a tracklist',
            os.path.expanduser("~"), "Plain-Text file (*.txt)")
        if len(file) > 0:
            self.tracklist = file[0]
            self._tracklist_edit.setText(file[0])
    
    def _filepicker_youtubedl(self, signal):
        file = pyqt_widgets.QFileDialog.getOpenFileName(self._widget, 'Select youtube-dl executable',
            os.path.expanduser("~"), "Executable file (*)")
        if len(file) > 0:
            self.youtubedl = file[0]
            self._youtube_edit.setText(file[0])
    
    def _filepicker_ffmpeg(self, signal):
        file = pyqt_widgets.QFileDialog.getOpenFileName(self._widget, 'Select ffmpeg executable',
            os.path.expanduser("~"), "Executable file (*)")
        if len(file) > 0:
            self.ffmpeg = file[0]
            self._ffmpeg_edit.setText(file[0])

    def _filepicker_output(self, signal):
        file = pyqt_widgets.QFileDialog.getExistingDirectory(self._widget, 'Select directory',
            os.path.expanduser('~'))
        if len(file) > 0:
            self.output = file
            self._output_edit.setText(file)

    def _keep_toggle(self, signal):
        self.keep = not self.keep

    def _format_change(self, signal):
        self.format = signal

    def _quality_change(self, signal):
        self.quality = signal

    def _init_widget(self):
        self._widget.setWindowTitle('sya')
        #self._widget.setWindowIcon(pyqt_uwidgets.QIcon('icon.png'))
        self._widget.setFixedSize(400, 470)
        sg = pyqt_widgets.QDesktopWidget().screenGeometry()
        wg = self._widget.geometry()
        self._widget.move(sg.width() / 2 - wg.width() / 2,
            sg.height() / 2 - wg.height() / 2)

    def _init_tracklist(self):
        y = 220
        x = 25
        self._tracklist_pbtn.setIcon(pyqt_gui.QIcon(os.path.dirname(__file__) + '/folder.png'))
        self._tracklist_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._tracklist_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._tracklist_pbtn.clicked.connect(self._filepicker_tracklist)
        self._tracklist_label.move(self._getx_label(x), self._gety_label(y))
        self._tracklist_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._tracklist_edit.resize(300, 25)
        self._tracklist_help.setIcon(pyqt_gui.QIcon(os.path.dirname(__file__) + '/question.png'))
        self._tracklist_help.move(self._getx_label(x) + 280, self._gety_label(y) - 50)

        self._tracklist_help.resize(18, 20)
    
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
        y = 315
        x = 30
        self._keep_checkbox.move(x, y)
        self._keep_checkbox.toggled.connect(self._keep_toggle)

    def _init_format(self):
        y = 275
        x = 30
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
        y = 275
        x = 190
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
        y = 355
        x = 25
        print(__file__)
        self._output_pbtn.setIcon(pyqt_gui.QIcon(os.path.dirname(__file__) + '/folder.png'))
        self._output_pbtn.move(self._getx_btn(x), self._gety_btn(y))
        self._output_pbtn.resize(self._sizex_btn, self._sizey_btn)
        self._output_pbtn.clicked.connect(self._filepicker_output)
        self._output_label.move(self._getx_label(x), self._gety_label(y))
        self._output_edit.move(self._getx_edit(x), self._gety_edit(y))
        self._output_edit.resize(300, 25)
        self._output_edit.setText(self.output)

    def _init_readme(self):
        x = 25
        y = 60
        self._info_label.move(x, y)
#        self._info_textedit.resize(450, 300)
        self._info_textedit.resize(350, 115)
        self._info_textedit.move(x, y + 20)
        self._info_textedit.setReadOnly(True)
        self._info_textedit.setPlainText('''sya is a simple python script that downloads youtube videos, extracts their audio and splits that audio into mutliple tracks using "youtube-dl" and "ffmpeg".

Click "?" for help.''')

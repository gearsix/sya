
import os
import sys
import PyQt5.QtCore as pyqt_core
import PyQt5.QtWidgets as pyqt_widgets
import PyQt5.QtGui as pyqt_gui

class Args:
    def __init__(self, args):
        self.args = args
        self._edits = {}

        self._app = pyqt_widgets.QApplication(sys.argv)
        self._widget = pyqt_widgets.QWidget()
        
        layout = pyqt_widgets.QGridLayout()
        self._tracklistKey = 'Tracklist:'
        layout.addLayout(self._init_filepicker(self._tracklistKey, self._filepicker_tracklist), 0, 0, 1, 3)

        formats = ['mp3', 'flv', 'wav', 'ogg', 'aac']
        layout.addLayout(self._init_combobox('Format:', self._set_format, formats), 1, 0)

        qualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']
        layout.addLayout(self._init_combobox('Quality:', self._set_quality, qualities), 2, 0)

        self.args.quality = '0'
        keep = pyqt_widgets.QCheckBox('keep original', self._widget)
        keep.toggled.connect(self._keep_toggle)
        layout.addWidget(keep, 1, 1, 2, 1)

        self._outputKey = 'Output:'
        layout.addLayout(self._init_filepicker(self._outputKey, self._filepicker_output), 3, 0, 1, 3)

        self._ok = pyqt_widgets.QPushButton('OK')
        self._ok.clicked.connect(self._exit)
        layout.addWidget(self._ok, 4, 1)
        self._check_exit()

        self._widget.setWindowTitle('sya')
        self._widget.setLayout(layout)
        #widget.setWindowIcon(pyqt_widgets.QIcon(''))
        sg = pyqt_widgets.QDesktopWidget().screenGeometry()
        wg = self._widget.geometry()
        self._widget.move(sg.width() / 2 - wg.width() / 2, sg.height() / 2 - wg.height() / 2)
        self._widget.show()
        self._app.exec()

    def _init_filepicker(self, labelText, filepickerFn):
        layout = pyqt_widgets.QHBoxLayout()
        label = pyqt_widgets.QLabel(labelText, self._widget)
        layout.addWidget(label)
        self._edits[labelText] = pyqt_widgets.QLineEdit(self._widget)
        layout.addWidget(self._edits[labelText])
        button_logo = pyqt_gui.QIcon(os.path.dirname(__file__) + '/folder.png')
        button = pyqt_widgets.QPushButton(button_logo, '', self._widget)
        button.clicked.connect(filepickerFn)
        layout.addWidget(button)
        return layout

    def _init_combobox(self, label, setFn, options):
        layout = pyqt_widgets.QHBoxLayout()
        label = pyqt_widgets.QLabel(label, self._widget)
        layout.addWidget(label)
        combo = pyqt_widgets.QComboBox(self._widget)
        combo.activated[str].connect(setFn)
        for opt in options:
            combo.addItem(opt)
        layout.addWidget(label)
        layout.addWidget(combo)
        layout.setStretch(0, 2)
        return layout
    
    def _filepicker_tracklist(self, signal):
        file = pyqt_widgets.QFileDialog.getOpenFileName(self._widget,
            'Select a tracklist', os.path.expanduser("~"), "Plain-Text file (*.txt)")
        if len(file) > 0:
            self.args.tracklist = file[0]
            self._edits[self._tracklistKey].setText(self.args.tracklist)
            if len(self._edits[self._outputKey].text()) == 0:
                self.args.output = os.path.splitext(self.args.tracklist)[0]
                self._edits[self._outputKey].setText(self.args.output)
            self._check_exit()

    def _filepicker_output(self, signal):
        file = pyqt_widgets.QFileDialog.getExistingDirectory(self._widget,
            'Select directory', os.path.expanduser('~'))
        if len(file) > 0:
            self.args.output = file
            self._edits[self._outputKey].setText(file)
        self._check_exit()

    def _set_format(self, format):
        self.args.format = format

    def _set_quality(self, quality):
        self.args.quality = quality[0]

    def _keep_toggle(self):
        self.args.keep = not self.args.keep

    def _check_exit(self):
        if self.args.tracklist != None and os.path.exists(self.args.tracklist) and len(self.args.output) > 0:
            self._ok.setEnabled(True)
        else:
            self._ok.setEnabled(False)

    def _exit(self):
        self.args.gui = False
        self._app.quit()

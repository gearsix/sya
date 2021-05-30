#!/usr/bin/env python3

# std
import os
import sys
import threading
# pip
import PyQt5.QtCore as pyqt_core
import PyQt5.QtWidgets as pyqt_widgets
import PyQt5.QtGui as pyqt_gui

def centerWidget(widget):
    sg = pyqt_widgets.QDesktopWidget().screenGeometry()
    wg = widget.geometry()
    return pyqt_core.QPoint(sg.width() / 2 - wg.width() / 2, sg.height() / 2 - wg.height() / 2)   

class LogStream(pyqt_core.QObject):
    txt = pyqt_core.pyqtSignal(str)

    def write(self, txt):
        self.txt.emit(str(txt))

class SyaGui(pyqt_widgets.QMainWindow):
    def __init__(self, fnSya, args):
        super().__init__()

        self.fnSya = fnSya
        self.args = args
        self._edits = {}

        options = pyqt_widgets.QWidget()
        options.setWindowTitle('sya')
        options = self._init_options(options)
        #options.setWindowIcon(pyqt_options.QIcon(''))
        options.move(centerWidget(options))
        self._options = options

        logs = pyqt_widgets.QPlainTextEdit()
        logs.setReadOnly(True)
        logs.resize(350, 350)
        logs.move(centerWidget(logs))
        self._logs = logs
        sys.stdout = LogStream(txt=self.log)
        
        self._options.show()

    def _init_options(self, options):
        layout = pyqt_widgets.QGridLayout()
        # tracklist
        self._tracklistLabel = 'Tracklist:'
        layout.addLayout(self._init_filepicker(options, self._tracklistLabel, self._filepicker_tracklist), 0, 0, 1, 3)
        # formats
        formats = ['mp3', 'flv', 'wav', 'ogg', 'aac']
        layout.addLayout(self._init_combobox(options, 'Format:', self._set_format, formats), 1, 0)
        # quality
        qualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']
        layout.addLayout(self._init_combobox(options, 'Quality:', self._set_quality, qualities), 2, 0)
        # keep
        self.args.quality = '0'
        keep = pyqt_widgets.QCheckBox('keep original', options)
        keep.toggled.connect(self._keep_toggle)
        layout.addWidget(keep, 1, 1, 2, 1)
        # output
        self._outputLabel = 'Output:'
        layout.addLayout(self._init_filepicker(options, self._outputLabel, self._filepicker_output), 3, 0, 1, 3)
        # ok
        self._ok_btn = pyqt_widgets.QPushButton('OK')
        self._ok_btn.clicked.connect(self._ok)
        layout.addWidget(self._ok_btn, 4, 1)
        self._check_ok()

        options.setLayout(layout)
        return options

    def _init_filepicker(self, widget, labelText, filepickerFn):
        layout = pyqt_widgets.QHBoxLayout()
        # label
        label = pyqt_widgets.QLabel(labelText, widget)
        layout.addWidget(label)
        # line edit
        self._edits[labelText] = pyqt_widgets.QLineEdit(widget)
        layout.addWidget(self._edits[labelText])
        # filepicker btn
        button_logo = pyqt_gui.QIcon(os.path.dirname(__file__) + '/folder.png')
        button = pyqt_widgets.QPushButton(button_logo, '', widget)
        button.clicked.connect(filepickerFn)
        layout.addWidget(button)

        return layout

    def _init_combobox(self, widget, label, setFn, options):
        layout = pyqt_widgets.QHBoxLayout()
        # label
        label = pyqt_widgets.QLabel(label, widget)
        layout.addWidget(label)
        # combobox
        combo = pyqt_widgets.QComboBox(widget)
        combo.activated[str].connect(setFn)
        for opt in options:
            combo.addItem(opt)
        layout.addWidget(combo)

        layout.setStretch(0, 2)
        return layout
    
    def _filepicker_tracklist(self, signal):
        file = pyqt_widgets.QFileDialog.getOpenFileName(self._options,
            'Select a tracklist', os.path.expanduser("~"), "Plain-Text file (*.txt)")
        if len(file) > 0:
            self.args.tracklist = file[0]
            self._edits[self._tracklistLabel].setText(self.args.tracklist)
            if len(self._edits[self._outputLabel].text()) == 0:
                self.args.output = os.path.splitext(self.args.tracklist)[0]
                self._edits[self._outputLabel].setText(self.args.output)
            self._check_ok()

    def _filepicker_output(self, signal):
        file = pyqt_widgets.QFileDialog.getExistingDirectory(self._options,
            'Select directory', os.path.expanduser('~'))
        if len(file) > 0:
            self.args.output = file
            self._edits[self._outputLabel].setText(file)
        self._check_ok()

    def _set_format(self, format):
        self.args.format = format

    def _set_quality(self, quality):
        self.args.quality = quality[0]

    def _keep_toggle(self):
        self.args.keep = not self.args.keep

    def _check_ok(self):
        if self.args.tracklist != None and os.path.exists(self.args.tracklist) and len(self.args.output) > 0:
            self._ok_btn.setEnabled(True)
        else:
            self._ok_btn.setEnabled(False)

    def _ok(self):
        del(self._options)
        self._logs.show()
        threading.Thread(target=self.fnSya, args=[self.args]).start()

    def log(self, msg):
        cursor = self._logs.textCursor()
        cursor.movePosition(pyqt_gui.QTextCursor.End)
        cursor.insertText(msg)
        self._logs.setTextCursor(cursor)
        self._logs.ensureCursorVisible()


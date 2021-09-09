#!/usr/bin/env python3

# std
import os
import sys
import subprocess
# sya
import sya
# pip
import PyQt5.QtCore as qtcore
import PyQt5.QtWidgets as qtwidg
import PyQt5.QtGui as qtgui

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def centerWidget(widget):
    sg = qtwidg.QDesktopWidget().screenGeometry()
    wg = widget.geometry()
    return qtcore.QPoint(round(sg.width() / 2) - round(wg.width() / 2), round(sg.height() / 2) - round(wg.height() / 2))

class LogStream(qtcore.QObject):
    txt = qtcore.pyqtSignal(str)

    def write(self, txt):
        self.txt.emit(str(txt))

class SyaGuiMain(qtcore.QThread):
    def __init__(self, fn, args=None):
        super().__init__()
        self.fn = fn
        self.args = args

    def run(self):
        if self.args != None:
            self.fn(self.args)
        else:
            self.fn()

class SyaGui(qtwidg.QMainWindow):
    def __init__(self, fnSya, args):
        super().__init__()

        self.args = args
        self.fnSya = fnSya
        
        self._edits = {}
        options = qtwidg.QWidget()
        options.setWindowTitle('sya')
        options = self._init_options(options)
        #options.setWindowIcon(pyqt_options.QIcon(''))
        options.move(centerWidget(options))
        self._options = options

        logs = qtwidg.QWidget()
        logs.resize(800, 400)
        logs = self._init_logs(logs)
        logs.move(centerWidget(logs))
        self._logs = logs

        sys.stdout = LogStream(txt=self.log)
        self._options.show()

    def _init_options(self, options):
        layout = qtwidg.QGridLayout()
        # tracklist
        self._tracklistLabel = 'Tracklist:'
        layout.addLayout(self._init_filepicker(options, self._tracklistLabel,
            self._filepicker_tracklist, self.args.tracklist), 0, 0, 1, 3)
        # formats
        formats = ['mp3', 'flv', 'wav', 'ogg', 'aac']
        layout.addLayout(self._init_combobox(options, 'Format:', self._set_format, formats,
            self.args.format), 1, 0)
        # quality
        qualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']
        layout.addLayout(self._init_combobox(options, 'Quality:', self._set_quality, qualities,
            self.args.quality), 2, 0)
        # keep
        keep = qtwidg.QCheckBox('keep original', options)
        if self.args.keep == True:
            keep.setChecked(True)
        keep.toggled.connect(self._keep_toggle, self.args.keep)
        layout.addWidget(keep, 1, 2, 2, 1)
        # output
        self._outputLabel = 'Output:'
        layout.addLayout(self._init_filepicker(options, self._outputLabel, self._filepicker_output,
            self.args.output), 3, 0, 1, 3)
        # quit
        quit_btn = qtwidg.QPushButton('Quit')
        quit_btn.clicked.connect(sys.exit)
        layout.addWidget(quit_btn, 4, 1)
        # ok
        self._ok_btn = qtwidg.QPushButton('OK')
        self._ok_btn.clicked.connect(self._ok)
        layout.addWidget(self._ok_btn, 4, 2)
        self._check_ok()

        options.setLayout(layout)
        return options

    def _init_logs(self, logs):
        layout = qtwidg.QGridLayout()
        # textbox
        logbox = qtwidg.QPlainTextEdit()
        logbox.setReadOnly(True)
        self._logbox = logbox
        layout.addWidget(logbox, 1, 0, 1, 5)
        # cancel
        cancel_btn = qtwidg.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.cancel)
        layout.addWidget(cancel_btn, 2, 0)
        # warning
        warning = qtwidg.QLabel('Be patient, this might take a while.')
        layout.addWidget(warning, 2, 1, 1, 2)
        # done
        self._done_btn = qtwidg.QPushButton('Done')
        self._done_btn.clicked.connect(sys.exit)
        self._done_btn.setEnabled(False)
        layout.addWidget(self._done_btn, 2, 4)

        logs.setLayout(layout)
        return logs

    def _init_filepicker(self, widget, labelText, filepickerFn, default=None, icon='folder'):
        layout = qtwidg.QHBoxLayout()
        # label
        label = qtwidg.QLabel(labelText, widget)
        layout.addWidget(label)
        # line edit
        self._edits[labelText] = qtwidg.QLineEdit(widget)
        if default != None:
            self._edits[labelText].setText(default)
        layout.addWidget(self._edits[labelText])
        # filepicker btn
        button_logo = qtgui.QIcon(resource_path('{}.png'.format(icon)))
        button = qtwidg.QPushButton(button_logo, '', widget)
        button.clicked.connect(filepickerFn)
        layout.addWidget(button)

        return layout

    def _init_combobox(self, widget, label, setFn, options, default):
        layout = qtwidg.QHBoxLayout()
        # label
        label = qtwidg.QLabel(label, widget)
        layout.addWidget(label)
        # combobox
        combo = qtwidg.QComboBox(widget)
        for opt in options:
            combo.addItem(opt)
        if default in options:
            combo.setCurrentIndex(options.index(default))
        combo.activated[str].connect(setFn)
        layout.addWidget(combo)

        layout.setStretch(0, 2)
        return layout
    
    def _filepicker_tracklist(self, signal):
        file = qtwidg.QFileDialog.getOpenFileName(self._options,
            'Select a tracklist', os.path.expanduser("~"), "Plain-Text file (*.txt)")
        if len(file) > 0:
            self.args.tracklist = file[0]
            self._edits[self._tracklistLabel].setText(self.args.tracklist)
            if len(self._edits[self._outputLabel].text()) == 0:
                self.args.output = os.path.splitext(self.args.tracklist)[0]
                self._edits[self._outputLabel].setText(self.args.output)
            self._check_ok()

    def _filepicker_output(self, signal):
        file = qtwidg.QFileDialog.getExistingDirectory(self._options,
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
        if self.args.tracklist != None and self.args.output != None and \
        os.path.exists(self.args.tracklist) and len(self.args.output) > 0:
            self._ok_btn.setEnabled(True)
        else:
            self._ok_btn.setEnabled(False)

    def _ok(self):
        del(self._options)
        del(self._ok_btn)
        self._logs.show()
        self.start_main()

    def log(self, msg):
        cursor = self._logbox.textCursor()
        cursor.insertText(msg)
        self._logbox.setTextCursor(cursor)
        self._logbox.ensureCursorVisible()

    def start_main(self):
        self.main_t = SyaGuiMain(self.fnSya, args=self.args)
        self.check_t = SyaGuiMain(self._check_done)
        self.main_t.start()
        self.check_t.start()

    def _check_done(self):
        while self.main_t.isFinished() != True:
            continue
        self._done_btn.setEnabled(True)

    def cancel(self):
        self.main_t.exit()
        self.check_t.exit()
        sys.exit()

if __name__ == '__main__':
    app = qtwidg.QApplication(sys.argv)
    options = SyaGui(sya, sya.parse_args())
    sys.exit(app.exec_())

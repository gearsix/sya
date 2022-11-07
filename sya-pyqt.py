#!/usr/bin/env python3

# std
import os
import sys
import subprocess
import shutil
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


def center_widget(widget):
    sg = qtwidg.QDesktopWidget().screenGeometry()
    wg = widget.geometry()
    return qtcore.QPoint(
        round(sg.width() / 2) - round(wg.width() / 2),
        round(sg.height() / 2) - round(wg.height() / 2))


class SyaGuiThread(qtcore.QThread):
    def __init__(self, fn, args=None):
        super().__init__()
        self.fn = fn
        self.args = args

    def run(self):
        if self.args is None:
            self.fn()
        else:
            self.fn(self.args)


class SyaGuiLogStream(qtcore.QObject):
    txt = qtcore.pyqtSignal(str)

    def write(self, txt):
        self.txt.emit(str(txt))


def sya_gui_combobox(parent, label, items, default_item, fn_update):
    label = qtwidg.QLabel(label, parent)

    combobox = qtwidg.QComboBox(parent)
    for i in items:
        combobox.addItem(i)
    if default_item in items:
        combobox.setCurrentIndex(items.index(default_item))
    combobox.activated[str].connect(fn_update)

    layout = qtwidg.QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(combobox)
    layout.setStretch(0, 2)
    
    return layout


def sya_gui_filepicker(parent, label, fn_select, fn_update, default_value='', icon=''):
    label = qtwidg.QLabel(label, parent)

    lineEdit = qtwidg.QLineEdit(parent)
    lineEdit.setText(default_value)
    lineEdit.textChanged.connect(fn_update)

    btnIcon = qtgui.QIcon(resource_path('{}.png'.format(icon)))
    btn = qtwidg.QPushButton(btnIcon, '', parent)
    btn.clicked.connect(fn_select)
    
    layout = qtwidg.QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(lineEdit)
    layout.addWidget(btn)
    
    return layout, lineEdit


class SyaGui(qtwidg.QMainWindow):
    def __init__(self, fn_sya, fn_sya_args):
        super().__init__()

        self.fnSya = fn_sya
        self.fnSyaArgs = fn_sya_args

        self.availableFormats = ['mp3', 'flv', 'wav', 'ogg', 'aac']
        self.availableQualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']

        self._init_options_value()
        self._init_options()
        self._init_logger()

        self.optionsQuit.clicked.connect(self.quit)
        self.optionsOk.clicked.connect(self.main)
        self.loggerCancel.clicked.connect(self.cancel)
        self.loggerDone.clicked.connect(self.done)

        sys.stdout = SyaGuiLogStream(txt=self.log)
        self.running = 0

    # Runtime Methods        
    def log(self, msg):
        self.loggerTextbox.moveCursor(qtgui.QTextCursor.End)
        self.loggerTextbox.textCursor().insertText(msg)
        self.loggerTextbox.ensureCursorVisible()

    def cancel(self):
        if self.running > 0:
            self.main_t.terminate()
            self.main_t.wait()
            self.running -= 1
        if os.path.exists(self.fnSyaArgs.output):
            shutil.rmtree(self.fnSyaArgs.output)
        self.logger.hide()
        self.loggerTextbox.clear()

    def quit(self):
        if self.running > 0:
            self.cancel()
        del self.logger
        del self.options
        sys.exit()
        
    def done(self):
        self.set_tracklist('')
        self.set_output('')
        self.optionsOk.setEnabled(True)
        self.logger.hide()
        self.loggerTextbox.clear()
        
    def preMain(self):
        self.optionsOk.setEnabled(False)
        self.loggerDone.setEnabled(False)
        
    def postMain(self):
        self.loggerDone.setEnabled(True)

    def main(self):
        self.fnSyaArgs.tracklist = self.optionsValue[self.tracklistLabel]
        self.fnSyaArgs.format = self.optionsValue[self.formatLabel]
        self.fnSyaArgs.quality = self.optionsValue[self.qualityLabel]
        self.fnSyaArgs.keep = self.optionsValue[self.keepLabel]
        self.fnSyaArgs.output = self.optionsValue[self.outputLabel]
        
        self.main_t = SyaGuiThread(self.fnSya, self.fnSyaArgs)
        self.main_t.started.connect(self.preMain)
        self.main_t.finished.connect(self.postMain)
        
        self.logger.setWindowTitle(self.fnSyaArgs.output)
        self.logger.show()
        self.main_t.start()

    # optionsValue
    def _init_options_value(self):
        self.tracklistLabel = 'Tracklist:'
        self.formatLabel = 'Format:'
        self.qualityLabel = 'Quality:'
        self.keepLabel = 'Keep unsplit audio file'
        self.outputLabel = 'Output:'
        self.optionsValue = {
            self.tracklistLabel: self.fnSyaArgs.tracklist,
            self.formatLabel: self.fnSyaArgs.format,
            self.qualityLabel: self.fnSyaArgs.quality,
            self.keepLabel: self.fnSyaArgs.keep,
            self.outputLabel: self.fnSyaArgs.output
        }

    # options
    def _init_options(self):
        self.options = qtwidg.QWidget()
        self.optionsOk = qtwidg.QPushButton('OK')
        self.optionsQuit = qtwidg.QPushButton('Quit')
        
        layout = qtwidg.QGridLayout()
        layout.addLayout(self._init_options_tracklist(), 0, 0, 1, 3)
        layout.addLayout(self._init_options_format(), 1, 0)
        layout.addLayout(self._init_options_quality(), 2, 0)
        layout.addLayout(self._init_options_output(), 3, 0, 1, 3)
        layout.addWidget(self._init_options_keep(), 1, 2, 2, 1)
        layout.addWidget(self.optionsQuit, 4, 1)
        layout.addWidget(self.optionsOk, 4, 2)
        
        self.update_options_ok()
        
        self.options.setLayout(layout)
        self.options.setWindowTitle('sya (split youtube audio)')
        self.options.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        self.options.move(center_widget(self.options))
        self.options.show()

    def _init_options_tracklist(self):
        label = self.tracklistLabel
        layout, self.optionsTracklist = sya_gui_filepicker(self.options, label, self.select_tracklist, self.set_tracklist, self.optionsValue[label], 'file')
        return layout

    def _init_options_format(self):
        label = self.formatLabel
        self.optionsFormat = sya_gui_combobox(self.options, label, self.availableFormats, self.optionsValue[label], self.set_format)
        return self.optionsFormat

    def _init_options_quality(self):
        label = self.qualityLabel
        self.optionsQuality = sya_gui_combobox(self.options, label, self.availableQualities, self.optionsValue[label], self.set_quality)
        return self.optionsQuality

    def _init_options_keep(self):
        label = self.keepLabel
        self.optionsKeep = qtwidg.QCheckBox(label, self.options)
        if self.optionsValue[label]:
            self.optionsKeep.setChecked(True)
        self.optionsKeep.toggled.connect(self.toggle_keep)
        return self.optionsKeep

    def _init_options_output(self):
        label = self.tracklistLabel
        layout, self.optionsOutput = sya_gui_filepicker(self.options, label, self.select_output, self.set_output, self.optionsValue[label], 'folder')
        return layout

    # Options Callbacks
    def select_tracklist(self):
        dialog = qtwidg.QFileDialog()
        dialog.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        file = dialog.getOpenFileName(self.options, 'Select a tracklist', os.path.expanduser('~'), "Text file (*.txt)", None, qtwidg.QFileDialog.DontUseNativeDialog)
        if len(file) > 0:
            self.set_tracklist(file[0])

    def set_tracklist(self, text):
        self.optionsValue[self.tracklistLabel] = text
        self.optionsTracklist.setText(text)
        self.set_output(os.path.splitext(text)[0])
        self.update_options_ok()

    def select_output(self):
        dialog = qtwidg.QFileDialog()
        dialog.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        file = dialog.getExistingDirectory(self.options, 'Select directory', os.path.expanduser('~'), qtwidg.QFileDialog.DontUseNativeDialog)
        if len(file) > 0:
            self.set_output(file[0])

    def set_output(self, text):
        self.optionsValue[self.outputLabel] = text
        self.optionsOutput.setText(text)
        self.update_options_ok()

    def set_format(self, option):
        if option not in self.availableFormats:
            return
        self.optionsValue[self.formatLabel] = option
        self.update_options_ok()

    def set_quality(self, option):
        if option not in self.availableQualities:
            return
        self.optionsValue[self.qualityLabel] = option
        self.update_options_ok()

    def toggle_keep(self):
        self.optionsValue[self.keepLabel] = not self.optionsValue[self.keepLabel]
        self.update_options_ok()

    def update_options_ok(self):
        tracklist = self.optionsValue[self.tracklistLabel]
        output = self.optionsValue[self.outputLabel]
        if os.path.exists(tracklist) and len(output) > 0:
            self.optionsOk.setEnabled(True)
        else:
            self.optionsOk.setEnabled(False)

    # Logger Widget
    def _init_logger(self):
        layout = qtwidg.QGridLayout()
        layout.addWidget(self._init_logger_textbox(), 1, 0, 1, 5)
        layout.addWidget(self._init_logger_cancel(), 2, 0)
        layout.addWidget(self._init_logger_warning(), 2, 1, 1, 2)
        layout.addWidget(self._init_logger_done(), 2, 4)
        
        self.logger = qtwidg.QWidget()
        self.logger.setLayout(layout)
        self.logger.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        self.logger.resize(800, 400)
        self.logger.move(center_widget(self.logger))

    def _init_logger_textbox(self):
        self.loggerTextbox = qtwidg.QPlainTextEdit()
        self.loggerTextbox.setReadOnly(True)
        return self.loggerTextbox

    def _init_logger_cancel(self):
        self.loggerCancel = qtwidg.QPushButton('Cancel')
        return self.loggerCancel

    @staticmethod
    def _init_logger_warning():
        return qtwidg.QLabel('This might take a while. You can click "Done" when it\'s finished.')

    def _init_logger_done(self):
        self.loggerDone = qtwidg.QPushButton('Done')
        self.loggerDone.setEnabled(False)
        return self.loggerDone


# Main
if __name__ == '__main__':
    app = qtwidg.QApplication(sys.argv)
    
    args = sya.parse_args()
    if args.tracklist is None:
        args.tracklist = ''
    if args.output is None:
        args.output = ''
    if args.youtubedl == None:
        args.youtubedl = resource_path('yt-dlp') if sys.platform != 'win32' else resource_path('yt-dlp.exe')
    if args.ffmpeg == None:
        args.youtubedl = resource_path('ffmpeg') if sys.platform != 'win32' else resource_path('ffmpeg.exe')
    gui = SyaGui(sya.sya, args)

    sys.exit(app.exec_())

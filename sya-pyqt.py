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


def new_combobox(parent, items, default_item, fn_update):
    combobox = qtwidg.QComboBox(parent)
    for i in items:
        combobox.addItem(i)
    if default_item in items:
        combobox.setCurrentIndex(items.index(default_item))
    combobox.activated[str].connect(fn_update)

    layout = qtwidg.QHBoxLayout()
    layout.addWidget(combobox)

    return layout


def new_filepicker(parent, fn_select, fn_update, default_value='', icon=''):
    line_edit = qtwidg.QLineEdit(parent)
    line_edit.setText(default_value)
    line_edit.textChanged.connect(fn_update)

    btn_icon = qtgui.QIcon(resource_path('{}.png'.format(icon)))
    btn = qtwidg.QPushButton(btn_icon, '', parent)
    btn.clicked.connect(fn_select)

    layout = qtwidg.QHBoxLayout()
    layout.addWidget(line_edit)
    layout.addWidget(btn)

    return layout, line_edit


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


class SyaGuiOptions(qtwidg.QWidget):
    def __init__(self, init_values):
        super().__init__()
        self.labels = {
            'tracklist': 'Tracklist:',
            'format': 'Format:',
            'quality': 'Quality:',
            'keep': 'Keep unsplit file',
            'output': 'Output:'}
        self.values = {
            'tracklist': init_values.tracklist,
            'format': init_values.format,
            'quality': init_values.quality,
            'keep': init_values.keep,
            'output': init_values.output}

        self.availableFormats = ['mp3', 'wav', 'ogg', 'aac']
        self.availableQualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']

        self._layout = qtwidg.QGridLayout()
        self.tracklist = self._init_tracklist()
        self.format = self._init_format()
        self.quality = self._init_quality()
        self._init_spacer()
        self.keep = self._init_keep()
        self.output = self._init_output()
        self.help = self._init_help()
        self.ok = self._init_ok()
        self.setLayout(self._layout)

        self.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        self.setWindowTitle('sya (split youtube audio)')
        self.setFixedSize(int(self.width() / 1.5), self.minimumHeight())
        self.show()

    def _init_tracklist(self):
        label = self.labels['tracklist']
        self._layout.addWidget(qtwidg.QLabel(label, self), 0, 0, 1, 3)
        layout, line_edit = new_filepicker(self, self.select_tracklist, self.set_tracklist, self.values['tracklist'],
                                           'file')
        self._layout.addLayout(layout, 0, 1, 1, 3)
        return line_edit

    def _init_format(self):
        label = self.labels['format']
        self._layout.addWidget(qtwidg.QLabel(label, self), 1, 0)
        combo_box = new_combobox(self, self.availableFormats, self.values['format'], self.set_format)
        self._layout.addLayout(combo_box, 1, 1)
        return combo_box

    def _init_quality(self):
        label = self.labels['quality']
        self._layout.addWidget(qtwidg.QLabel(label, self), 2, 0)
        combo_box = new_combobox(self, self.availableQualities, self.values['quality'], self.set_quality)
        self._layout.addLayout(combo_box, 2, 1)
        return combo_box

    def _init_spacer(self):
        size_policy = qtwidg.QSizePolicy.Expanding
        spacer = qtwidg.QSpacerItem(int(self.width() / 4), 0, size_policy, size_policy)
        self._layout.addItem(spacer)

    def _init_keep(self):
        label = self.labels['keep']
        checkbox = qtwidg.QCheckBox(label, self)
        if self.values['keep']:
            checkbox.setChecked(True)
        self._layout.addWidget(checkbox, 1, 3, 2, 1)
        checkbox.toggled.connect(self.toggle_keep)
        return checkbox

    def _init_output(self):
        label = self.labels['output']
        self._layout.addWidget(qtwidg.QLabel(label, self), 3, 0)
        layout, line_edit = new_filepicker(self, self.select_output, self.set_output, self.values['output'], 'folder')
        self._layout.addLayout(layout, 3, 1, 1, 3)
        return line_edit

    def _init_help(self):
        btn = qtwidg.QPushButton('Help')
        self._layout.addWidget(btn, 4, 0)
        return btn

    def _init_ok(self):
        btn = qtwidg.QPushButton('OK')
        self._layout.addWidget(btn, 4, 3)
        return btn

    # callbacks
    def select_tracklist(self):
        dialog = qtwidg.QFileDialog()
        dialog.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        file = dialog.getOpenFileName(self, 'Select a tracklist', os.path.expanduser('~'), "Text file (*.txt)", None,
                                      qtwidg.QFileDialog.DontUseNativeDialog)
        if len(file) > 0:
            self.set_tracklist(file[0])

    def set_tracklist(self, text):
        self.values['tracklist'] = text
        self.tracklist.setText(text)
        self.set_output(os.path.splitext(text)[0])
        self.update_ok()

    def select_output(self):
        dialog = qtwidg.QFileDialog()
        dialog.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        file = dialog.getExistingDirectory(self, 'Select directory', os.path.expanduser('~'),
                                           qtwidg.QFileDialog.DontUseNativeDialog)
        if len(file) > 0:
            self.set_output(file)

    def set_output(self, text):
        self.values['output'] = text
        self.output.setText(text)
        self.update_ok()

    def set_format(self, option):
        if option in self.availableFormats:
            self.values['format'] = option
            self.update_ok()

    def set_quality(self, option):
        if option in self.availableQualities:
            self.values['quality'] = option
            self.update_ok()

    def toggle_keep(self):
        self.values['keep'] = not self.values['keep']
        self.update_ok()

    def update_ok(self):
        self.ok.setEnabled(os.path.exists(self.values['tracklist']) and len(self.values['output']) > 0)


class SyaGuiHelp(qtwidg.QTextEdit):
    def __init__(self, options):
        super().__init__()
        self.options = options
        self.setWindowIcon(qtgui.QIcon(resource_path('sya.png')))
        self.setWindowTitle('sya help')
        with open(resource_path("HELP.md")) as f:
            self.setMarkdown(f.read())
        self.resize(500, 500)
        self.setReadOnly(True)

    def show(self):
        self.move(self.options.x() - self.options.width() - 100, self.options.y() - self.options.height())
        super().show()
        self.options.help.setEnabled(False)

    def hide(self, signal):
        super().hide()
        self.options.help.setEnabled(True)


class SyaGui(qtwidg.QMainWindow):
    def __init__(self, fn_sya, fn_sya_args):
        super().__init__()

        self.fnSya = fn_sya
        self.fnSyaArgs = fn_sya_args

        self.options = SyaGuiOptions(self.fnSyaArgs)
        self.help = SyaGuiHelp(self.options)

        self.options.closeEvent = self.quit
        self.options.help.clicked.connect(self.help.show)
        self.options.ok.clicked.connect(self.main)
        self.help.closeEvent = self.help.hide

        self._init_logger()
        self.loggerCancel.clicked.connect(self.cancel)
        self.loggerDone.clicked.connect(self.done)

        sys.stdout = SyaGuiLogStream(txt=self.log)
        self.running = 0

    # runtime Methods
    def log(self, msg):
        self.loggerTextbox.moveCursor(qtgui.QTextCursor.End)
        self.loggerTextbox.textCursor().insertText(msg)
        self.loggerTextbox.ensureCursorVisible()

    def quit(self, event):
        sys.stdout = sys.__stdout__
        if self.running > 0:
            self.cancel()
        self.options.close()
        self.logger.close()
        self.close()

    def cancel(self):
        if self.running > 0:
            self.main_t.terminate()
            self.main_t.wait()
            self.running -= 1
        self.logger.hide()
        self.loggerTextbox.clear()

    def done(self):
        self.set_tracklist('')
        self.set_output('')
        self.optionsOk.setEnabled(True)
        self.logger.hide()
        self.loggerTextbox.clear()

    # main runtime functions that call 'sya.py'
    def preMain(self):
        x = self.options.x() + self.options.width() + 50
        y = self.options.y() - self.options.height()
        self.logger.move(x, y)
        self.logger.setWindowTitle('sya {}'.format(self.fnSyaArgs.output))
        self.options.ok.setEnabled(False)
        self.loggerDone.setEnabled(False)

    def postMain(self):
        self.loggerDone.setEnabled(True)

    def main(self):
        self.fnSyaArgs.tracklist = self.options.values['tracklist']
        self.fnSyaArgs.format = self.options.values['format']
        self.fnSyaArgs.quality = self.options.values['quality']
        self.fnSyaArgs.keep = self.options.values['keep']
        self.fnSyaArgs.output = self.options.values['output']

        self.main_t = SyaGuiThread(self.fnSya, self.fnSyaArgs)
        self.main_t.started.connect(self.preMain)
        self.main_t.finished.connect(self.postMain)

        self.logger.show()
        self.running += 1
        self.main_t.start()

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

    def _init_logger_textbox(self):
        self.loggerTextbox = qtwidg.QPlainTextEdit()
        self.loggerTextbox.setReadOnly(True)
        self.loggerTextbox.setLineWrapMode(qtwidg.QPlainTextEdit.NoWrap)
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
    if args.youtubedl is None:
        args.youtubedl = resource_path('yt-dlp') if sys.platform != 'win32' else resource_path('yt-dlp.exe')
    if args.ffmpeg is None:
        args.ffmpeg = resource_path('ffmpeg') if sys.platform != 'win32' else resource_path('ffmpeg.exe')
    gui = SyaGui(sya.sya, args)

    sys.exit(app.exec_())

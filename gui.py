
import os
import PyQt5.QtWidgets as pyqt_widgets
import PyQt5.QtGui as pyqt_gui

class Args:
    def __init__(self, args):
        self.args = args
        self.done = False
        self._widget = pyqt_widgets.QWidget()
        self._edits = {}
        # elements
        layout = pyqt_widgets.QGridLayout()
        self._tracklistKey = 'Tracklist:'
        layout.addLayout(self._init_filepicker(self._tracklistKey, self._filepicker_tracklist), 0, 0, 1, 3)
        formats = ['mp3', 'flv', 'wav', 'ogg', 'aac']
        layout.addLayout(self._init_combobox('Format:', self._set_format, formats), 1, 0)
        qualities = ['0 (better)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (worse)']
        layout.addLayout(self._init_combobox('Quality:', self._set_quality, qualities), 2, 0)
        keep = pyqt_widgets.QCheckBox('keep original', self._widget)
        keep.toggled.connect(self._keep_toggle)
        self._outputKey = 'Output:'
        layout.addWidget(keep, 2, 1)
        layout.addLayout(self._init_filepicker(self._outputKey, self._filepicker_output), 3, 0, 1, 3)
        done_btn = pyqt_widgets.QPushButton('OK')
        layout.addWidget(done_btn)
        # container
        self._widget.setLayout(layout)
        self._widget.show()

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
            self.tracklist = file[0]
            self._edits[self._tracklistKey].setText(file[0])

    def _filepicker_output(self, signal):
        file = pyqt_widgets.QFileDialog.getExistingDirectory(self._widget,
            'Select directory', os.path.expanduser('~'))
        if len(file) > 0:
            self.args.output = file
            self._edits[self._outputKey].setText(file)

    def _set_format(self, signal):
        self.args.format = signal

    def _set_quality(self, signal):
        self.args.quality = signal

    def _keep_toggle(self, signal):
        self.args.keep = not self.args.keep

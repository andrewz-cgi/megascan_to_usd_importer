from PySide2.QtWidgets import QMainWindow, QSizePolicy, QWidget, QVBoxLayout

from .widgets import QuickMegascanWidget, UsdBuilderWidget

class MainWindow(QMainWindow):

    TITLE = 'USD Importer'
    VERSION = '0.1'

    def __init__(self, parent=None, debug=True):

        self.debug = debug

        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(f'{self.TITLE} {self.VERSION}')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(400, 350)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        quick_megascan_widget = QuickMegascanWidget()
        self.main_layout.addWidget(quick_megascan_widget)

        asd = UsdBuilderWidget()
        self.main_layout.addWidget(asd)
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

import glob, os
import hou

from ..modules import megascan_importer as megascan
from ..modules import usd_importer as importer

class UsdImporterUi(QMainWindow):

    def __init__(self, parent=None, debug=True):
        
        self.debug = debug
        self.asset_info = {}

        super(UsdImporterUi, self).__init__(parent)

        self.setWindowTitle("Usd importer 0.1")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(400, 350)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        megascan_groupbox = QGroupBox("Megascan import")
        megascan_groupbox_layout = QVBoxLayout(megascan_groupbox)
        #
        megascan_path_layout = QHBoxLayout()
        self.megascan_asset_folder_line = QLineEdit()
        self.megascan_asset_folder_line.setPlaceholderText("Select asset folder ...")
        megascan_path_btn = QPushButton("Load")
        megascan_path_btn.clicked.connect(self.on_megascan_load_asset)
        megascan_path_layout.addWidget(self.megascan_asset_folder_line)
        megascan_path_layout.addWidget(megascan_path_btn)
        megascan_groupbox_layout.addLayout(megascan_path_layout)
        #
        megascan_quick_btn = QPushButton("Quick import")
        megascan_quick_btn.clicked.connect(self.on_megascan_quick_export)
        megascan_groupbox_layout.addWidget(megascan_quick_btn)
        #

        main_layout.addWidget(megascan_groupbox)
    
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_megascan_load_asset(self):

        asset_info_path = hou.ui.selectFile(hou.getenv("HOME"), title="Asset Folder", file_type=hou.fileType.Directory)

        if asset_info_path:
            self.megascan_asset_folder_line.setText(asset_info_path)

    def on_megascan_quick_export(self):

        asset_folder_path = hou.expandString(self.megascan_asset_folder_line.text())

        if not asset_folder_path:
            self.hou_error_message("Specify a target folder for the megascan asset")
            return

        json_files_list = glob.glob(os.path.join(asset_folder_path, '*.json'))
        if not json_files_list or len(json_files_list) != 1:
            self.hou_error_message("Folder {} does not contain a valid json file".format(asset_folder_path))
            return

        megascan_asset_info = megascan.format_asset_info(json_files_list[0])
        importer.megascan_usd_import(megascan_asset_info)

    def hou_error_message(self, message, title=None):

        hou.ui.displayMessage(message, severity=hou.severityType.Error, title="Error" if not title else title)
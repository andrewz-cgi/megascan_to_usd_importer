from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QPushButton
import glob, os

import hou

class QuickMegascanWidget(QGroupBox):

    def __init__(self, parent=None):

        super(QuickMegascanWidget, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.setTitle('Quick Megascan import')
        self.setLayout(self.main_layout)

        megascan_asset_folder_path_layout = QHBoxLayout()
        #
        self.megascan_asset_folder_line = QLineEdit()
        self.megascan_asset_folder_line.setPlaceholderText('Select megascan asset folder ...')
        #
        megascan_asset_folder_btn = QPushButton("Load")
        megascan_asset_folder_btn.clicked.connect(self.on_megascan_load_asset)
        #
        megascan_asset_folder_path_layout.addWidget(self.megascan_asset_folder_line)
        megascan_asset_folder_path_layout.addWidget(megascan_asset_folder_btn)
        #
        self.main_layout.addLayout(megascan_asset_folder_path_layout)
        #
        megascan_quick_btn = QPushButton("Quick import")
        megascan_quick_btn.clicked.connect(self.on_megascan_quick_export)
        self.main_layout.addWidget(megascan_quick_btn)

    def on_megascan_load_asset(self):

        asset_info_path = hou.ui.selectFile(hou.getenv("HOME"), title="Asset Folder", file_type=hou.fileType.Directory)

        if asset_info_path:
            self.megascan_asset_folder_line.setText(asset_info_path)

    def on_megascan_quick_export(self):

        asset_folder_path = hou.expandString(self.megascan_asset_folder_line.text())

        if not asset_folder_path:
            hou.ui.displayMessage('Specify a target folder for the megascan asset', severity=hou.severityType.Error, title="Error")
            return

        json_files_list = glob.glob(os.path.join(asset_folder_path, '*.json'))
        if not json_files_list or len(json_files_list) != 1:
            hou.ui.displayMessage(f'Folder {asset_folder_path} does not contain a valid json file', severity=hou.severityType.Error, title="Error")
            return
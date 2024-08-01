import glob, os, json, shutil
import hou

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from .new_ui_widgets.settings.settings_tabs_widget import SettingsTabsWidget

from ..modules import megascan_importer as megascan
from ..modules import usd_importer as importer

from ..types.preset import UsdImpotertPreset, UsdImpotertPresetEncoder, UsdImpotertPresetDecoder
from ..types.settings import UsdImporterSettings

DEBUG = True

class NewUI(QMainWindow):

    """
    Main User Interfece for the import USD tool.

    Attributes:

        asset_info: megascan.MegascanAsset -> A class containting the parsed megascan asset json information.

        active_preview: str -> The active usd preview, usualy the last that was build.

        active_preview: str -> The active usd preview, usualy the last that was build.
        
        active_preview: str -> The active usd preview, usualy the last that was build.

    """

    asset_info: megascan.MegascanAsset = None
    active_preview: str = None
    active_component_output = None
    last_selected_asset_folder = None

    def __init__(self, parent=None, debug=DEBUG):
        
        self.debug = debug

        super(NewUI, self).__init__(parent)

        self.setWindowTitle("Usd importer 0.1")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(600, 525)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        asset_folder_layout =  QHBoxLayout()
        asset_folder_layout.addWidget(QLabel('Original Asset Folder'))
        self.asset_folder_line = QLineEdit()
        self.asset_folder_line.mousePressEvent = self.on_asset_folder_line_mouse_press
        asset_folder_layout.addWidget(self.asset_folder_line)
        self.asset_folder_btn = QPushButton('Load')
        asset_folder_layout.addWidget(self.asset_folder_btn)
        self.asset_folder_btn.clicked.connect(self.on_megascan_load_asset)
        main_layout.addLayout(asset_folder_layout)

        destination_folder =  QHBoxLayout()
        destination_folder.addWidget(QLabel('Destination Save Folder'))
        self.destination_folder_line = QLineEdit()
        self.destination_folder_line.setPlaceholderText('Same as asset folder...')
        self.destination_folder_line.mousePressEvent = self.on_destination_folder_line_mouse_press
        destination_folder.addWidget(self.destination_folder_line)
        self.change_save_location_btn = QPushButton('Change Directory')
        self.change_save_location_btn.clicked.connect(self.on_change_save_directory)
        destination_folder.addWidget(self.change_save_location_btn)
        """
        self.save_to_disk_btn = QPushButton('Save to disk')
        self.save_to_disk_btn.setEnabled(False)
        destination_folder.addWidget(self.save_to_disk_btn)
        """
        main_layout.addLayout(destination_folder)

        asset_name =  QHBoxLayout()
        asset_name.addWidget(QLabel('Asset name'))
        self.asset_name_line = QLineEdit()
        self.asset_name_line.setPlaceholderText('Same as loaded asset ...')
        self.asset_name_line.setEnabled(False)
        asset_name.addWidget(self.asset_name_line)
        main_layout.addLayout(asset_name)

        self.existing_preset_layout = QHBoxLayout()
        self.existing_preset_layout.addWidget(QLabel('Load Existing Preset'))
        self.preset_list_combo = QComboBox()
        self.existing_preset_layout.addWidget(self.preset_list_combo)
        self.save_preset_btn = QPushButton('Save Current as New Preset')
        self.save_preset_btn.clicked.connect(self.on_save_preset)
        self.existing_preset_layout.addWidget(self.save_preset_btn)
        self.delete_preset_btn = QPushButton('Delete Preset')
        self.delete_preset_btn.clicked.connect(self.on_delete_preset)
        self.existing_preset_layout.addWidget(self.delete_preset_btn)
        main_layout.addLayout(self.existing_preset_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        self.tab_widget = SettingsTabsWidget(self)
        main_layout.addWidget(self.tab_widget)

        layout = QHBoxLayout()
        self.preview_btn = QPushButton('Preview')
        self.preview_btn.clicked.connect(self.on_preview)
        self.preview_btn.setEnabled(False)
        layout.addWidget(self.preview_btn)
        self.save_btn = QPushButton('Save on disk')
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.on_save_on_disk)
        layout.addWidget(self.save_btn)
        main_layout.addLayout(layout)

        self.populate_preset_box()
        self.preset_list_combo.currentIndexChanged.connect(self.on_load_preset)

        if self.debug: print('Ui initialized, all parameters are at default values')

    @property
    def settings(self) -> UsdImporterSettings:
        return UsdImporterSettings(
            self.asset_name_line.text(),
            'textures_path',
            self.save_path,
            self.tab_widget.settings
        )

    @property
    def preset(self) -> UsdImpotertPreset:
        return UsdImpotertPreset(
            self.save_path,
            self.tab_widget.preset
        )

    @property
    def save_path(self) -> str:
        destination_folder = hou.text.expandString(self.destination_folder_line.text())

        if destination_folder:
            return hou.text.expandString(self.destination_folder_line.text())
        
        return hou.text.expandString(self.asset_folder_line.text())


    @property
    def preset_path(self) -> str:
        houdini_version = hou.applicationVersion()
        return hou.expandString(f'{hou.getenv("HOME")}/houdini{houdini_version[0]}.{houdini_version[1]}/scripts/usd_importer/presets')

    @property
    def selected_preset(self) -> str:

        if self.preset_list_combo.currentIndex() == 0:
            return None

        preset_text = self.preset_list_combo.currentText()
        if preset_text:
            return os.path.join(self.preset_path, f'{preset_text}.json')

        return None


    """
    Load a new asset, create the preview network, and save to disk
    """
    def on_megascan_load_asset(self):

        asset_info_path = hou.ui.selectFile(hou.getenv("HOME") if not self.last_selected_asset_folder else self.last_selected_asset_folder, title="Asset Folder", file_type=hou.fileType.Directory)

        if asset_info_path:
            
            asset_folder_full_path = hou.text.expandString(asset_info_path)

            json_files_list = glob.glob(os.path.join(asset_folder_full_path, '*.json'))
            if not json_files_list or len(json_files_list) != 1:
                hou.ui.displayMessage(f'Folder {asset_folder_full_path} does not contain a valid json file', severity=hou.severityType.Error, title="Error")
                return

            self.last_selected_asset_folder = asset_folder_full_path
            self.asset_info = megascan.format_asset_info(json_files_list[0])

            self.active_preview = None
            self.active_component_output = None

            self.asset_folder_line.setText(asset_info_path)
            self.asset_name_line.setText(self.asset_info.name)
            self.asset_name_line.setPlaceholderText(self.asset_info.name)
            self.change_save_location_btn.setEnabled(True)
            self.preview_btn.setEnabled(True)
            self.save_btn.setEnabled(False)
            self.asset_name_line.setEnabled(True)

            self.tab_widget.update_info(self.asset_info)

    def on_change_save_directory(self):
        save_path = hou.ui.selectFile(hou.getenv("HOME"), title="Asset Folder", file_type=hou.fileType.Directory)
        if save_path: self.destination_folder_line.setText(save_path)

    def on_preview(self):

        if self.asset_info: 
            self.active_preview, self.active_component_output = importer.usd_component_builder(self.asset_info, self.settings)
            self.save_btn.setEnabled(True)

    def on_save_on_disk(self):

        if self.active_preview and self.active_component_output:
            
            save_path = hou.text.expandString(hou.node(self.active_component_output).parm('lopoutput').eval())
            save_folder = os.path.dirname(save_path)

            if os.path.exists(save_folder):
                result = hou.ui.displayMessage(f'you want to over it?', buttons=('Overwrite', 'Increment Name', 'Cancel'))
                if result == 2:
                    return
                elif result == 1:
                    file_name = os.path.basename(save_path)
                    file_name, file_extension = os.path.splitext(file_name)
                    file_name = hou.text.incrementNumberedString(file_name)
                    hou.node(self.active_component_output).setName(file_name)
                    temp = self.active_component_output.split('/')
                    self.active_component_output = f'/{temp[1]}/{temp[2]}/{file_name}'
                else:
                    shutil.rmtree(save_folder)

            hou.node(self.active_component_output).parm('execute').pressButton()

            if self.settings.settings.extra.import_thumbnail and self.asset_info.thumbnail:
                shutil.copy(self.asset_info.thumbnail, save_folder)


    """
    Load, Delete or Create a new preset
    """
    def on_save_preset(self):
        """
        Creates a new preset based of the settings
        """

        result = hou.ui.readInput('Enter new preset name:', buttons=('OK', 'Cancel'))

        if result[0] == 0: 

            preset_name = result[1]
            new_preset_full_path = os.path.join(self.preset_path, f'{preset_name}.json')

            if not os.path.exists(os.path.dirname(new_preset_full_path)):
                os.makedirs(os.path.dirname(new_preset_full_path))

            if os.path.exists(new_preset_full_path):
                result = hou.ui.displayMessage(f'Preset {preset_name} already exsist, do you want to over it?', buttons=('OK', 'Cancel'))
                if result == 1: return

            with open(new_preset_full_path, 'w') as json_file:
                json_file.write(json.dumps(self.preset, indent=4, cls=UsdImpotertPresetEncoder))

            self.populate_preset_box(new_preset_full_path)

    def on_delete_preset(self):
        """
        Delete a preset after a confirmation dialog
        """
        if self.selected_preset and os.path.exists(self.selected_preset):
            
            result = hou.ui.displayMessage(f'Are you sure you want to delete the preset?', buttons=('OK', 'Cancel'))
            if result == 1: return
            
            os.remove(self.selected_preset)
            self.populate_preset_box()

    def on_load_preset(self):

        preset_path = self.selected_preset
        
        # Default preset
        preset = UsdImpotertPreset()

        if preset_path:

            with open(preset_path, 'r') as json_file:
                data = json.load(json_file)

            preset: UsdImpotertPreset = json.loads(json.dumps(data), object_hook=UsdImpotertPresetDecoder)

        self.destination_folder_line.setText(preset.save_path)
        self.tab_widget.load_preset(preset.settings)

    def on_reset_preset():
        pass

    def populate_preset_box(self, active=None):

        json_files_list = sorted(glob.glob(os.path.join(self.preset_path, '*.json')))

        self.preset_list_combo.clear()
        self.preset_list_combo.addItem('Default')

        for index, preset in enumerate(json_files_list):
            self.preset_list_combo.addItem(os.path.splitext(os.path.basename(preset))[0])
            if preset == active:
                self.preset_list_combo.setCurrentIndex(index+1)


    """
    Expand or collapse path strings
    """
    def on_asset_folder_line_mouse_press(self, event):

        if event.button() == Qt.MiddleButton:
            self.expand_or_collapse(self.asset_folder_line)

    def on_destination_folder_line_mouse_press(self, event):
        
        if event.button() == Qt.MiddleButton:
            self.expand_or_collapse(self.destination_folder_line)

    def expand_or_collapse(self, item):

        vars = ['$HOME', '$HIP', '$JOB']
        text = item.text()
        if text:
            if any(substring in text for substring in vars):
                item.setText(hou.text.expandString(text))
            else:
                item.setText(hou.text.collapseCommonVars(text, vars = vars))

def run_ui():

    win = NewUI(parent=hou.qt.mainWindow())
    win.show()
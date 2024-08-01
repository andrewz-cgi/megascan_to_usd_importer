from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox, QCheckBox, QSlider, QHBoxLayout
from PySide2.QtCore import Qt

from ....types.megascan_asset import MegascanAsset
from ....types.megascan_asset import MegascanVariant
from ....types.megascan_asset import MegascanGeomerty
from ....types.preset import GeometryPreset
from ....types.settings import GeometrySettings

class GeometrySettingsTabWidget(QWidget):

    title = 'Geometry Settings'

    def __init__(self, parent=None):

        super(GeometrySettingsTabWidget, self).__init__(parent)

        tab_layout = QVBoxLayout(self)

        #
        self.render_group = QGroupBox()
        self.render_group.setTitle('Render')
        self.render_geomerty_layout = QGridLayout()
        self.render_geomerty_layout.setColumnStretch(0, 3)
        self.render_geomerty_layout.setColumnStretch(1, 7)
        self.render_group.setLayout(self.render_geomerty_layout)
        self.render_geomerty_layout.addWidget(QLabel('Render Geomery'), 0, 0)
        self.render_geomerty_lods = QComboBox()
        self.render_geomerty_layout.addWidget(self.render_geomerty_lods, 0, 1)
        self.render_enable_polyreduce_checkbox = QCheckBox('Enable PolyReduce')
        self.render_geomerty_layout.addWidget(self.render_enable_polyreduce_checkbox, 1, 0)
        self.render_enable_polyreduce_checkbox.stateChanged.connect(self.on_enable_render_polyreduce_checkbox_changed)
        self.render_polyreduce_slider = QSlider()
        self.render_polyreduce_slider.setOrientation(Qt.Horizontal)
        self.render_polyreduce_slider.setEnabled(False)
        self.render_polyreduce_slider.setRange(0, 100)
        self.render_polyreduce_slider.setValue(80)
        self.render_geomerty_layout.addWidget(self.render_polyreduce_slider, 1, 1)

        tab_layout.addWidget(self.render_group)

        #
        self.proxy_group = QGroupBox()
        self.proxy_group.setTitle('Proxy')
        self.proxy_geomerty_layout = QGridLayout()
        self.proxy_geomerty_layout.setColumnStretch(0, 3)
        self.proxy_geomerty_layout.setColumnStretch(1, 7)
        self.proxy_group.setLayout(self.proxy_geomerty_layout)
        self.enable_proxy_geometry_checkbox = QCheckBox('Enable Proxy Geometry')
        self.enable_proxy_geometry_checkbox.stateChanged.connect(self.on_enable_proxy_geometry_checkbox_changed)
        self.proxy_geomerty_layout.addWidget(self.enable_proxy_geometry_checkbox, 0, 0)
        self.proxy_geomerty_layout.addWidget(QLabel('Proxy Geometry'), 1, 0)
        self.proxy_geomerty_lods = QComboBox()
        self.proxy_geomerty_layout.addWidget(self.proxy_geomerty_lods, 1, 1, 1, 2)
        self.proxy_geomerty_lods.setEnabled(False)
        self.proxy_enable_polyreduce_checkbox = QCheckBox('Enable PolyReduce')
        self.proxy_enable_polyreduce_checkbox.setEnabled(False)
        self.proxy_enable_polyreduce_checkbox.stateChanged.connect(self.on_enable_proxy_polyreduce_checkbox_changed)
        self.proxy_geomerty_layout.addWidget(self.proxy_enable_polyreduce_checkbox, 2, 0)
        lay = QHBoxLayout()
        self.proxy_polyreduce_label = QLabel()
        lay.addWidget(self.proxy_polyreduce_label)
        self.proxy_polyreduce_slider = QSlider()
        self.proxy_polyreduce_slider.setOrientation(Qt.Horizontal)
        self.proxy_polyreduce_slider.setEnabled(False)
        self.proxy_polyreduce_slider.setRange(0, 100)
        self.proxy_polyreduce_slider.setValue(50)
        lay.addWidget(self.proxy_polyreduce_slider)
        self.proxy_geomerty_layout.addLayout(lay, 2, 1)
        tab_layout.addWidget(self.proxy_group)
        self.update_proxy_polyreduce_label()
        self.proxy_polyreduce_slider.valueChanged.connect(self.update_proxy_polyreduce_label)   

        #
        self.sim_proxy_group = QGroupBox()
        self.sim_proxy_group.setTitle('Sim Proy')
        self.sim_proxy_geomerty_layout = QGridLayout()
        self.sim_proxy_geomerty_layout.setColumnStretch(0, 3)
        self.sim_proxy_geomerty_layout.setColumnStretch(1, 7)
        self.sim_proxy_group.setLayout(self.sim_proxy_geomerty_layout)
        self.enable_sim_proxy_geometry_checkbox = QCheckBox('Enable SimProxy Geometry')
        self.enable_sim_proxy_geometry_checkbox.stateChanged.connect(self.on_enable_sim_proxy_geometry_checkbox_changed)
        self.sim_proxy_geomerty_layout.addWidget(self.enable_sim_proxy_geometry_checkbox, 0, 0)
        self.sim_proxy_geomerty_layout.addWidget(QLabel('SimProxy Geometry'), 1, 0)
        self.sim_proxy_geomerty_lods = QComboBox()
        self.sim_proxy_geomerty_layout.addWidget(self.sim_proxy_geomerty_lods, 1, 1, 1, 2)
        self.sim_proxy_geomerty_lods.setEnabled(False)
        self.sim_proxy_enable_polyreduce_checkbox = QCheckBox('Enable PolyReduce')
        self.sim_proxy_enable_polyreduce_checkbox.setEnabled(False)
        self.sim_proxy_enable_polyreduce_checkbox.stateChanged.connect(self.on_enable_sim_proxy_polyreduce_checkbox_changed)
        self.sim_proxy_geomerty_layout.addWidget(self.sim_proxy_enable_polyreduce_checkbox, 2, 0)
        lay = QHBoxLayout()
        self.sim_proxy_polyreduce_label = QLabel()
        lay.addWidget(self.sim_proxy_polyreduce_label)
        self.sim_proxy_polyreduce_slider = QSlider()
        self.sim_proxy_polyreduce_slider.setOrientation(Qt.Horizontal)
        self.sim_proxy_polyreduce_slider.setEnabled(False)
        self.sim_proxy_polyreduce_slider.setRange(0, 100)
        self.sim_proxy_polyreduce_slider.setValue(50)
        lay.addWidget(self.sim_proxy_polyreduce_slider)
        self.sim_proxy_geomerty_layout.addLayout(lay, 2, 1)
        tab_layout.addWidget(self.sim_proxy_group)
        self.update_sim_proxy_polyreduce_label()
        self.sim_proxy_polyreduce_slider.valueChanged.connect(self.update_sim_proxy_polyreduce_label)

    @property
    def settings(self) -> GeometrySettings:
        return GeometrySettings(
            self.render_geomerty_lods.currentText(),
            self.render_enable_polyreduce_checkbox.isChecked(),
            self.render_polyreduce_slider.value(),
            self.enable_proxy_geometry_checkbox.isChecked(),
            self.proxy_geomerty_lods.currentText(),
            self.proxy_enable_polyreduce_checkbox.isChecked(),
            self.proxy_polyreduce_slider.value(),
            self.enable_sim_proxy_geometry_checkbox.isChecked(),
            self.sim_proxy_geomerty_lods.currentText(),
            self.sim_proxy_enable_polyreduce_checkbox.isChecked(),
            self.sim_proxy_polyreduce_slider.value()
        )

    @property
    def preset(self) -> GeometryPreset:
        return GeometryPreset(
            self.render_enable_polyreduce_checkbox.isChecked(),
            self.render_polyreduce_slider.value(),
            self.enable_proxy_geometry_checkbox.isChecked(),
            self.proxy_enable_polyreduce_checkbox.isChecked(),
            self.proxy_polyreduce_slider.value(),
            self.enable_sim_proxy_geometry_checkbox.isChecked(),
            self.sim_proxy_enable_polyreduce_checkbox.isChecked(),
            self.sim_proxy_polyreduce_slider.value()
        )

    def load_preset(self, preset: GeometryPreset):
        self.render_enable_polyreduce_checkbox.setChecked(preset.render_polyreduce_enable)
        self.render_polyreduce_slider.setValue(preset.render_polyreduce)
        self.render_polyreduce_slider.setEnabled(preset.render_polyreduce_enable)
        self.enable_proxy_geometry_checkbox.setChecked(preset.enable_proxy_geometry)
        self.proxy_polyreduce_slider.setValue(preset.proxy_polyreduce)
        self.proxy_polyreduce_slider.setEnabled(preset.enable_proxy_geometry and preset.proxy_geometry_polyreduce_enable)
        self.proxy_geomerty_lods.setEnabled(preset.enable_proxy_geometry)
        self.enable_sim_proxy_geometry_checkbox.setChecked(preset.enable_sim_proxy_geometry)
        self.sim_proxy_polyreduce_slider.setValue(preset.sim_proxy_polyreduce)
        self.sim_proxy_polyreduce_slider.setEnabled(preset.enable_sim_proxy_geometry and preset.sim_proxy_geometry_polyreduce_enable)
        self.sim_proxy_geomerty_lods.setEnabled(preset.enable_proxy_geometry)

    def on_enable_render_polyreduce_checkbox_changed(self, state):
        self.render_polyreduce_slider.setEnabled(state)

    def on_enable_proxy_geometry_checkbox_changed(self, state):
        self.proxy_geomerty_lods.setEnabled(state)
        self.proxy_enable_polyreduce_checkbox.setEnabled(state)
        self.proxy_polyreduce_slider.setEnabled(state and self.proxy_enable_polyreduce_checkbox.isChecked())

    def on_enable_sim_proxy_geometry_checkbox_changed(self, state):
        self.sim_proxy_geomerty_lods.setEnabled(state)
        self.sim_proxy_enable_polyreduce_checkbox.setEnabled(state)
        self.sim_proxy_polyreduce_slider.setEnabled(state and self.sim_proxy_enable_polyreduce_checkbox.isChecked())

    def on_enable_proxy_polyreduce_checkbox_changed(self, state):
        self.proxy_polyreduce_slider.setEnabled(state and self.enable_proxy_geometry_checkbox.isChecked())

    def on_enable_sim_proxy_polyreduce_checkbox_changed(self, state):
        self.sim_proxy_polyreduce_slider.setEnabled(state and  self.enable_sim_proxy_geometry_checkbox.isChecked())


    def update_proxy_polyreduce_label(self):
        self.proxy_polyreduce_label.setText(f'{self.proxy_polyreduce_slider.value()} %')

    def update_sim_proxy_polyreduce_label(self):
        self.sim_proxy_polyreduce_label.setText(f'{self.sim_proxy_polyreduce_slider.value()} %')


    def update_settings(self, asset_info: MegascanAsset):

        lods = []

        variant: MegascanVariant = asset_info.variants[sorted(asset_info.variants)[0]]
        
        for lod in variant.lods:
            lods.append(lod.name)

        self.render_geomerty_lods.clear()
        self.proxy_geomerty_lods.clear()
        self.sim_proxy_geomerty_lods.clear()

        for lod in lods:
            self.render_geomerty_lods.addItem(lod)
            self.proxy_geomerty_lods.addItem(lod)
            self.sim_proxy_geomerty_lods.addItem(lod)

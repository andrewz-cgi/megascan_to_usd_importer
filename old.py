import sys, os, importlib
import hou 

houdini_version = hou.applicationVersion()

if houdini_version < (19, 5, 0):
    hou.ui.displayMessage("At least Houdini 19.5 version is required", severity=hou.severityType.Error)
    sys.exit()

scritps_path = os.path.join(hou.getenv("HOME"), "houdini{}.{}".format(houdini_version[0], houdini_version[1]), "scripts")

if scritps_path not in sys.path:
    sys.path.append(scritps_path)

import unload_packages
importlib.reload(unload_packages)

unload_packages.unload_packages(packages=["usd_importer"])

from usd_importer import run_ui

usd_importer.run()





import os
import re

import hou

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

DEBUG = False

NORMAL_TYP = '3d'
COMBINED_TYP = 'combined'
PLANTS_TYP = '3dplant'

FBX_TYPE = 'application/x-fbx'

class MegascanGeometryInfo():

    def __init__(self) -> None:
        self._uri = self._name = None

    def __str__(self) -> str:
        out_str = "Name -> {}\n\t\t\tUri -> {}".format(self._name, self._uri)
        return out_str

    # Name property
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    # Uri property
    @property
    def uri(self):
        return self._uri
    @uri.setter
    def uri(self, value):
        self._uri = value

class MegascanVariantInfo():

    def __init__(self) -> None:
        self._original: MegascanGeometryInfo = None
        self._lods: list[MegascanGeometryInfo] = []

    def __str__(self) -> str:
        otu_str = "\t\t--- Original ---\n"
        otu_str += "\t\t\t{}\n".format(self._original.__str__())
        otu_str += "\t\t--- Lods ---\n"
        for lod in self._lods:
            otu_str += "\t\t\t{}\n".format(lod.__str__())
        return otu_str
    
    # Original property
    @property
    def original(self):
        return self._original
    @original.setter
    def original(self, value):
        self._original = value

    # Lods property
    @property
    def lods(self):
        return self._lods
    @lods.setter
    def lods(self, value):
        self._lods = value 

class MegascanTextureInfo():
    
    JPEG = "image/jpeg"
    EXR = "image/x-exr"

    def __init__(self) -> None:
        self._resolution = None
        self._formats: dict[self.JPEG | self.EXR, str ] = {}
    
    # Formats property
    @property
    def formats(self):
        return self._formats
    @formats.setter
    def formats(self, value):
        self._formats = value

class MegascanMapInfo():
    
    def __init__(self) -> None:
        self._textures: dict[str, MegascanTextureInfo] = {}
        self._name = None

    # Name property
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    # Textures property
    @property
    def textures(self):
        return self._textures
    @textures.setter
    def textures(self, value):
        self._textures = value

class MegascanAssetInfo():
    
    NORMAL_TYP = '3d'
    COMBINED_TYP = 'combined'
    PLANTS_TYP = '3dplant'

    VALID_ASSET_TYPES = (NORMAL_TYP, COMBINED_TYP, PLANTS_TYP)

    def __init__(self) -> None:
        self._name = self._type = self._id = self._thumbnail = self._folder_path = None
        self._groups = []
        self._variants: dict[str, MegascanVariantInfo] = {}
        self._maps: dict[str, MegascanMapInfo] = {}

    def __str__(self) -> str:
        out_str = "Name -> {}\nType -> {}\nFolder path -> {}\nGroups -> {}\n".format(self._name, self._type, self._folder_path, self._groups)
        out_str += "--- Variants ---\n" 
        for key, var in self._variants.items():
            out_str += "\t{}\n{}".format(key, var.__str__())
        return out_str

    # Name property
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    # Type property
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if value not in self.VALID_ASSET_TYPES:
            hou.ui.displayMessage("Type {} not supported\nValid asset types are {}".format(value, self.VALID_TYPES), severity=hou.severityType.Error, title="Asset type unrecognized")
            return
        self._type = value

    # Id property
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    # Thumbnail property
    @property
    def thumbnail(self):
        return self._thumbnail
    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value

    # Folder_folder property
    @property
    def folder_path(self):
        return self._folder_path
    @folder_path.setter
    def folder_path(self, value):
        self._folder_path = value

    # Groups property
    @property
    def groups(self):
        return self._groups
    @groups.setter
    def groups(self, value):
        self._groups = value

    # Geometries property
    @property
    def variants(self):
        return self._variants
    @variants.setter
    def variants(self, value):
        self._variants = value

    # Maps property
    @property
    def maps(self):
        return self._maps
    @maps.setter
    def maps(self, value):
        self._maps = value

class MainWindow(QMainWindow):

    def __init__(self):

        self.asset_info = {}

        super(MainWindow, self).__init__(hou.ui.mainQtWindow())

        # Main window settings
        self.setWindowTitle("PySide Base Window")
        self.setGeometry(100, 100, 400, 300)  # Set the window geometry (x, y, width, height)

        # Central widget creation
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Asset folder layout
        asset_folder_lyt = QHBoxLayout()

        self.asset_folder_path = QLineEdit()
        self.asset_folder_path.setPlaceholderText("Asset folder path")
        asset_folder_lyt.addWidget(self.asset_folder_path)

        asset_folder_btn = QPushButton("Select asset folder")
        asset_folder_btn.clicked.connect(self.show_folder_dialog)
        asset_folder_lyt.addWidget(asset_folder_btn)

        main_layout.addLayout(asset_folder_lyt)

        # Load info btn
        load_info_btn = QPushButton("Load info")
        load_info_btn.clicked.connect(self.load_asset_info)
        main_layout.addWidget(load_info_btn)

        # ----- START LOADED ASSET TYPE -----
        line = self.create_h_line()
        main_layout.addWidget(line)

        self.type_lbl = QLabel()
        self.type_lbl.setText('Asset type: ')
        main_layout.addWidget(self.type_lbl)

        line = self.create_h_line()
        main_layout.addWidget(line)
        # ----- END LOADED ASSET TYPE -----


        # ----- START QUICK EXPORT -----
        self.quick_btn = QPushButton("Quick export")
        self.quick_btn.setEnabled(False)
        self.quick_btn.clicked.connect(self.on_quick_export)
        main_layout.addWidget(self.quick_btn)
        # ----- END QUICK EXPORT -----


        # ----- START GEO/MATERIAL TABS -----
        self.geo_mat_toolbox = QToolBox()
        self.geo_mat_toolbox.setEnabled(False)
        # Tabs widget
        self.geo_tab = self.def_geo_tab_waiting_widget()
        self.mat_tab = self.build_material_tab()
        # Add tabs to toolbox
        self.geo_mat_toolbox.addItem(self.geo_tab, "Geomerty")
        self.geo_mat_toolbox.addItem(self.mat_tab, "Material")
        main_layout.addWidget(self.geo_mat_toolbox)
        # ----- END GEO/MATERIAL TABS -----

        # ----- START SAVE -----
        save_widg = QWidget()
        save_widg_lyt = QVBoxLayout()
        self.asset_name = QLineEdit()
        save_widg_lyt.addWidget(self.asset_name)
        save_path_lyt = QHBoxLayout()
        self.path_input = QLineEdit()
        save_button = QPushButton("Choose path")
        save_path_lyt.addWidget(self.path_input)
        save_path_lyt.addWidget(save_button)
        save_button.clicked.connect(self.show_save_dialog)
        save_widg_lyt.addLayout(save_path_lyt)
        save_widg.setLayout(save_widg_lyt)
        main_layout.addWidget(save_widg)
        # ----- END SAVE -----

        central_widget.setLayout(main_layout)

        # Menu bar
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 505, 21))
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setTitle('Options')
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setTitle('About')
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.actionSave_settings = QAction(self)
        self.actionSave_settings.setText('Save settings ...')
        self.actionReset_settings = QAction(self)
        self.actionReset_settings.setText('Reset settings')
        self.actionDocumentation = QAction(self)
        self.actionDocumentation.setText('Help')
        self.menuOptions.addAction(self.actionSave_settings)
        self.menuOptions.addAction(self.actionReset_settings)
        self.menuAbout.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        return

    def on_quick_export(self):

        if DEBUG: print("START QUICK EXPORT PROCEDURE")
        if DEBUG: print(self.asset_info)

        stage: hou.LopNetwork = hou.node("/stage")

        """
        for child_node in stage.children():
            child_node.destroy()
        """

        component_out = None
        if self.asset_info['type'] == NORMAL_TYP:
            componentgeometry = self.create_componentgeometry_node(
                self.asset_folder_path.text(),
                stage,
                self.asset_info['geo']['lods'][0],
                self.asset_info['geo']['lods'][-1],
                self.asset_info['geo']['lods'][-1]
            )
            component_out = componentgeometry
        elif self.asset_info['type'] == PLANTS_TYP:
            componentgeometryvariants = stage.createNode("componentgeometryvariants", "componentgeometryvariants")
            componentgeometryvariants.parm("variantset").set("variant")
            index = 0
            for key, value in self.asset_info['variants'].items():
                componentgeometry = self.create_componentgeometry_node(
                    self.asset_folder_path.text() + "/" + key,
                    stage, 
                    value['original'] if value['original'] else value['lods'][0],
                    value['lods'][-1],
                    value['lods'][-1]
                )
                componentgeometry.parm("geovariantname").set(key)
                componentgeometryvariants.setInput(index, componentgeometry, 0)
                index = index +1
            component_out = componentgeometryvariants
        elif self.asset_info['type'] == COMBINED_TYP:
            componentgeometryvariants = stage.createNode("componentgeometryvariants", "componentgeometryvariants")
            componentgeometryvariants.parm("variantset").set("variant")
            index = 0
            for key, value in self.asset_info['variants'].items():
                componentgeometry = self.create_componentgeometry_node(
                    self.asset_folder_path.text(),
                    stage,
                    value['original'] if value['original'] else value['lods'][0],
                    value['lods'][-1],
                    value['lods'][-1],
                    subpart = self.asset_info['names'][index]
                )
                componentgeometry.parm("geovariantname").set(key)
                componentgeometryvariants.setInput(index, componentgeometry, 0)
                index = index +1
            component_out = componentgeometryvariants
        
        materiallibrary: hou.LopNode = stage.createNode("materiallibrary", "materiallibrary")
        materiallibrary.parm("matpathprefix").set("/ASSET/mtl/")
        componentmaterial: hou.LopNode = stage.createNode("componentmaterial", "componentmaterial")
        componentoutput: hou.LopNode = stage.createNode("componentoutput", self.asset_info['name'].replace(" ", "_"))

        self.create_mtlx_material(materiallibrary, self.asset_info['name'].replace(" ", "_") + "_MAT")

        componentmaterial.setInput(0, component_out, 0)
        componentmaterial.setInput(1, materiallibrary, 0)

        componentoutput.parm('lopoutput').set('C:/Users/Andrewz/Documents/Usd/`chs("name")`/`chs("filename")`')
        if DEBUG: componentoutput.parm("filename").set('`chs("name")`.usd')
        #componentoutput.parm('savestyle').set('flattenstage')
        componentoutput.setInput(0, componentmaterial, 0)

        if DEBUG: stage.layoutChildren()

        componentoutput.parm("execute").pressButton()

    def create_componentgeometry_node(self, folder, context: hou.LopNetwork, default_geo, proxy_geo=None, simprox_geo=None, subpart=None):

        componentgeometry: hou.LopNode = context.createNode("componentgeometry", "componentgeometry")
        geo_subnet: hou.ObjNode = hou.node("/".join([componentgeometry.path(), "sopnet", "geo"]))

        default = geo_subnet.node("default")
        proxy = geo_subnet.node("proxy")
        simproxy = geo_subnet.node("simproxy")

        def_out = self.create_componentgeometry_output(
            geo_subnet,
            default,
            os.path.join(folder, default_geo['uri']),
            "_".join([self.asset_info['name'],default_geo['name']]),
            "_".join([subpart, default_geo['name']]) if subpart else None
        )

        proxy_out = None
        if default_geo == proxy_geo:
            proxy.setInput(0, def_out, 0)
        else:
            proxy_out = self.create_componentgeometry_output(
                geo_subnet,
                proxy,
                os.path.join(folder, proxy_geo['uri']),
                "_".join([self.asset_info['name'],proxy_geo['name']]),
                "_".join([subpart, proxy_geo['name']]) if subpart else None
            )
    
        if simprox_geo == default_geo:
            simproxy.setInput(0, def_out, 0)
        elif simprox_geo == proxy_geo:
            simproxy.setInput(0, proxy_out, 0)
        else:
            self.create_componentgeometry_output(
                geo_subnet,
                simproxy,
                os.path.join(folder, simprox_geo['uri']),
                "_".join([self.asset_info['name'], simprox_geo['name']]),
                "_".join([subpart, simprox_geo['name']]) if subpart else None
            )

        geo_subnet.layoutChildren()

        return componentgeometry

    def create_componentgeometry_output(self, subnet, output, uri, name, subpart = None):
        file = subnet.createNode("file", "file")
        file.parm("file").set(uri)
        xform = subnet.createNode("xform", "rescale")
        xform.parm("scale").set(0.01)
        if subpart:
            blast = subnet.createNode("blast", "blast")
            blast.parm("group").set("@name={}".format(subpart))
            blast.parm("negate").set(True)
            blast.parm("removegrp").set(True)
            blast.setInput(0, file, 0)
            xform.setInput(0, blast, 0)
        else:
            xform.setInput(0, file, 0)
        rename = subnet.createNode("name", "rename")
        rename.parm("name1").set(name)
        rename.setInput(0, xform, 0)
        output.setInput(0, rename, 0)
        return rename

    def create_mtlx_material(self, materiallibrary, mat_name):

        mtlx_material_subnet: hou.VopNode = materiallibrary.createNode("subnet", mat_name)
        mtlx_material_subnet.setMaterialFlag(True)

        for child in mtlx_material_subnet.children():
            child.destroy()

        mtlx_standard_surface: hou.VopNode = mtlx_material_subnet.createNode("mtlxstandard_surface", "mtlxstandard_surface")
        
        # Standard surface parameter creation
        mtlx_standard_surface.insertParmGeneratorsForAllInputs(hou.vopParmGenType.SubnetInput, True)

        """
        # ---- START BASE -----
        base = self.create_vop_parameter(mtlx_material_subnet, "base", "subnet", "float", 0)
        mtlx_standard_surface.setInput(0, base, 0)
        diffuse_roughness = self.create_vop_parameter(mtlx_material_subnet, "diffuse_roughness", "subnet", "float", 0)
        mtlx_standard_surface.setInput(2, diffuse_roughness, 0)
        # ---- END BASE -----

        # ----- SPECULAR START -----
        specular = self.create_vop_parameter(mtlx_material_subnet, "specular", "subnet", "float", 0)
        mtlx_standard_surface.setInput(4, specular, 0)
        specular_color = self.create_vop_parameter(mtlx_material_subnet, "specular_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput(5, specular_color, 0)
        specular_IOR = self.create_vop_parameter(mtlx_material_subnet, "specular_IOR", "subnet", "float", 0)
        mtlx_standard_surface.setInput(7, specular_IOR, 0)
        specular_anisotropy = self.create_vop_parameter(mtlx_material_subnet, "specular_anisotropy", "subnet", "float", 0)
        mtlx_standard_surface.setInput(8, specular_anisotropy, 0)
        specular_rotation = self.create_vop_parameter(mtlx_material_subnet, "specular_rotation", "subnet", "float", 0)
        mtlx_standard_surface.setInput(9, specular_rotation, 0)
        # ----- SPECULAR END -----

        # ----- TRANSMISSION START -----
        transmission = self.create_vop_parameter(mtlx_material_subnet, "transmission", "subnet", "float", 0)
        mtlx_standard_surface.setInput( 10, transmission, 0)
        transmission_color = self.create_vop_parameter(mtlx_material_subnet, "transmission_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput( 11, transmission_color, 0)
        transmission_depth = self.create_vop_parameter(mtlx_material_subnet, "transmission_depth", "subnet", "float", 0)
        mtlx_standard_surface.setInput( 12, transmission_depth, 0)
        transmission_scatter = self.create_vop_parameter(mtlx_material_subnet, "transmission_scatter", "subnet", "color", 0)
        mtlx_standard_surface.setInput( 13, transmission_scatter, 0)
        transmission_scatter_anisotropy = self.create_vop_parameter(mtlx_material_subnet, "transmission_scatter_anisotropy", "subnet", "float", 0)
        mtlx_standard_surface.setInput( 14, transmission_scatter_anisotropy, 0)
        transmission_dispersion = self.create_vop_parameter(mtlx_material_subnet, "transmission_dispersion", "subnet", "float", 0)
        mtlx_standard_surface.setInput( 15, transmission_dispersion, 0)
        transmission_extra_roughness = self.create_vop_parameter(mtlx_material_subnet, "transmission_extra_roughness", "subnet", "float", 0)
        mtlx_standard_surface.setInput( 16, transmission_extra_roughness, 0)
        # ----- TRANSMISSION END -----

        # ----- SUBSURFACE START ------
        subsurface = self.create_vop_parameter(mtlx_material_subnet, "subsurface", "subnet", "float", 0)
        mtlx_standard_surface.setInput(17, subsurface, 0)
        subsurface_color = self.create_vop_parameter(mtlx_material_subnet, "subsurface_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput(18, subsurface_color, 0)
        subsurface_radius = self.create_vop_parameter(mtlx_material_subnet, "subsurface_radius", "subnet", "color", 0)
        mtlx_standard_surface.setInput(19, subsurface_radius, 0)
        subsurface_scale = self.create_vop_parameter(mtlx_material_subnet, "subsurface_scale", "subnet", "float", 0)
        mtlx_standard_surface.setInput(20, subsurface_scale, 0)
        subsurface_anisotropy = self.create_vop_parameter(mtlx_material_subnet, "subsurface_anisotropy", "subnet", "float", 0)
        mtlx_standard_surface.setInput(21, subsurface_anisotropy, 0)
        # ----- SUBSURFACE END -----

        # ----- SHEEN START -----
        sheen = self.create_vop_parameter(mtlx_material_subnet, "sheen", "subnet", "float", 0)
        mtlx_standard_surface.setInput(22, sheen, 0)
        sheen_color = self.create_vop_parameter(mtlx_material_subnet, "sheen_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput(23, sheen_color, 0)
        sheen_roughness = self.create_vop_parameter(mtlx_material_subnet, "sheen_roughness", "subnet", "float", 0)
        mtlx_standard_surface.setInput(24, sheen_roughness, 0)
        # ----- SHEEN END -------

        # ----- COAT START ------
        coat = self.create_vop_parameter(mtlx_material_subnet, "coat", "subnet", "float", 0)
        mtlx_standard_surface.setInput(25, coat, 0)
        coat_color = self.create_vop_parameter(mtlx_material_subnet, "coat_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput(26, coat_color, 0)
        coat_roughness = self.create_vop_parameter(mtlx_material_subnet, "coat_roughness", "subnet", "float", 0)
        mtlx_standard_surface.setInput(27, coat_roughness, 0)
        coat_anisotropy = self.create_vop_parameter(mtlx_material_subnet, "coat_anisotropy", "subnet", "float", 0)
        mtlx_standard_surface.setInput(28, coat_anisotropy, 0)
        coat_rotation = self.create_vop_parameter(mtlx_material_subnet, "coat_rotation", "subnet", "float", 0)
        mtlx_standard_surface.setInput(29, coat_rotation, 0)
        coat_IOR = self.create_vop_parameter(mtlx_material_subnet, "coat_IOR", "subnet", "float", 0)
        mtlx_standard_surface.setInput(30, coat_IOR, 0)
        coat_normal = self.create_vop_parameter(mtlx_material_subnet, "coat_normal", "subnet", "vector", 0)
        mtlx_standard_surface.setInput(31, coat_normal, 0)
        coat_affect_color = self.create_vop_parameter(mtlx_material_subnet, "coat_affect_color", "subnet", "float", 0)
        mtlx_standard_surface.setInput(32, coat_affect_color, 0)
        coat_affect_roughness = self.create_vop_parameter(mtlx_material_subnet, "coat_affect_roughness", "subnet", "float", 0)
        mtlx_standard_surface.setInput(33, coat_affect_roughness, 0)
        # ----- COAT END -------

        # ----- THIN FILM START -----
        thin_film_thickness = self.create_vop_parameter(mtlx_material_subnet, "thin_film_thickness", "subnet", "float", 0)
        mtlx_standard_surface.setInput(34, thin_film_thickness, 0)
        thin_film_IOR = self.create_vop_parameter(mtlx_material_subnet, "thin_film_IOR", "subnet", "float", 0)
        mtlx_standard_surface.setInput(35, thin_film_IOR, 0)
        # ----- THIN FILM END -------

        # ----- EMISSION START -----
        emission = self.create_vop_parameter(mtlx_material_subnet, "emission", "subnet", "float", 0)
        mtlx_standard_surface.setInput(36, emission, 0)
        emission_color = self.create_vop_parameter(mtlx_material_subnet, "emission_color", "subnet", "color", 0)
        mtlx_standard_surface.setInput(37, emission_color, 0)
        # ----- EMISSION END -----

        # ----- GEOMETRY START ------
        opacity = self.create_vop_parameter(mtlx_material_subnet, "opacity", "subnet", "color", 0)
        mtlx_standard_surface.setInput(38, opacity, 0)
        thin_walled = self.create_vop_parameter(mtlx_material_subnet, "thin_walled", "subnet", "int", 0)
        mtlx_standard_surface.setInput(39, thin_walled, 0)
        tangent = self.create_vop_parameter(mtlx_material_subnet, "tangent", "subnet", "vector", 0)
        mtlx_standard_surface.setInput(41, tangent, 0)
        # ----- GEOMERTY END ------
        """


        mtlx_surface = self.create_vop_parameter(mtlx_material_subnet, "mtlx_surface", "subnet", "surface", 1)
        mtlx_surface.setInput(0, mtlx_standard_surface, 0 )

        mtlx_material_subnet.layoutChildren()

        # Albedo
        for res, maps in self.asset_info['textures']['albedo'].items():
            if 'image/jpeg' in maps:
                mtlx_image = mtlx_material_subnet.createNode('mtlximage', 'albedo_IMG')
                mtlx_image.parm("file").set(os.path.join(self.asset_folder_path.text(),maps['image/jpeg']))
                mtlx_standard_surface.setInput(1, mtlx_image, 0)
                continue
        
        # Roughness
        for res, maps in self.asset_info['textures']['roughness'].items():
            if 'image/jpeg' in maps:
                mtlx_image = mtlx_material_subnet.createNode('mtlximage', 'roughness_IMG')
                mtlx_image.parm("signature").set("float")
                mtlx_image.parm("file").set(os.path.join(self.asset_folder_path.text(),maps['image/jpeg']))
                mtlx_standard_surface.setInput(6, mtlx_image, 0)
                continue

        # Normal
        for res, maps in self.asset_info['textures']['normal'].items():
            if 'image/jpeg' in maps:
                mtlx_image = mtlx_material_subnet.createNode('mtlximage', 'normal_IMG')
                mtlx_image.parm("signature").set("vector3")
                mtlx_image.parm("file").set(os.path.join(self.asset_folder_path.text(),maps['image/jpeg']))
                mtlx_normalmap = mtlx_material_subnet.createNode('mtlxnormalmap', 'mtlxnormalmap')
                mtlx_normalmap.setInput(0, mtlx_image, 0)
                mtlx_standard_surface.setInput(37, mtlx_normalmap, 0)
                continue
            
        
        mtlx_material_subnet.layoutChildren()

        return
    


        output: hou.VopNode = mtlx_material_subnet.createNode("subnetconnector", "material_output")
        output.parm("connectorkind").set("output")
        output.parm("parmtype").set("surface")

        mtlxstandard_surface: hou.VopNode = mtlx_subnet.createNode("mtlxstandard_surface", "mtlxstandard_surface")

        base_color_img = mtlx_subnet.createNode("mtlximage", "base_color")
        for res, maps in self.asset_info['textures']['albedo'].items():
            if maps.get('image/jpeg'):
                base_color_img.parm("file").set(os.path.join(self.asset_folder_path.text(), maps['image/jpeg']))
                continue
        roughness_img = mtlx_subnet.createNode("mtlximage", "roughness")
        roughness_img.parm("signature").set("float")
        for res, maps in self.asset_info['textures']['roughness'].items():
            if maps.get('image/jpeg'):
                roughness_img.parm("file").set(os.path.join(self.asset_folder_path.text(), maps['image/jpeg']))
                continue

        mtlxstandard_surface.setInput(1, base_color_img, 0)
        mtlxstandard_surface.setInput(2, roughness_img, 0)

        
        output.setInput(0, mtlxstandard_surface, 0)
        if DEBUG: mtlx_subnet.layoutChildren()

    def create_vop_parameter(self, context, name, scope, type, export):
        vop_parameter: hou.VopNode =  context.createNode("parameter", name)
        vop_parameter.parm("parmscope").set(scope)
        vop_parameter.parm("parmname").set(name)
        vop_parameter.parm("parmtype").set(type)
        vop_parameter.parm("exportparm").set(export)
        return vop_parameter

    def show_folder_dialog(self):

        folder_path = hou.ui.selectFile(hou.getenv("HOME"), title="Asset Folder", file_type=hou.fileType.Directory)

        if folder_path:
            self.asset_folder_path.setText(folder_path)

    def show_save_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)")

        if file_path:
            self.path_input.setText(file_path)

    def create_h_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def load_asset_info(self):

        import os
        import glob
        import json

        asset_folder_path = hou.expandString(self.asset_folder_path.text())

        if not asset_folder_path:
            self.hou_error_message("Specify a target folder for the asset")
            return
        
        json_files_list = glob.glob(os.path.join(asset_folder_path, '*.json'))
        if not json_files_list or len(json_files_list) != 1:
            self.hou_error_message("Folder {} does not contain a valid json file".format(asset_folder_path))
            return
        
        json_file = json_files_list[0]
        with open(json_file) as raw_data:
            json_info = json.load(raw_data)
       
        self.asset_info = format_asset_info(json_info, asset_folder_path)

        if DEBUG: print(self.asset_info)
        
        if not self.asset_info:
            self.hou_error_message("Json file {} does not contain valid data".format(json_file))
            return
        
        self.type_lbl.setText("Asset type: {}".format(self.asset_info['type']))

        self.quick_btn.setEnabled(True)
        self.geo_mat_toolbox.setEnabled(True)
        self.geo_tab.setLayout(QVBoxLayout())

        return
        geo_tab_widget = self.def_geo_tab_asset_widget()
        self.geo_mat_toolbox.removeItem(0)
        self.geo_mat_toolbox.insertItem(0, geo_tab_widget, "Geomerty")
        self.geo_mat_toolbox.setCurrentIndex(0)
        self.geo_mat_toolbox.setEnabled(True)      
    
    def def_geo_tab_waiting_widget(self):

        def_wait_widget = QWidget()
        lyt = QVBoxLayout()
        lbl = QLabel("Load asset folder ...")
        lyt.addWidget(lbl)
        lbl = QLabel("Load asset folder ...")
        lyt.addWidget(lbl)
        def_wait_widget.setLayout(lyt)

        return def_wait_widget
    
    def build_material_tab(self):

        mat_widg = QWidget()
        mat_layout = QVBoxLayout(mat_widg)

        # Albedo
        lbl = self.create_texture_selection("Albedo")
        mat_layout.addLayout(lbl)
        # Metalness
        lbl = self.create_texture_selection("Metalness")
        mat_layout.addLayout(lbl)
        # Roughness
        lbl = self.create_texture_selection("Roughness")
        mat_layout.addLayout(lbl)
        # Normal
        lbl = self.create_texture_selection("Normal")
        mat_layout.addLayout(lbl)
        # Displacement
        lbl = self.create_texture_selection("Displacement")
        mat_layout.addLayout(lbl)
        # Displacement
        lbl = self.create_texture_selection("Normal")
        mat_layout.addLayout(lbl)
        # AO
        lbl = self.create_texture_selection("AO")
        mat_layout.addLayout(lbl)

        return mat_widg
    
    def create_texture_selection(self, name):

        lay = QHBoxLayout()

        check = QCheckBox(name)
        lbl = QLabel(name)

        combo_box = QComboBox()
        combo_box.addItem("1K Resolution", userData="1024x1024")
        combo_box.addItem("2K Resolution", userData="2048x2048")
        combo_box.addItem("4K Resolution", userData="4096x4096")
        combo_box.addItem("8K Resolution", userData="8192x8192")

        lay.addWidget(check)
        lay.addWidget(lbl)
        lay.addWidget(combo_box)

        return lay

    def def_geo_tab_asset_widget(self):

        wid = QWidget()
        lyt = QVBoxLayout(wid)
        lyt.addWidget(self.create_asset_widget("Render"))
        lyt.addWidget(self.create_asset_widget("Proxy"))
        lyt.addWidget(self.create_asset_widget("Simproxy"))
        return wid

    def create_geo_tab_lyt(self):

        self.geo_tab_lyt = QVBoxLayout()

        # Waiting layout
        self.waiting_lyt = QVBoxLayout()

        waiting_lbl = QLabel("Load asset folder ...")
        self.waiting_lyt.addWidget(waiting_lbl)

        # Simple layout
        self.simple_lyt = QVBoxLayout()

        render_box = QGroupBox()
        render_box.setTitle("Render")
        render_box_lyt = QVBoxLayout()
        btn = QPushButton("Prova")
        render_box_lyt.addWidget(btn)
        render_box.setLayout(render_box_lyt)

        proxy_box = QGroupBox()
        proxy_box.setTitle("Proxy")
        proxy_box_lyt = QVBoxLayout(proxy_box)
        btn = QPushButton("Prova")
        proxy_box_lyt.addWidget(btn)
        proxy_box.setLayout(proxy_box_lyt)

        simproxy_box = QGroupBox()
        simproxy_box.setTitle("Simproxi")
        simproxy_box_lyt = QVBoxLayout(simproxy_box)
        btn = QPushButton("Prova")
        simproxy_box_lyt.addWidget(btn)
        simproxy_box.setLayout(simproxy_box_lyt)

        self.simple_lyt.addWidget(render_box)
        self.simple_lyt.addWidget(proxy_box)
        self.simple_lyt.addWidget(simproxy_box)

        self.simple_lyt.hide()

        self.geo_tab_lyt.addLayout(self.waiting_lyt)
        self.geo_tab_lyt.addLayout(self.simple_lyt)

        self.geo_tab.setLayout(self.geo_tab_lyt)

    def create_asset_widget(self, title):
        container = QGroupBox(title)
        cnt_layout = QGridLayout()
        label = QLabel("Lorem")
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 10)
        check = QCheckBox()
        check.setText("Check box text")
        button_prw = QPushButton("Preview")
        button_clr = QPushButton("Clear")
        cnt_layout.addWidget(label, 0, 0)
        cnt_layout.addWidget(slider, 0, 1)
        cnt_layout.addWidget(check, 1, 0)
        cnt_layout.addWidget(button_prw, 2, 0)
        cnt_layout.addWidget(button_clr, 2, 1)
        container.setLayout(cnt_layout)
        container.setEnabled(False)
        return container

    def hou_error_message(self, message, title=None):
        hou.ui.displayMessage(message, severity=hou.severityType.Error, title="Error" if not title else title)


def format_asset_info(raw_data, asset_folder_path):

    info_class = MegascanAssetInfo()
    asset_info = {}
    
    # name
    asset_info['name'] = raw_data['name']
    info_class.name = raw_data['name']
    
    # type
    categories = raw_data['categories']
    asset_info['type'] = PLANTS_TYP if PLANTS_TYP in categories else COMBINED_TYP if COMBINED_TYP in categories else NORMAL_TYP if NORMAL_TYP in categories else None 
    info_class.type = PLANTS_TYP if PLANTS_TYP in categories else COMBINED_TYP if COMBINED_TYP in categories else NORMAL_TYP if NORMAL_TYP in categories else None 
    
    # id
    asset_info['id'] = raw_data['id']
    info_class.id = raw_data['id']

    # folder path
    info_class.folder_path = asset_folder_path

    thumbnail = '.'.join([raw_data['id'] + "_Preview", "png"])
    asset_info['thumbnail'] = thumbnail if does_file_exist(os.path.join(asset_folder_path, thumbnail)) else None
    info_class.thumbnail = thumbnail if does_file_exist(os.path.join(info_class.folder_path, thumbnail)) else None

    # variants
    if info_class.type in (info_class.NORMAL_TYP, info_class.COMBINED_TYP):
        variant = MegascanVariantInfo()
        for mesh in raw_data['meshes']:
            for uri in mesh['uris']:
                if uri['mimeType'] == FBX_TYPE:
                    if does_file_exist(os.path.join(info_class.folder_path, uri['uri'])):
                        geo = MegascanGeometryInfo()
                        geo.name = clear_name(info_class.id, 'fbx', uri['uri'])
                        geo.uri = uri['uri']
                        if mesh['type'] == 'lod':
                            variant.lods.append(geo)
                        else:
                            variant.original = geo
        if info_class.type == info_class.COMBINED_TYP:
            obj = hou.node("/obj")
            geo_node = obj.createNode("geo", "tmp_geo_node")
            file_node = geo_node.createNode("file", "tmp_load_file")
            file_node.parm('file').set(os.path.join(info_class.folder_path, variant.lods[-1].uri))
            name_attr = file_node.geometry().findPrimAttrib("name")
            names = name_attr.strings()
            geo_node.destroy()
            pattern = re.compile(r'_LOD\d+$', re.IGNORECASE)
            for i in range(0, len(names)):
                variant_name = "Var"+str(i)
                info_class.variants[variant_name] = variant
                info_class.groups.append(pattern.sub('', names[i])) 
        else:
            info_class.variants[info_class.name] = variant
    else:
        for model in raw_data['models']:
            if model['mimeType'] == FBX_TYPE:
                if does_file_exist(os.path.join(info_class.folder_path, model['uri'])):
                    variant_name, uri = os.path.split(model['uri'])
                    if info_class.variants.get(variant_name) is None:
                        variant = MegascanVariantInfo()
                        info_class.variants[variant_name] = variant
                    geo = MegascanGeometryInfo()
                    geo.name = clear_name(variant_name, 'fbx', uri)
                    geo.uri = uri
                    if model['type'] == 'lod':
                        info_class.variants[variant_name].lods.append(geo)
                    else:
                        info_class.variants[variant_name].original = geo

    # textures

    if DEBUG: (info_class)

    # geomertries
    if asset_info['type'] == NORMAL_TYP:
        asset_info['geo'] = {}
        asset_info['geo']['lods'] = []
        asset_info['geo']['original'] = {}
        for mesh in raw_data['meshes']:
            for uri in mesh['uris']:
                if uri['mimeType'] == FBX_TYPE:
                    if does_file_exist(os.path.join(asset_folder_path, uri['uri'])):
                        ciao = {}
                        ciao['name'] = clear_name(asset_info['id'], 'fbx', uri['uri'])
                        ciao['uri'] = uri['uri']
                        if mesh['type'] == 'lod':
                            asset_info['geo']['lods'].append(ciao)
                        else:
                            asset_info['geo']['original'] = ciao
    else:
        asset_info['variants'] = {}
        if asset_info['type'] == PLANTS_TYP:
            for model in raw_data['models']:
                if model['mimeType'] == FBX_TYPE:
                    if does_file_exist(os.path.join(asset_folder_path, model['uri'])):
                        variant_name, uri = os.path.split(model['uri'])
                        if asset_info['variants'].get(variant_name) is None:
                            asset_info['variants'][variant_name] = {}
                            asset_info['variants'][variant_name]['lods'] = []
                            asset_info['variants'][variant_name]['original'] = {}
                        ciao = {}
                        ciao['name'] = clear_name(variant_name, 'fbx', uri)
                        ciao['uri'] = uri
                        if model['type'] == 'lod':
                            asset_info['variants'][variant_name]['lods'].append(ciao)
                        else:
                            asset_info['variants'][variant_name]['original'] = ciao
        elif asset_info['type'] == COMBINED_TYP:
            tmp = {}
            tmp['lods'] = []
            tmp['original'] = {}
            for mesh in raw_data['meshes']:
                for uri in mesh['uris']:
                    if uri['mimeType'] == FBX_TYPE:
                        if does_file_exist(os.path.join(asset_folder_path, uri['uri'])):
                            ciao = {}
                            ciao['name'] = clear_name(asset_info['id'], 'fbx', uri['uri'])
                            ciao['uri'] = uri['uri']
                            if mesh['type'] == 'lod':
                                tmp['lods'].append(ciao)
                            else:
                                tmp['original'] = ciao

            obj = hou.node("/obj")
            geo_node = obj.createNode("geo", "tmp_geo_node")
            file_node = geo_node.createNode("file", "tmp_load_file")
            file_node.parm('file').set(os.path.join(asset_folder_path, tmp['lods'][-1]['uri']))

            name_attr = file_node.geometry().findPrimAttrib("name")
            names = name_attr.strings()
            geo_node.destroy()
            asset_info['names'] = []
            
            pattern = re.compile(r'_LOD\d+$', re.IGNORECASE)
            for i in range(0, len(names)):
                variant_name = "Var"+str(i)
                asset_info['variants'][variant_name] = {}
                asset_info['variants'][variant_name]['lods'] = tmp['lods']
                asset_info['variants'][variant_name]['original'] = tmp['original']
                asset_info['names'].append(pattern.sub('', names[i]))
    
    # textures old
    asset_info['textures'] = {}
    if asset_info['type'] == NORMAL_TYP or  asset_info['type'] == COMBINED_TYP:
        for component in raw_data["components"]:
            if asset_info['textures'].get(component['type']) is None:
                asset_info['textures'][component['type']] = {}
            for res in component["uris"][0]["resolutions"]: 
                asset_info['textures'][component['type']][res["resolution"]] = {}
                for format in res["formats"]:
                    if does_file_exist(os.path.join(asset_folder_path, format["uri"])):
                        asset_info['textures'][component['type']][res["resolution"]][format["mimeType"]] = format["uri"]
    else:
        for map in raw_data["maps"]:
            if asset_info['textures'].get(map['type']) is None:
                asset_info['textures'][map['type']] = {}
            if asset_info['textures'][map['type']].get(map['resolution']) is None:
                asset_info['textures'][map['type']][map['resolution']] = {}
            if does_file_exist(os.path.join(asset_folder_path, map["uri"])):
                asset_info['textures'][map['type']][map["resolution"]][map["mimeType"]] = map["uri"]

    # textures class
    if asset_info['type'] == NORMAL_TYP or  asset_info['type'] == COMBINED_TYP:
        for component in raw_data["components"]:
            if info_class.maps.get(component['type']) is None:
                info_class.maps[component['type']] = MegascanMapInfo()
            for texture in component["uris"][0]["resolutions"]: 
                res = texture["resolution"]
                formats = {}
                for format in texture["formats"]:
                    if does_file_exist(os.path.join(asset_folder_path, format["uri"])):
                        formats[format["mimeType"]] = format["uri"]
                if formats:
                    texture = MegascanTextureInfo()
                    texture.formats = formats
                    info_class.maps[res] = texture
                    print(formats)


    for name, map in info_class.maps.items():
        print(name)

    return asset_info

def does_file_exist(file_path):
    return os.path.isfile(file_path)

def clear_name(id, ext, name):
    return name.replace(id+'_', '').replace('.'+ext, '')

win = MainWindow()
win.show()

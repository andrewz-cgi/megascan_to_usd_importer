import hou

import os

from ..modules.megascan_importer import *
from ..modules import texture_importer as matx_importer

from ..types.megascan_asset import MegascanAsset
from ..types.settings import UsdImporterSettings
from ..types.settings import ExportSettings

def usd_component_builder(asset_info: MegascanAsset, settings: UsdImporterSettings):

    asset_name = settings.asset_name if settings.asset_name else asset_info.name

    stage: hou.LopNetwork = hou.node('/stage')
    subnet_name = hou.text.variableName(asset_name)

    subnet: hou.LopNode = stage.node(subnet_name)

    #if subnet: subnet.destroy()

    subnet: hou.LopNode = stage.createNode('subnet', hou.text.variableName(subnet_name))
    for child_node in subnet.children():
            child_node.destroy()

    stage.layoutChildren()

    component_output = new_usd_importer(subnet, asset_name, settings, asset_info)

    subnet.setDisplayFlag(True)

    return subnet.name(), component_output
    
def new_usd_importer(context: hou.LopNode, asset_name:str, importer_settings: UsdImporterSettings, asset_info: MegascanAsset):

    materiallibrary: hou.LopNode = context.createNode('materiallibrary', hou.text.variableName(f'{asset_name}_matlibrary'))
    materiallibrary.parm("matpathprefix").set("/ASSET/mtl/")
    materiallibrary.parm("genpreviewshaders").set(importer_settings.settings.material.create_usd_preview_surface)
    componentmaterial: hou.LopNode = context.createNode('componentmaterial', 'componentmaterial')
    componentoutput: hou.LopNode = context.createNode('componentoutput', hou.text.variableName(asset_name))
    componentoutput.parm('savestyle').set(ExportSettings.export_variants_values[importer_settings.settings.export.export_variants])
    componentoutput.parm('payloadlayer').set(importer_settings.settings.export.payload_layer_name)
    componentoutput.parm('geolayer').set(importer_settings.settings.export.geometry_layer_name)
    componentoutput.parm('mtllayer').set(importer_settings.settings.export.material_layer_name) 
    componentoutput.parm('extralayer').set(importer_settings.settings.export.extra_layer_name)
    componentoutput.parm('localize').set(importer_settings.settings.export.localize_external)
    componentoutput.parm('variantlayers').set(importer_settings.settings.main.enable_variant_layers)
    componentoutput.parm('variantlayersset').set(importer_settings.settings.main.variant_set)
    componentoutput.parm('variantlayersdir').set(importer_settings.settings.main.variant_directory)
    componentoutput.parm('doclassinherit').set(importer_settings.settings.extra.class_inherit)
    componentoutput.parm('lopoutput').set(f'{importer_settings.save_path}`chs("name")`/`chs("filename")`')

    # Creazione component geometry
    variant_limit = importer_settings.settings.main.variant_number
    if importer_settings.settings.main.variant_number == 0:
        variant_limit = len(asset_info.variants.items())

    geomerty_components = []
    variants_list = sorted(asset_info.variants)

    for variant_index in range(variant_limit):

        variant: MegascanVariant = asset_info.variants[variants_list[variant_index]]

        group = None
        if asset_info.names_group:
            group = asset_info.names_group[variant_index]

        render_geometry = get_geomerty_from_lod_name(variant.lods, importer_settings.settings.geometry.render_geomerty)
        proxy_geometry = get_geomerty_from_lod_name(variant.lods, importer_settings.settings.geometry.proxy_geomerty)
        sim_proxy_geometry = get_geomerty_from_lod_name(variant.lods, importer_settings.settings.geometry.sim_proxy_geomerty)

        geomerty_components.append(create_componentgeometry_node(
            context,
            name=hou.text.variableName(variants_list[variant_index]),
            default_uri=os.path.join(asset_info.asset_path, render_geometry.uri),
            default_name=hou.text.variableName(f'{variant.name}_render'),
            def_lod=render_geometry.name,
            render_polyreduce=importer_settings.settings.geometry.render_polyreduce if importer_settings.settings.geometry.render_polyreduce_enable else 0,
            proxy_uri=os.path.join(
                asset_info.asset_path,
                proxy_geometry.uri) if proxy_geometry and importer_settings.settings.geometry.enable_proxy_geometry else None,
            proxy_name=hou.text.variableName(f'{variants_list[variant_index]}_proxy'),
            proxy_lod=proxy_geometry.name,
            proxy_polyreduce=importer_settings.settings.geometry.proxy_polyreduce if importer_settings.settings.geometry.proxy_geometry_polyreduce_enable else 0,
            simprox_uri=os.path.join(
                asset_info.asset_path, 
                sim_proxy_geometry.uri) if sim_proxy_geometry and importer_settings.settings.geometry.enable_sim_proxy_geometry else None,
            simprox_name=hou.text.variableName(f'{variants_list[variant_index]}_simproxy'),
            sim_proxy_lod=sim_proxy_geometry.name,
            simproxy_polyreduce=importer_settings.settings.geometry.sim_proxy_polyreduce if importer_settings.settings.geometry.sim_proxy_geometry_polyreduce_enable else 0,
            group=group
        ))

    # Set up varianti
    geo_out = geomerty_components[0]
    if len(geomerty_components) > 1:
        componentgeometryvariants: hou.LopNode = context.createNode("componentgeometryvariants", "componentgeometryvariants")
        index = 0
        for comp in geomerty_components:
            componentgeometryvariants.setInput(index, comp)
            index +=1
        geo_out = componentgeometryvariants

        componentoutput.parm('setdefaultvariants').set(True)
        componentoutput.parm('variantdefaultgeo').set(importer_settings.settings.main.default_variant)

    # Creazione materiale
    matx_importer.import_materialx(asset_info.texture_path, hou.text.variableName(f'{asset_name}_mtl'), materiallibrary, importer_settings.settings.material)

    componentmaterial.setInput(0, geo_out)
    componentmaterial.setInput(1, materiallibrary)
    componentoutput.setInput(0, componentmaterial)
    componentoutput.setDisplayFlag(True)

    context.layoutChildren()

    return componentoutput.path()

def get_geomerty_from_lod_name(lods: list[MegascanGeomerty], lod_name) -> MegascanGeomerty:

    geo = None

    for lod in lods:
        if lod.name == lod_name:
            return lod

    return geo
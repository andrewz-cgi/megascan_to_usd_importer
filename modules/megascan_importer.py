import hou
import os, json
from . import common as cmm

from ..types.megascan_asset import MegascanAsset, MegascanVariant, MegascanGeomerty

def format_asset_info(json_path):
    
    with open(json_path) as raw_data:
        asset_data = json.load(raw_data)

    asset_info = MegascanAsset()

    # name
    asset_info.name = asset_data['name']

    # type
    categories = asset_data['categories']
    asset_info.type = MegascanAsset.PLANTS_TYP if MegascanAsset.PLANTS_TYP in categories else MegascanAsset.COMBINED_TYP if MegascanAsset.COMBINED_TYP in categories else MegascanAsset.NORMAL_TYP if MegascanAsset.NORMAL_TYP in categories else None 

    # id
    asset_info.id = asset_data['id']

    # folder path
    asset_info.asset_path = os.path.dirname(json_path)

    # thumbnail
    thumbnail = '.'.join([asset_data['id'] + "_Preview", "png"])
    asset_info.thumbnail = os.path.join(asset_info.asset_path, thumbnail) if cmm.does_file_exist(os.path.join(asset_info.asset_path, thumbnail)) else None

    # texture path
    if asset_info.type == MegascanAsset.PLANTS_TYP:
        asset_info.texture_path = f'{asset_info.asset_path}/Textures/Atlas'
    else:
        asset_info.texture_path = f'{asset_info.asset_path}'

    # variants
    variants = {}
    # Asdrubale
    if asset_info.type in (MegascanAsset.NORMAL_TYP, MegascanAsset.COMBINED_TYP):
        
        variant = MegascanVariant()
        variant.name = asset_info.name

        for mesh in asset_data['meshes']:
            for uri in mesh['uris']:
                # Check if the variant file exists
                if os.path.isfile(os.path.join(asset_info.asset_path, uri['uri'])):
                    if mesh['type'] == 'lod':
                        variant.lods.append(
                            MegascanGeomerty(
                                cmm.clear_name(asset_info.id, 'fbx', uri['uri']),
                                uri['uri'])
                            )
                    else:
                         variant.lods.insert(0,MegascanGeomerty(
                            cmm.clear_name(asset_info.id, 'fbx', uri['uri']),
                            uri['uri']
                        ))

        # In case the geomerty it's is plitted, each version will be considered as a variant         
        obj = hou.node("/obj")
        geo_node = obj.createNode("geo", "tmp_geo_node")
        file_node = geo_node.createNode("file", "tmp_load_file")
        file_node.parm('file').set(os.path.join(asset_info.asset_path, variant.lods[-1].uri))
        name_attr = file_node.geometry().findPrimAttrib("name")
        names = name_attr.strings()
        geo_node.destroy()
        if len(names) > 1:
            names = [name.split('_LOD')[0] for name in names]
            for index in range(len(names)):
                variant_index = index if index > 9 else f'0{index + 1}'
                variant_name = f'Var_{variant_index}'
                variants[variant_name] = variant
            asset_info.names_group = names
        else:
            variants[asset_info.name] = variant

        """
        #
        if asset_info.type == MegascanAsset.COMBINED_TYP:
            obj = hou.node("/obj")
            geo_node = obj.createNode("geo", "tmp_geo_node")
            file_node = geo_node.createNode("file", "tmp_load_file")
            file_node.parm('file').set(os.path.join(asset_info.asset_path, variant.lods[-1].uri))
            name_attr = file_node.geometry().findPrimAttrib("name")
            names = name_attr.strings()
            geo_node.destroy()
            names = [name.split('_LOD')[0] for name in names]
            for index in range(len(names)):
                variant_index = index if index > 9 else f'0{index + 1}'
                variant_name = f'Var_{variant_index}'
                variants[variant_name] = variant
            asset_info.names_group = names
        else:
            variants[asset_info.name] = variant
        """
    # In case of plants or foliage
    else:
        for model in asset_data['models']:
            if os.path.isfile(os.path.join(asset_info.asset_path, model['uri'])):

                variant_original_name, uri = os.path.split(model['uri'])
                variant_number = variant_original_name.lower().split('var')[1]
                variant_number = variant_number if int(variant_number) > 9 else f'0{variant_number}'
                variant_name = f'Var_{variant_number}'

                if variants.get(variant_name) is None:
                    variants[variant_name] = MegascanVariant()
                    variants[variant_name].name = variant_name

                if model['type'] == 'lod':
                    variants[variant_name].lods.append(
                        MegascanGeomerty(
                            cmm.clear_name(variant_original_name, 'fbx', uri),
                            model['uri']
                        )
                    )
                else:
                    variants[variant_name].insert(0, MegascanGeomerty(
                            cmm.clear_name(variant_original_name, 'fbx', uri['uri']),
                            uri['uri']
                    ))

    asset_info.variants = variants

    return asset_info

def create_componentgeometry_node(context: hou.LopNetwork, name, default_uri, default_name, def_lod, render_polyreduce=0, proxy_uri=None, proxy_name=None, proxy_lod=None, proxy_polyreduce=0, simprox_uri=None, simprox_name=None, sim_proxy_lod=None, simproxy_polyreduce=0, group=None):

    componentgeometry: hou.LopNode = context.createNode('componentgeometry', name)
    geo_subnet: hou.ObjNode = hou.node('/'.join([componentgeometry.path(), 'sopnet', 'geo']))

    default: hou.LopNode = geo_subnet.node('default')
    proxy: hou.LopNode = geo_subnet.node('proxy')
    simproxy: hou.LopNode = geo_subnet.node('simproxy')

    # render geometry
    render_out, render_rescaled = create_componentgeometry_output(
        geo_subnet,
        default_uri,
        default_name,
        f'{group}_{def_lod}' if group else None,
        render_polyreduce
    )
    default.setInput(0, render_out)

    # proxy geometry
    proxy_out = None
    if proxy_uri:
        if proxy_uri == default_uri:
            proxy_out, proxy_rescaled = create_componentgeometry_output_from_existing(
                geo_subnet,
                render_rescaled,
                proxy_name,
                proxy_polyreduce
            )
        else:
            proxy_out, proxy_rescaled = create_componentgeometry_output(
                geo_subnet,
                proxy_uri,
                proxy_name,
                f'{group}_{proxy_lod}' if group else None,
                proxy_polyreduce
            )
        proxy.setInput(0, proxy_out)

    # simproxy geometry
    simproxy_out = None
    if simprox_uri:
        if simprox_uri == proxy_uri:
            simproxy_out, simproxy_rescaled = create_componentgeometry_output_from_existing(
                geo_subnet,
                proxy_rescaled,
                simprox_name,
                simproxy_polyreduce
            )
        elif simprox_uri == default_uri:
            simproxy_out, simproxy_rescaled = create_componentgeometry_output_from_existing(
                geo_subnet,
                render_rescaled,
                simprox_name,
                simproxy_polyreduce
            )
        else:
            simproxy_out, simproxy_rescaled = create_componentgeometry_output(
                geo_subnet,
                simprox_uri,
                simprox_name,
                f'{group}_{sim_proxy_lod}' if group else None,
                simproxy_polyreduce
            )
        simproxy.setInput(0, simproxy_out)

    geo_subnet.layoutChildren()

    return componentgeometry

def create_componentgeometry_output(context, uri, name, group=None, polyreduce=0):
        
        file: hou.LopNode = context.createNode('file', 'file')
        file.parm('file').set(uri)

        file_output = file
        if group:
            blast: hou.LopNode = context.createNode('blast', 'blast')
            blast.parm('group').set(f'@name={group}')
            blast.parm('negate').set(True)
            blast.parm('removegrp').set(True)
            blast.setInput(0, file)
            file_output = blast

        delete_attr: hou.LopNode = context.createNode('attribdelete', 'attribdelete')
        delete_attr.parm('negate').set(True)
        delete_attr.parm('ptdel').set('N')
        delete_attr.parm('vtxdel').set('uv')
        delete_attr.setInput(0, file_output)

        xform: hou.LopNode = context.createNode('xform', 'rescale')
        xform.parm('scale').set(0.01)
        xform.setInput(0, delete_attr)

        rescale_output = xform
        if polyreduce > 1:
            polyreduce_node: hou.LopNode = context.createNode('polyreduce', 'polyreduce')
            polyreduce_node.parm('percentage').set(polyreduce)
            polyreduce_node.setInput(0, xform)
            rescale_output = polyreduce_node

        rename: hou.LopNode = context.createNode('name', 'rename')
        rename.parm('name1').set(name)
        rename.setInput(0, rescale_output)

        return rename, xform

def create_componentgeometry_output_from_existing(context, rescaled, name, polyreduce=0):

    rescale_output = rescaled
    if polyreduce > 1:
        polyreduce_node: hou.LopNode = context.createNode('polyreduce', 'polyreduce')
        polyreduce_node.parm('percentage').set(polyreduce)
        polyreduce_node.setInput(0, rescaled)
        rescale_output = polyreduce_node

    rename: hou.LopNode = context.createNode('name', 'rename')
    rename.parm('name1').set(name)
    rename.setInput(0, rescale_output)

    return rename, rescaled

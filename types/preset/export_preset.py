class ExportPreset():

    export_variants_values = [
        'flattenimplicitlayers',
        'flattenalllayers',
        'separate',
        'flattenstage'
    ]

    def_payload_layer_name = 'payload.usdc'
    def_geometry_layer_name = 'geo.usdc'
    def_material_layer_name = 'mtl.usdc'
    def_extra_layer_name = 'extra.usdc'

    def __init__(self, 
            payload_layer_name = def_payload_layer_name,
            geometry_layer_name = def_geometry_layer_name,
            material_layer_name = def_material_layer_name, 
            extra_layer_name = def_extra_layer_name,
            localize_external = False,
            export_variants = 0):
        
        self.payload_layer_name = payload_layer_name
        self.geometry_layer_name = geometry_layer_name
        self.material_layer_name = material_layer_name
        self.extra_layer_name = extra_layer_name
        self.localize_external = localize_external
        self.export_variants = export_variants
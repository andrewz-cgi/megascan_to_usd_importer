from ..preset.export_preset import ExportPreset

class ExportSettings(ExportPreset):

    def __init__(
            self,
            payload_layer_name: str = ExportPreset.def_payload_layer_name,
            geometry_layer_name: str = ExportPreset.def_geometry_layer_name,
            material_layer_name: str = ExportPreset.def_material_layer_name,
            extra_layer_name: str = ExportPreset.def_extra_layer_name,
            localize_external: bool = False,
            export_variants = 0):
        
        super().__init__(payload_layer_name, geometry_layer_name, material_layer_name, extra_layer_name, localize_external, export_variants)
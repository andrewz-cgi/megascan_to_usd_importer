from ..preset.material_preset import MaterialPreset

class MaterialSettings(MaterialPreset):

    def __init__(
            self, 
            metalness: bool = False, 
            opacity: bool = False,
            displacement: bool = False,
            translucency: bool = False,
            ao: bool = False,
            color_variation: bool = False,
            color_variation_name: str = MaterialPreset.def_color_variation_name,
            invert_roughness: bool = False,
            create_usd_preview_surface: bool = False):

        super().__init__(metalness, opacity, displacement, translucency, ao, color_variation, color_variation_name, invert_roughness, create_usd_preview_surface)
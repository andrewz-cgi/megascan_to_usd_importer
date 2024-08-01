class MaterialPreset():

    def_color_variation_name = 'ColorVariation'

    def __init__(self, 
            metalness: bool = False,
            opacity: bool = False,
            displacement: bool = False,
            translucency: bool = False,
            ao: bool = False,
            color_variation: bool = False,
            color_variation_name: str = def_color_variation_name,
            invert_roughness: bool = False,
            create_usd_preview_surface: bool = False):
        
        self.metalness = metalness
        self.opacity = opacity
        self.displacement = displacement
        self.translucency = translucency
        self.ao = ao
        self.color_variation = color_variation
        self.color_variation_name = color_variation_name
        self.invert_roughness = invert_roughness
        self.create_usd_preview_surface = create_usd_preview_surface
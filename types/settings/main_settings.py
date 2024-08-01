from ..preset.main_preset import MainPreset

class MainSettings(MainPreset):

    def __init__(self, enable_variant_layers=False, variant_set=MainPreset.def_variant_set, variant_directory=MainPreset.def_variant_directory, default_variant: str = None, variant_number: int = 0):

        super().__init__(enable_variant_layers, variant_set, variant_directory)

        self.default_variant = default_variant
        self.variant_number = variant_number
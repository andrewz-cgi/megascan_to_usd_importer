class MainPreset():

    def_variant_set = 'geo'
    def_variant_directory = 'variants'

    def __init__(self, enable_variant_layers=False, variant_set=def_variant_set, variant_directory=def_variant_directory):
        self.enable_variant_layers = enable_variant_layers
        self.variant_set = variant_set
        self.variant_directory = variant_directory
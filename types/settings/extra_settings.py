from ..preset.extra_preset import ExtraPreset

class ExtraSettings(ExtraPreset):

    def __init__(self,double_sided=False, class_inherit=False, import_thumbnail=False):

        super().__init__(double_sided, class_inherit, import_thumbnail)
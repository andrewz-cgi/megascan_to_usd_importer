from json import JSONEncoder
from collections import namedtuple

from .preset_settings import PresetSettings

class UsdImpotertPreset():
    
    def __init__(self, save_path: str = '', settings = PresetSettings()):
        
        self.save_path = save_path
        self.settings = settings

# subclass JSONEncoder
class UsdImpotertPresetEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
        
def UsdImpotertPresetDecoder(studentDict):
    return namedtuple('UsdImpotertPresetEncoder', studentDict.keys())(*studentDict.values())
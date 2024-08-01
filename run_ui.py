from .ui.usd_importer_ui import UsdImporterUi
import hou

def run():

    win = UsdImporterUi(parent=hou.qt.mainWindow())
    win.show()

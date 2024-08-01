from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit

from .usd_variants import UsdVariantsWidget

class UsdBuilderWidget(QGroupBox):

    def __init__(self, parent=None):

        super(UsdBuilderWidget, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.setTitle('USD Builder')
        self.setLayout(self.main_layout)

        self.asset_name_line = QLineEdit()
        self.asset_name_line.setPlaceholderText('Asset name ...')
        self.main_layout.addWidget(self.asset_name_line)

        self.usd_variants_wdgt = UsdVariantsWidget()
        self.main_layout.addWidget(self.usd_variants_wdgt)
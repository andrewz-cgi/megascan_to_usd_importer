from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget

class UsdVariantsWidget(QWidget):

    def __init__(self, parent=None):

        super(UsdVariantsWidget, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        actions_btn_layout = QHBoxLayout()
        #
        add_variant_btn = QPushButton('Add variant')
        add_variant_btn.clicked.connect(self.add_tab)
        actions_btn_layout.addWidget(add_variant_btn)
        #
        remove_variant_btn = QPushButton('Add variant')
        remove_variant_btn.clicked.connect(self.delete_tab)
        actions_btn_layout.addWidget(remove_variant_btn)
        #
        self.main_layout.addLayout(actions_btn_layout)

    def add_tab(self):
        new_tab = QWidget()
        self.tab_widget.addTab(new_tab, f"Tab {self.tab_widget.count() + 1}")

    def delete_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

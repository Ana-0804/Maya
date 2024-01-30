import os
import sys

sys.path.append('env/Lib/site-packages')

from functools import partial
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class UnrealCacheExporter(QWidget):
    def __init__(self, *args, **kwargs):
        super(UnrealCacheExporter, self).__init__(*args, **kwargs)

        # Parent widget under Maya main window
        #self.setWindowFlags(Qt.Window)

        # Set the object name
        self.setObjectName('UnrealCacheExporter')
        self.setWindowTitle('Unreal Cache Exporter')
        self.setGeometry(500, 500, 500, 500)
        ##########
        # enable custom window hint
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        #
        # # disable (but not hide) close button
        # self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint)
        ##########
        self.initUI()
        self.cmd = None

    def initUI(self):
        self.main_layout = QGridLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)

        self.other_assets_label = QLabel("Other Assets (fbx)")

        self.character_assets_label = QLabel("Character Assets (abc)")

        self.other_asset_list = QListWidget()
        self.other_asset_list.setAlternatingRowColors(True)
        self.other_asset_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.character_asset_list = QListWidget()
        self.character_asset_list.setAlternatingRowColors(True)
        self.character_asset_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.do_poly_smooth_button = QPushButton("Do Polysmooth")

        self.export_cache_button = QPushButton("Export Cache")

        self.switch_to_fin_master = QPushButton("Switch Assets To Fin Master")
        self.switch_to_fin_master.setEnabled(False)

        self.abc_select_all_check_box = QCheckBox("Select all character assets")

        self.fbx_select_all_check_box = QCheckBox("Select all other assets")

        self.radio_button_layout = QHBoxLayout()
        self.radio_button_layout.addWidget(self.abc_select_all_check_box)
        self.radio_button_layout.addWidget(self.fbx_select_all_check_box)

        self.main_layout.addLayout(self.radio_button_layout, 0, 0, 1, 2)
        self.main_layout.addWidget(self.character_assets_label, 1, 0, 1, 1)
        self.main_layout.addWidget(self.character_asset_list, 2, 0, 1, 1)
        self.main_layout.addWidget(self.other_assets_label, 1, 1, 1, 1)
        self.main_layout.addWidget(self.other_asset_list, 2, 1, 1, 1)
        self.main_layout.addWidget(self.progress_bar, 3, 0, 1, 2)
        self.main_layout.addWidget(self.do_poly_smooth_button, 4, 0, 1, 2)
        self.main_layout.addWidget(self.export_cache_button, 5, 0, 1, 2)
        # self.main_layout.addWidget(self.switch_to_fin_master, 6, 0, 1, 2)

        self.setLayout(self.main_layout)

    def conformation_message(self, msg, title):
        """
        this function is use to display an error messages to the user
        """
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle(title)
        self.message_box.setText(msg)
        return_value = self.message_box.exec_()

    def save_local_prompt(self):
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle("Save file to local?")
        self.message_box.setText("To perform fbx export this file is needed to be saved on the local drive\n"
                                 "Shotgrid won't be functioning after you save to local\n"
                                 "Do you want to continue?")
        self.message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        return self.message_box

    def disable_list_widget_item(self, widget_item):
        widget_item.setFlags(Qt.NoItemFlags)

    def find_list_widget_item(self, list_widget, current_list_item_text):
        for each_index in range(list_widget.count()):
            item = list_widget.item(each_index)
            item_text = item.text()
            print (item_text, ">>>>")
            print (current_list_item_text, ">>>>>")
            if current_list_item_text.endswith("_SET"):
                current_list_item_text = current_list_item_text.replace("SET", "static")
            if item_text == current_list_item_text:
                return item


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = UnrealCacheExporter()
    obj.show()
    sys.exit(app.exec_())
# Description: This script is used to create a UI for Alembic Cache Exporter tool. in Maya 2018
# Author: Sanjay Kamble
# Date: 2020-04-20
# Last Update: 2020-04-20
# Version: 1.0
'''
import sys
sys.path.append("C:/cosmos/alembicCache")
from source import MainUI
reload(MainUI)
MainUI.show_window()
'''
# ==========================================================================================================

import os
import sys
import yaml
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtUiTools
import shiboken2
import maya.OpenMayaUI as omui

from importlib import reload
import __init__ as init

# ==========================================================================================================
SCRIPT_LOC = os.path.dirname(__file__)
icons = os.path.join(SCRIPT_LOC, 'resource')

configPath = os.path.join(SCRIPT_LOC, 'Config.yaml').replace('\\', '/')
# config = init.readConfig(configPath)
# print(config)

# ==========================================================================================================
def get_maya_window():
    """
    Get the main Maya window as a QWidget
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance((main_window_ptr), QtWidgets.QWidget)

# ==========================================================================================================
def load_ui(ui_file, parent=None):
    """
    Load the .ui file and return the corresponding widget
    """
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui_widget = loader.load(ui_file, parent)
    ui_file.close()
    return ui_widget

# ==========================================================================================================
class MyWindow(QtWidgets.QMainWindow):
    """ Main window class """
    main_ui = os.path.join(SCRIPT_LOC, "ui", "almbicUI.ui")
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), self.main_ui)
        self.ui = load_ui(ui_file, parent=self)
        # reside the window
        self.setWindowTitle("Alembic Cache Exporter")
        self.resize(1400, 600)
        self.setCentralWidget(self.ui)

        self.init_ui()
        self.createConnections()
        self.add_layers()

    def init_ui(self):
        self.ui.destroyed.connect(self.on_exit_code)

    # ==========================================================================================================
    def createConnections(self):
        """ Create the signal/slot connections """
        pass

    # ==========================================================================================================
    def on_exit_code(self):
        """ Cleanup when the UI is closed """
        sys.stdout.write("UI successfully closed\n")
        self.deleteLater()

    # ==========================================================================================================
    def add_layers(self):
        # setting splitter frame sizes
        self.ui.splitter_6.setSizes([200, 200, 200])
        self.ui.splitFrameA.setSizes([300, 900])
        self.ui.splitFrameB_2.setSizes([550, 50])

        # setting table widget
        self.ui.tableWidgetA.setColumnCount(3)
        self.ui.tableWidgetA.setRowCount(0)
        self.ui.tableWidgetA.setHorizontalHeaderLabels(["SHOTS_NAME", "SHOTS_PATH","SHOTS_STATUS",])
        self.ui.tableWidgetA.horizontalHeader().setVisible(True)
        self.ui.tableWidgetA.setColumnWidth(0, 150)
        self.ui.tableWidgetA.setColumnWidth(1, 700)
        self.ui.tableWidgetA.setColumnWidth(2, 150)

# ==========================================================================================================
def show_window():
    """ Show the window """
    global my_window
    my_window = MyWindow(parent=get_maya_window())
    try:
        my_window.close()  # Close the window if it already exists
    except:
        pass

    my_window.show()

# ==========================================================================================================
# Show window in Maya
# if __name__ == "__main__":
#     try:
#         my_window.close()  # Close the window if it already exists
#     except:
#         pass
#     show_window()

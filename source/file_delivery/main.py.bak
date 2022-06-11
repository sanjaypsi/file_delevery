"""
Tools Name :  File_delivery
Description: This tool helps out by sorting the multiple file formats by file
            extension within a given output directory.
Author name: Sanjay Kamble
Date:04.06.2022
Points:
    When you click on the Input button, it opens QFileDialog, where you can select the input folder path.
    When you click on the Input button, it opens QFileDialog, where you can select the input folder path.
    Path to the form's output To obtain the output path, click the output button.
    This Qline edit holds output paths.
    When you click on the Execute button, it runs the code.
    To clear the widget, click on the clear button.

    To use these tools, you need to click on app.bat file 
"""

from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
import qdarktheme
import sys
import os
from file_delivery import core
SCRIPT_LOC = os.path.dirname(__file__)


class MainUI(QtWidgets.QMainWindow):
    """
    This is Main Window class call MainUI
    variables :ui that store File_delivery.ui path
    variables:logo store Icon path
    """
    ui = os.path.join(SCRIPT_LOC, 'ui', "File_delivery.ui")
    logo = os.path.join(SCRIPT_LOC, 'resource', "file-cabinet-icon.png")

    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi(self.ui, self)
        self.setWindowIcon(QtGui.QIcon(self.logo))
        self.show()

        self.setup_layout()
        self.setup_connection()

    def setup_layout(self):
        """
        This functions
        :return: setSizes QSplitter and setMinimum progressbar value
        """
        self.splitterC.setSizes([300, 75])
        self.splitterD.setSizes([300, 75])
        self.splitterE.setSizes([300, 75])
        self.progressBar.setMinimum(0)

    def setup_connection(self):
        """
        This functions
        :return:
        """
        self.InputPB.clicked.connect(self.load_input_directory)
        self.OutputPB.clicked.connect(self.load_output_directory)
        self.ExecutePB.clicked.connect(self.get_directory_path)
        self.ClearPB.clicked.connect(self.clear_all_widgets)

    def load_input_directory(self):
        """
        This functions
        :return:  Get the input folder path
        """
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self, " File dialog ")
        self.listWidget.addItem(dialog)
        self.set_message('INPUT PATH IS ADD >>>>> ' + dialog)

    def load_output_directory(self):
        """
        This functions
        :return: Get output folder path
        """
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self, " File dialog ")
        self.OutputLE.setText(dialog)
        self.set_message('OUTPUT PATH IS ADD >>>>> ' + dialog)

    def get_directory_path(self):
        """
        This functions
        :return: Get all Input path and output path which store in self.listWidget and OutputLE widgets
        and pass through Core functions  and return the target path and store in Json file

        if the input path and output path is not in widgets
        its print message in statusBar of UI

        """
        inputs_count = self.listWidget.count()
        input_dirs = []
        for x in range(inputs_count):
            list_items = (self.listWidget.item(x))
            input_dirs.append(list_items.text())

        output_dirs = self.OutputLE.text()
        if not (output_dirs and input_dirs):
            self.set_message("Output and Inputs are Mendatory to proceed.")
            return

        s = core.MainCore(input_data=input_dirs,
                          output_path=output_dirs)

        s.progress_changed.connect(self.set_progress)

        try:
            s.file_transfer()
            self.set_message('FILE TRANSFER SUCCESSFUL')
        except core.TransferFailed:
            self.set_message('FILE TRANSFER FAILED')
            return

        s.write_manifest()

    def set_message(self, value, timeout=0):
        return self.statusBar.showMessage(value, timeout)

    def set_progress(self, value):
        """
        This functions
        :return: Its display progressBar and statusBar result

        """
        return self.progressBar.setValue(value)

    def clear_all_widgets(self):
        """
        This functions
        :return: Clear all the Widgets
        """
        self.listWidget.clear()
        self.OutputLE.clear()
        self.progressBar.setMinimum(0)
        self.statusBar.clearMessage()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainUI()
    app.exec_()

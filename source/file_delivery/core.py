"""
This is Main core functions.where you get all the information to run the process
"""
import os
import time
import shutil
import json
import re
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class TransferFailed(Exception):
    """
    This functions
        : If file failed to transfer it well pass the  Exception Message to Ui statusBar
    """
    pass


class MainCore(QObject):
    progress_changed = pyqtSignal(float)

    def __init__(self, input_data=None, output_path=None):
        super(MainCore, self).__init__()

        self._input_data = input_data
        self.output_path = output_path
        self._data = dict()

    def file_transfer(self):
        """
        This functions
        :return: take all input path and output path
        Using parsed information from the filename, move the image sequences into
        the provided output structure.
        """
        timezone = time.gmtime()
        date_format = (time.strftime("%Y%m%d%H%M", timezone))

        target_path = []
        file_extension = []
        progress = 0
        self.progress_changed.emit(progress)

        all_files = list()
        for input_data in self._input_data:
            for root, dirs, files in os.walk(input_data, topdown=False):
                all_files.extend([os.path.join(root, f) for f in files])

        if not all_files:
            return

        total_files = len(all_files)
        step = 100.0/total_files

        for each_file in all_files:
            file_name = os.path.basename(each_file)
            project_name, shot_name, task_name = file_name.split('_')
            task_name, frame_number, fil_extension = task_name.split('.')

            output_path = os.path.join(self.output_path, project_name, date_format,
                                       project_name + '_' + shot_name, task_name,
                                       fil_extension.upper()).replace('\\', '/')

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            dst_path = os.path.join(output_path, file_name.replace('\\', '/'))

            try:
                shutil.copy(each_file, dst_path)
                target_path.append(dst_path)
                file_extension.append(fil_extension.upper())

            except Exception:
                raise TransferFailed("FILE TRANSFER NOT SUCCESSFUL >>>>>" + dst_path)

            progress += step
            self.progress_changed.emit(progress)

        self.progress_changed.emit(100)

        file_path_list = []
        for ext in list(dict.fromkeys(file_extension)):
            for my_list in target_path:
                if re.search(ext, my_list):
                    lists = my_list.replace('\\', '/')
                    file_path_list.append(lists)

        self._data['Manifest'] = file_path_list

    def write_manifest(self):
        """
        This functions
        :return: this store all the file target path into json format
        """
        json_path = os.path.join(self.output_path,
                                 'manifest.json').replace('\\', '/')

        with open(json_path, "w") as outfile:
            json.dump(self._data, outfile, indent=4, sort_keys=True)

        outfile.close()



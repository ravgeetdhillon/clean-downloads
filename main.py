"""
Main Module for the app.
"""

import datetime
import platform
import shutil
import os
from os.path import isfile, join
from os import listdir


def creation_date(path_to_file):
    """
    Get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    """

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(DOWNLOADS_DIR + '/' + path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def sort_folder(mypath):
    """
    A function to sort the files in a download folder
    into their respective categories
    """

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    file_extensions_dir = {
        'images': ['png', 'jpg', 'jpeg', 'gif', 'svg'],
        'documents': ['pdf', 'doc', 'docx', 'xls', 'csv', 'tsv', 'log',  'xlsx', 'ppt', 'pptx'],
        'audio': ['mp3'],
        'video': ['mp4', 'wav'],
        'files': ['zip', 'rar', 'gz', 'tar'],
    }

    for fl in files:
        file_creation_date = int(creation_date(fl))
        year = datetime.datetime.utcfromtimestamp(file_creation_date).strftime('%Y')
        path = DOWNLOADS_DIR + '/' + year
        if not os.path.exists(path):
            os.mkdir(path)

        month = datetime.datetime.utcfromtimestamp(file_creation_date).strftime('%B').lower()
        path = DOWNLOADS_DIR + '/' + year + '/' + month
        if not os.path.exists(path):
            os.mkdir(path)

        file_type = fl.split('.')[-1].lower()
        for key in file_extensions_dir.keys():
            if file_type in file_extensions_dir[key]:
                path = DOWNLOADS_DIR + '/' + year + '/' + month + '/' + key
                if not os.path.exists(path):
                    os.mkdir(path)
                break
        else:
            path = DOWNLOADS_DIR + '/' + year + '/' + month + '/others'
            if not os.path.exists(path):
                os.mkdir(path)

        src = DOWNLOADS_DIR + '/' + fl
        dest = path + '/' + fl
        shutil.move(src, dest)

        print('Moved ' + src + ' >>> ' + dest)


if __name__ == '__main__':
    DOWNLOADS_DIR = 'path/to/downloads/directory'
    sort_folder(DOWNLOADS_DIR)

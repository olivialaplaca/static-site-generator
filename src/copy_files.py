import os.path
import shutil

def copy_directory(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for i in os.listdir(source):
        path = os.path.join(source, i)
        if os.path.isfile(path):
            shutil.copy(path, destination)
        else:
            copy_directory(path, os.path.join(destination, i))
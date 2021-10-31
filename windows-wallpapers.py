from getpass import getuser
import os
from shutil import copy
from PIL import Image

src = f"/Users/{getuser()}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy" \
      f"/LocalState/Assets"
dest = f"/Users/{getuser()}/Desktop/WindowsWallpapers"


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_current_max_index():
    max_index = 1
    if os.path.isdir(dest):
        for file_name in os.listdir(dest):
            index = os.path.splitext(file_name)[0]
            if represents_int(index):
                if int(index) > max_index:
                    max_index = int(index) + 1
    else:
        os.mkdir(dest)
    return max_index


def get_wallpapers(index):
    src_files = os.listdir(src)
    for file_name in src_files:
        src_name = os.path.join(src, file_name)
        dest_name = os.path.join(dest, f"{index}.jpg")

        not_exist = True
        for file in os.listdir(dest):
            if os.path.getsize(src_name) == os.path.getsize(os.path.join(dest, file)):
                not_exist &= False

        if not_exist:
            copy(src_name, dest_name)
            try:
                im = Image.open(dest_name)
                width, height = im.size
                im.close()
                if width != 1920 or height != 1080:
                    os.remove(dest_name)
                else:
                    index += 1
            except OSError:
                os.remove(dest_name)
                continue


if __name__ == "__main__":
    max_index = get_current_max_index()
    get_wallpapers(max_index)

from getpass import getuser
import os
from shutil import copy
from PIL import Image
from screeninfo import get_monitors

monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

src = f"/Users/{getuser()}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy" \
      f"/LocalState/Assets"
dest = f"/Users/{getuser()}/Desktop/WindowsWallpapers"


def get_current_max_index():
    max_index = 1
    if os.path.isdir(dest):
        for file_name in os.listdir(dest):
            index = os.path.splitext(file_name)[0]
            if index.isdigit():
                if int(index) > max_index:
                    max_index = int(index) + 1
    else:
        os.mkdir(dest)
    return max_index


def get_wallpapers(index):
    first_index = index
    for file_name in os.listdir(src):
        src_name = os.path.join(src, file_name)
        dest_name = os.path.join(dest, f"{index}.jpg")

        exist = False
        for file in os.listdir(dest):
            if os.path.getsize(src_name) == os.path.getsize(os.path.join(dest, file)):
                exist = True
                break

        if not exist:
            copy(src_name, dest_name)
            try:
                im = Image.open(dest_name)
                width, height = im.size
                im.close()
                if width != screen_width or height != screen_width:
                    os.remove(dest_name)
                else:
                    index += 1
            except OSError:
                os.remove(dest_name)
    return index - first_index - 1


if __name__ == "__main__":
    max_index = get_current_max_index()
    images_count = get_wallpapers(max_index)
    if images_count > 0:
        print(f"Put {images_count} images in '{dest}'")
    else:
        print("No images found")
    input("\nClick any button to exit...")

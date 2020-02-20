import os, shutil
from file_utils import Folder, MediaFile
from PIL import Image

GET_DIRECTORY = r'D:\Aditya\Pictures Test\From'
DEST_DIRECTORY = r'D:\Aditya\Pictures Test\To'

def main():
    get_dir = Folder(GET_DIRECTORY)
    dest_dir = Folder(DEST_DIRECTORY)
    videos = Folder(os.path.join(dest_dir.path, 'Videos'))
    images = Folder(os.path.join(dest_dir.path, 'Images'))
    audio = Folder(os.path.join(dest_dir.path, 'Audio'))
    duplicates = Folder(os.path.join(dest_dir.path, 'Duplicates'))
    other = Folder(os.path.join(dest_dir.path, 'Other'))
    with Image.open(os.path.join(get_dir.path, 'IMG_8853.jpg')) as img:
        print(img._getexif()[36867][:7].replace(':', '-'))

if __name__ == '__main__':
    main()
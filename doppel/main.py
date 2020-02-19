import os, shutil
from file_utils import Folder, MediaFile

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

    for f in get_dir.files():
        if f.type is None:
            f.move(other)
        elif f.type == 'Video':
            f.move(videos)
        elif f.type == 'Image':
            f.move(images)
        elif f.type == 'Audio':
            f.move(audio)
        else:
            print(f'something went wrong with {f}')

if __name__ == '__main__':
    main()
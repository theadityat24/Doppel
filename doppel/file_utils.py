import os, imghdr, shutil
from pymediainfo import MediaInfo
from PIL import Image


class MediaFile:
    def __init__(self, path):
        self.path = path
        info = os.stat(self.path)
        self.type = self.getType(self.path)
        self.date = self.getDate(self.path)
        
    def move(self, new_dir):
        shutil.move(self.path, new_dir.path)

    def copy(self, new_dir):
        shutil.copy2(self.path, new_dir.path)

    def get_file_data(self):
        with open(self.path, 'rb') as f:
            return f.read()

    def get_file_data_small(self):
        with open(self.path, 'rb') as f:
            return f.read(int(os.path.getsize(self.path)*.01))

    def is_duplicate_of(self, f):
        return self.get_file_data() == f.getFileData()

    def is_duplicate_of_small(self, f):
        return self.get_file_data_small() == f.get_file_data_small()
        
    def __str__(self):
        return str(self.path)

    @staticmethod
    def getType(path):
        if (imghdr.what(path) != None):
            return 'Image'
        else:
            mediainfo = [track.track_type for track in MediaInfo.parse(path).tracks]
            if 'Audio' in mediainfo and 'Video' not in mediainfo:
                return 'Audio'
            elif 'Video' in mediainfo:
                return 'Video'
            else:
                return None

    @staticmethod
    def getDate(path):
        with Image.open(path) as img:
            return img._getexif()[36867][:7].replace(':', '-')

class Folder:
    def __init__(self, path):
        self.path = path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def files(self):
        f = []
        for root, dirs, names in os.walk(self.path):
            for n in names:
                f.append(MediaFile(os.path.join(root, n)))
        return f

    def makeFolderIn(self, name):
        return Folder(os.path.join(self.path, name))
            
    
class SourceFolder(Folder):
    def __init__(self, path):
        super().__init__(path)

    def sort_files(self, dest):
        files = self.files()
        for f in files:
            i = files.index(f)
            if i < len(files) - 1:
                for f2 in files[i+1:]:
                    if f.is_duplicate_of_small(f2):
                        f2.move(dest.duplicates)
                        files.remove(f2)
            if f.type == 'Image':
                d = dest.images.addDateFolder(f.date)
                f.move(d)
            elif f.type == 'Video':
                d = dest.videos.addDateFolder(f.date)
                f.move(d)
            elif f.type == 'Audio':
                d = dest.audio.addDateFolder(f.date)
                f.move(d)
            else:
                d = dest.other.addDateFolder(f.date)
                f.move(d)
            

class TypeFolder(Folder):
    def __init__(self, dest, t):
        super().__init__(dest.path)
        self.type = t

    def addDateFolder(self, date):
        Folder(os.path.join(self.path, date))
        
         
class DestinationFolder(Folder):
    def __init__(self, path):
        super().__init__(path)
        self.videos = TypeFolder(self, 'Videos')
        self.images = TypeFolder(self, 'Images')
        self.audio = TypeFolder(self, 'Audio')
        self.other = TypeFolder(self, 'Other')
        self.duplicates = TypeFolder(self, 'Duplicates')

    





        
        
    

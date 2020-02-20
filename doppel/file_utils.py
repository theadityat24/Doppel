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

    def getFileData(self):
        with open(self.path, 'rb') as f:
            return f.read()

    def getFileDataSmall(self):
        with open(self.path, 'rb') as f:
            return f.read(int(os.path.getsize(self.path)*.01))

    def isDuplicateOf(self, f):
        return self.getFileData() == f.getFileData()

    def isDuplicateOfSmall(self, f):
        return self.getFileDataSmall() == f.getFileDataSmall()
        
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
            
    
class SourceFolder(Folder):
    def __init__(self, path):
        super().__init__(path)
        
            

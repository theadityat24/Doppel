import os, imghdr
from pymediainfo import MediaInfo



class MediaFile:
    def __init__(self, path):
        self.path = path
        info = os.stat(self.path)
        self.type = self.getType(self.path)
        
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
        
    
            
            

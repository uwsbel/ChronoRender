from chronorender.movie import Movie

class FFMPEG(Movie):
    @staticmethod
    def getTypeName():
        return "ffmpeg"

    def encode(self):
        return

def build(**kwargs):
    return FFMPEG(**kwargs)

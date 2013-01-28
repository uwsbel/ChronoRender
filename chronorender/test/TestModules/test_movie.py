import unittest

from chronorender.movie import Movie, FFMPEG

class MovieTestCase(unittest.TestCase):

    def test_ffmpeg_encode(self):
        mov = FFMPEG( framerate=60
                )
        print mov

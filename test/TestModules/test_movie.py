import unittest, os

from chronorender.movie import Movie, FFMPEG, MovieFactory

class MovieTestCase(unittest.TestCase):

    def setUp(self):
        self.infilepath = os.path.abspath('./input/frames/out.00.tif')
        self.outdir     = os.path.abspath('./output')

    def test_ffmpeg_encode(self):
        return
        mov = FFMPEG(framerate=12)
        mov.setInputFile(self.infilepath)
        mov.outdir = self.outdir
        mov.encode()

        expected_out = os.path.join(self.outdir, "default.mp4")
        self.assertTrue(os.path.exists(expected_out))

        os.remove(expected_out)

    def test_factory(self):
        fact = MovieFactory()
        mov = fact.build('ffmpeg')

        self.assertTrue(isinstance(mov, FFMPEG))

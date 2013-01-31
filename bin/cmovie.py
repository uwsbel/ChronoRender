import argparse, os
import script_utils as su
su.addCRToPath()

from chronorender.movie import MovieFactory

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('inputfile', help='directory containing image sequence')
    parser.add_argument('output', help='path/name of output file')

    parser.add_argument('-p', '--program', 
            help='program to use for video encoding', 
            default='ffmpeg',
            required=False)

    parser.add_argument('-r', '--framerate', 
            help='framerate', 
            default=24,
            type=int,
            required=False)

    parser.add_argument('-res', '--resolution',
            nargs=2,
            help='resolution of output',
            default=[640, 480],
            type=int,
            required=False)

    parser.add_argument('-f', '--format', 
            help='image format', 
            default='default',
            required=False)

    parser.add_argument('-c', '--codec', 
            help='codec to compress image with', 
            default='default',
            required=False)

    parser.add_argument('-b', '--bitrate', 
            help='quality know', 
            default='default',
            required=False)

    parser.add_argument('-vpreset', '--vpreset', 
            help='quality preset', 
            default='default',
            required=False)

    args = vars(parser.parse_args())

    convertToMovie(args)

def convertToMovie(args):
    mov = _buildMovieWrapper(args)
    mov.encode()

def _buildMovieWrapper(args):
    fact = MovieFactory()
    mov = fact.build(args['program'], **args)
    mov.setInputFile(os.path.abspath(args['inputfile']))
    _verifyOutputFile(args, mov)
    return mov

def _verifyOutputFile(args, mov):
    if os.path.isdir(args['output']):
        mov.outdir = args['output']
        return

    path, f = os.path.split(args['output'])
    mov.outdir = path
    mov.output = f

if __name__ == '__main__':
    main()

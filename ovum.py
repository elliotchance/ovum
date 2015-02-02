import sys

__version__ = '1.0'

def main(args):
    if args[0] == 'require':
        print "Usage: ovum require <package>"
    else:
        print "ovum v%s" % __version__

if __name__ == "__main__":
    main(sys.argv[1:])

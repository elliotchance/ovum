import sys

__version__ = '1.0'

def require(args):
    if len(args) == 0:
        print "Usage: ovum require <package>"
        return

    open('ovum.yml', 'a').close()

def main(args):
    if args[0] == 'require':
        return require(args[1:])

    print "ovum v%s" % __version__

if __name__ == "__main__":
    main(sys.argv[1:])

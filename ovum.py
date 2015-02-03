import sys
import yaml
import os

__version__ = '1.0'
__ovum_yml__ = 'ovum.yml'

def fetch_pypi(name):
    print "Could not find package: %s" % name

def require(args, dev):
    key = 'require-dev' if dev else 'require'

    if len(args) == 0:
        print "Usage: ovum %s <package>" % key
        return

    yml = {}
    if os.path.exists(__ovum_yml__):
        with open(__ovum_yml__, 'r') as file:
            yml = yaml.load(file)
    else:
        open(__ovum_yml__, 'w').close()

    if key not in yml:
        yml[key] = []

    yml[key].append(args[0])

    with open(__ovum_yml__, 'w') as file:
        file.write(yaml.dump(yml, default_flow_style=False))

    fetch_pypi(args[0])

def main(args):
    if args[0] == 'require':
        return require(args[1:], False)
    elif args[0] == 'require-dev':
        return require(args[1:], True)
    elif args[0] == 'install':
        if not os.path.exists('vendor'):
            os.mkdir('vendor')

    print "ovum v%s" % __version__

if __name__ == "__main__":
    main(sys.argv[1:])

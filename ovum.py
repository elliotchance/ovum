import sys
import yaml
import os.path

__version__ = '1.0'
__ovum_yml__ = 'ovum.yml'

def require(args):
    if len(args) == 0:
        print "Usage: ovum require <package>"
        return

    yml = {}
    if os.path.exists(__ovum_yml__):
        with open(__ovum_yml__, 'r') as file:
            yml = yaml.load(file)
    else:
        open('ovum.yml', 'w').close()

    if 'require' not in yml:
        yml['require'] = []

    yml['require'].append(args[0])

    with open('ovum.yml', 'w') as file:
        file.write(yaml.dump(yml, default_flow_style=False))

def main(args):
    if args[0] == 'require':
        return require(args[1:])
    elif args[0] == 'require-dev':
        print "Usage: ovum require-dev <package>"
    else:
        print "ovum v%s" % __version__

if __name__ == "__main__":
    main(sys.argv[1:])

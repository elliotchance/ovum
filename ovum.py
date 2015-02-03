import sys
import yaml
import os
import urllib2
import json
from version import Version
import re

__version__ = '1.0'
__ovum_yml__ = 'ovum.yml'

class Versions:
    def __init__(self, versions):
        self.versions = [Version(self.normalized(version)) for version
                         in versions]

    def normalized(self, version):
        if re.match('^(\d+)$', version):
            return "%s.0.0" % version
        if re.match('^(\d+).(\d+)$', version):
            return "%s.0" % version
        return version

    def __len__(self):
        return len(self.versions)

    def latest(self):
        if self.versions:
            return sorted(self.versions, reverse=True)[0]

        return None

class PyPIPackage:
    def __init__(self, name):
        self.name = name

    def fetch(self):
        # This is a temporary safety precaution and should be removed in the
        # future.
        if not self.name:
            return

        url = 'http://pypi.python.org/pypi/%s/json' % self.name

        try:
            data = urllib2.urlopen(url).read()
        except:
            raise RuntimeError("Could not find package: %s" % self.name)

class CLI:
    def get_package_for_name(self, name):
        return PyPIPackage(name)

    def require(self, args, dev):
        key = 'require-dev' if dev else 'require'

        if len(args) == 0:
            print "Usage: ovum %s <package>" % key
            return

        try:
            package = self.get_package_for_name(args[0])
            package.fetch()
        except RuntimeError as e:
            print e
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

    def main(self, args):
        if args[0] == 'require':
            return self.require(args[1:], False)
        elif args[0] == 'require-dev':
            return self.require(args[1:], True)
        elif args[0] == 'install':
            if not os.path.exists('vendor'):
                os.mkdir('vendor')

        print "ovum v%s" % __version__

if __name__ == "__main__":
    cli = CLI()
    cli.main(sys.argv[1:])

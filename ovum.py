import sys
import os
import urllib2
import json
from version import Version
import re

__version__ = '1.0'
__ovum_file__ = 'ovum.json'
__ovum_lock_file__ = 'ovum.lock'

class Versions:
    def __init__(self, versions):
        self.versions = []
        for version in versions:
            try:
                self.versions.append(Version(self.normalized(version)))
            except:
                # Unfortunately we must ignore this version. :(
                pass

    def normalized(self, version):
        if re.match('^\d+.\d+$', version):
            version = "%s.0" % version
        elif re.match('^\d+$', version):
            version = "%s.0.0" % version

        m = re.match('^(.+)([ab])(\d*)$', version)
        if m:
            n = m.group(3) if m.group(3) else 1
            if m.group(2) is 'a':
                version = "%s-alpha.%s" % (m.group(1), n)
            else:
                version = "%s-beta.%s" % (m.group(1), n)

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
            return json.loads(urllib2.urlopen(url).read())
        except:
            raise RuntimeError("Could not find package: pypi:%s" % self.name)

    def available_versions(self):
        return Versions(self.fetch()["releases"].keys())

class BaseConfigFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.config, file, indent=2)

class LockFile(BaseConfigFile):
    def __init__(self):
        BaseConfigFile.__init__(self, __ovum_lock_file__)

    def add_resolved(self, package_name, version):
        if 'resolved' not in self.config:
            self.config['resolved'] = {}
        self.config['resolved'][package_name] = version

class ConfigFile(BaseConfigFile):
    def __init__(self):
        BaseConfigFile.__init__(self, __ovum_file__)

    def add_require(self, package_name, version, dev):
        key = 'require-dev' if dev else 'require'
        if key not in self.config:
            self.config[key] = {}
        self.config[key][package_name] = version

class CLI:
    def get_package_for_name(self, name):
        return PyPIPackage(name)

    def require(self, args, dev):
        key = 'require-dev' if dev else 'require'

        if len(args) == 0:
            print "Usage: ovum %s <package>" % key
            return

        package_name = args[0]
        config_file = ConfigFile()
        lock_file = LockFile()

        config_file.add_require(package_name, "*", dev)

        try:
            package = self.get_package_for_name(package_name[5:])
            package.fetch()
        except RuntimeError as e:
            print e
            return

        latest_version = str(package.available_versions().latest())
        lock_file.add_resolved(package_name, latest_version)

        config_file.save()
        lock_file.save()

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

from unittest import TestCase
import subprocess
from ovum import *
import ovum

class TestOvum(TestCase):
    def setup_config_file(self, contents):
        with open(ovum.__ovum_file__, 'w') as file:
            file.write(contents)

    def assertJSON(self, json1, json2):
        self.assertEqual(json.loads(json1), json.loads(json2))

    def run_ovum(self, args):
        command = ['python', 'ovum.py']
        p = subprocess.Popen(command + args, stdout=subprocess.PIPE)
        return p.communicate()

    def assert_ovum_output(self, args, expected_output, expected_error=None):
        """
        :type args: list
        """
        out, err = self.run_ovum(args)
        self.assertEqual(err, expected_error)
        self.assertEqual(out, expected_output)

    def test_version(self):
        self.assert_ovum_output(['--version'], "ovum v1.0\n")

    def test_module_version(self):
        self.assertEqual(ovum.__version__, '1.0')

    def test_require_with_missing_argument(self):
        self.assert_ovum_output(['require'], "Usage: ovum require <package>\n")

    def test_requiredev_with_missing_argument(self):
        self.assert_ovum_output(['require-dev'],
                                "Usage: ovum require-dev <package>\n")

    def test_install(self):
        try:
            os.remove('vendor')
        except:
            pass
        self.run_ovum(['install'])
        self.assertTrue(os.path.exists('vendor'))

    def test_installing_pypi_package_that_does_not_exist(self):
        self.assert_ovum_output(['require', 'pypi:hkdsfhgfd'],
                                "Could not find package: pypi:hkdsfhgfd\n")

    def test_installing_a_package_that_doesnt_exist_does_not_modify_json(self):
        original_json = '{"require-dev":["pypi:mock"]}'
        self.setup_config_file(original_json)
        self.run_ovum(['require', 'pypi:hkdsfhgfd'])
        with open(ovum.__ovum_file__, "r") as yml:
            data = yml.read()
            self.assertJSON(data, original_json)

    def assertConfigFile(self, expected):
        with open(ovum.__ovum_file__, "r") as config:
            data = config.read()
            self.assertJSON(data, expected)

    def assertLockFile(self, expected):
        with open(ovum.__ovum_lock_file__, "r") as config:
            data = config.read()
            self.assertJSON(data, expected)

    def test_require_with_no_config_file(self):
        os.remove(ovum.__ovum_file__)
        os.remove(ovum.__ovum_lock_file__)

        self.run_ovum(['require', 'pypi:mock'])

        self.assertConfigFile('{"require":{"pypi:mock":"*"}}')
        self.assertLockFile('{"resolved":{"pypi:mock":"1.0.1"}}')


class TestPyPIPackage(TestCase):
    def test_fetching_a_package_that_exists_will_not_raise_exception(self):
        package = PyPIPackage('mock')
        package.fetch()

    def test_available_versions(self):
        package = PyPIPackage('mock')
        self.assertTrue(Version('1.0.1')
                        in package.available_versions().versions)


class TestVersions(TestCase):
    def test_size_of_no_items_is_zero(self):
        versions = Versions([])
        self.assertEqual(len(versions), 0)

    def test_size_of_one_version_is_one(self):
        versions = Versions(['1.0.0'])
        self.assertEqual(len(versions), 1)

    def test_latest_version_with_zero_versions_is_none(self):
        versions = Versions([])
        self.assertEqual(versions.latest(), None)

    def test_latest_version_with_one_versions(self):
        versions = Versions(['1.0.0'])
        self.assertEqual(versions.latest(), Version('1.0.0'))

    def test_latest_version_with_two_versions(self):
        versions = Versions(['1.0.0', '1.2.0'])
        self.assertEqual(versions.latest(), Version('1.2.0'))

    def test_alternate_format_1(self):
        versions = Versions(['1.0'])
        self.assertEqual(versions.latest(), Version('1.0.0'))

    def test_alternate_format_2(self):
        versions = Versions(['1'])
        self.assertEqual(versions.latest(), Version('1.0.0'))

    def test_alternate_format_3(self):
        versions = Versions(['2.3.1b14'])
        self.assertEqual(versions.latest(), Version('2.3.1-beta.14'))

    def test_alternate_format_4(self):
        versions = Versions(['2.3.1b'])
        self.assertEqual(versions.latest(), Version('2.3.1-beta.1'))

    def test_alternate_format_5(self):
        versions = Versions(['2.3.1a2'])
        self.assertEqual(versions.latest(), Version('2.3.1-alpha.2'))

    def test_bad_version_will_not_be_included(self):
        versions = Versions(['1', 'foo'])
        self.assertEqual(versions.latest(), Version('1.0.0'))

from unittest import TestCase
import subprocess
import os.path
from ovum import *
from mock import MagicMock
import ovum

class OvumTestCase(TestCase):
    def setup_yml(self, yml):
        with open('ovum.yml', 'w') as file:
            file.write(yml)

class TestCLI(OvumTestCase):
    def run_cli(self, args):
        cli = CLI()
        cli.get_package_for_name = MagicMock(return_value=PyPIPackage(''))
        cli.main(args)
        return cli

    def test_require_will_append_yml_file(self):
        self.setup_yml('require:\n- "pypi:mock"')
        self.run_cli(['require', 'pypi:mock2'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require:\n- pypi:mock\n- pypi:mock2\n')

    def test_require_will_create_yml_if_not_exists(self):
        os.remove('ovum.yml')
        self.run_cli(['require', 'pypi:mock'])
        self.assertTrue(os.path.exists('ovum.yml'))

    def test_require_will_setup_yml_file(self):
        os.remove('ovum.yml')
        self.run_cli(['require', 'pypi:mock'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require:\n- pypi:mock\n')

    def test_requiredev_will_append_yml_file(self):
        self.setup_yml('require-dev:\n- "pypi:mock"')
        self.run_cli(['require-dev', 'pypi:mock2'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require-dev:\n- pypi:mock\n- pypi:mock2\n')

    def test_requiredev_will_create_yml_if_not_exists(self):
        os.remove('ovum.yml')
        self.run_cli(['require-dev', 'pypi:mock'])
        self.assertTrue(os.path.exists('ovum.yml'))

    def test_requiredev_will_setup_yml_file(self):
        os.remove('ovum.yml')
        self.run_cli(['require-dev', 'pypi:mock'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require-dev:\n- pypi:mock\n')

class TestOvum(OvumTestCase):
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

    def test_cli_version(self):
        self.assert_ovum_output(['--version'], "ovum v1.0\n")

    def test_module_version(self):
        self.assertEqual(ovum.__version__, '1.0')

    def test_require_with_missing_argument(self):
        self.assert_ovum_output(['require'], "Usage: ovum require <package>\n")

    def test_requiredev_with_missing_argument(self):
        self.assert_ovum_output(['require-dev'],
                                "Usage: ovum require-dev <package>\n")

    def test_install_creates_vendor_folder(self):
        try:
            os.remove('vendor')
        except:
            pass
        self.run_ovum(['install'])
        self.assertTrue(os.path.exists('vendor'))

    def test_installing_pypi_package_that_does_not_exist(self):
        self.assert_ovum_output(['require', 'pypi:hkdsfhgfd'],
                                "Could not find package: pypi:hkdsfhgfd\n")

    def test_installing_a_package_that_doesnt_exist_does_not_modify_yml(self):
        self.setup_yml('require-dev:\n- pypi:mock\n')
        self.run_ovum(['require', 'pypi:hkdsfhgfd'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require-dev:\n- pypi:mock\n')


class TestPyPIPackage(TestCase):
    def test_fetching_a_package_that_exists_will_not_raise_exception(self):
        package = PyPIPackage('mock')
        package.fetch()


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

from unittest import TestCase
import subprocess
import ovum
import os.path

class TestOvum(TestCase):
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

    def test_require_will_create_yml_if_not_exists(self):
        os.remove('ovum.yml')
        self.run_ovum(['require', 'pypi:mock'])
        self.assertTrue(os.path.exists('ovum.yml'))

    def test_require_will_setup_yml_file(self):
        os.remove('ovum.yml')
        self.run_ovum(['require', 'pypi:mock'])
        with open("ovum.yml", "r") as yml:
            data = yml.read()
            self.assertEqual(data, 'require:\n- "pypi:mock"')

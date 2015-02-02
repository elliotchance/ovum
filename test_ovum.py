from unittest import TestCase
import subprocess
import ovum

class TestOvum(TestCase):
    def assert_ovum_output(self, args, expected_output, expected_error=None):
        """
        :type args: list
        """
        command = ['python', 'ovum.py']
        p = subprocess.Popen(command + args, stdout=subprocess.PIPE)
        out, err = p.communicate()
        self.assertEqual(err, expected_error)
        self.assertEqual(out, expected_output)

    def test_cli_version(self):
        self.assert_ovum_output(['--version'], "ovum v1.0\n")

    def test_module_version(self):
        self.assertEqual(ovum.__version__, '1.0')

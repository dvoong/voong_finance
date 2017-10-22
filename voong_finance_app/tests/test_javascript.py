from django.test import TestCase
from voong_finance.settings import BASE_DIR
import os
import subprocess

class TestJavascript(TestCase):

    def test(self):
        os.chdir(BASE_DIR)
        self.assertEqual(subprocess.call(["qunit", 'voong_finance_app/tests/js/*.js']), 0)
        

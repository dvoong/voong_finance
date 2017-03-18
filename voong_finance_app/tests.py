from unittest import mock
from django.test import TestCase

class VoongTestCase(TestCase):

    def setUp(self):
        self.patches = []

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        
    def mock(self, path):
        patch = mock.patch(path)
        self.patches.append(patch)
        return patch.start()

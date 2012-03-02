from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
import unittest


class TestTool(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def test_dummy(self):
        self.assertTrue(1)

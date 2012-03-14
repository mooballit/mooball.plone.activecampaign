from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.tool import ActiveCampaignList
import unittest
import zope.interface


class TestListUnit(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignList, ActiveCampaignList))

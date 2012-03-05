from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
import unittest
import zope.interface
from mooball.plone.activecampaign.tool import ActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber


class TestToolInterfaces(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignTool, ActiveCampaignTool))
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignSubscriber, ActiveCampaignSubscriber))

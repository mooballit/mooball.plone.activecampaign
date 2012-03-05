from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from mooball.plone.activecampaign.tool import ActiveCampaignTool
import unittest
import zope.interface


class TestToolInterfaces(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignTool, ActiveCampaignTool))
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignSubscriber, ActiveCampaignSubscriber))


class TestTool(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def test_retrieval(self):
        tool = getToolByName(self.layer['portal'],
                             'portal_activecampaign')
        self.assertTrue(
            IActiveCampaignTool.providedBy(tool))

        tool = zope.component.getUtility(IActiveCampaignTool)
        self.assertTrue(
            IActiveCampaignTool.providedBy(tool))

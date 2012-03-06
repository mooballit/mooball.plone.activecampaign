from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from mooball.plone.activecampaign.tool import ActiveCampaignTool
import unittest
import zope.interface


class TestToolUnit(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignTool, ActiveCampaignTool))
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignSubscriber, ActiveCampaignSubscriber))

    def test_format_url_keys(self):
        tool = ActiveCampaignTool()
        result = tool.format_url_keys('p', [1, 'short-list'])
        self.assertEquals(['p[1]', 'p[short-list]'], result)


class TestTool(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def setUp(self):
        self.tool = getToolByName(self.layer['portal'],
                                  'portal_activecampaign')

    def test_retrieval(self):
        tool = getToolByName(self.layer['portal'],
                             'portal_activecampaign')
        self.assertTrue(
            IActiveCampaignTool.providedBy(tool))

        tool = zope.component.getUtility(IActiveCampaignTool)
        self.assertTrue(
            IActiveCampaignTool.providedBy(tool))

    def test_properties(self):
        self.assertEqual('', self.tool.get_api_url())

    def test_add_subscriber(self):
        self.assertRaises(AssertionError, self.tool.add_subscriber,
                          object, [])
        self.assertRaises(AssertionError,
                          self.tool.add_subscriber,
                          ActiveCampaignSubscriber(u'tom@mooball.net'),
                          [])

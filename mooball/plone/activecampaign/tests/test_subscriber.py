from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
import unittest
import zope.interface


class TestSubscriberUnit(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignSubscriber, ActiveCampaignSubscriber))

    def test_assertion_on_creation(self):
        self.assertTrue(
            ActiveCampaignSubscriber(
                u'tom@mooball.net', sid=long(2)))

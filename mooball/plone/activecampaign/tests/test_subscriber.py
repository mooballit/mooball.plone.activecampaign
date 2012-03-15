from mooball.plone.activecampaign.interfaces import IActiveCampaignList
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

    def test_convert_listdata(self):
        data = {'2': dict(status=1, id=u'20', listname=u'TestList')}
        subscriber = ActiveCampaignSubscriber(
            u'tom@mooball.net', lists=data)
        self.assertEqual(1, len(subscriber.lists))
        self.assertEqual('TestList', subscriber.lists[0].name)
        self.assertTrue(
            IActiveCampaignList.providedBy(subscriber.lists[0]))

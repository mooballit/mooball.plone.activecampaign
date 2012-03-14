from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.interfaces import IActiveCampaignField
from mooball.plone.activecampaign.tool import ActiveCampaignList
import unittest
import zope.interface


class TestListUnit(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignList, ActiveCampaignList))

    def test_convert_fields(self):
        list = ActiveCampaignList(
            name=u'Test List',
            listid=u'1',
            fields=[dict(id=u'1', title=u'Country', req=u'1')]
        )
        self.assertTrue(IActiveCampaignField.providedBy(list.fields[0]))

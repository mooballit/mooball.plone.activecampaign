from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.tool import ActiveCampaignList
import json
import unittest
import zope.interface


class TestListUnit(unittest.TestCase):

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignList, ActiveCampaignList))

    def test_from_json(self):
        list = ActiveCampaignList.from_json(
            json.dumps(
                dict(result_code=0,
                     listid='2',
                     name='Test List')
            )
        )
        self.assertTrue(IActiveCampaignList.providedBy(list))

from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
from mooball.plone.activecampaign.interfaces import IActiveCampaignField
from mooball.plone.activecampaign.tool import ActiveCampaignField
import unittest
import zope.interface
import zope.schema.interfaces


class TestFieldUnit(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def test_interfaces(self):
        self.assertTrue(
            zope.interface.verify.verifyClass(
                IActiveCampaignField, ActiveCampaignField))

    def test_get_parameters(self):
        data = dict(title=u'Field 1', type=u'1', req=u'1',
                    onfocus=u'', bubble_content=u'New Field')
        field = ActiveCampaignField(**data)

        data.update(perstag=u'', show_in_list='1', label='1')
        self.assertEquals(data, field.get_parameters())

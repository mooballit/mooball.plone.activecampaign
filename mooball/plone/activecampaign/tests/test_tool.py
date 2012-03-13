from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from mooball.plone.activecampaign.tool import ActiveCampaignTool
import StringIO
import fudge
import fudge.inspector
import json
import logging
import testfixtures
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

    def test_get_formatted_fields(self):
        tool = ActiveCampaignTool()
        expected = {'p[1]': '1', 'p[short-list]': 'short-list'}
        result = tool.get_formatted_fields('p', ['1', 'short-list'])
        self.assertEquals(expected, result)

        expected = {'p[1]': 'foo'}
        result = tool.get_formatted_fields('p', ['1'], ['foo'])
        self.assertEquals(expected, result)


class TestToolFudged(unittest.TestCase):

    def setUp(self):
        self.tool = ActiveCampaignTool()
        self.tool.manage_addProperty('api_url', 'http://ignored', 'string')
        self.tool.manage_addProperty('api_username', '', 'string')
        self.tool.manage_addProperty('api_password', '', 'string')

    def fudgify(self, resultdata, fakeurlopen):
        """ Encodes it to json and declares a call order on the fudged
            urllib2.urlopen.
        """
        returnval = StringIO.StringIO(json.dumps(resultdata))
        fakeurlopen.is_callable().with_args(
            'http://ignored',
            fudge.inspector.arg.any()).returns(returnval)
        return fakeurlopen

    @fudge.patch('urllib2.urlopen')
    def test_add_list(self, urlopen):
        expected = 1
        resultdata = dict(id=expected,
                          result_code=1,
                          result_message="success",
                          result_output="json")
        urlopen = self.fudgify(resultdata, urlopen)

        result = self.tool.add_list('api-test', 'API Testing')
        self.assertEqual(expected, result)

    @fudge.patch('urllib2.urlopen')
    def test_get_list_information(self, urlopen):
        resultdata = {
            0: {'id': '2',
                'stringid': 'bd-test',
                'name': 'BD-Test',
                'listid': '2'
               },
            1: {'id': 'foobar',
                'stringid': 'another-test',
                'name': 'Bla',
                'listid': '8',
               },
            'result_code': 1,
            'result_message': 'success',
            'result_output': 'json',
        }
        urlopen = self.fudgify(resultdata, urlopen)

        result = self.tool.get_list_information()
        self.assertEqual(2, len(result))

        result = self.tool.get_list_ids()
        self.assertEqual([u'8', u'2'], result)

    @fudge.patch('urllib2.urlopen')
    def test_post_to_active_campaign(self, urlopen):
        result = dict(result_code=0,
                     result_message=u"error occured",
                     result_output="json")

        urlopen = self.fudgify(result, urlopen)

        with testfixtures.LogCapture(level=logging.ERROR) as l:
            self.tool.post_to_active_campaign(dict(api_action='api_action'))
            l.check(
                (self.tool.id, 'ERROR', result['result_message'])
            )

    @fudge.patch('urllib2.urlopen')
    def test_post_to_active_campaign_garbaged(self, urlopen):
        result = "Garbage"
        urlopen = self.fudgify(result, urlopen)

        self.assertRaises(ValueError, self.tool.post_to_active_campaign,
                          dict(api_action='api_action'))


class TestTool(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def setUp(self):
        self.tool = zope.component.getUtility(IActiveCampaignTool)

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

    def test_add_subscriber_parameters(self):
        self.assertRaises(AssertionError, self.tool.add_subscriber,
                          object, [])
        self.assertRaises(AssertionError,
                          self.tool.add_subscriber,
                          ActiveCampaignSubscriber(u'tom@mooball.net'),
                          [])


from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from mooball.plone.activecampaign.interfaces import APIUnauthorized
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from mooball.plone.activecampaign.tool import ActiveCampaignTool
from mooball.plone.activecampaign.tool import after_tool_added
import StringIO
import fudge
import fudge.inspector
import json
import logging
import os.path
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
        self.assertEqual(['p[1]', 'p[short-list]'], result)

    def test_get_formatted_fields(self):
        tool = ActiveCampaignTool()
        expected = {'p[1]': '1', 'p[short-list]': 'short-list'}
        result = tool.get_formatted_fields('p', ['1', 'short-list'])
        self.assertEqual(expected, result)

        expected = {'p[1]': 'foo'}
        result = tool.get_formatted_fields('p', ['1'], ['foo'])
        self.assertEqual(expected, result)


class TestToolFudged(unittest.TestCase):

    layer = ACTIVECAMPAIGN_FUNCTIONAL_TESTING

    def setUp(self):
        self.tool = ActiveCampaignTool()
        after_tool_added(self.tool, None)
        self.tool.manage_changeProperties(api_url='http://ignored')

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

        result = self.tool.get_list_information(['2'])
        self.assertEqual(1, len(result))
        self.assertEqual('BD-Test', result[0].name)

        result = self.tool.get_list_ids()
        self.assertEqual([u'foobar', u'2'], result)

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

    @fudge.patch('urllib2.urlopen')
    def test_post_to_active_unauthorized(self, urlopen):
        urlopen = self.fudgify(
            dict(result_code=0,
                 result_message='You are not authorized to access this file',
                 result_output='json'), urlopen)

        self.assertRaises(APIUnauthorized,
                          self.tool.post_to_active_campaign,
                          dict(api_action='api_action'))

    @fudge.patch('urllib2.urlopen')
    def test_get_lists_by(self, urlopen):
        resultfilep = os.path.join(
            os.path.dirname(__file__), 'testdata', 'get_lists_by.json')
        list_listfp = os.path.join(
            os.path.dirname(__file__), 'testdata', 'list_list.json')
        jsondata = json.load(open(list_listfp, 'r'))

        urlopen = self.fudgify(json.load(open(resultfilep, 'r')), urlopen)
        urlopen.next_call().with_args(
            'http://ignored',
            fudge.inspector.arg.any()).returns(
                StringIO.StringIO(json.dumps(jsondata)))

        subscriber = ActiveCampaignSubscriber(email=u'roman@mooball.net')
        result = self.tool.get_lists_by(subscriber)
        self.assertEqual(1, len(result))


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


# -*- coding: utf-8 -*-
from mooball.plone.activecampaign.testing import\
        ACTIVECAMPAIGN_INTEGRATION_TESTING
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from plone.testing import layered
import doctest
import os.path
import transaction
import unittest
import zope.component


def debug_contents(browsercontents):
    with open('/tmp/debug.html', 'w') as f:
        f.write(browsercontents)


def set_api_url_to_action(api_action):
    tool = zope.component.getUtility(IActiveCampaignTool)
    api_url = os.path.join(os.path.dirname(__file__), 'testdata',
                           '{api_action}.json'.format(api_action=api_action))
    tool.manage_changeProperties(api_url='file://{api_url}'.format(
        api_url=api_url))
    transaction.commit()


GLOBS = dict(debug_contents=debug_contents,
             set_api_url_to_action=set_api_url_to_action)
OPTIONS = (doctest.REPORT_ONLY_FIRST_FAILURE |
           doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)


def tool_setUp(context):
    tool = zope.component.getUtility(IActiveCampaignTool)
    tool.manage_changeProperties(api_url='file:///tmp/test.json',
                                 api_username='roman',
                                 api_password='secret')
    transaction.commit()


def test_suite():
    return unittest.TestSuite([
        layered(doctest.DocFileSuite(
            'README.txt', package='mooball.plone.activecampaign',
            optionflags=OPTIONS, globs=GLOBS, setUp=tool_setUp),
            layer=ACTIVECAMPAIGN_INTEGRATION_TESTING),
        ])

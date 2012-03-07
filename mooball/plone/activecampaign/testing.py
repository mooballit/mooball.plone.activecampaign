from Products.CMFCore.utils import getToolByName
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig
import mooball.plone.activecampaign
import os


TESTLISTID = 'mooball-ac-testlist'


class ActiveCampaignBase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        xmlconfig.file('configure.zcml', mooball.plone.activecampaign,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'mooball.plone.activecampaign:default')

        # configure test environment
        ac_tool = getToolByName(portal, 'portal_activecampaign')
        keys = ['api_url', 'api_user', 'api_password']
        # this obviously dies if the developer hasn't set the
        # correct environment variables, but we can't run tests with
        # half of the information we really need.
        options = [(k, os.environ[k]) for k in keys]
        ac_tool.manage_changeProperties(**dict(options))

        # create a test list
        self.listid = ac_tool.add_list(TESTLISTID, 'Mooball Plone AC TestList')

    def tearDownPloneSite(self, portal):
        ac_tool = getToolByName(portal, 'portal_activecampaign')
        ac_tool.delete_lists([self.listid])


ACTIVECAMPAIGN_FIXTURE = ActiveCampaignBase()
ACTIVECAMPAIGN_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ACTIVECAMPAIGN_FIXTURE,), name="ActiveCampaignBase:Integration")
ACTIVECAMPAIGN_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ACTIVECAMPAIGN_FIXTURE,), name="ActiveCampaignBase:Functional")

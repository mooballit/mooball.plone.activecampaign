from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig
import mooball.plone.activecampaign


class ActiveCampaignBase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        xmlconfig.file('configure.zcml', mooball.plone.activecampaign,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'mooball.plone.activecampaign:default')


ACTIVECAMPAIGN_FIXTURE = ActiveCampaignBase()
ACTIVECAMPAIGN_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ACTIVECAMPAIGN_FIXTURE,), name="ActiveCampaignBase:Integration")
ACTIVECAMPAIGN_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ACTIVECAMPAIGN_FIXTURE,), name="ActiveCampaignBase:Functional")

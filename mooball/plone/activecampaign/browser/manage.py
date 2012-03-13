from five import grok
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool


class ManageMailingLists(grok.View):
    grok.context(IActiveCampaignTool)
    grok.require('cmf.ManagePortal')

from Products.CMFCore import utils as cmf_utils


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    from mooball.plone.activecampaign.tool import ActiveCampaignTool

    cmf_utils.ToolInit(
        'ActiveCampaign Tool',
        tools=(ActiveCampaignTool, ),
        icon='tool.gif',
        ).initialize(context)

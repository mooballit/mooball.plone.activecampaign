import zope.interface


class IActiveCampaignTool(zope.interface.Interface):
    """
    Interface to synchronise user data with with active campaign
    (eg.for mailing list subscriptions).
    """

    def synchronise_user_data(data):
        """synchronise given user data."""


class IActiveCampaignUser(zope.interface.Interface):
    """
    Marker interface for users who can be subscribed/unsubscribed to
    active campaign.
    """

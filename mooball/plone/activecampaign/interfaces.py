import zope.interface
import zope.schema


UNCONFIRMED = 0
ACTIVE = 1
UNSUBSCRIBED = 2


class IActiveCampaignTool(zope.interface.Interface):
    """
    Interface to synchronise user data with with active campaign
    (eg.for mailing list subscriptions).
    """

    def add_subscriber(subscriber, listids, custom_parameters):
        """
        Adds given instance which provides
        :class:`IActiveCampaignSubscriber` to the given lists.

        :param subscriber: A :class:`IActiveCampaignSubscriber` instance
        :param listids: A list of mailing list ids to subscribe the
                        given subscriber to.
        :param custom_parameters: Custom parameters as a dictionary which are
                       passed onto the subscribe POST (e.g. if you want
                       to pass in additional fields). No further
                       checking is done on these arguments, so be sure
                       you are passing in correct data.
        :rtype: None
        :raises: raises ``AssertionError`` if given subscriber does not
                 provide :class:`IActiveCampaignSubscriber`

        """

    def get_list_ids():
        """
        Returns all ids of available mailing lists.

        :rtype: list of ids
        """

    def get_api_url():
        """
        Returns the API URL or '' if no URL is set.

        The property name is: ``api_url``
        """

    def get_api_username():
        """
        Returns the API username or '' if no URL is set.

        The property name is: ``api_user``
        """

    def get_api_password():
        """
        Returns the API password or '' if no password is set.

        The property name is: ``api_password``
        """


class IActiveCampaignUser(zope.interface.Interface):
    """
    Marker interface for users who can be subscribed/unsubscribed to
    active campaign.
    """


class IActiveCampaignSubscriber(zope.interface.Interface):
    """
    A subscriber which can be added/removed from mailing lists.

    """

    email = zope.schema.TextLine(
        title=u'Email',
    )

    first_name = zope.schema.TextLine(
        title=u'First Name'
    )

    last_name = zope.schema.TextLine(
        title=u'Last Name'
    )

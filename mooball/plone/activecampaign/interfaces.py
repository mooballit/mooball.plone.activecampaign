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

    def add_subscriber(subscriber, lists):
        """
        Adds given instance which provides
        :class:`IActiveCampaignSubscriber` to the given lists.

        :param subscriber: A :class:`IActiveCampaignSubscriber` instance
        :param lists: The `lists` should be a list of tuples (listid,
                      status). The `status` should be either
                      :const:`UNCONFIRMED`, :const:`ACTIVE`,
                      :const:`UNSUBSCRIBED`.

        :rtype: None
        :raises: raises ``AssertionError`` if given subscriber does not
                 provide :class:`IActiveCampaignSubscriber`

        """

    def get_list_ids():
        """
        Returns all ids of available mailing lists.

        :rtype: list of ids
        """

    def get_api_key():
        """
        Returns the API key or None if no api key is set.
        """

    def get_api_url(self):
        """
        Returns the API URL or None if no URL is set.
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

    def get_listids():
        """
        Returns list ids for given subscriber.

        :rtype: Returns a list of tuples for each mailing list this
                subscriber is subscribed to, e.g. (listid, status)
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

    listids = zope.schema.List(
        title=u'Mailing lists',
        description=(u'A list of tuples of mailing list ids the'
                     ' subscriber should be added to with status, e.g.'
                     ' (listid, status)')
    )
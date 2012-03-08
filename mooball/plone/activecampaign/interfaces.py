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

    def post_to_active_campaign(query):
        """
        Performs the actual post to active campaign and check the
        response.

        The given query is updated with the following data:

        api_user, api_pass, api_output='json'
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
        :raises: ``AssertionError`` if given subscriber does not
                 provide :class:`IActiveCampaignSubscriber`

        """

    def add_list(name, title, **kw):
        """
        Creates a new list with given parameters.

        :param name: URL-safe list name, e.g.: 'api-test'
        :param title: List title for internal use.
        :param kw: Additional keyword arguments which are passed on to
                   the API.
        :rtype: id (int) of the list
        """

    def delete_lists(listids):
        """
        Deletes given mailing list with given ``listids``.

        :param listids: A list of mailing list ids, either string or
                        integer.
        :rtype: 1 = successfull, 0 = failure
        """

    def delete_subscribers(subscribers):
        """
        Deletes given subscribers.

        The given subscribers are looked up by ``email`` to find their
        id and deleted by the given subscriber id.

        :param subscribers: a list of objects providing
                            :class:`IActiveCampaignSubscriber`
        :rtype: None
        """

    def get_subscriber_by(email):
        """
        Returns a subscriber providing :class:`IActiveCampaignSubscriber`.

        :param email: email of the subscriber to look up as string
        :rtype: subscriber or None if the subscriber can not be found.
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

    The subscriber can be created by only providing the email address.
    """

    email = zope.schema.TextLine(
        title=u'Email',
    )

    first_name = zope.schema.TextLine(
        title=u'First Name',
        required=False,
    )

    last_name = zope.schema.TextLine(
        title=u'Last Name',
        required=False,
    )

    sid = zope.schema.Int(
        title=u'Subscriber ID',
        required=False,
    )


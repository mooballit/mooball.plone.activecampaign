import zope.interface
import zope.schema


UNCONFIRMED = 0
ACTIVE = 1
UNSUBSCRIBED = 2


ERROR_CODES = {
    0: "Unknown response code. Please resubmit the subscription form.",
    1: "This list is currently not accepting subscribers. This list has met its top number of allowed subscribers.",
    2: "Your subscription request for this list could not be processed as you are missing required fields.",
    3: "This e-mail address is already subscribed to this mailing list.",
    4: "This e-mail address has been processed in the past to be subscribed, however your subscription was never confirmed.",
    5: "This e-mail address cannot be added to list.",
    6: "This e-mail address has been processed. Please check your email to confirm your subscription.",
    7: "This e-mail address has subscribed to the list.",
    8: "E-mail address is invalid.",
    9: "Subscription could not be processed since you did not select a list. Please select a list and try again.",
    10: "This e-mail address has been processed. Please check your email to confirm your unsubscription.",
    11: "This e-mail address has been unsubscribed from the list.",
    12: "This e-mail address was not subscribed to the list.",
    13: "Thank you for confirming your subscription.",
    14: "Thank you for confirming your unsubscription.",
    15: "Your changes have been saved.",
    16: "Your subscription request for this list could not be processed as you must type your name.",
    17: "This e-mail address is on the global exclusion list.",
    18: "Please type the correct text that appears in the image.",
    19: "Subscriber ID is invalid.",
    20: "You are unable to be added to this list at this time.",
    21: "You selected a list that does not allow duplicates. This email is in the system already, please edit that subscriber instead.",
    22: "This e-mail address could not be unsubscribed.",
    23: "This subscriber does not exist.",
    24: "The link to modify your account has been sent. Please check your email.",
    25: "The image text you typed did not register. Please go back, reload the page, and try again.",
}


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

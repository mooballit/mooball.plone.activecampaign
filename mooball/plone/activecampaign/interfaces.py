import plone.directives.form
import zope.interface
import zope.schema
import zope.schema.vocabulary


UNCONFIRMED = 0
ACTIVE = 1
UNSUBSCRIBED = 2


class APIUnauthorized(IOError):
    """
    Error which is raised if we get an Unauthorized error from the api.

    This error very vague, as it is only specified by a string we
    receive from the API and an error code which is always 0 by a
    failure. This error is raised in :meth:`post_to_active_campaign`
    if:

        * the error code is 0 and
        * ``not authorized`` as a substring of the error message
    """


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

        :raises: ``ValueError`` if the response from the active
                 campaign API call can not be decoded as json
        :raises: ``APIUnauthorized`` if the API can not be accessed due
                 to wrong credentials.
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

    def add_custom_field(field, listids):
        """
        Adds a custom field to mailing lists.

        :param field: A field definition providing
                      :class:`IActiveCampaignField`.
        :param listids: A list of listids.
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

    def delete_subscribers(emails):
        """
        Deletes given subscribers.

        The given subscribers are looked up by ``email`` to find their
        id and deleted by the given subscriber id.

        :param emails: a list of emails of subscribers which should be
                       deleted.
        :rtype: None
        """

    def get_subscriber_by(email):
        """
        Returns a subscriber providing :class:`IActiveCampaignSubscriber`.

        :param email: email of the subscriber to look up as string
        :rtype: subscriber or None if the subscriber can not be found.
        """

    def get_lists_by(subscriber):
        """
        Returns objects providing :class:`IActiveCampaignList` if the
        given subscriber is subscribed to a mailing list. If not, an
        empty list is returned.

        :param subscriber: Object providing :class:`IActiveCampaignSubscriber`
        :rtype: List of objects
        """

    def get_list_ids():
        """
        Returns all ids of available mailing lists.

        :rtype: list of ids
        """

    def get_list_information(listids=None):
        """
        Returns information associated with each mailing list.

        This method is heavily cached (for 1h). The information could be
        outdated.

        :param listids: Can be given a list of listids which are
                        strings. Optional.
        :rtype: List of :class:`IActiveCampaignList` provided objects.
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

    api_url = zope.schema.TextLine(
        title=u'API URL',
    )

    api_user = zope.schema.TextLine(
        title=u'API Username',
    )

    api_password = zope.schema.TextLine(
        title=u'API Password',
        description=(u'An API password to communicate with the API. The'
                     ' password is stored in clear text and send in'
                     ' clear text.')
    )


class IActiveCampaignSubscriber(zope.interface.Interface):
    """
    A subscriber which can be added/removed from mailing lists.

    The subscriber can be created by only providing the email address.

    .. note::

        The subscriber id is an ASCII string. Whatever you pass in,
        it'll become a string. This is because the API doesn't care
        about any other datatype and even returns id's as strings.
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

    sid = zope.schema.ASCIILine(
        title=u'Subscriber ID',
        required=False,
    )

    lists = zope.schema.List(
        title=u'Subscribed Lists',
        required=False,
    )


def field_type_vocab(context):
    return zope.schema.vocabulary.SimpleVocabulary(
        [zope.schema.vocabulary.SimpleTerm(title=u'Field', value=u'1'),
         zope.schema.vocabulary.SimpleTerm(title=u'Text Box', value=u'2'),
         zope.schema.vocabulary.SimpleTerm(title=u'Checkbox', value=u'3'),
         zope.schema.vocabulary.SimpleTerm(title=u'Radio', value=u'4'),
         zope.schema.vocabulary.SimpleTerm(title=u'Dropdown', value=u'5'),
         zope.schema.vocabulary.SimpleTerm(title=u'Hidden field', value=u'6'),
         zope.schema.vocabulary.SimpleTerm(title=u'List Box', value=u'7'),
         zope.schema.vocabulary.SimpleTerm(title=u'Checkbox Group',
                                           value=u'8'),
         zope.schema.vocabulary.SimpleTerm(title=u'Date', value=u'9'),
        ]
    )


class IActiveCampaignField(zope.interface.Interface):
    """
    A field definition for an active campaigin mailing list field.
    """

    title = zope.schema.TextLine(
        title=u'Field Title',
        description=u'Example: Field 1',
    )

    type = zope.schema.Choice(
        title=u'Field Type',
        vocabulary='Field Types',
    )

    req = zope.schema.TextLine(
        title=u'Required Field?',
    )

    onfocus = zope.schema.TextLine(
        title=u'Default Value',
        required=False,
    )

    bubble_content = zope.schema.TextLine(
        title=u'Tooltip',
        required=False,
    )

    label = zope.schema.Choice(
        title=u'Label Position',
        values=['1', '0'],
        default='1',
    )

    show_in_list = zope.schema.Choice(
        title=u'Show on list page?',
        description=u'Show on subscriber list page (as another column)?',
        values=['1', '0'],
        default='1',
    )

    perstag = zope.schema.TextLine(
        title=u'Placeholder tag',
        description=u'Unique tag used as a placeholder for dynamic content',
        default=u'',
    )

    fieldtype = zope.interface.Attribute(
        'Human readable field type, e.g.: Checkbox')

    def get_parameters():
        """
        Returns a dictionary of parameters retrieved from
        :class:`IActiveCampaignField` attributes.
        """


class IActiveCampaignList(plone.directives.form.Schema):
    """
    An active campaign mailing list.
    """

    plone.directives.form.omitted('listid')
    listid = zope.schema.TextLine(
        title=u'List ID',
    )

    name = zope.schema.TextLine(
        title=u'Title',
    )

    plone.directives.form.omitted('cdate')
    cdate = zope.schema.Datetime(
        title=u'Created',
    )

    plone.directives.form.omitted('subscribers')
    subscribers = zope.schema.TextLine(
        title=u'Subscribers',
    )

    plone.directives.form.omitted('campaigns')
    campaigns = zope.schema.TextLine(
        title=u'Campaigns Sent',
    )

    plone.directives.form.omitted('emails')
    emails = zope.schema.TextLine(
        title=u'Emails Sent',
    )

    plone.directives.form.omitted('fields')
    fields = zope.schema.List(
        title=u'Fields',
        value_type=zope.schema.Object(
            schema=IActiveCampaignField
        ),
        required=False,
    )

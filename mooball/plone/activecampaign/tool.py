from mooball.plone.activecampaign.interfaces import ACTIVE
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
import Globals
import OFS.Folder
import OFS.SimpleItem
import Products.CMFCore.utils
import json
import logging
import urllib
import urllib2
import zope.container.interfaces
import zope.interface


class ActiveCampaignTool(Products.CMFCore.utils.UniqueObject,
                         OFS.Folder.Folder):

    zope.interface.implements(IActiveCampaignTool)

    id = 'portal_activecampaign'
    meta_type = 'ActiveCampaignTool'
    plone_tool = 1

    manage_options = OFS.Folder.Folder.manage_options
    manage_options = [opt for opt in manage_options if opt['label'] not in
                      ['Contents', 'View']]

    def add_subscriber(self, subscriber, listids, custom_parameters=None):
        assert IActiveCampaignSubscriber.providedBy(subscriber)

        params = dict(
            api_user=self.get_api_username(),
            api_pass=self.get_api_password(),
            api_action='subscriber_add',
            api_output='json',
            email=subscriber.email,
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
        )
        # XXX WTF
        params.update(
            self.get_formatted_fields('p', listids, listids)
        )
        params.update(
            self.get_formatted_fields('status', listids,
                                      [ACTIVE] * len(listids))
        )

        if custom_parameters is not None:
            params.update(custom_parameters)

        self.post_to_active_campaign(params)

    def add_list(self, listid, title, **kw):
        params = dict(api_action='list_add',
                      name=title,
                      stringid=listid)
        params.update(kw)
        result = self.post_to_active_campaign(params)
        return result['id']

    def delete_lists(self, listids):
        params = dict(api_action='list_delete_list',
                      ids=','.join(listids))
        result = self.post_to_active_campaign(params)
        return result['result_code']

    def post_to_active_campaign(self, query):
        """
        Performs the actual post to active campaign and check the
        response.
        """
        logger = logging.getLogger(self.id)
        url = self.get_api_url()
        assert url

        query.update(dict(
            api_user=self.get_api_username(),
            api_pass=self.get_api_password(),
            api_output='json',
        ))

        msg = ("Calling {url}/{api_action} with {query}".format(
            url=url, query=query, **query))
        logger.info(msg)
        result = urllib2.urlopen(url, urllib.urlencode(query)).read()
        logger.info(result)

        result = json.loads(result)
        if result['result_code'] == 0:
            logger.error(result['result_message'])
        return result

    def format_url_keys(self, name, items):
        """
        Formats each list item given by items to a active campaign
        POST compatible format.

        e.g. name = "p", items = [1, 2] it will return ['p[1]', 'p[2]']
        """
        return ['{name}[{x}]'.format(name=name, x=x) for x in items]

    def get_formatted_fields(self, name, keys, values=None):
        """
        Returns a dictionary of formatted fields.

        This is a helper method to format keys and values into a
        specific format the API expects.


        :param name: A prefix for each key.
        :param keys: An iterable of keys.
        :param values: An iterable of values. If None, the keys are used
                       as values.
        :rtype: A dictionary of zipped keys and values.
        """
        values = values is not None and values or keys
        return dict(zip(self.format_url_keys(name, keys), values))

    def get_list_ids(self):
        return []

    def get_api_url(self):
        return self.getProperty('api_url')

    def get_api_username(self):
        return self.getProperty('api_user')

    def get_api_password(self):
        return self.getProperty('api_password')


Globals.InitializeClass(ActiveCampaignTool)


@zope.component.adapter(IActiveCampaignTool,
                        zope.container.interfaces.IObjectAddedEvent)
def after_tool_added(tool, event):
    """
    Prepopulate the tool with properties we need.
    """
    tool.manage_addProperty('api_url', '', 'string')
    tool.manage_addProperty('api_user', '', 'string')
    tool.manage_addProperty('api_password', '', 'string')


class ActiveCampaignSubscriber(object):

    zope.interface.implements(IActiveCampaignSubscriber)

    email = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['email'])
    first_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['first_name'])
    last_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['last_name'])

    def __init__(self, email, first_name=u'', last_name=u''):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
import Globals
import OFS.Folder
import OFS.SimpleItem
import Products.CMFCore.utils
import logging
import urllib
import urllib2
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
        url = self.get_api_url()

        assert IActiveCampaignSubscriber.providedBy(subscriber)
        assert url

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
            dict(
                (self.format_url_keys('p', subscriber.listids),
                 subscriber.listids),
                (self.format_url_keys('status', subscriber.listids),
                 subscriber.listids)
            )
        )
        if custom_parameters is not None:
            params.update(custom_parameters)

        result = urllib2.urlopen(url, urllib.urlencode(params)).read()
        logger = logging.getLogger(self.id)
        logger.log(
            logging.INFO, "Subscribing: %s?%s\n%s" % (url, params, result))

    def format_url_keys(self, name, items):
        """ Formats each list item given by items to a active campaign
        POST compatible format.

        e.g. name = "p", items = [1, 2] it will return ['p[1]', 'p[2]']
        """
        return ['{name}[{x}]'.format(name=name, x=x) for x in items]

    def get_list_ids(self):
        return []

    def get_api_url(self):
        return self.getProperty('api_url')

    def get_api_username(self):
        return self.getProperty('api_user')

    def get_api_password(self):
        return self.getProperty('api_password')


Globals.InitializeClass(ActiveCampaignTool)


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

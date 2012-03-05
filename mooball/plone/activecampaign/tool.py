from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import ACTIVE
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

    def add_subscriber(self, subscriber):
        assert IActiveCampaignSubscriber.providedBy(subscriber)
        url = self.get_api_url()
        params = dict(
            api_user=self.api_username,
            api_pass=self.api_pass,
            api_action='subscriber_add',
            api_output='json',
            email=subscriber.email,
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
        )
        # XXX WTF
        params.update({'p[123]': subscriber.listids,
                       'status[123]': ACTIVE
                      })
        if not params:
            return

        result = urllib2.urlopen(url, urllib.urlencode(params)).read()
        logger = logging.getLogger(self.id)
        logger.log(
            logging.INFO, "Subscribing: %s?%s\n%s" % (url, params, result))

    def get_list_ids(self):
        return []

    def get_api_key(self):
        return self.getProperty('apikey')

    def get_api_url(self):
        return self.getProperty('apiurl')


Globals.InitializeClass(ActiveCampaignTool)


class ActiveCampaignSubscriber(object):

    zope.interface.implements(IActiveCampaignSubscriber)

    email = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['email'])
    first_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['first_name'])
    last_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['last_name'])
    listids = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['listids'])

    def __init__(self, email, first_name='', last_name='',
                 listids=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        if listids is not None:
            self.listids = listids

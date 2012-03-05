from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
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
        url = self.get_api_url()
        params = self.get_synchronise_params(user)
        if not params:
            return

        logger = logging.getLogger(self.id)
        result = urllib2.urlopen(url, params).read()
        logger.log(
            logging.INFO, "Subscribing: %s?%s\n%s" % (url, params, result))

    def get_synchronise_params(self, user):
        encoded = ''
        if not user.email or not user.country:
            msg = ("Can't subscribe users with empty"
                   " e-mail/country: %s" % user.username)
            logger = logging.getLogger(self.id)
            logger.log(logging.ERROR, msg)
        else:
            encoded = urllib.urlencode(
                dict(ApiKey=self.get_api_key(),
                     ListID=self.get_listid_for_user(user),
                     Email=user.email,
                     Name=user.firstName)
            )
        return encoded

    def get_list_ids(self):
        return []

    def get_api_key(self):
        return self.getProperty('apikey')

    def get_api_url(self):
        return self.getProperty(
            'apiurl', 'http://api.createsend.com/api/api.asmx/Subscriber.Add')


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

    def get_subscribed_list_ids(self):
        return []

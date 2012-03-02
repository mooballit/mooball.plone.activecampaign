import Globals
import OFS.Folder
import OFS.SimpleItem
import Products.CMFCore.utils
import logging
import mooball.plone.activecampaign.interfaces
import urllib
import urllib2
import zope.interface


class ActiveCampaignTool(Products.CMFCore.utils.UniqueObject,
                         OFS.Folder.Folder):

    zope.interface.implements(
        mooball.plone.activecampaign.interfaces.IActiveCampaignTool)

    id = 'portal_activecampaign'
    meta_type = 'ActiveCampaignTool'
    plone_tool = 1

    manage_options = OFS.Folder.Folder.manage_options
    manage_options = [opt for opt in manage_options if opt['label'] not in
                      ['Contents', 'View']]

    def synchronise_user_data(self, user):
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

    def get_listid_for_user(self, user):
        # to avoid circular imports
        listid = ''
        testlistid = self.getProperty('testlistid')
        au_media = self.getProperty('aumedia', '1D6D359BE3260F38')
        au_nomedia = self.getProperty('aunomedia', '35670385E4D2C5D9')
        nz_media = self.getProperty('nzmedia', '0EF4DDFE2544494E')
        nz_nomedia = self.getProperty('nznomedia', '5A1B9A6C01B1CB7E')
        if not mooball.plone.activecampaign.interfaces.\
           IActiveCampaignUser.providedBy(user):
            return listid

        if testlistid:
            listid = testlistid
        elif user.country == 'AU':
            listid = user.user_type == 'Media' and au_media or au_nomedia
        elif user.country == 'NZ':
            listid = user.user_type == 'Media' and nz_media or nz_nomedia
        return listid

    def get_api_key(self):
        return self.getProperty('apikey', 'a1d27585d57cfa7d3c88225e9bb98af5')

    def get_api_url(self):
        return self.getProperty(
            'apiurl', 'http://api.createsend.com/api/api.asmx/Subscriber.Add')


Globals.InitializeClass(ActiveCampaignTool)

from AccessControl.class_init import InitializeClass
from mooball.plone.activecampaign.interfaces import ACTIVE, UNSUBSCRIBED
from mooball.plone.activecampaign.interfaces import APIUnauthorized
from mooball.plone.activecampaign.interfaces import IActiveCampaignField
from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.interfaces import IActiveCampaignSubscriber
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
import OFS.Folder
import OFS.SimpleItem
import Products.CMFCore.utils
import datetime
import json
import logging
import mooball.plone.activecampaign.cache
import plone.memoize.volatile
import urllib
import urllib2
import zope.container.interfaces
import zope.interface
import zope.schema


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

        result = self.post_to_active_campaign(params)
        return result['result_code']

    def sync_subscriber( self, subscriber, subids = [], unsubids = [] ):
        assert IActiveCampaignSubscriber.providedBy(subscriber)
        
        params = dict(
            api_user=self.get_api_username(),
            api_pass=self.get_api_password(),
            api_action='subscriber_sync',
            api_output='json',
            email=subscriber.email,
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
        )

        params.update(
            self.get_formatted_fields('p', subids + unsubids, subids + unsubids)
        )
        params.update(
            self.get_formatted_fields('status', subids,
                                      [ACTIVE] * len(subids))
        )
        params.update(
            self.get_formatted_fields('status', unsubids,
                                      [UNSUBSCRIBED] * len(unsubids))
        )

        result = self.post_to_active_campaign(params)
        return result['result_code']


    def add_list(self, name, title, **kw):
        params = dict(api_action='list_add',
                      name=title,
                      stringid=name)
        
        if self.hosted_account:
            # Add required fields for hosted accounts
            params.update( {
                'sender_name': self.hosted_sender_name,
                'sender_addr1': self.hosted_sender_addr1,
                'sender_zip': self.hosted_sender_zip,
                'sender_city': self.hosted_sender_city,
                'sender_country': self.hosted_sender_country,
            } )
        
        params.update(kw)
        result = self.post_to_active_campaign(params)
        return result['id']

    def add_custom_field(self, field, listids):
        params = field.get_parameters()
        params.update(api_action='list_field_add')
        params.update(
            self.get_formatted_fields('p', listids, listids)
        )
        self.post_to_active_campaign(params)

    def delete_lists(self, listids):
        params = dict(api_action='list_delete_list',
                      ids=','.join(listids))
        result = self.post_to_active_campaign(params)
        return result['result_code']

    def delete_subscribers(self, emails):
        ids_to_delete = []

        for email in emails:
            sub = self.get_subscriber_by(email)
            if sub is not None:
                ids_to_delete.append(sub.sid)

        if ids_to_delete:
            params = dict(api_action='subscriber_delete_list',
                          ids=','.join(ids_to_delete))
            self.post_to_active_campaign(params)

    def post_to_active_campaign(self, query):
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
        logger.debug(msg)
        result = urllib2.urlopen(url, urllib.urlencode(query)).read()
        logger.debug(result)

        try:
            result = json.loads(result)
            result_code = result.get('result_code')
        except (AttributeError, ValueError), err:
            raise ValueError('An error occured contacting the api. Only'
                             ' garbage was received. This should not'
                             ' happen: {error} - {0}'.format(
                                 result, error=err))
        if (result_code == 0 and 'not authorized' in
            result['result_message']):
            result.update(api_url=self.get_api_url(),
                          api_username=self.get_api_username(),
                          api_password=self.get_api_password())
            msg = ('{result_message}. Perhaps you were providing the'
                   ' wrong credentials and API URL? URL: {api_url},'
                   ' api_username: {api_username}'.format(**result))
            raise APIUnauthorized(msg)
        if result_code == 0:
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
        return [x.listid for x in self.get_list_information()]

    def get_list_information(self, listids=None, forcereload=False):
        idstolist = listids is not None and ','.join(listids) or 'all'
        result = []
        json = self._get_list_information_helper(forcereload)
        for k in json.keys():
            json[k]['listid'] = json[k]['id']
            if idstolist == 'all' or json[k]['listid'] in idstolist:
                result.append(ActiveCampaignList(**json[k]))
        return result

    @plone.memoize.volatile.cache(
        mooball.plone.activecampaign.cache._get_list_information_cachekey,
        get_cache=mooball.plone.activecampaign.cache.store_on_self)
    def _get_list_information_helper(self, forcereload=False):
        json = self.post_to_active_campaign(
            dict(api_action='list_list',
                 ids='all',
                 global_fields='1')
        )
        del json['result_code']
        del json['result_output']
        del json['result_message']
        return json

    def get_api_url(self):
        return self.getProperty('api_url')

    def get_api_username(self):
        return self.getProperty('api_user')

    def get_api_password(self):
        return self.getProperty('api_password')

    def get_subscriber_by(self, email):
        params = dict(api_action='subscriber_view_email',
                      email=email)
        result = self.post_to_active_campaign(params)
        if result['result_code'] == 1:
            if result['lists']:
                lists = self.get_list_information(
                    listids=result['lists'].keys())
            return ActiveCampaignSubscriber(
                result['email'], result['first_name'],
                result['last_name'], sid=result['id'],
                lists=lists
            )

    def get_lists_by(self, subscriber):
        subscriber = self.get_subscriber_by(subscriber.email)
        if subscriber is not None:
            return subscriber.lists


InitializeClass(ActiveCampaignTool)


@zope.component.adapter(IActiveCampaignTool,
                        zope.container.interfaces.IObjectAddedEvent)
def after_tool_added(tool, event):
    """
    Prepopulate the tool with properties we need. The properties are set
    to an empty string. Properties which are created by default are:

        * api_url
        * api_user
        * api_password
    """
    tool.manage_addProperty('api_url', '', 'string')
    tool.manage_addProperty('api_user', '', 'string')
    tool.manage_addProperty('api_password', '', 'string')
    tool.manage_addProperty('hosted_account', False, 'boolean')
    tool.manage_addProperty('hosted_sender_name', '', 'string')
    tool.manage_addProperty('hosted_sender_addr1', '', 'string')
    tool.manage_addProperty('hosted_sender_zip', '', 'string')
    tool.manage_addProperty('hosted_sender_city', '', 'string')
    tool.manage_addProperty('hosted_sender_country', '', 'string')


class ActiveCampaignSubscriber(object):

    zope.interface.implements(IActiveCampaignSubscriber)

    sid = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['sid'])
    email = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['email'])
    first_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['first_name'])
    last_name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['last_name'])
    lists = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignSubscriber['lists'])

    def __init__(self, email, first_name=u'', last_name=u'', sid='0',
                 lists=None):
        self.sid = str(sid)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.lists = lists


class ActiveCampaignField(object):

    zope.interface.implements(IActiveCampaignField)

    title = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['title'])
    type = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['type'])
    req = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['req'])
    onfocus = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['onfocus'])
    bubble_content = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['bubble_content'])
    label = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['label'])
    show_in_list = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['show_in_list'])
    perstag = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignField['perstag'])

    def __init__(self, **kw):
        for key, val in kw.items():
            setattr(self, key, val)

    def get_parameters(self):
        result = dict()
        for fid, field in zope.schema.getFieldsInOrder(
            IActiveCampaignField):
            result[fid] = field.get(self)
        return result

    @property
    def fieldtype(self):
        result = None
        vocab = zope.component.getUtility(
            zope.schema.interfaces.IVocabularyFactory,
            name=u'Field Types')(self)
        try:
            term = vocab.getTermByToken(self.type)
            result = term.title
        except LookupError:
            pass
        return result


class ActiveCampaignList(OFS.SimpleItem.SimpleItem):

    zope.interface.implements(IActiveCampaignList)

    listid = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['listid'])
    name = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['name'])
    cdate = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['cdate'])
    subscribers = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['subscribers'])
    campaigns = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['campaigns'])
    emails = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['emails'])
    fields = zope.schema.fieldproperty.FieldProperty(
        IActiveCampaignList['fields'])

    _dateformat = '%Y-%m-%d %H:%M:%S'

    def __init__(self, **kw):
        for fid, field in zope.schema.getFieldsInOrder(
            IActiveCampaignList):
            val = kw.get(fid)
            if val is None:
                continue
            if fid == 'cdate':
                val = datetime.datetime.strptime(val, self._dateformat)
            if fid == 'fields':
                val = self.convert_fields(val)
            setattr(self, fid, val)

    def convert_fields(self, fielddata):
        result = []
        for data in fielddata:
            field = ActiveCampaignField(**data)
            result.append(field)
        return result


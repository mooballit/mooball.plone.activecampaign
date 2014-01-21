from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from mooball.plone.activecampaign.interfaces import APIUnauthorized
from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.app.controlpanel.form import ControlPanelForm
from plone.i18n.normalizer.interfaces import IURLNormalizer
import plone.directives.form
import plone.protect
import z3c.form.field
import zope.component
import zope.event
import zope.formlib.form
import zope.publisher.interfaces


class AddMailingList(plone.directives.form.SchemaAddForm):
    grok.context(IActiveCampaignTool)
    grok.require('cmf.ManagePortal')
    schema = IActiveCampaignList
    ignoreContext = True

    def create(self, data):
        return data

    def add(self, data):
        name = zope.component.getUtility(IURLNormalizer).normalize(
            data['name'])
        mlistid = self.context.add_list(name=name, title=data['name'])
        self.context.get_list_information(forcereload=True)
        IStatusMessage(self.request).addStatusMessage(
            '{mlistid} added'.format(mlistid=mlistid), type='info')
        url = zope.component.getMultiAdapter(
            (self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url + '/managemailinglists')


class ManageTool(ControlPanelForm):
    form_name = "Active Campaign Settings"
    description = "Tool Settings for Active Campaign API Tool"
    form_fields = zope.formlib.form.FormFields(IActiveCampaignTool)

    @zope.formlib.form.action(u'Save', name=u'save')
    def handle_edit_action(self, action, data):
        plone.protect.CheckAuthenticator(self.request)
        self.context.manage_changeProperties(**data)
        try:
            self.context.get_list_information()
        except APIUnauthorized, err:
            IStatusMessage(self.request).addStatusMessage(err,
                                                          type='error')
            return
        zope.event.notify(ConfigurationChangedEvent(self, data))
        self.status = "Changes saved."


class ISearchSubscribers(zope.interface.Interface):

    searchTerm = zope.schema.TextLine(
        title=u'Email',
        description=u'Find mailing lists which contain given email',
        required=False,
    )


class SearchSubscribers(plone.directives.form.Form):
    grok.require('cmf.ManagePortal')
    grok.context(IActiveCampaignTool)
    ignoreContext = True
    fields = z3c.form.field.Fields(ISearchSubscribers)
    mlists = None

    @z3c.form.button.buttonAndHandler(u'Search', name='search')
    def search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if data.get('searchTerm') is None:
            self.status = u'The given e-mail is empty'
            return

        mlists = self.context.get_lists_by(
            ActiveCampaignSubscriber(email=data['searchTerm']))
        if not mlists:
            self.status = u'No mailing lists found'
        else:
            self.mlists = mlists


class ManageMailingLists(grok.View):
    grok.context(IActiveCampaignTool)
    grok.require('cmf.ManagePortal')
    grok.name('index_html')
    mlists = None

    def __call__(self):
        if 'delete' in self.request.form.keys():
            self.delete_lists()
        return super(ManageMailingLists, self).__call__()

    def update(self):
        self.searchform = SearchSubscribers(self.context, self.request)
        self.searchform.update()
        if self.provides_api_information():
            self.mlists = (self.searchform.mlists and
                           self.searchform.mlists or
                           self.context.get_list_information())

    def provides_api_information(self):
        """
        Returns True if api_url and api_key are set
        and therefore an API call can be made.
        """
        return (self.context.get_api_url() and
                self.context.get_api_key())

    def delete_lists(self):
        if self.context.delete_lists(self.request.form['delete']):
            self.context.get_list_information(forcereload=True)

            msg = u'Successfully deleted list(s).'
            IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.url())


class ManageList(grok.View):
    grok.context(IActiveCampaignList)
    grok.require('cmf.ManagePortal')


class ListTraverser(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        view = zope.component.queryMultiAdapter(
            (self.context, self.request), name=name)
        if view is not None:
            return view
        elif hasattr(self.context, name):
            return getattr(self.context, name)
        else:
            info = self.context.get_list_information()
            mlist = [x for x in info if x.listid == name]
            if not mlist:
                raise zope.publisher.interfaces.NotFound(
                    self.context, name, self.request)
            return mlist[0].__of__(self.context)

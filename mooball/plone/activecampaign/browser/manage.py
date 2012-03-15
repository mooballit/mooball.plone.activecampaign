from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from mooball.plone.activecampaign.interfaces import APIUnauthorized
from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.app.controlpanel.form import ControlPanelForm
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser.textwidgets import PasswordWidget
import plone.protect
import zope.component
import zope.event
import zope.formlib.form
import zope.publisher.interfaces


class ManageTool(ControlPanelForm):
    form_name = "Active Campaign Settings"
    description = "Tool Settings for Active Campaign API Tool"
    form_fields = zope.formlib.form.FormFields(IActiveCampaignTool)
    pass_widget = CustomWidgetFactory(PasswordWidget,
                                      extra='autocomplete="off"')
    form_fields['api_password'].custom_widget = pass_widget

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


class ManageMailingLists(grok.View):
    grok.context(IActiveCampaignTool)
    grok.require('cmf.ManagePortal')

    def __call__(self):
        if 'delete' in self.request.form.keys():
            self.delete_lists()
        return super(ManageMailingLists, self).__call__()

    def provides_api_information(self):
        """
        Returns True if api_url, api_username and api_password are set
        and therefore an API call can be made.
        """
        return (self.context.get_api_url() and
                self.context.get_api_username() and
                self.context.get_api_password())

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
        else:
            info = self.context.get_list_information()
            mlist = [x for x in info if x.listid == name]
            if not mlist:
                raise zope.publisher.interfaces.NotFound(
                    self.context, name, self.request)
            return mlist[0].__of__(self.context)

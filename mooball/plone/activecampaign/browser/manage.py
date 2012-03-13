from five import grok
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
from Products.statusmessages.interfaces import IStatusMessage


class ManageMailingLists(grok.View):
    grok.context(IActiveCampaignTool)
    grok.require('cmf.ManagePortal')

    def __call__(self):
        if 'delete' in self.request.form.keys():
            self.delete_lists()
        return super(ManageMailingLists, self).__call__()

    def delete_lists(self):
        if self.context.delete_lists(self.request.form['delete']):
            self.context.get_list_information(forcereload=True)

            msg = u'Successfully deleted list(s).'
            IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.url())

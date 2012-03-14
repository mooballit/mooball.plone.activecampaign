from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from mooball.plone.activecampaign.interfaces import IActiveCampaignList
from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
import zope.component
import zope.publisher.interfaces


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

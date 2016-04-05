from cs.subsites.subsite import ISubSite
from five import grok
from plone.app.layout.viewlets.common import ViewletBase

from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Acquisition import aq_inner
grok.templatedir('templates')


class MainSiteViewlet(ViewletBase):

    def is_subsite(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
        if ISubSite.providedBy(context):
            return True
        return False

    def mainsite_url(self):
        context = aq_inner(self.context)
        portal_state = context.restrictedTraverse("plone_portal_state")
        portal = portal_state.portal()
        return portal.absolute_url()

    def mainsite_title(self):
        context = aq_inner(self.context)
        portal_state = context.restrictedTraverse("plone_portal_state")
        return portal_state.portal_title()
from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
grok.templatedir('templates')


class MainSiteViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('cs.subsite.mainsite')
    grok.order(1)
    grok.viewletmanager(IPortalHeader)

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

    def get_logo(self):
        context = aq_inner(self.context)
        portal_state = context.restrictedTraverse("plone_portal_state")
        portal = portal_state.portal()
        bprops = portal.restrictedTraverse('base_properties', None)
        if bprops is not None:
            logoName = bprops.logoName
        else:
            logoName = 'logo.jpg'

        logoTitle = portal_state.portal_title()
        return portal.restrictedTraverse(logoName).tag(title=logoTitle, alt=logoTitle)

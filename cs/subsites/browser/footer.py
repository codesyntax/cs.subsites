from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalFooter
grok.templatedir('templates')


class Footer(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('cs.subsite.footer')
    grok.viewletmanager(IPortalFooter)

    def is_subsite(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
        if ISubSite.providedBy(context):
            return True
        return False

    def get_footer_text(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
        return context.footer

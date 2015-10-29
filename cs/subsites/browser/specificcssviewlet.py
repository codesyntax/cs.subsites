from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from Acquisition import aq_inner
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
grok.templatedir('templates')


class SpecificCss(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('cs.subsites.specificcss')
    grok.viewletmanager(IHtmlHeadLinks)

    def subsite_element(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
        if ISubSite.providedBy(context):
            return context
        return None

    def is_subsite(self):
        subsite = self.subsite_element()
        if subsite:
            return True
        else:
            return False

    def subsite_url(self):
        subsite = self.subsite_element()
        if subsite:
            return subsite.absolute_url()
        else:
            return ''

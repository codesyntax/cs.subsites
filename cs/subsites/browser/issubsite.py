from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from Acquisition import aq_inner


class IsSubsite(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('issubsite')

    def render(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            return True
        else:
            return False

from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from Acquisition import aq_inner


class SpecificCss(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('specificcss.css')

    def render(self):
        context = aq_inner(self.context)
        self.response.setHeader('Content-Type', 'text/css;charset=utf-8')
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            css = context.specific_css
            return css
        else:
            return ''

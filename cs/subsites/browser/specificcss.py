from Products.Five.browser import BrowserView
from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Acquisition import aq_inner


class SpecificCss(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        self.request.response.setHeader('Content-Type', 'text/css;charset=utf-8')
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            css = context.specific_css
            return css
        else:
            return ''

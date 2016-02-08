from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Acquisition import aq_inner


class IsSubsite(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            return True
        else:
            return False

from plone.memoize import ram
from time import time
from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Acquisition import aq_inner


def cache_key(fun, self):
    context = aq_inner(self.context)
    return [context.absolute_url(), time() // (60 * 60 * 24)]


class IsSubsite(BrowserView):

    @ram.cache(cache_key)
    def __call__(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            return True
        else:
            return False

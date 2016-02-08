from plone.app.layout.viewlets.common import ViewletBase
from cs.subsites.subsite import ISubSite
from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_parent
from Acquisition import aq_inner


class SpecificCss(ViewletBase):

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

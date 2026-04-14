from plone.app.layout.viewlets.common import LogoViewlet as LogoViewletPlone
from plone.app.layout.navigation.interfaces import INavigationRoot
from cs.subsites.subsite import ISubSite
from Acquisition import aq_parent, aq_inner


class LogoViewlet(LogoViewletPlone):

    def update(self):
        super().update()
        context = self.context
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        # Override the logo if we are in a subsite
        if ISubSite.providedBy(context):
            if context.restrictedTraverse("@@images").scale("image"):
                self.img_src = context.restrictedTraverse("@@images").scale("image").url
                self.navigation_root_title = context.Title()
            else:
                # if there is no logo set in the subsite, override just the title
                self.navigation_root_title = context.Title()

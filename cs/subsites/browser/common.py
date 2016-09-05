from plone.app.layout.viewlets.common import LogoViewlet as LogoViewletPlone
from plone.app.layout.navigation.interfaces import INavigationRoot
from cs.subsites.subsite import ISubSite
from Acquisition import aq_parent, aq_inner


class LogoViewlet(LogoViewletPlone):

    def update(self):
        super(LogoViewlet, self).update()

        portal = self.portal_state.portal()
        bprops = portal.restrictedTraverse('base_properties', None)
        if bprops is not None:
            logoName = bprops.logoName
        else:
            logoName = 'logo.jpg'
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            logoTitle = context.Title()
            if context.restrictedTraverse('@@images').scale('image', 'large'):
                self.logo_tag = context.restrictedTraverse('@@images').scale('image').tag()
                self.navigation_root_title = context.Title()
            else:
                logoTitle = self.portal_state.portal_title()
                self.logo_tag = portal.restrictedTraverse(logoName).tag(title=logoTitle, alt=logoTitle)
                self.navigation_root_title = context.Title()

        else:
            logoTitle = self.portal_state.portal_title()
            self.logo_tag = portal.restrictedTraverse(logoName).tag(title=logoTitle, alt=logoTitle)
            self.navigation_root_title = self.portal_state.navigation_root_title()
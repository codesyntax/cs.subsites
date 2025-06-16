from plone.app.layout.globals.layout import IBodyClassAdapter
from plone.dexterity.interfaces import IDexterityContent
from plone.app.layout.navigation.interfaces import INavigationRoot
from cs.subsites.subsite import ISubSite
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from Acquisition import aq_inner

@adapter(IDexterityContent, Interface)
@implementer(IBodyClassAdapter)
class ContentBodyClasses(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)

        if ISubSite.providedBy(context):
            return ["issubsite"]
        else:
            return ""

from ..interfaces import ICSSubsitesLayer
from cs.subsites.utils import get_current_context
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from cs.subsites.subsite import ISubSite
import transaction


def handler(proxy, settings):
    """Taken from plone.app.multilingual.subscriber
    and modified to setup the multilingual configuration
    in the LRFs inside the current childsite.
    """
    if settings.record.__name__ != "plone.available_languages":
        return

    request = getRequest()
    context = get_current_context()

    # We can't restrict subscribers to be run when some browser layer
    # is provided, so we check it here
    #
    if (
        IPloneAppMultilingualInstalled.providedBy(request)
        and ICSSubsitesLayer.providedBy(request)
        and context is not None
        and ISubSite.providedBy(context)
        and context.allow_custom_set_of_languages
    ):
        # The import is added here to avoid circular import errors
        from plone.app.multilingual.browser.setup import SetupMultilingualSite

        setup_tool = SetupMultilingualSite()
        setup_tool.setupSite(context)

        layout = context.getLayout()
        if layout is None or layout == "view":
            context.setLayout("language-switcher")

    elif IPloneAppMultilingualInstalled.providedBy(request):
        # In case our product is not installed or custom set of languages are note enabled
        # behave like the p.a.multilingual
        # subscriber.
        # This is done like this because we are unconfiguring the original subscriber
        # because it clashes its behavior with ours.

        # The import is added here to avoid circular import errors
        from plone.app.multilingual.browser.setup import SetupMultilingualSite

        setupTool = SetupMultilingualSite()
        portal = getSite()
        setupTool.setupSite(portal)

    return

from Products.CMFCore.interfaces import IContentish
from zope.globalrequest import getRequest


def get_current_context():
    # 1. Fetch the global request
    request = getRequest()
    if not request:
        return None

    # 2. Inspect what Zope is currently publishing
    published = request.get("PUBLISHED", None)

    # If a BrowserView is being published, look for __parent__ or context
    context = getattr(published, "__parent__", None)
    if context is None:
        context = getattr(published, "context", None)

    # 3. Fall back to the Zope traversal lineage (PARENTS)
    if context is None:
        parents = request.get("PARENTS", [])
        if parents:
            # The immediate parent of the published view/method is the context object
            context = parents[0]

    # 4. Content verification (Optional but Recommended)
    # This ensures you got actual Plone content,
    # rather than a skin template or system resource
    if context and IContentish.providedBy(context):
        return context

    return None

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from Acquisition import aq_inner
from cs.subsites import MessageFactory as _
from zope.interface import alsoProvides
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.view import memoize
from zope.interface import implementer
from plone import api
from collective.lineage.interfaces import IChildSite


# Interface class; used to define content-type schema.
class ISubSite(model.Schema, IImageScaleTraversable, INavigationRoot, IChildSite):
    """
    SubSite creator element
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/subsite.xml to define the content type
    # and add directives here as necessary.
    image = NamedBlobImage(
        title=_("Lead Image"),
        description="",
        required=False,
    )

    text = RichText(
        title=_("Subsite homepage text"),
        description=_("This text will be shown in the subsite homepage"),
        required=False,
    )

    footer = RichText(
        title=_("Footer text"),
        description=_("This text will be shown in the Footer"),
        required=False,
    )

    specific_css = schema.Text(
        title=_("Specific css for this SubSiteq"),
        description=_("This css is just for this subsite"),
        required=False,
    )

    allow_custom_set_of_languages = schema.Bool(
        title=_(
            "Allow configuring a custom set of languages?",
        ),
        description=_(
            "This is useful to create URLs like http://portal/subsite/en, instead of the traditional http://portal/en/subsite"
        ),
        required=False,
        default=False,
        readonly=False,
    )


alsoProvides(ISubSite["image"], ILanguageIndependentField)
alsoProvides(ISubSite["specific_css"], ILanguageIndependentField)
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.


@implementer(ISubSite)
class SubSite(Container):
    """ """

    # Add your class methods and properties here

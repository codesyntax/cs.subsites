from five import grok
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from cs.subsites import MessageFactory as _
from zope.interface import alsoProvides
from plone.multilingualbehavior.interfaces import ILanguageIndependentField
from plone.app.layout.navigation.interfaces import INavigationRoot

# Interface class; used to define content-type schema.
class ISubSite(form.Schema, IImageScaleTraversable, INavigationRoot):
    """
    SubSite creator element
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/subsite.xml to define the content type
    # and add directives here as necessary.
    image = NamedBlobImage(
            title=_(u"Lead Image"),
            description=u"",
            required=False,
        )

    text = RichText(title=_(u'Subsite homepage text'),
        description=_(u'This text will be shown in the subsite homepage'),
        required=False,
        )

    footer = RichText(title=_(u'Footer text'),
        description=_(u'This text will be shown in the Footer'),
        required=False,
        )

    specific_css = schema.Text(
        title=_(u'Specific css for this SubSiteq'),
        description=_(u'This css is just for this subsite'),
        required=False,
        )


alsoProvides(ISubSite['image'], ILanguageIndependentField)
alsoProvides(ISubSite['specific_css'], ILanguageIndependentField)
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.


class SubSite(dexterity.Container):
    grok.implements(ISubSite)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called subsiteview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type
grok.templatedir('templates')


class SubSiteView(grok.View):
    grok.context(ISubSite)
    grok.require('zope2.View')
    grok.name('view')

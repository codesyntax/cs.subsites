from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from Acquisition import aq_inner
from cs.subsites import MessageFactory as _
from zope.interface import alsoProvides
from collective import dexteritytextindexer
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.view import memoize
from zope.interface import implements


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

    dexteritytextindexer.searchable('text')
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
    implements(ISubSite)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called subsiteview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# This will make this view the default view for your content-type
class SubSiteView(BrowserView):

    @memoize
    def carousel_items(self):
        context = aq_inner(self.context)
        home_sections_folder = context.get('portadako-destakatuak', None)
        if home_sections_folder:
            carousel_folder = home_sections_folder.get('carousel', None)
            if carousel_folder:
                items = carousel_folder.getFolderContents({'portal_type':'Featured','review_state' : 'published'})
                return IContentListing(items)
        return []

    @memoize
    def carousel_items_len(self):
        items = self.carousel_items()
        return len(items) > 1

    @memoize
    def news(self):
        context = aq_inner(self.context)
        pcat = getToolByName(context, 'portal_catalog')
        articles_dict = dict(portal_type='News Item',
                        review_state='published',
                        sort_on='effective',
                        sort_order='reverse',
                        sort_limit=3)
        articles_folder = self.articles_folder_element()
        if articles_folder:
            path = '/'.join(articles_folder.getPhysicalPath())
            articles_dict['path'] = path
        else:
            return None
        articles = pcat(articles_dict)
        if articles:
            return articles
        else:
            return None

    @memoize
    def articles_folder_element(self):
        context = aq_inner(self.context)
        lang = self.request.LANGUAGE
        try:
            context_eu = ITranslationManager(context).get_translation('eu')
            if not context_eu:
                eu_articles_folder = context.get('albisteak', None)
            else:
                eu_articles_folder = context_eu.get('albisteak', None)
            if eu_articles_folder:
                articles_folder = ITranslationManager(eu_articles_folder).get_translation(lang)
                if articles_folder:
                    return articles_folder
            return None
        except:
            return None

    @memoize
    def articles_folder_element_path(self):
        context = aq_inner(self.context)
        articles_folder = self.articles_folder_element()
        if articles_folder:
            return articles_folder.absolute_url()
        else:
            return context.absolute_url()

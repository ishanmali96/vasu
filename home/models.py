

from django.db import models
from django.db.models.fields import TextField
from django.utils.translation import templatize


from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailcodeblock.blocks import CodeBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel,RichTextFieldPanel,PageChooserPanel
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from django_extensions.db.fields import AutoSlugField



class HomePage(Page):
    """home page"""
    body = models.TextField()
    
    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]
   


class BlogIndex(Page):
    """for blog index page"""
    template = 'home/blog_index.html'
    topic = models.CharField(max_length=50)
    body = RichTextField()
    image = models.ForeignKey('wagtailimages.Image',  on_delete=models.CASCADE, related_name='+'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('topic'),
        RichTextFieldPanel('body'),
        ImageChooserPanel('image', heading= "image")
    ]


class BlogPage(Page):
    """For blog page"""
    topic =models.CharField(max_length=100,null=False, blank=False)

    date = models.DateTimeField(auto_now=True)

    intro = TextField()

    intro_image =  models.ForeignKey('wagtailimages.Image',  on_delete=models.CASCADE, related_name='+'
    )

    content = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
        ('code', CodeBlock())

    ])

    search_fields = Page.search_fields + [
        index.SearchField('topic'),
        index.SearchField('content'),
    ]


    content_panels = Page.content_panels + [
        FieldPanel('topic'),
        FieldPanel('intro'),
        ImageChooserPanel('intro_image'),
        RichTextFieldPanel('content'),
    ]



class FormField(AbstractFormField):
    """for contact form field"""
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    """for contact form field"""
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


@register_setting
class SocialMediaSettings(BaseSetting):
    """Social media settings for our custom website."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")
    mailid = models.EmailField(blank=True, null=True, help_text="Your mail Id")
    linkedin = models.URLField(blank=True, null=True, help_text="Your linkedin URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),
            FieldPanel('mailid'),
            FieldPanel('linkedin')


        ], heading="Social Media Settings")
    ]

#-------------For menu setting----------------
class MenuItem(Orderable):

    link_title = models.CharField(blank=True,null=True,max_length=50)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True,blank=True,related_name="+",on_delete=models.CASCADE,)
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'


@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    # slug = models.SlugField()

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title



class AboutPage(Page):
    template = 'home/about_page.html'

    content = RichTextField()

    content_panels = Page.content_panels + [ 
        RichTextFieldPanel('content',heading= "Massage for About us")
    ]


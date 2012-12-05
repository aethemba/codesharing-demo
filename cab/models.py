from django.db import models
from django.core.urlresolvers import reverse
from pygments import lexers, formatters, highlight
from tagging.fields import TagField
from django.contrib.auth.models import User
from markdown import markdown
import datetime

from cab import managers

class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    language_code = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)

    objects = managers.LanguageManager()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cab_language_detail', kwargs={'slug': self.slug})

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language)
    author = models.ForeignKey(User)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    tags = TagField()
    pub_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)

    objects = managers.SnippetManager()

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def highlight(self):
        ''' Args: code to highlight, lexer to use, formatter '''
        return highlight(self.code, self.language.get_lexer(),
                                    formatters.HtmlFormatter(lineos=True))

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.update_date = datetime.datetime.now()

        self.description_html = markdown(self.description)
        self.highlighted_code = self.highlight()
        super(Snippet, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return reverse('cab_snippet_detail', kwargs={'object_id':self.id})


from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list
from django.db.models import Count
from cab.models import Snippet, Language

def top_authors(request):
    return object_list(request, queryset=Snippet.objects.top_authors(),
                                template_name="cab/top_authors.html",
                                paginate_by=20)

def top_languages(request):
    return object_list(request, queryset=Language.objects.top_languages(),
                                template_name="cab/top_languages.html",
                                paginate_by=20)



import django

django.setup()

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

flat_page = FlatPage()
flat_page.url = '/home/'
flat_page.title = 'Home'
flat_page.save()
flat_page.sites.add(Site.objects.get_current())
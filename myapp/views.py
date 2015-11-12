from django.shortcuts import render

from myapp.models import Match,Links
# Create your views here.
from django.contrib.auth.decorators import login_required


def match_view(request):
    active_match=Match.objects.filter(is_active=True).prefetch_related('links_set')
    
    for match in active_match:
    	print match.name
    	for link in match.links_set.all():
    		print link


    return render(request, 'match.html', {"match": active_match})
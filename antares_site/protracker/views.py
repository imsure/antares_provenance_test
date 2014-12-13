from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from protracker.models import Alert, Image, Attribute, \
    AttributeValue, DerivedAttribute
from datetime import datetime

decisions = {
    'Throttled Alert': 'T',
    'Diverted immediately': 'D',
    'Level-I Alert': 'L1',
    'Level-II Alert': 'L2',
    'Rarest of the rare Alert': 'R',
}

# Create your views here.

def index( request ):
    image_list = Image.objects.all()
    template = loader.get_template( 'protracker/index.html' )
    context = { 'image_list': image_list, 'alert_types': decisions.keys() }
    return render( request, 'protracker/index.html', context )

def alert_search( request ):
    if request.method == "GET":
        taken_at = ( request.GET['taken_at'] )
        d = datetime.strptime(taken_at, '%b. %d, %Y, %H:%M p.m.')
        d = d.date()
        alert_type = ( request.GET['alert_type'] )
        alert_list = Alert.objects.filter( Decision__exact=decisions[alert_type],
                                           TakenAt__year=d.year, TakenAt__month=d.month, TakenAt__day=d.day )
        context = { 'alert_list': alert_list,
                    'taken_at': taken_at,
                    'alert_type': alert_type }
        return render( request, 'protracker/alert_search.html', context )
    
def alert_attr( request, alert_id ):
    alert = get_object_or_404( Alert, pk=alert_id )
    attrs = AttributeValue.objects.filter( ContainerID=alert_id,
                                           ContainerType='E' )
    context = { 'attrs': attrs,
                'alert': alert }
    return render( request, 'protracker/alert_attr.html', context )

def derived_attr( request, attrname ):
    derives = DerivedAttribute.objects.filter( AttrName_id=attrname )
    context = { 'derived_attr': derives[0] }
    return render( request, 'protracker/derived_attr.html', context )

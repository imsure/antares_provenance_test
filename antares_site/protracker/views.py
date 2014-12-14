from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from protracker.models import Alert, Image, Attribute, \
    AttributeValue, DerivedAttribute, AlertReplica, \
    AstroObject, ReplicaAssociatedWith, Locus, Source
from datetime import datetime
from protracker.github import GitHub
import re

decisions = {
    'Throttled Alert': 'T',
    'Diverted immediately': 'D',
    'Level-I Alert': 'L1',
    'Level-II Alert': 'L2',
    'Rarest of the rare Alert': 'R',
}

gituser = 'imsure'
repo = 'antares_provenance_test'

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

def attr_code( request, sha1 ):
    gh = GitHub()
    commit = gh.repos( gituser, repo ).commits( sha1 ).get()
    url2code = commit['html_url'].replace( 'commit', 'tree' )
    return redirect( url2code )

def func_code( request, funcname, sha1 ):
    gh = GitHub()
    query = """{0} in:file language:py repo:{1}/{2}""".format( funcname, gituser, repo )
    search = gh.search.code.get( q=query )
    url2code = search['items'][0]['html_url']
    sha1_start = url2code.find('/blob/') + 6
    sha1_end = sha1_start + 40
    oldsha1 = url2code[ sha1_start : sha1_end ]
    url2code = url2code.replace( oldsha1, sha1 )
#    url2code += '#L3'
    return redirect( url2code )

def replicas( request, alert_id ):
    reps = AlertReplica.objects.filter( AlertID_id=alert_id )
    context = { 'replicas': reps,
                'alert' : alert_id }
    return render( request, 'protracker/replica.html', context )

def replica_attr( request, replica_id ):
    replica = get_object_or_404( AlertReplica, pk=replica_id )
    attrs = AttributeValue.objects.filter( ContainerID=replica_id,
                                           ContainerType='R' )
    context = { 'attrs': attrs,
                'replica': replica }
    return render( request, 'protracker/replica_attr.html', context )

def astro( request, replica_id ):
    replica_astro = ReplicaAssociatedWith.objects.filter( ReplicaID_id=replica_id )
    astroobj = None
    if replica_astro:
        astroobj = get_object_or_404( AstroObject, AstroObjectID=replica_astro[0].AstroObjectID_id )
    
    context = { 'replica_id' : replica_id,
                'astro' : astroobj }
    return render( request, 'protracker/astro.html', context )

def alert_attr( request, alert_id ):
    alert = get_object_or_404( Alert, pk=alert_id )
    attrs = AttributeValue.objects.filter( ContainerID=alert_id,
                                           ContainerType='E' )
    context = { 'attrs': attrs,
                'alert': alert }
    return render( request, 'protracker/alert_attr.html', context )

def locus( request, locus_id ):
    loc = get_object_or_404( Locus, pk=locus_id )
    context = { 'locus': loc }
    return render( request, 'protracker/locus.html', context )

def source( request, source_id ):
    src = get_object_or_404( Source, pk=source_id )
    context = { 'source': src }
    return render( request, 'protracker/source.html', context )

def image( request, image_id ):
    img = get_object_or_404( Image, pk=image_id )
    context = { 'image': img }
    return render( request, 'protracker/image.html', context )


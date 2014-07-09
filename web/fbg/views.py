# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from fbg.models import NrsEnvironment
from fbg.models import FbgPicture
from fbg.models import NrsNode
from fbg.models import NrsDatastream
from fbg.models import NrsDatastreamPicture
from fbg.models import NrsDatastream
from fbg.forms import FilterForm
from fbg.render import PrintColorMap
from django.core.context_processors import csrf	
from django.contrib.auth.decorators import login_required
from datetime import datetime
import os

@login_required
def index(request):	
    picture_list = []
    data_dict = {}
    environment = 17
    n = NrsEnvironment.objects.get(pk=environment)
    picture_list = n.fbgpicture_set.all()
    env_list = NrsEnvironment.objects.all().order_by('-title')
    #print "index-1"
    if request.method == 'POST': # If the form has been submitted...
        #print "index-2"
        form = FilterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #print "index-2.1"
            #environment = form.cleaned_data['environment']
            datetime_from = form.cleaned_data['datetime_from']
            datetime_to = form.cleaned_data['datetime_to']
            view_option = form.cleaned_data['view_option']
            aggregate_option = form.cleaned_data['aggregate_option']
            interpolation_method = form.cleaned_data['interpolation_method']
            #print "index-2.2"
            for pict in picture_list:
                #if pict.filename=='h665.png' or pict.filename=='h680.png':
                #todo modificare path e rimuovere if
                splitted_path = os.path.split(pict.filepath)
                sDir = splitted_path[0]
                retVals = my_custom_sql(pict.filename,datetime_to,datetime_from)
                imagefpath ,imagefname = PrintColorMap(dateFrom=datetime_from,dateTo=datetime_to,sOutDir=sDir, imgFilePath=pict.filepath, imgFileName=pict.filename, sMethod=interpolation_method)
                #print "index-2.2.2 after PrintColorMap - len(retVals)=%d " % len(retVals)
                pict.filepath = imagefpath
                pict.filename = imagefname
                data_dict[pict.id] = retVals
    else:
        #print "index-3"
        form = FilterForm()
    c = {'env_list': env_list, 'form':form, 'picture_list':picture_list, 'data_dict':data_dict}
    c.update(csrf(request))
    #print "index-4"
    return render_to_response('fbg/index.html',c)

	
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def my_custom_sql(picture_name,date_to,date_from):
    sDtFrom = date_from.strftime('%Y-%m-%d')
    sDtTo = date_to.strftime('%Y-%m-%d')
    sHHFrom = "00"
    sMMFrom = "00"
    sSSFrom = "00"
    sHHTo = "23"
    sMMTo = "59"
    sSSTo = "59"
    sDtFrom = "%s %s:%s:%s.000000" % (sDtFrom,sHHFrom,sMMFrom,sSSFrom)
    sDtTo = "%s %s:%s:%s.000000" % (sDtTo,sHHTo,sMMTo,sSSTo)
    dtf=datetime.strptime(sDtFrom,"%Y-%m-%d %H:%M:%S.%f")
    dtt=datetime.strptime(sDtTo,"%Y-%m-%d %H:%M:%S.%f")
    sAt_from = dtf.strftime('%Y%m%d%H%M%S%f')  
    sAt_to = dtt.strftime('%Y%m%d%H%M%S%f')
    from django.db import connection
    cursor = connection.cursor()
    sQuery = """SELECT
            nrs_datastream.id AS nrs_id, 
            nrs_datastream.title AS nrs_title, 
            AVG(nrs_datapoint.value_at) AS nrs_value ,
            nrs_datastream.constant_value,
            nrs_datastream.lambda_value,
            nrs_datastream.factor_value, 
            nrs_datastream.factor_value_2, 
            nrs_datastream.ds_formula, 
            --nrs_datapoint.datetime_at AS nrs_datetime,
            nrs_datastream_picture.px AS nrs_px,
            nrs_datastream_picture.py AS nrs_py
            FROM
            fbg_picture
            JOIN nrs_datastream_picture ON    nrs_datastream_picture.filename  =     fbg_picture.filename
            JOIN nrs_datastream ON nrs_datastream.id  = nrs_datastream_picture.datastream_id 
            JOIN nrs_datapoint ON nrs_datapoint.nrs_datastream_id = nrs_datastream.id
            WHERE
            fbg_picture.filename = '%s' AND
            nrs_datapoint.datetime_at <= '%s' AND nrs_datapoint.datetime_at >= '%s'
            GROUP BY nrs_datastream.id,
            -- nrs_datapoint.datetime_at,
            nrs_datastream_picture.px, nrs_datastream_picture.py ,
            nrs_datastream.constant_value,
            nrs_datastream.lambda_value,
            nrs_datastream.factor_value, 
            nrs_datastream.factor_value_2,
            nrs_datastream.ds_formula
            ORDER BY nrs_datastream.id, nrs_datapoint.datetime_at
            """ % (picture_name,sAt_to,sAt_from)
    #print "sQuery=%s" % sQuery
    cursor.execute(sQuery)
    return dictfetchall(cursor)

def env_detail(request, nrs_environment_id):
    env = get_object_or_404(NrsEnvironment, pk=nrs_environment_id)
    return render_to_response('fbg/env_detail.html', {'env': env})

def node_detail(request, nrs_node_id):
    node = get_object_or_404(NrsNode, pk=nrs_node_id)
    return render_to_response('fbg/node_detail.html', {'node': node})

def results(request, nrs_environment_id):
    return HttpResponse("You're looking at the results of Environment %s." % nrs_environment_id)

def update(request, nrs_environment_id):
    return HttpResponse("You're updating on Environment %s." % nrs_environment_id)

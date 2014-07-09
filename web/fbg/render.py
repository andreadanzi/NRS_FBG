import re, time, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from scipy.interpolate import griddata
import matplotlib.image as mpimg
from scipy.ndimage.measurements import label
from scipy.misc.pilutil import imread
from scipy import ndimage
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

# choose method between 'linear', 'cubic','nearest'
def PrintColorMap(dateFrom,dateTo,sOutDir, imgFilePath, imgFileName, sMethod ):
    #print "PrintColorMap-1"
    sDtFrom = dateFrom.strftime('%Y-%m-%d')
    sDtTo = dateTo.strftime('%Y-%m-%d')
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
    img = imread(imgFilePath)
    img_shape=img.shape
    delta = 1.0
    x = np.arange(0, img_shape[1], delta)
    y = np.arange(0, img_shape[0], delta)
    yj=img_shape[0]+1
    xj=img_shape[1]+1
    W = float(img_shape[1])
    H = float(img_shape[0])
    FW = W / float(800)
    FH = H / float(600)
    gx, gy =  np.mgrid[0:xj, 0:yj]
    mysensors = np.zeros((0,2))
    myvalues = np.zeros(0,'f')
    #print "PrintColorMap-2 before LoadDatapoints"
    rowList = LoadDatapoints(imgFileName,sAt_from, sAt_to)    
    for row in rowList:
        at_val = float(row['avg_value_at'])
        const = float(row['constant_value']) #constant_value
        lambda_val = float(row['lambda_value']) #lambda_value
        first = float(row['factor_value']) #factor_value
        second = float(row['factor_value_2']) #factor_value_2
        sFormula = row['ds_formula']
        delta_val = at_val - lambda_val
        x = delta_val
        try:
            retVal = eval(sFormula)
        except Exception, e:
            retVal = 0.0
            logger.error("PrintColorMap Exception on eval for %s: error message is '%s'" % (imgFileName,str(e)))
        mysensors = np.append(mysensors,[[FW*row['px'],H-FH*row['py']]],axis=0)
        myvalues = np.append(myvalues,[retVal],axis=0)
    #print "PrintColorMap-3 after LoadDatapoints"
    try:
        m_interp_cubic = griddata(mysensors, myvalues, (gx, gy), method=sMethod)
    except Exception, e:
        logger.error("PrintColorMap Exception on griddata for %s: error message is '%s'" % (imgFileName,str(e)))
        return imgFilePath , imgFileName
    #print "PrintColorMap-4 after griddata"
    fig = plt.figure(dpi=200,facecolor='none')
    #print "PrintColorMap-4.1 after figure"
    plt.plot(mysensors[:,0], mysensors[:,1], 'rD', ms=2)
    #print "PrintColorMap-4.2 after plot"
    imgDam = mpimg.imread(imgFilePath)
    #print "PrintColorMap-4.3 after imread"
    imgBackground = plt.imshow(imgDam,extent=(0,img_shape[1],0,img_shape[0]),origin='upper')
    #print "PrintColorMap-5 after imshow"
    ax = fig.add_subplot(111)
    imgInterpolation = ax.imshow(m_interp_cubic.T, extent=(0,img_shape[1],0,img_shape[0]),origin='lower', alpha=0.8)
    divider = make_axes_locatable(ax)
    ax_cb = divider.append_axes("right", size="5%", pad=0.05)
    #print "PrintColorMap-6"
    plt.colorbar(imgInterpolation, cax=ax_cb)
    ax.axis('off')
    levels = np.arange(20, 40, 0.5)
    CS = ax.contour(gx, gy, m_interp_cubic,levels=levels)
    ax.clabel(CS, inline=1, fontsize=8)
    newFilename= "interpolation_%s_%s.png" % (sMethod,imgFileName.split('.')[0])
    imagefname=os.path.join(sOutDir,newFilename)
    #print "PrintColorMap-7 before savefig(%s)" % imagefname
    if os.path.exists(imagefname):
        os.remove(imagefname)
    plt.savefig(imagefname,dpi=200,format='png', bbox_inches='tight', pad_inches=0)
    #print "PrintColorMap-8 after savefig(%s)" % imagefname
    return imagefname , newFilename

def LoadDatapoints(sFilename, sAt_from, sAt_to):
    from django.db import connection
    cursor = connection.cursor()
    sQuery = """
        SELECT 
			nrs_datastream.id, 
			nrs_datastream_picture.px, 
			nrs_datastream_picture.py,
			AVG(value_at) AS avg_value_at  
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
        FROM nrs_datastream_picture, nrs_datastream, nrs_datapoint
        WHERE
        nrs_datastream_picture.datastream_id = nrs_datastream.id
        AND
        nrs_datapoint.nrs_datastream_id = nrs_datastream.id
        AND
        nrs_datastream_picture.filename = '%s'
        AND 
        nrs_datapoint.datetime_at <= '%s' AND nrs_datapoint.datetime_at >= '%s'
        GROUP BY nrs_datastream.id, nrs_datastream_picture.px, nrs_datastream_picture.py
        ORDER BY nrs_datastream_picture.py, nrs_datastream_picture.px
    """ % (sFilename, sAt_to, sAt_from)
    cursor.execute(sQuery)
    retValues = dictfetchall(cursor)
    return retValues
    
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

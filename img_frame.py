#Boa:Dialog:imgAssociation

import wx
import wx.lib.buttons
import wx.lib.scrolledpanel
import sqlite3, re, time, os
import matplotlib
import numpy as np 
import Image
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.image as mpimg
from scipy.ndimage.measurements import label
from scipy.misc.pilutil import imread
from scipy import ndimage
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

def create(parent):
    return imgAssociation(parent)

[wxID_IMGASSOCIATION, wxID_IMGASSOCIATIONBTNADD, wxID_IMGASSOCIATIONBTNREMOVE, 
 wxID_IMGASSOCIATIONBTNRENDER, wxID_IMGASSOCIATIONBTNSAVE, 
 wxID_IMGASSOCIATIONCHCINTERPOLATION, wxID_IMGASSOCIATIONCHCPOINTS, 
 wxID_IMGASSOCIATIONDATEFROM, wxID_IMGASSOCIATIONDATETO, 
 wxID_IMGASSOCIATIONIMGINTERPOLATION, wxID_IMGASSOCIATIONIMGMAIN, 
 wxID_IMGASSOCIATIONLISTCTRLDATASTREAM, 
 wxID_IMGASSOCIATIONLSTCTRLASSOCIATEDDATASTREAM, wxID_IMGASSOCIATIONNTBKIMG, 
 wxID_IMGASSOCIATIONPANEL1, wxID_IMGASSOCIATIONPANEL2, 
 wxID_IMGASSOCIATIONPANEL3, wxID_IMGASSOCIATIONRBTFILTERBYCODE, 
 wxID_IMGASSOCIATIONRBTFILTERBYNAME, wxID_IMGASSOCIATIONSCRLWIN, 
 wxID_IMGASSOCIATIONSTATICBOX1, wxID_IMGASSOCIATIONSTATICBOX2, 
 wxID_IMGASSOCIATIONSTATICTEXT1, wxID_IMGASSOCIATIONSTATICTEXT2, 
 wxID_IMGASSOCIATIONTEXTCLICKED, wxID_IMGASSOCIATIONTXTDESCRIZIONE, 
 wxID_IMGASSOCIATIONTXTFILTERDSBYNAME, wxID_IMGASSOCIATIONTXTOUTPUTFILE, 
 wxID_IMGASSOCIATIONTXTPOSITION, wxID_IMGASSOCIATIONTXTPX, 
 wxID_IMGASSOCIATIONTXTPY, 
] = [wx.NewId() for _init_ctrls in range(31)]

class imgAssociation(wx.Dialog):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel3, 0, border=0, flag=0)

    def _init_coll_listCtrlDatastream_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=u'Nome',
              width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Codice', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading=u'CWL',
              width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT, heading=u'Data',
              width=-1)

    def _init_coll_ntbkImg_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=True,
              text=u'Datastreams')
        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text=u'Image')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Interpolation')

    def _init_coll_lstCtrlAssociatedDatastream_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Datastream', width=100)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading=u'CWL',
              width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading=u'File',
              width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading=u'Descrizione', width=120)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT, heading=u'x',
              width=50)
        parent.InsertColumn(col=5, format=wx.LIST_FORMAT_LEFT, heading=u'y',
              width=50)
        parent.InsertColumn(col=6, format=wx.LIST_FORMAT_LEFT, heading=u'id',
              width=-1)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.ntbkImg.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_IMGASSOCIATION, name=u'imgAssociation',
              parent=prnt, pos=wx.Point(353, 41), size=wx.Size(958, 727),
              style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.TRANSPARENT_WINDOW | wx.DEFAULT_DIALOG_STYLE,
              title=u'Datastream to Image Association')
        self.SetClientSize(wx.Size(942, 689))
        self.Show(True)

        self.ntbkImg = wx.Notebook(id=wxID_IMGASSOCIATIONNTBKIMG,
              name=u'ntbkImg', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1263, 685), style=0)

        self.panel1 = wx.Panel(id=wxID_IMGASSOCIATIONPANEL1, name='panel1',
              parent=self.ntbkImg, pos=wx.Point(0, 0), size=wx.Size(1255, 659),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_IMGASSOCIATIONPANEL2, name='panel2',
              parent=self.ntbkImg, pos=wx.Point(0, 0), size=wx.Size(1255, 659),
              style=wx.TAB_TRAVERSAL)

        self.txtPosition = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTPOSITION,
              name=u'txtPosition', parent=self.panel2, pos=wx.Point(24, 8),
              size=wx.Size(88, 21), style=0, value=u'')
        self.txtPosition.SetEditable(False)

        self.textClicked = wx.TextCtrl(id=wxID_IMGASSOCIATIONTEXTCLICKED,
              name=u'textClicked', parent=self.panel2, pos=wx.Point(120, 8),
              size=wx.Size(88, 21), style=0, value=u'')
        self.textClicked.SetEditable(False)

        self.scrlWin = wx.ScrolledWindow(id=wxID_IMGASSOCIATIONSCRLWIN,
              name=u'scrlWin', parent=self.panel2, pos=wx.Point(8, 32),
              size=wx.Size(984, 616), style=wx.HSCROLL | wx.VSCROLL)

        self.imgMain = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_IMGASSOCIATIONIMGMAIN, name=u'imgMain',
              parent=self.scrlWin, pos=wx.Point(8, 8), size=wx.Size(800, 600),
              style=wx.THICK_FRAME)
        self.imgMain.Enable(True)
        self.imgMain.SetAutoLayout(True)
        self.imgMain.SetMaxSize(wx.Size(550, 1200))
        self.imgMain.Bind(wx.EVT_MOTION, self.OnImgMainMotion)
        self.imgMain.Bind(wx.EVT_ENTER_WINDOW, self.OnImgMainEnterWindow)
        self.imgMain.Bind(wx.EVT_LEAVE_WINDOW, self.OnImgMainLeaveWindow)
        self.imgMain.Bind(wx.EVT_LEFT_UP, self.OnImgMainLeftUp)
        self.imgMain.Bind(wx.EVT_MOUSEWHEEL, self.OnImgMainMousewheel)
        self.imgMain.Bind(wx.EVT_LEFT_DOWN, self.OnImgMainLeftDown)

        self.lstCtrlAssociatedDatastream = wx.ListCtrl(id=wxID_IMGASSOCIATIONLSTCTRLASSOCIATEDDATASTREAM,
              name=u'lstCtrlAssociatedDatastream', parent=self.panel1,
              pos=wx.Point(416, 48), size=wx.Size(485, 480),
              style=wx.LC_REPORT)
        self._init_coll_lstCtrlAssociatedDatastream_Columns(self.lstCtrlAssociatedDatastream)
        self.lstCtrlAssociatedDatastream.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnLstCtrlAssociatedDatastreamListItemSelected,
              id=wxID_IMGASSOCIATIONLSTCTRLASSOCIATEDDATASTREAM)
        self.lstCtrlAssociatedDatastream.Bind(wx.EVT_LEFT_DCLICK,
              self.OnLstCtrlAssociatedDatastreamLeftDclick)

        self.btnAdd = wx.lib.buttons.GenButton(id=wxID_IMGASSOCIATIONBTNADD,
              label=u'>>', name=u'btnAdd', parent=self.panel1, pos=wx.Point(360,
              128), size=wx.Size(48, 25), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_IMGASSOCIATIONBTNADD)

        self.btnRemove = wx.lib.buttons.GenButton(id=wxID_IMGASSOCIATIONBTNREMOVE,
              label=u'<<', name=u'btnRemove', parent=self.panel1,
              pos=wx.Point(360, 175), size=wx.Size(48, 25), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_IMGASSOCIATIONBTNREMOVE)

        self.txtDescrizione = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTDESCRIZIONE,
              name=u'txtDescrizione', parent=self.panel1, pos=wx.Point(424,
              560), size=wx.Size(184, 72), style=wx.VSCROLL | wx.TE_MULTILINE,
              value=u'')

        self.txtPX = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTPX, name=u'txtPX',
              parent=self.panel1, pos=wx.Point(640, 560), size=wx.Size(40, 21),
              style=0, value=u'')
        self.txtPX.SetEditable(True)

        self.txtPY = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTPY, name=u'txtPY',
              parent=self.panel1, pos=wx.Point(712, 560), size=wx.Size(40, 21),
              style=0, value=u'')

        self.staticText1 = wx.StaticText(id=wxID_IMGASSOCIATIONSTATICTEXT1,
              label=u'X', name='staticText1', parent=self.panel1,
              pos=wx.Point(688, 536), size=wx.Size(7, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_IMGASSOCIATIONSTATICTEXT2,
              label=u'Y', name='staticText2', parent=self.panel1,
              pos=wx.Point(760, 536), size=wx.Size(7, 13), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_IMGASSOCIATIONSTATICBOX1,
              label=u'Coordinate', name='staticBox1', parent=self.panel1,
              pos=wx.Point(624, 536), size=wx.Size(160, 112), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_IMGASSOCIATIONSTATICBOX2,
              label=u'Descrizione', name='staticBox2', parent=self.panel1,
              pos=wx.Point(416, 536), size=wx.Size(200, 112), style=0)

        self.listCtrlDatastream = wx.ListCtrl(id=wxID_IMGASSOCIATIONLISTCTRLDATASTREAM,
              name=u'listCtrlDatastream', parent=self.panel1, pos=wx.Point(24,
              48), size=wx.Size(328, 624), style=wx.LC_REPORT)
        self._init_coll_listCtrlDatastream_Columns(self.listCtrlDatastream)
        self.listCtrlDatastream.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlDatastreamListItemSelected,
              id=wxID_IMGASSOCIATIONLISTCTRLDATASTREAM)
        self.listCtrlDatastream.Bind(wx.EVT_LEFT_DCLICK,
              self.OnListCtrlDatastreamLeftDclick)

        self.btnSave = wx.Button(id=wxID_IMGASSOCIATIONBTNSAVE,
              label=u'Modifica', name=u'btnSave', parent=self.panel1,
              pos=wx.Point(640, 600), size=wx.Size(75, 23), style=0)
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_IMGASSOCIATIONBTNSAVE)

        self.chcPoints = wx.Choice(choices=[], id=wxID_IMGASSOCIATIONCHCPOINTS,
              name=u'chcPoints', parent=self.panel2, pos=wx.Point(216, 8),
              size=wx.Size(264, 21), style=0)
        self.chcPoints.SetSelection(0)
        self.chcPoints.SetStringSelection(u'')
        self.chcPoints.SetToolTipString(u'choice1')
        self.chcPoints.Bind(wx.EVT_CHOICE, self.OnChcPointsChoice,
              id=wxID_IMGASSOCIATIONCHCPOINTS)

        self.panel3 = wx.Panel(id=wxID_IMGASSOCIATIONPANEL3, name='panel3',
              parent=self.ntbkImg, pos=wx.Point(0, 0), size=wx.Size(816, 640),
              style=wx.TAB_TRAVERSAL)

        self.imgInterpolation = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_IMGASSOCIATIONIMGINTERPOLATION, name=u'imgInterpolation',
              parent=self.panel3, pos=wx.Point(16, 40), size=wx.Size(800, 600),
              style=wx.THICK_FRAME)
        self.imgInterpolation.Enable(True)
        self.imgInterpolation.SetAutoLayout(True)
        self.imgInterpolation.SetMaxSize(wx.Size(550, 1200))

        self.btnRender = wx.Button(id=wxID_IMGASSOCIATIONBTNRENDER,
              label=u'Visualizza', name=u'btnRender', parent=self.panel3,
              pos=wx.Point(296, 5), size=wx.Size(75, 23), style=0)
        self.btnRender.Bind(wx.EVT_BUTTON, self.OnBtnRenderButton,
              id=wxID_IMGASSOCIATIONBTNRENDER)

        self.dateFrom = wx.DatePickerCtrl(id=wxID_IMGASSOCIATIONDATEFROM,
              name=u'dateFrom', parent=self.panel3, pos=wx.Point(102, 6),
              size=wx.Size(88, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dateFrom.SetToolTipString(u'dtFrom')
        self.dateFrom.SetValue(wx.DateTimeFromDMY(1, 0, 2012, 0, 0, 0))
        self.dateFrom.SetLabel(u'01/01/2012')

        self.dateTo = wx.DatePickerCtrl(id=wxID_IMGASSOCIATIONDATETO,
              name=u'dateTo', parent=self.panel3, pos=wx.Point(206, 6),
              size=wx.Size(80, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dateTo.SetToolTipString(u'dtTo')
        self.dateTo.SetValue(wx.DateTimeFromDMY(26, 9, 2012, 18, 25, 32))
        self.dateTo.SetLabel(u'26/10/2012')

        self.txtOutputFile = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTOUTPUTFILE,
              name=u'txtOutputFile', parent=self.panel3, pos=wx.Point(400, 8),
              size=wx.Size(364, 21), style=wx.NO_3D | wx.NO_BORDER, value=u'')
        self.txtOutputFile.SetEditable(False)

        self.chcInterpolation = wx.Choice(choices=['linear', 'cubic',
              'nearest'], id=wxID_IMGASSOCIATIONCHCINTERPOLATION,
              name=u'chcInterpolation', parent=self.panel3, pos=wx.Point(8, 6),
              size=wx.Size(60, 21), style=0)
        self.chcInterpolation.SetSelection(0)

        self.txtFilterDSByName = wx.TextCtrl(id=wxID_IMGASSOCIATIONTXTFILTERDSBYNAME,
              name=u'txtFilterDSByName', parent=self.panel1, pos=wx.Point(120,
              16), size=wx.Size(224, 21), style=wx.TE_PROCESS_ENTER, value=u'')
        self.txtFilterDSByName.Bind(wx.EVT_TEXT_ENTER,
              self.OnTxtFilterDSByNameTextEnter,
              id=wxID_IMGASSOCIATIONTXTFILTERDSBYNAME)

        self.rbtFilterByName = wx.RadioButton(id=wxID_IMGASSOCIATIONRBTFILTERBYNAME,
              label=u'Filtra Nome', name=u'rbtFilterByName', parent=self.panel1,
              pos=wx.Point(24, 8), size=wx.Size(81, 13), style=0)
        self.rbtFilterByName.SetValue(True)
        self.rbtFilterByName.Bind(wx.EVT_RADIOBUTTON,
              self.OnRbtFilterByNameRadiobutton,
              id=wxID_IMGASSOCIATIONRBTFILTERBYNAME)

        self.rbtFilterByCode = wx.RadioButton(id=wxID_IMGASSOCIATIONRBTFILTERBYCODE,
              label=u'Filtra Codice', name=u'rbtFilterByCode',
              parent=self.panel1, pos=wx.Point(24, 24), size=wx.Size(81, 13),
              style=0)
        self.rbtFilterByCode.SetValue(True)
        self.rbtFilterByCode.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton,
              id=wxID_IMGASSOCIATIONRBTFILTERBYCODE)

        self._init_coll_ntbkImg_Pages(self.ntbkImg)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.pps = 8
        self.scrlWin.SetScrollbars(self.pps,self.pps,8,8)
        self.imgFile = None
        self.zoomfactor = 0
        self.scale = self.getScaleFactor()
        self.scrlWin.center = self.calcCenter()
        self.scrlWin.imDirty = True
        self.points = []
        self.currentThickness = 3
        self.currentColour = 'Red'
        self.previousPosition = (0, 0)
        
    def getScaleFactor(self):
        return float(2**self.zoomfactor)

    def calcCenter(self):
        if self.imgFile:
            w, h = self.calcClientSize()
            w = w / self.scale
            h = h / self.scale
            w = w / 2.0
            h = h / 2.0
            viewStart = self.scrlWin.GetViewStart()  # in scroll units
            vsx = (viewStart[0] * float(self.pps)) / self.scale
            vsy = (viewStart[1] * float(self.pps)) / self.scale
            return (w+vsx, h+vsy)
        else:
            return (0.0, 0.0)

    def calcClientSize(self):
        clientSize = self.scrlWin.GetClientSizeTuple()
        virtualW = float(self.imgFile.GetWidth()) * self.scale
        virtualH = float(self.imgFile.GetHeight()) * self.scale
        w = min(virtualW, float(clientSize[0]))
        h = min(virtualH, float(clientSize[1]))
        return (w, h)
    
    def setParameters(self,imgFile,datastreamList,available_datastreamList,imgFileName,imgFilePath, database, min_date, max_date, env_dir):
        self.database = database
        self.imgFile=imgFile
        self.EnvDir = env_dir
        self.imgFileName = imgFileName
        self.imgFilePath = imgFilePath
        self.scrlWin.center = self.calcCenter()
        self.datastreamList = datastreamList
        self.wxMinDatetime_at = min_date
        self.wxMaxDatetime_at = max_date
        if min_date:
			self.dateFrom.SetValue(min_date)
        if max_date:
			self.dateTo.SetValue(max_date)        
        self.default_available_datastreamList = available_datastreamList 
        self.available_datastreamList = available_datastreamList
        self.setAvailableDatastreams()
        self.setDatastreamsPicutes()
        self.setImageToPreview(self.imgFile)
        self.initPointsBuffer()
        
    def setImageToPreview(self, wxImgFile):
        Img = wxImgFile
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = 800
            NewH = 800 * H / W                
        else:
            NewH = 600
            NewW = 600 * W / H
        ImgScaled = Img.Scale(NewW,NewH)
        self.imgMain.SetBitmap(wx.BitmapFromImage(ImgScaled))
        self.imgScaled = ImgScaled
        self.imgMain.Refresh()     
        self.scrlWin.Refresh() 
        self.Refresh()
        

    def setDatastreamsPicutes(self):
        self.lstCtrlAssociatedDatastream.DeleteAllItems()
        x = 0
        chcItems = self.chcPoints.GetItems()
        # nrs_datastream_picture.id, nrs_datastream.id, nrs_datastream.title, nrs_datastream_picture.filename, nrs_datastream_picture.description, frequency
        for row in self.datastreamList:
            self.lstCtrlAssociatedDatastream.InsertStringItem(x,row[2])
            if row[4]==None:
                row[4]=""
            self.lstCtrlAssociatedDatastream.SetStringItem(x,1,u'%f' % row[8])
            self.lstCtrlAssociatedDatastream.SetStringItem(x,2,row[3])
            self.lstCtrlAssociatedDatastream.SetStringItem(x,3,row[4])
            self.lstCtrlAssociatedDatastream.SetStringItem(x,4,u'%d' % row[6])
            self.lstCtrlAssociatedDatastream.SetStringItem(x,5,u'%d' % row[7])
            self.lstCtrlAssociatedDatastream.SetStringItem(x,6,u'%d' % row[1])
            self.lstCtrlAssociatedDatastream.SetItemData(x,row[0])
            chcItems.append("%s-(%d)" % (row[2], row[0]))
            self.points.append([self.currentColour, self.currentThickness,[row[6], row[7]],row[0],False])
            x = x + 1        
        self.chcPoints.SetItems(chcItems)
        if len(chcItems) > 0:
            self.chcPoints.SetSelection(0)
        sSelected = self.chcPoints.GetStringSelection()
        m = re.compile(r'-\((.*?)\)').search(sSelected)
        if m != None:
            sm = m.group(1)
            id = int(sm)        
            data = self.GetDatastreamPicture(id)
            self.textClicked.SetValue(u'%d-%d' % (data['px'], data['py']))


    def filterAvailableDatastreams(self, sValue, sType):
        self.listCtrlDatastream.DeleteAllItems()
        x = 0
        for row in self.available_datastreamList:
            if sType == "C":
                str1 = row[1]
                if str1.find(sValue) == -1:
                    continue                
            if sType == "N":
                str0 = row[0]
                if str0.find(sValue) == -1:
                    continue
            self.listCtrlDatastream.InsertStringItem(x,row[0])
            if row[4]==None:
                row[4]=""
            self.listCtrlDatastream.SetStringItem(x,1,row[1])
            self.listCtrlDatastream.SetStringItem(x,2,str(row[8]))
            self.listCtrlDatastream.SetStringItem(x,3,row[2])
            self.listCtrlDatastream.SetItemData(x,row[3])
            x = x + 1

    def setAvailableDatastreams(self):
        self.listCtrlDatastream.DeleteAllItems()
        x = 0
        for row in self.available_datastreamList:
            self.listCtrlDatastream.InsertStringItem(x,row[0])
            if row[4]==None:
                row[4]=""
            self.listCtrlDatastream.SetStringItem(x,1,row[1])
            self.listCtrlDatastream.SetStringItem(x,2,str(row[8]))
            self.listCtrlDatastream.SetStringItem(x,3,row[2])
            self.listCtrlDatastream.SetItemData(x,row[3])
            x = x + 1
            

    def OnImgMainMotion(self, event):
        wxPoint = event.GetPosition()
        self.txtPosition.SetValue(u'%d-%d' % ( wxPoint.x, wxPoint.y ))
        event.Skip()

    def OnImgMainEnterWindow(self, event):
        self.currentCursor = self.GetCursor();
        self.SetCursor(wx.StockCursor(id=wx.CURSOR_CROSS))
        event.Skip()

    def OnImgMainLeaveWindow(self, event):
        self.SetCursor(self.currentCursor)
        event.Skip()

    def OnImgMainLeftUp(self, event):
        event.Skip()

    def OnImgMainMousewheel(self, event):
        
        event.Skip()

    def OnListCtrlDatastreamListItemSelected(self, event):
        idx = event.m_itemIndex
        id=self.listCtrlDatastream.GetItemData(idx)
        self.selected_available_ds_id = id
        self.selected_available_ds_title = self.listCtrlDatastream.GetItem(idx,0).GetText()
        self.selected_available_ds_frequency = self.listCtrlDatastream.GetItem(idx,2).GetText()
        event.Skip()

    def OnLstCtrlAssociatedDatastreamListItemSelected(self, event):
        idx = event.m_itemIndex
        self.selectedAssDsIndex = idx
        id = self.lstCtrlAssociatedDatastream.GetItemData(idx)
        data = self.GetDatastreamPicture(id)
        self.selectedAssDsID = id
        sDescr = data['description']
        if sDescr == None:
            sDescr = ""
        self.txtDescrizione.SetValue( u'%s' % sDescr)
        self.txtPX.SetValue(u'%d' % data['px'] )
        self.txtPY.SetValue(u'%d' % data['py'])
        
        sTitle = self.lstCtrlAssociatedDatastream.GetItem(self.selectedAssDsIndex,0).GetText()
        sSelected = "%s-(%d)" % (sTitle, id)
        chcItems = self.chcPoints.GetItems()
        iy = 0
        for chcItem in chcItems:
            if chcItem==sSelected:
                break
            iy = iy + 1
        if len(chcItems) > 0:
            self.chcPoints.SetSelection(iy)
            
        self.textClicked.SetValue(u'%d-%d' % (data['px'], data['py']))
        for point in self.points:
            point[0] = "Red"
            point[4] = False
            if point[3]== id:
                point[0] = "Blue"
                point[4] = True
        self.UpdatePointsOnBitmap()
        event.Skip()

    def GetDatastreamPicture(self, id):
        return_value = {}
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT id, datastream_id, filename, filepath,  px, py, description
            FROM nrs_datastream_picture
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = {'id':row[0],'datastream_id':row[1],'filename':row[2],'filepath':row[3],'px':row[4],'py':row[5],'description':row[6]} 
        db_conn.close()
        return return_value

    def OnBtnAddButton(self, event):
        self.putNewDatastream()
        event.Skip()

    def AddDatastreamPicture(self):
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        if self.txtPX.GetValue() == None or self.txtPX.GetValue() == '':
            self.txtPX.SetValue("0")
        if self.txtPY.GetValue() == None or self.txtPY.GetValue() == '':
            self.txtPY.SetValue("0")
        insert_params = (self.selected_available_ds_id,self.imgFileName, self.imgFilePath, int(self.txtPX.GetValue()), int(self.txtPY.GetValue()), u'%s' % self.txtDescrizione.GetValue())
        sQuery = """
            INSERT INTO 
            nrs_datastream_picture  
            (datastream_id, filename, filepath,  px, py, description) 
            VALUES (?,?,?,?,?,?)
        """
        db_cur.execute(sQuery,insert_params)
        retVal = db_cur.lastrowid
        db_conn.commit()      
        db_conn.close()
        return retVal

    def UpdateDatastreamPicture(self):
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        if self.txtPX.GetValue() == None or self.txtPX.GetValue() == '':
            self.txtPX.SetValue("0")
        if self.txtPY.GetValue() == None or self.txtPY.GetValue() == '':
            self.txtPY.SetValue("0")
        sQuery = """
            UPDATE 
            nrs_datastream_picture  SET 
            px = %d, py = %d , description = '%s'
            WHERE
            nrs_datastream_picture.id = %d
        """ % (int(self.txtPX.GetValue()),int(self.txtPY.GetValue()),self.txtDescrizione.GetValue(),self.selectedAssDsID)
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal
    
    def OnBtnRemoveButton(self, event):
        idxes, ids = self._getSelectedIndices(self.lstCtrlAssociatedDatastream)
        idelCount = 0
        delItems = []
        newItems = []
        for idx in idxes:
            delIds = idx - idelCount
            idds = self.lstCtrlAssociatedDatastream.GetItemData(delIds)
            self.delDatastream(idds)
            sTitle = self.lstCtrlAssociatedDatastream.GetItem(delIds,0).GetText()
            self.lstCtrlAssociatedDatastream.DeleteItem(delIds)
            sSelected = "%s-(%d)" % (sTitle, idds)
            for chcItem in self.chcPoints.GetItems():
                if chcItem==sSelected:
                    delItems.append(chcItem)
            idelCount = idelCount + 1
            idpos = 0
            for point in self.points:
                if point[3]== idds:
                    self.points.pop(idpos)
                    break;
                idpos = idpos + 1
        for delItem in delItems:
           delNum = self.chcPoints.FindString(delItem)
           self.chcPoints.Delete(delNum)
        if len(self.chcPoints.GetItems()) > 0:
            self.chcPoints.SetSelection(0)
        self.UpdatePointsOnBitmap()

    def OnListCtrlDatastreamLeftDclick(self, event):
        self.putNewDatastream()
        event.Skip()
    
    
    def delDatastream(self,selectedAssDsID):
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        sQuery = """
            DELETE FROM 
            nrs_datastream_picture  
            WHERE
            id = %d
        """ % selectedAssDsID
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal
        
    def _findExistingDS(self, dsid, imgFileName):
        return_value = {}
        bFound = False
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT id, datastream_id, filename, filepath,  px, py, description
            FROM nrs_datastream_picture
            WHERE datastream_id = %d AND filename = '%s'
        """ % (dsid, imgFileName)
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            bFound = True
            return_value = {'id':row[0],'datastream_id':row[1],'filename':row[2],'filepath':row[3],'px':row[4],'py':row[5],'description':row[6]} 
        db_conn.close()
        return bFound, return_value
    
    def putNewDatastream(self):
        idxes, ids = self._getSelectedIndices(self.listCtrlDatastream)
        for idx in idxes:
            itCount = self.lstCtrlAssociatedDatastream.GetItemCount()
            id=self.listCtrlDatastream.GetItemData(idx)
            bFound, retitem = self._findExistingDS(id,self.imgFileName)
            if bFound:
                continue
            self.selected_available_ds_id = id
            self.selected_available_ds_title = self.listCtrlDatastream.GetItem(idx,0).GetText()
            self.selected_available_ds_frequency = self.listCtrlDatastream.GetItem(idx,2).GetText()
            retVal = self.AddDatastreamPicture()
            self.lstCtrlAssociatedDatastream.InsertStringItem(itCount, self.selected_available_ds_title)
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,1, self.selected_available_ds_frequency )
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,2, self.imgFileName )
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,3, u'%s' % self.txtDescrizione.GetValue() )  
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,6,u'%d' % id)
            self.lstCtrlAssociatedDatastream.SetItemData(itCount,retVal)
            chcItems = self.chcPoints.GetItems()
            chcItems.append("%s-(%d)" % (self.selected_available_ds_title, retVal))
            self.chcPoints.SetItems(chcItems)
            if len(chcItems) > 0:
                self.chcPoints.SetSelection(len(chcItems)-1)
            sSelected = self.chcPoints.GetStringSelection()
            m = re.compile(r'-\((.*?)\)').search(sSelected)
            sm = m.group(1)
            id = int(sm)
            data = self.GetDatastreamPicture(id)  
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,4,u'%d' % data['px'])
            self.lstCtrlAssociatedDatastream.SetStringItem(itCount,5,u'%d' % data['py'])
            self.textClicked.SetValue(u'%d-%d' % (data['px'], data['py']))
            # 0 => currentColour, 1 => currentThickness,2 => (px, py),3 => id, 4=>Selected(True)
            self.points.append(["Red", self.currentThickness,[data['px'], data['py']],id,True])
        self.UpdatePointsOnBitmap()
        

    def OnBtnSaveButton(self, event):
        self.UpdateDatastreamPicture()
        data = self.GetDatastreamPicture(self.selectedAssDsID)
        sDescr = data['description']
        if sDescr == None:
            sDescr = ""
        self.lstCtrlAssociatedDatastream.SetStringItem(self.selectedAssDsIndex,3,u'%s' % sDescr)
        self.lstCtrlAssociatedDatastream.SetStringItem(self.selectedAssDsIndex,4,u'%d' % data['px'])
        self.lstCtrlAssociatedDatastream.SetStringItem(self.selectedAssDsIndex,5,u'%d' % data['py'])
        self.lstCtrlAssociatedDatastream.SetStringItem(self.selectedAssDsIndex,6,u'%d' % data['datastream_id'])
        # 0 => currentColour, 1 => currentThickness,2 => (px, py),3 => id, 4=>Selected(False)
        for point in self.points:
            if point[3]== self.selectedAssDsID:
                point[2][0]=data['px']
                point[2][1]=data['py']
        self.UpdatePointsOnBitmap()
        event.Skip()

    def OnChcPointsChoice(self, event):
        sSelected = self.chcPoints.GetStringSelection()
        m = re.compile(r'-\((.*?)\)').search(sSelected)
        sm = m.group(1)
        id = int(sm)        
        data = self.GetDatastreamPicture(id)
        self.textClicked.SetValue(u'%d-%d' % (data['px'], data['py']))
        for point in self.points:
            point[0] = "Red"
            point[4] = False
            if point[3]== id:
                point[0] = "Blue"
                point[4] = True
        self.UpdatePointsOnBitmap()
        event.Skip()


    def UpdateDatastreamPicturePosition(self, ipx, ipy, idChc):
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
        sQuery = """
            UPDATE 
            nrs_datastream_picture  SET 
            px = %d, py = %d 
            WHERE
            nrs_datastream_picture.id = %d
        """ % (ipx,ipy,idChc)
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal
    
    def initPointsBuffer(self):
        ''' Initialize the bitmap used for buffering the display. '''
        memDC = wx.MemoryDC()
        bitmapUpdated = self.drawPoints(memDC, self.imgMain.GetBitmap(), *self.points)
        memDC.SelectObject( wx.NullBitmap )
        self.imgMain.SetBitmap(bitmapUpdated)

    # Other methods
    @staticmethod
    def drawPoints( dc,imgBitmap, *points):
        ''' drawPoints takes a device context (dc) and a list of points
        as arguments. Each point is a three-tuple: (colour, thickness,
        linesegments). linesegments is a list of coordinates: (x1, y1,
        x2, y2). '''
        dc.SelectObject(imgBitmap)
        #dc.BeginDrawing()
        for colour, thickness, point, point_it, point_enabled in points:
            pen = wx.Pen(wx.NamedColour(colour), thickness, wx.SOLID)
            dc.SetPen(pen)
            #dc.DrawPoint(*point) # x,y tuple
            dc.DrawCircle(point[0],point[1],thickness+1)
        #dc.EndDrawing()
        return imgBitmap

    def OnImgMainLeftDown(self, event):
        wxPoint = event.GetPosition()
        self.textClicked.SetValue(u'%d-%d' % ( wxPoint.x, wxPoint.y ))
        self.txtPX.SetValue(u'%d' % ( wxPoint.x ))
        self.txtPY.SetValue(u'%d' % ( wxPoint.y ))
        sSelected = self.chcPoints.GetStringSelection()
        m = re.compile(r'-\((.*?)\)').search(sSelected)
        sm = m.group(1)
        id = int(sm)
        data = self.GetDatastreamPicture(id)
        self.UpdateDatastreamPicturePosition(wxPoint.x,wxPoint.y,id)
        for point in self.points:
            point[0] = "Red"
            point[4] = False
            if point[3]== id:
                point[2][0] = wxPoint.x
                point[2][1] = wxPoint.y
                point[0] = "Blue"
                point[4] = True
        # Update the List with X,Y
        itemCount = self.lstCtrlAssociatedDatastream.GetItemCount()
        for idx in range(0, itemCount):
              idItem = self.lstCtrlAssociatedDatastream.GetItemData(idx)
              if id == idItem:
                  self.lstCtrlAssociatedDatastream.SetStringItem(idx,4,u'%d' % wxPoint.x)
                  self.lstCtrlAssociatedDatastream.SetStringItem(idx,5,u'%d' % wxPoint.y)
                  break
        # Visualize the point currently Updated
        self.UpdatePointsOnBitmap()
        
    def UpdatePointsOnBitmap(self):
        memDC = wx.MemoryDC()
        localBmp = wx.BitmapFromImage(self.imgScaled)
        bitmapUpdated = self.drawPoints(memDC, localBmp, *self.points)
        memDC.SelectObject( wx.NullBitmap )
        self.imgMain.SetBitmap(bitmapUpdated)

    def OnLstCtrlAssociatedDatastreamLeftDclick(self, event):
        self.ntbkImg.SetSelection(1)
        event.Skip()

    def OnBtnRenderButton(self, event):
        mycur = self.GetCursor();
        self.txtOutputFile.SetValue("")
        self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))        
        localBmp = wx.BitmapFromImage(self.imgScaled)
        sDtFrom = self.dateFrom.GetValue().Format('%Y-%m-%d')
        sDtTo = self.dateTo.GetValue().Format('%Y-%m-%d')
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
        self.imgFileName = self.imgFileName
        img = imread(self.imgFilePath)
        img_shape=img.shape
        delta = 1.0
        x = np.arange(0, img_shape[1], delta)
        y = np.arange(0, img_shape[0], delta)
        yj=img_shape[0]+1 #1201 601
        xj=img_shape[1]+1 #1601 801
        W = float(img_shape[1])
        H = float(img_shape[0])
        FW = W / float(800)
        FH = H / float(600)
        gx, gy =  np.mgrid[0:xj, 0:yj]
        mysensors = np.zeros((0,2))
        myvalues = np.zeros(0,'f')
        rowList = self.LoadDatapoints(self.imgFileName,sAt_from, sAt_to)
        for row in rowList:
            at_val = float(row[3])
            const = row[4] #constant_value
            lambda_val = float(row[5]) #lambda_value
            first = row[6] #factor_value
            second = row[7] #factor_value_2
            sFormula = row[8]
            delta_val = at_val - lambda_val
            x = delta_val
            #resVal = second*x*x + first*x + const
            retVal = eval(sFormula)
            mysensors = np.append(mysensors,[[FW*row[1],H-FH*row[2]]],axis=0)
            #mysensors = np.append(mysensors,[[row[1],600-row[2]]],axis=0)
            myvalues = np.append(myvalues,[retVal],axis=0)
        sMethod = self.chcInterpolation.GetStringSelection()
        m_interp_cubic = griddata(mysensors, myvalues, (gx, gy), method=sMethod)
        fig = plt.figure(dpi=200,facecolor='none')
        plt.plot(mysensors[:,0], mysensors[:,1], 'rD', ms=2)
        imgDam = mpimg.imread(self.imgFilePath)
        imgBackground = plt.imshow(imgDam,extent=(0,img_shape[1],0,img_shape[0]),origin='upper')
        ax = fig.add_subplot(111)
        imgInterpolation = ax.imshow(m_interp_cubic.T, extent=(0,img_shape[1],0,img_shape[0]),origin='lower', alpha=0.8)
        divider = make_axes_locatable(ax)
        #ax_cb = divider.new_horizontal(size="5%", pad=0.05)
        ax_cb = divider.append_axes("right", size="5%", pad=0.05)
        #fig.add_axes(ax_cb)
        plt.colorbar(imgInterpolation, cax=ax_cb)
        #cbar = plt.colorbar(imgInterpolation, orientation='vertical')
        ax.axis('off')
        levels = np.arange(20, 40, 0.5)
        CS = ax.contour(gx, gy, m_interp_cubic,levels=levels)
        ax.clabel(CS, inline=1, fontsize=8)
        #plt.title('Cubic griddata with labels')
        sAt = time.strftime('%Y%m%d%H%M%S')   
        newFilename= "interpolation_%s_%s.png" % (sAt,self.imgFileName.split('.')[0])
        imagefname=os.path.join(self.EnvDir,newFilename)
        plt.savefig(imagefname,dpi=200,format='png', bbox_inches='tight', pad_inches=0)
        Img = wx.Image(imagefname, wx.BITMAP_TYPE_PNG)
        self.wxInterpolImg = Img
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = 800
            NewH = 800 * H / W
        else:
            NewH = 600
            NewW = 600 * W / H
        Img = Img.Scale(NewW,NewH)
        self.imgInterpolation.SetBitmap(wx.BitmapFromImage(Img))
        self.txtOutputFile.SetValue(newFilename)
        self.Refresh()
        self.SetCursor(mycur)

    def LoadDatapoints(self, sFilename, sAt_from, sAt_to):
        #controllare formula danzi.tn@20140702
        db_conn = sqlite3.connect(self.database)
        db_cur = db_conn.cursor()
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
            GROUP BY 
            nrs_datastream.id, 
            nrs_datastream_picture.px, 
            nrs_datastream_picture.py
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            ORDER BY nrs_datastream_picture.py, nrs_datastream_picture.px
        """ % (sFilename, sAt_to, sAt_from)
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        retValues = []
        for row in rows:
            retValues.append(row)
        db_conn.close()
        return retValues

    def checkDsFilters(self):
        sFilter = self.txtFilterDSByName.GetValue()
        sType = "N"
        if self.rbtFilterByCode.GetValue():
            sType = "C"
        self.filterAvailableDatastreams(sFilter, sType)


    def OnTxtFilterDSByNameTextEnter(self, event):
        self.checkDsFilters()
        event.Skip()

    def OnRbtFilterByNameRadiobutton(self, event):
        event = event
        event.Skip()

    def OnRadioButton1Radiobutton(self, event):
        self.checkDsFilters()
        event.Skip()

    def _getSelectedIndices( self, wxList, state =  wx.LIST_STATE_SELECTED):
        indices = []
        ids = []
        lastFound = -1
        while True:
                index = wxList.GetNextItem(
                        lastFound,
                        wx.LIST_NEXT_ALL,
                        state,
                )
                if index == -1:
                        break
                else:
                        lastFound = index
                        indices.append( index )
                        id = wxList.GetItemData(index)
                        ids.append( id )
        return indices, ids

#Boa:Frame:Frame1

import wx
import random
import wx.lib.filebrowsebutton, shutil, sqlite3, time, os, csv
import settings
import logging, os, stat
import time
from nrs_message import Messaggio
from img_frame import imgAssociation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sets import Set
from GibeToNrsWin32_new import GibeToNrs
from scpi_client import SCPICli
from datetime import datetime
from datetime import timedelta
from glob import *
from wxPython.wx import *

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BTNACQUSTART, wxID_FRAME1BTNACQUSTOP, 
 wxID_FRAME1BTNCANELLATUTTO, wxID_FRAME1BTNCLOSE, wxID_FRAME1BTNDELETEADMIN, 
 wxID_FRAME1BTNEXPORT, wxID_FRAME1BTNEXPORTFILE, wxID_FRAME1BTNIMPORTA, 
 wxID_FRAME1BTNIMPORTSCHE, wxID_FRAME1BTNIPAD, wxID_FRAME1BTNLISTA, 
 wxID_FRAME1BTNRANDOMGEN, wxID_FRAME1BTNSAVEPERI_SAM, wxID_FRAME1BTNTEST, 
 wxID_FRAME1BTNUPDATECODE, wxID_FRAME1BUTTONDELETE, wxID_FRAME1BUTTONSAVE, 
 wxID_FRAME1CHECKBOX1, wxID_FRAME1CHECKBOX2, wxID_FRAME1CHKALLDS, 
 wxID_FRAME1CHKBYNODE, wxID_FRAME1CHKDATAFILTER, wxID_FRAME1CHKFORMAT, 
 wxID_FRAME1DATABASEBROWSEBUTTON, wxID_FRAME1DATEFROM, 
 wxID_FRAME1DATEPICKERCTRL1, wxID_FRAME1DATEPICKERCTRL2, wxID_FRAME1DATETO, 
 wxID_FRAME1DTFROM, wxID_FRAME1DTTO, wxID_FRAME1ENVNOME, 
 wxID_FRAME1FILEBROWSEBUTTON1, wxID_FRAME1IMGCHART, wxID_FRAME1IMGMAP, 
 wxID_FRAME1LISTCTRL1, wxID_FRAME1LISTCTRLDATAPOINT, 
 wxID_FRAME1LISTCTRLDATASTREAM, wxID_FRAME1LISTCTRLENV, 
 wxID_FRAME1LISTCTRLIMAGES, wxID_FRAME1LISTCTRLNODE, wxID_FRAME1LSTDIR, 
 wxID_FRAME1MEASUREFILEBROWSEBUTTON, wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1PANELDATAPOINT, 
 wxID_FRAME1PANELDATASTREAM, wxID_FRAME1PANELENV, wxID_FRAME1PANELNODE, 
 wxID_FRAME1PARAMETRI, wxID_FRAME1PNLCENTRALINA, wxID_FRAME1PNLSCPICONF, 
 wxID_FRAME1PNLTEMPDIR, wxID_FRAME1RBTCOMMA, wxID_FRAME1RBTPOINT, 
 wxID_FRAME1STATICBOX1, wxID_FRAME1STATICBOX2, wxID_FRAME1STATICBOX4, 
 wxID_FRAME1STATICBOX5, wxID_FRAME1STATICLINE1, wxID_FRAME1STATICLINE2, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT10, wxID_FRAME1STATICTEXT11, 
 wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT13, wxID_FRAME1STATICTEXT14, 
 wxID_FRAME1STATICTEXT15, wxID_FRAME1STATICTEXT16, wxID_FRAME1STATICTEXT17, 
 wxID_FRAME1STATICTEXT18, wxID_FRAME1STATICTEXT19, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT20, wxID_FRAME1STATICTEXT21, wxID_FRAME1STATICTEXT22, 
 wxID_FRAME1STATICTEXT23, wxID_FRAME1STATICTEXT24, wxID_FRAME1STATICTEXT25, 
 wxID_FRAME1STATICTEXT26, wxID_FRAME1STATICTEXT27, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, wxID_FRAME1STATICTEXT9, 
 wxID_FRAME1STATICTEXTMESSAGE, wxID_FRAME1TEXTCTRLCANTIERE, wxID_FRAME1TXTAVG, 
 wxID_FRAME1TXTCH, wxID_FRAME1TXTCONFHH, wxID_FRAME1TXTCONFMM, 
 wxID_FRAME1TXTCONFSAMPLES, wxID_FRAME1TXTCONFSS, wxID_FRAME1TXTCONST, 
 wxID_FRAME1TXTCTRLCENTRALINA, wxID_FRAME1TXTDEN, wxID_FRAME1TXTDSCODE, 
 wxID_FRAME1TXTDSLEN, wxID_FRAME1TXTDSTITLE, wxID_FRAME1TXTENVCOD, 
 wxID_FRAME1TXTENVLOCATION, wxID_FRAME1TXTENVNODE, wxID_FRAME1TXTENVTITLE, 
 wxID_FRAME1TXTFORMULA, wxID_FRAME1TXTHH, wxID_FRAME1TXTHHFROM, 
 wxID_FRAME1TXTIDEN, wxID_FRAME1TXTIP, wxID_FRAME1TXTLAMBDA, 
 wxID_FRAME1TXTMMFROM, wxID_FRAME1TXTMMTO, wxID_FRAME1TXTNODECODE, 
 wxID_FRAME1TXTNODEDATASTREAM, wxID_FRAME1TXTNODEIP, wxID_FRAME1TXTNODENAME, 
 wxID_FRAME1TXTNUMRANDOM, wxID_FRAME1TXTPERIH, wxID_FRAME1TXTPERIM, 
 wxID_FRAME1TXTPERIS, wxID_FRAME1TXTPORT1, wxID_FRAME1TXTPORT2, 
 wxID_FRAME1TXTPORTINPUT, wxID_FRAME1TXTPORTOUTPUT, wxID_FRAME1TXTSAMP, 
 wxID_FRAME1TXTSECOND, wxID_FRAME1TXTSSFROM, wxID_FRAME1TXTSSTO, 
 wxID_FRAME1TXTSTATUS, wxID_FRAME1WORKINGDIRBROWSEBUTTON, 
] = [wx.NewId() for _init_ctrls in range(134)]

class Frame1(wx.Frame):

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

    def _init_coll_listCtrlNode_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=u'Nome',
              width=95)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Codice', width=108)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading=u'Data',
              width=106)

    def _init_coll_listCtrlImages_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Filename', width=178)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading=u'Data',
              width=109)

    def _init_coll_listCtrl1_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Tabella', width=100)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_RIGHT,
              heading=u'Num. righe', width=90)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_CENTER,
              heading=u'Data', width=120)

    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=0, page=self.panelEnv, select=False,
              text=u'Environment')
        parent.AddPage(imageId=1, page=self.panelNode, select=True,
              text=u'Node')
        parent.AddPage(imageId=2, page=self.panelDatastream, select=False,
              text=u'Datastream')
        parent.AddPage(imageId=3, page=self.panelDatapoint, select=False,
              text=u'Datapoint')
        parent.AddPage(imageId=4, page=self.panel3, select=False,
              text=u'Image Mapping')

    def _init_coll_lstDir_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Directory', width=72)

    def _init_coll_listCtrlDatapoint_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=u'Nome',
              width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Updated', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading=u'Media',
              width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading=u'N\xb0 Campioni', width=-1)

    def _init_coll_listCtrlEnv_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=u'Nome',
              width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_RIGHT,
              heading=u'Codice', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_CENTER,
              heading=u'Data', width=-1)

    def _init_utils(self):
        # generated method, don't edit
        self.stockCursor1 = wx.StockCursor(id=wx.CURSOR_WAIT)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.listCtrl1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(189, 177), size=wx.Size(990, 541),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Import FBG')
        self._init_utils()
        self.SetClientSize(wx.Size(974, 503))
        self.SetMinSize(wx.Size(522, 481))
        self.SetMaxSize(wx.Size(1200, 800))

        self.pnlTempDir = wx.Panel(id=wxID_FRAME1PNLTEMPDIR, name=u'pnlTempDir',
              parent=self, pos=wx.Point(190, 80), size=wx.Size(440, 424),
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'Cartella di Import', name='staticBox1',
              parent=self.pnlTempDir, pos=wx.Point(8, 0), size=wx.Size(416, 80),
              style=0)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(190, 0), size=wx.Size(440, 80),
              style=wx.TAB_TRAVERSAL)

        self.measureFileBrowseButton = wx.lib.filebrowsebutton.FileBrowseButton(buttonText=u'Browse',
              dialogTitle=u'Choose a file', fileMask='*.*',
              id=wxID_FRAME1MEASUREFILEBROWSEBUTTON, initialValue='',
              labelText=u'File Misure:      ', parent=self.panel1,
              pos=wx.Point(16, 8), size=wx.Size(400, 56), startDirectory=u'.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')
        self.measureFileBrowseButton.SetName(u'measureFileBrowseButton')

        self.staticBox2 = wx.StaticBox(id=wxID_FRAME1STATICBOX2, label=u'Input',
              name='staticBox2', parent=self.panel1, pos=wx.Point(8, 1),
              size=wx.Size(416, 72), style=0)

        self.txtCtrlCentralina = wx.TextCtrl(id=wxID_FRAME1TXTCTRLCENTRALINA,
              name=u'txtCtrlCentralina', parent=self.pnlTempDir,
              pos=wx.Point(360, 88), size=wx.Size(56, 18), style=0,
              value=u'C1')
        self.txtCtrlCentralina.SetMaxLength(5)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'ID Centralina (max 5 car.)', name='staticText1',
              parent=self.pnlTempDir, pos=wx.Point(216, 88), size=wx.Size(126,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'ID Cantiere (max 5 car.)', name='staticText2',
              parent=self.pnlTempDir, pos=wx.Point(24, 88), size=wx.Size(118,
              13), style=0)

        self.textCtrlCantiere = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCANTIERE,
              name=u'textCtrlCantiere', parent=self.pnlTempDir,
              pos=wx.Point(152, 88), size=wx.Size(56, 18), style=0,
              value=u'GIBE3')
        self.textCtrlCantiere.SetMaxLength(5)

        self.btnImporta = wx.Button(id=wxID_FRAME1BTNIMPORTA, label=u'Importa',
              name=u'btnImporta', parent=self.pnlTempDir, pos=wx.Point(344,
              288), size=wx.Size(75, 23), style=0)
        self.btnImporta.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BTNIMPORTA)

        self.workingDirBrowseButton = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
              dialogTitle='', id=wxID_FRAME1WORKINGDIRBROWSEBUTTON,
              labelText=u'Cartella di lavoro:', newDirectory=False,
              parent=self.pnlTempDir, pos=wx.Point(16, 16), size=wx.Size(400,
              48), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Digita il percorso di una cartella o selezionala con il bottone')
        self.workingDirBrowseButton.SetLabel(u'Cartella di lavoro:')
        self.workingDirBrowseButton.SetValue(u'C:\\')
        self.workingDirBrowseButton.SetName(u'workingDirBrowseButton')
        self.workingDirBrowseButton.SetWindowVariant(wx.WINDOW_VARIANT_LARGE)

        self.databaseBrowseButton = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle=u'Choose a file', fileMask='*.*',
              id=wxID_FRAME1DATABASEBROWSEBUTTON, initialValue='',
              labelText=u'Scegli Database:', parent=self.pnlTempDir,
              pos=wx.Point(16, 112), size=wx.Size(400, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')
        self.databaseBrowseButton.SetName(u'databaseBrowseButton')
        self.databaseBrowseButton.SetWindowVariant(wx.WINDOW_VARIANT_LARGE)

        self.listCtrl1 = wx.ListCtrl(id=wxID_FRAME1LISTCTRL1, name='listCtrl1',
              parent=self.pnlTempDir, pos=wx.Point(72, 168), size=wx.Size(344,
              112), style=wx.LC_REPORT)
        self.listCtrl1.SetToolTipString(u'listCtrl1')
        self._init_coll_listCtrl1_Columns(self.listCtrl1)

        self.staticTextMessage = wx.StaticText(id=wxID_FRAME1STATICTEXTMESSAGE,
              label=u'Messaggi:', name=u'staticTextMessage',
              parent=self.pnlTempDir, pos=wx.Point(72, 288), size=wx.Size(256,
              32), style=0)
        self.staticTextMessage.SetMinSize(wx.Size(120, 60))

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self, pos=wx.Point(630, 0), size=wx.Size(344, 472),
              style=0)
        self.notebook1.Show(True)
        self.notebook1.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
              self.OnNotebook1NotebookPageChanged, id=wxID_FRAME1NOTEBOOK1)
        self.notebook1.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING,
              self.OnNotebook1NotebookPageChanging, id=wxID_FRAME1NOTEBOOK1)

        self.panelDatapoint = wx.Panel(id=wxID_FRAME1PANELDATAPOINT,
              name=u'panelDatapoint', parent=self.notebook1, pos=wx.Point(0, 0),
              size=wx.Size(336, 446), style=wx.TAB_TRAVERSAL)

        self.panelDatastream = wx.Panel(id=wxID_FRAME1PANELDATASTREAM,
              name=u'panelDatastream', parent=self.notebook1, pos=wx.Point(0,
              0), size=wx.Size(336, 446), style=wx.TAB_TRAVERSAL)

        self.panelNode = wx.Panel(id=wxID_FRAME1PANELNODE, name=u'panelNode',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(336, 446),
              style=wx.TAB_TRAVERSAL)

        self.panelEnv = wx.Panel(id=wxID_FRAME1PANELENV, name=u'panelEnv',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(336, 446),
              style=wx.TAB_TRAVERSAL)

        self.listCtrlEnv = wx.ListCtrl(id=wxID_FRAME1LISTCTRLENV,
              name=u'listCtrlEnv', parent=self.panelEnv, pos=wx.Point(8, 40),
              size=wx.Size(320, 152), style=wx.LC_REPORT)
        self._init_coll_listCtrlEnv_Columns(self.listCtrlEnv)
        self.listCtrlEnv.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlEnvListItemSelected, id=wxID_FRAME1LISTCTRLENV)

        self.listCtrlNode = wx.ListCtrl(id=wxID_FRAME1LISTCTRLNODE,
              name=u'listCtrlNode', parent=self.panelNode, pos=wx.Point(8, 40),
              size=wx.Size(320, 152), style=wx.LC_REPORT)
        self._init_coll_listCtrlNode_Columns(self.listCtrlNode)
        self.listCtrlNode.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlNodeListItemSelected, id=wxID_FRAME1LISTCTRLNODE)

        self.listCtrlDatastream = wx.ListCtrl(id=wxID_FRAME1LISTCTRLDATASTREAM,
              name=u'listCtrlDatastream', parent=self.panelDatastream,
              pos=wx.Point(8, 40), size=wx.Size(320, 152), style=wx.LC_REPORT)
        self._init_coll_listCtrlDatastream_Columns(self.listCtrlDatastream)
        self.listCtrlDatastream.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlDatastreamListItemSelected,
              id=wxID_FRAME1LISTCTRLDATASTREAM)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2', parent=self,
              pos=wx.Point(630, 472), size=wx.Size(344, 32),
              style=wx.TAB_TRAVERSAL)

        self.buttonSave = wx.Button(id=wxID_FRAME1BUTTONSAVE, label=u'Salva',
              name=u'buttonSave', parent=self.panel2, pos=wx.Point(64, 4),
              size=wx.Size(75, 23), style=0)
        self.buttonSave.Bind(wx.EVT_BUTTON, self.OnButtonSaveButton,
              id=wxID_FRAME1BUTTONSAVE)

        self.buttonDelete = wx.Button(id=wxID_FRAME1BUTTONDELETE,
              label=u'Elimina', name=u'buttonDelete', parent=self.panel2,
              pos=wx.Point(144, 4), size=wx.Size(75, 23), style=0)
        self.buttonDelete.Bind(wx.EVT_BUTTON, self.OnButtonDeleteButton,
              id=wxID_FRAME1BUTTONDELETE)

        self.txtEnvTitle = wx.TextCtrl(id=wxID_FRAME1TXTENVTITLE,
              name=u'txtEnvTitle', parent=self.panelEnv, pos=wx.Point(72, 216),
              size=wx.Size(152, 21), style=0, value=u'')
        self.txtEnvTitle.SetEditable(True)

        self.EnvNome = wx.StaticText(id=wxID_FRAME1ENVNOME, label=u'Nome',
              name=u'EnvNome', parent=self.panelEnv, pos=wx.Point(24, 216),
              size=wx.Size(28, 13), style=0)

        self.txtEnvCod = wx.TextCtrl(id=wxID_FRAME1TXTENVCOD, name=u'txtEnvCod',
              parent=self.panelEnv, pos=wx.Point(72, 240), size=wx.Size(152,
              21), style=0, value=u'')
        self.txtEnvCod.SetEditable(False)

        self.txtEnvLocation = wx.TextCtrl(id=wxID_FRAME1TXTENVLOCATION,
              name=u'txtEnvLocation', parent=self.panelEnv, pos=wx.Point(72,
              264), size=wx.Size(152, 21), style=0, value=u'')

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Codice', name='staticText3', parent=self.panelEnv,
              pos=wx.Point(24, 240), size=wx.Size(33, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Location', name='staticText4', parent=self.panelEnv,
              pos=wx.Point(24, 264), size=wx.Size(41, 13), style=0)

        self.txtEnvNode = wx.TextCtrl(id=wxID_FRAME1TXTENVNODE,
              name=u'txtEnvNode', parent=self.panelNode, pos=wx.Point(72, 8),
              size=wx.Size(108, 21), style=0, value=u'')
        self.txtEnvNode.SetEditable(False)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'Env. Code', name='staticText5', parent=self.panelNode,
              pos=wx.Point(8, 8), size=wx.Size(51, 13), style=0)

        self.txtNodeName = wx.TextCtrl(id=wxID_FRAME1TXTNODENAME,
              name=u'txtNodeName', parent=self.panelNode, pos=wx.Point(72, 216),
              size=wx.Size(152, 21), style=0, value=u'')
        self.txtNodeName.SetEditable(True)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Nome', name='staticText6', parent=self.panelNode,
              pos=wx.Point(24, 216), size=wx.Size(28, 13), style=0)

        self.txtNodeCode = wx.TextCtrl(id=wxID_FRAME1TXTNODECODE,
              name=u'txtNodeCode', parent=self.panelNode, pos=wx.Point(72, 240),
              size=wx.Size(152, 21), style=0, value=u'')
        self.txtNodeCode.SetEditable(False)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'Codice', name='staticText7', parent=self.panelNode,
              pos=wx.Point(24, 240), size=wx.Size(33, 13), style=0)

        self.txtNodeDatastream = wx.TextCtrl(id=wxID_FRAME1TXTNODEDATASTREAM,
              name=u'txtNodeDatastream', parent=self.panelDatastream,
              pos=wx.Point(72, 8), size=wx.Size(108, 21), style=0, value=u'')
        self.txtNodeDatastream.SetEditable(False)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label=u'Node. Code', name='staticText8',
              parent=self.panelDatastream, pos=wx.Point(8, 8), size=wx.Size(58,
              13), style=0)

        self.txtDsCode = wx.TextCtrl(id=wxID_FRAME1TXTDSCODE, name=u'txtDsCode',
              parent=self.panelDatastream, pos=wx.Point(48, 200),
              size=wx.Size(160, 21), style=0, value=u'')
        self.txtDsCode.SetEditable(False)

        self.txtDsLen = wx.TextCtrl(id=wxID_FRAME1TXTDSLEN, name=u'txtDsLen',
              parent=self.panelDatastream, pos=wx.Point(272, 200),
              size=wx.Size(56, 21), style=0, value=u'')
        self.txtDsLen.SetEditable(False)

        self.txtDsTitle = wx.TextCtrl(id=wxID_FRAME1TXTDSTITLE,
              name=u'txtDsTitle', parent=self.panelDatastream, pos=wx.Point(56,
              256), size=wx.Size(240, 21), style=0, value=u'')
        self.txtDsTitle.SetEditable(True)

        self.txtFormula = wx.TextCtrl(id=wxID_FRAME1TXTFORMULA,
              name=u'txtFormula', parent=self.panelDatastream, pos=wx.Point(88,
              304), size=wx.Size(200, 21), style=0, value=u'')

        self.txtLambda = wx.TextCtrl(id=wxID_FRAME1TXTLAMBDA, name=u'txtLambda',
              parent=self.panelDatastream, pos=wx.Point(24, 350),
              size=wx.Size(80, 21), style=0, value=u'')
        self.txtLambda.SetEditable(True)

        self.txtConst = wx.TextCtrl(id=wxID_FRAME1TXTCONST, name=u'txtConst',
              parent=self.panelDatastream, pos=wx.Point(107, 350),
              size=wx.Size(64, 21), style=0, value=u'')
        self.txtConst.SetEditable(True)

        self.txtDen = wx.TextCtrl(id=wxID_FRAME1TXTDEN, name=u'txtDen',
              parent=self.panelDatastream, pos=wx.Point(174, 350),
              size=wx.Size(64, 21), style=0, value=u'')
        self.txtDen.SetEditable(True)

        self.txtSecond = wx.TextCtrl(id=wxID_FRAME1TXTSECOND, name=u'txtSecond',
              parent=self.panelDatastream, pos=wx.Point(242, 350),
              size=wx.Size(64, 21), style=0, value=u'')
        self.txtSecond.SetEditable(True)

        self.staticText22 = wx.StaticText(id=wxID_FRAME1STATICTEXT22,
              label=u'Ordine 2', name='staticText22',
              parent=self.panelDatastream, pos=wx.Point(248, 334),
              size=wx.Size(42, 13), style=0)

        self.staticText23 = wx.StaticText(id=wxID_FRAME1STATICTEXT23,
              label=u'Formula', name='staticText23',
              parent=self.panelDatastream, pos=wx.Point(32, 307),
              size=wx.Size(39, 13), style=0)

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label=u'Nome', name='staticText11', parent=self.panelDatastream,
              pos=wx.Point(16, 256), size=wx.Size(28, 13), style=0)

        self.Parametri = wx.StaticBox(id=wxID_FRAME1PARAMETRI,
              label=u'Parametri', name=u'Parametri',
              parent=self.panelDatastream, pos=wx.Point(16, 280),
              size=wx.Size(304, 96), style=0)

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
              label=u'Ordine 0', name='staticText9',
              parent=self.panelDatastream, pos=wx.Point(120, 334),
              size=wx.Size(42, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label=u'CWL', name='staticText10', parent=self.panelDatastream,
              pos=wx.Point(40, 334), size=wx.Size(23, 13), style=0)

        self.staticText12 = wx.StaticText(id=wxID_FRAME1STATICTEXT12,
              label=u'Ordine 1', name='staticText12',
              parent=self.panelDatastream, pos=wx.Point(184, 334),
              size=wx.Size(42, 13), style=0)

        self.staticText13 = wx.StaticText(id=wxID_FRAME1STATICTEXT13,
              label=u'Lunghezza', name='staticText13',
              parent=self.panelDatastream, pos=wx.Point(216, 200),
              size=wx.Size(52, 13), style=0)

        self.imgChart = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_FRAME1IMGCHART, name=u'imgChart',
              parent=self.panelDatapoint, pos=wx.Point(8, 232),
              size=wx.Size(320, 176), style=0)
        self.imgChart.SetMaxSize(wx.Size(320, 240))
        self.imgChart.Bind(wx.EVT_LEFT_DCLICK, self.OnImgChartLeftDclick)

        self.listCtrlDatapoint = wx.ListCtrl(id=wxID_FRAME1LISTCTRLDATAPOINT,
              name=u'listCtrlDatapoint', parent=self.panelDatapoint,
              pos=wx.Point(8, 32), size=wx.Size(320, 155), style=wx.LC_REPORT)
        self._init_coll_listCtrlDatapoint_Columns(self.listCtrlDatapoint)
        self.listCtrlDatapoint.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlDatapointListItemSelected,
              id=wxID_FRAME1LISTCTRLDATAPOINT)
        self.listCtrlDatapoint.Bind(wx.EVT_LEFT_DCLICK,
              self.OnListCtrlDatapointLeftDclick)

        self.txtAvg = wx.TextCtrl(id=wxID_FRAME1TXTAVG, name=u'txtAvg',
              parent=self.panelDatapoint, pos=wx.Point(77, 198),
              size=wx.Size(128, 21), style=0, value=u'')
        self.txtAvg.SetEditable(False)

        self.staticText14 = wx.StaticText(id=wxID_FRAME1STATICTEXT14,
              label=u'Valore Medio', name='staticText14',
              parent=self.panelDatapoint, pos=wx.Point(12, 200),
              size=wx.Size(62, 13), style=0)

        self.staticText15 = wx.StaticText(id=wxID_FRAME1STATICTEXT15,
              label=u'Codice', name='staticText15', parent=self.panelDatastream,
              pos=wx.Point(11, 200), size=wx.Size(33, 13), style=0)

        self.btnExport = wx.Button(id=wxID_FRAME1BTNEXPORT, label=u'export',
              name=u'btnExport', parent=self.panelDatastream, pos=wx.Point(280,
              415), size=wx.Size(48, 25), style=0)
        self.btnExport.Bind(wx.EVT_BUTTON, self.OnBtnExportButton,
              id=wxID_FRAME1BTNEXPORT)

        self.dtFrom = wx.DatePickerCtrl(id=wxID_FRAME1DTFROM, name=u'dtFrom',
              parent=self.panelDatastream, pos=wx.Point(24, 384),
              size=wx.Size(88, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dtFrom.SetToolTipString(u'dtFrom')
        self.dtFrom.SetValue(wx.DateTimeFromDMY(1, 9, 2012, 0, 0, 0))
        self.dtFrom.SetLabel(u'01/10/2012')

        self.txtHHFrom = wx.TextCtrl(id=wxID_FRAME1TXTHHFROM, name=u'txtHHFrom',
              parent=self.panelDatastream, pos=wx.Point(24, 408),
              size=wx.Size(20, 21), style=0, value=u'00')
        self.txtHHFrom.SetMaxLength(2)
        self.txtHHFrom.SetHelpText(u'')

        self.txtMMFrom = wx.TextCtrl(id=wxID_FRAME1TXTMMFROM, name=u'txtMMFrom',
              parent=self.panelDatastream, pos=wx.Point(51, 408),
              size=wx.Size(20, 21), style=0, value=u'00')
        self.txtMMFrom.SetMaxLength(2)
        self.txtMMFrom.SetHelpText(u'')

        self.txtSSFrom = wx.TextCtrl(id=wxID_FRAME1TXTSSFROM, name=u'txtSSFrom',
              parent=self.panelDatastream, pos=wx.Point(76, 408),
              size=wx.Size(20, 21), style=0, value=u'00')
        self.txtSSFrom.SetMaxLength(2)
        self.txtSSFrom.SetHelpText(u'')

        self.dtTo = wx.DatePickerCtrl(id=wxID_FRAME1DTTO, name=u'dtTo',
              parent=self.panelDatastream, pos=wx.Point(128, 384),
              size=wx.Size(80, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dtTo.SetToolTipString(u'dtTo')
        self.dtTo.SetValue(wx.DateTimeFromDMY(26, 9, 2012, 18, 25, 32))
        self.dtTo.SetLabel(u'26/10/2012')

        self.txtHH = wx.TextCtrl(id=wxID_FRAME1TXTHH, name=u'txtHH',
              parent=self.panelDatastream, pos=wx.Point(128, 408),
              size=wx.Size(20, 21), style=0, value=u'23')
        self.txtHH.SetMaxLength(2)
        self.txtHH.SetHelpText(u'')

        self.txtMMTo = wx.TextCtrl(id=wxID_FRAME1TXTMMTO, name=u'txtMMTo',
              parent=self.panelDatastream, pos=wx.Point(155, 408),
              size=wx.Size(20, 21), style=0, value=u'59')
        self.txtMMTo.SetMaxLength(2)
        self.txtMMTo.SetHelpText(u'')

        self.txtSSTo = wx.TextCtrl(id=wxID_FRAME1TXTSSTO, name=u'txtSSTo',
              parent=self.panelDatastream, pos=wx.Point(180, 408),
              size=wx.Size(20, 21), style=0, value=u'59')
        self.txtSSTo.SetMaxLength(2)
        self.txtSSTo.SetHelpText(u'')

        self.btnClose = wx.Button(id=wxID_FRAME1BTNCLOSE, label=u'Chiudi',
              name=u'btnClose', parent=self.panel2, pos=wx.Point(120, -40),
              size=wx.Size(75, 23), style=0)
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRAME1BTNCLOSE)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(336, 446),
              style=wx.TAB_TRAVERSAL)

        self.fileBrowseButton1 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle=u'Choose a file', fileMask=u'*.png',
              id=wxID_FRAME1FILEBROWSEBUTTON1, initialValue='',
              labelText=u'Image:', parent=self.panel3, pos=wx.Point(24, 8),
              size=wx.Size(296, 48), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')
        self.fileBrowseButton1.SetLabel(u'Image:')
        self.fileBrowseButton1.SetValue(u'')

        self.imgMap = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_FRAME1IMGMAP, name=u'imgMap', parent=self.panel3,
              pos=wx.Point(32, 215), size=wx.Size(280, 210), style=0)
        self.imgMap.Bind(wx.EVT_LEFT_DCLICK, self.OnImgMapLeftDclick)

        self.listCtrlImages = wx.ListCtrl(id=wxID_FRAME1LISTCTRLIMAGES,
              name=u'listCtrlImages', parent=self.panel3, pos=wx.Point(24, 90),
              size=wx.Size(296, 120), style=wx.LC_REPORT)
        self._init_coll_listCtrlImages_Columns(self.listCtrlImages)
        self.listCtrlImages.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrlImagesListItemSelected,
              id=wxID_FRAME1LISTCTRLIMAGES)
        self.listCtrlImages.Bind(wx.EVT_LEFT_DCLICK,
              self.OnListCtrlImagesLeftDclick)

        self.dateFrom = wx.DatePickerCtrl(id=wxID_FRAME1DATEFROM,
              name=u'dateFrom', parent=self.panelDatapoint, pos=wx.Point(94, 6),
              size=wx.Size(88, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dateFrom.SetToolTipString(u'dtFrom')
        self.dateFrom.SetValue(wx.DateTimeFromDMY(1, 0, 2012, 0, 0, 0))
        self.dateFrom.SetLabel(u'01/01/2012')
        self.dateFrom.Bind(wx.EVT_DATE_CHANGED, self.OnDateFromDateChanged,
              id=wxID_FRAME1DATEFROM)

        self.dateTo = wx.DatePickerCtrl(id=wxID_FRAME1DATETO, name=u'dateTo',
              parent=self.panelDatapoint, pos=wx.Point(190, 6), size=wx.Size(80,
              21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dateTo.SetToolTipString(u'dtTo')
        self.dateTo.SetValue(wx.DateTimeFromDMY(26, 9, 2012, 18, 25, 32))
        self.dateTo.SetLabel(u'26/10/2012')
        self.dateTo.Bind(wx.EVT_DATE_CHANGED, self.OnDateToDateChanged,
              id=wxID_FRAME1DATETO)

        self.chkDataFilter = wx.CheckBox(id=wxID_FRAME1CHKDATAFILTER,
              label=u'Filtro Data', name=u'chkDataFilter',
              parent=self.panelDatapoint, pos=wx.Point(16, 6), size=wx.Size(70,
              13), style=0)
        self.chkDataFilter.SetValue(True)
        self.chkDataFilter.Bind(wx.EVT_CHECKBOX, self.OnChkDataFilterCheckbox,
              id=wxID_FRAME1CHKDATAFILTER)

        self.staticBox4 = wx.StaticBox(id=wxID_FRAME1STATICBOX4,
              label=u'Cancellazione alla data di importazione',
              name='staticBox4', parent=self.pnlTempDir, pos=wx.Point(72, 328),
              size=wx.Size(336, 80), style=0)

        self.datePickerCtrl1 = wx.DatePickerCtrl(id=wxID_FRAME1DATEPICKERCTRL1,
              name='datePickerCtrl1', parent=self.pnlTempDir, pos=wx.Point(110,
              348), size=wx.Size(88, 21),
              style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datePickerCtrl1.SetToolTipString(u'dtFrom')
        self.datePickerCtrl1.SetValue(wx.DateTimeFromDMY(1, 0, 2012, 0, 0, 0))
        self.datePickerCtrl1.SetLabel(u'01/01/2012')
        self.datePickerCtrl1.Bind(wx.EVT_DATE_CHANGED,
              self.OnDatePickerCtrl1DateChanged, id=wxID_FRAME1DATEPICKERCTRL1)

        self.datePickerCtrl2 = wx.DatePickerCtrl(id=wxID_FRAME1DATEPICKERCTRL2,
              name='datePickerCtrl2', parent=self.pnlTempDir, pos=wx.Point(110,
              372), size=wx.Size(88, 21),
              style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datePickerCtrl2.SetToolTipString(u'dtTo')
        self.datePickerCtrl2.SetValue(wx.DateTimeFromDMY(26, 9, 2012, 18, 25,
              32))
        self.datePickerCtrl2.SetLabel(u'26/10/2012')
        self.datePickerCtrl2.Bind(wx.EVT_DATE_CHANGED,
              self.OnDatePickerCtrl2DateChanged, id=wxID_FRAME1DATEPICKERCTRL2)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME1CHECKBOX1,
              label=u'Datastream', name='checkBox1', parent=self.pnlTempDir,
              pos=wx.Point(318, 352), size=wx.Size(88, 13), style=0)
        self.checkBox1.SetValue(False)
        self.checkBox1.SetToolTipString(u'checkBox1')
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME1CHECKBOX1)

        self.checkBox2 = wx.CheckBox(id=wxID_FRAME1CHECKBOX2,
              label=u'Datapoint', name='checkBox2', parent=self.pnlTempDir,
              pos=wx.Point(318, 376), size=wx.Size(88, 13), style=0)
        self.checkBox2.SetValue(False)
        self.checkBox2.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2Checkbox,
              id=wxID_FRAME1CHECKBOX2)

        self.btnDeleteAdmin = wx.Button(id=wxID_FRAME1BTNDELETEADMIN,
              label=u'Elimina', name=u'btnDeleteAdmin', parent=self.pnlTempDir,
              pos=wx.Point(216, 357), size=wx.Size(78, 32), style=0)
        self.btnDeleteAdmin.Bind(wx.EVT_BUTTON, self.OnBtnDeleteAdminButton,
              id=wxID_FRAME1BTNDELETEADMIN)

        self.staticText16 = wx.StaticText(id=wxID_FRAME1STATICTEXT16,
              label=u'da', name='staticText16', parent=self.pnlTempDir,
              pos=wx.Point(94, 352), size=wx.Size(13, 13), style=0)

        self.staticText17 = wx.StaticText(id=wxID_FRAME1STATICTEXT17,
              label=u'a', name='staticText17', parent=self.pnlTempDir,
              pos=wx.Point(100, 376), size=wx.Size(7, 13), style=0)

        self.chkFormat = wx.Choice(choices=['gg/mm/aaaa', 'mm/gg/aaaa',
              'aaaa-mm-gg'], id=wxID_FRAME1CHKFORMAT, name=u'chkFormat',
              parent=self.panelDatastream, pos=wx.Point(222, 384),
              size=wx.Size(106, 21), style=0)
        self.chkFormat.SetSelection(0)

        self.rbtComma = wx.RadioButton(id=wxID_FRAME1RBTCOMMA, label=u',',
              name=u'rbtComma', parent=self.panelDatastream, pos=wx.Point(250,
              408), size=wx.Size(20, 13), style=0)
        self.rbtComma.SetValue(True)

        self.rbtPoint = wx.RadioButton(id=wxID_FRAME1RBTPOINT, label=u'.',
              name=u'rbtPoint', parent=self.panelDatastream, pos=wx.Point(250,
              424), size=wx.Size(20, 13), style=0)
        self.rbtPoint.SetValue(False)

        self.staticText18 = wx.StaticText(id=wxID_FRAME1STATICTEXT18,
              label=u'sep.', name='staticText18', parent=self.panelDatastream,
              pos=wx.Point(225, 408), size=wx.Size(22, 13), style=0)

        self.staticText19 = wx.StaticText(id=wxID_FRAME1STATICTEXT19,
              label=u'sep.', name='staticText19', parent=self.panelDatastream,
              pos=wx.Point(225, 423), size=wx.Size(22, 13), style=0)

        self.pnlCentralina = wx.Panel(id=wxID_FRAME1PNLCENTRALINA,
              name=u'pnlCentralina', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(190, 506), style=wx.TAB_TRAVERSAL)

        self.staticBox5 = wx.StaticBox(id=wxID_FRAME1STATICBOX5,
              label=u'Centralina', name='staticBox5', parent=self.pnlCentralina,
              pos=wx.Point(-5, 0), size=wx.Size(186, 496), style=0)

        self.txtIP = wx.TextCtrl(id=wxID_FRAME1TXTIP, name=u'txtIP',
              parent=self.pnlCentralina, pos=wx.Point(10, 24), size=wx.Size(88,
              21), style=0, value=u'10.0.0.10')

        self.txtPort1 = wx.TextCtrl(id=wxID_FRAME1TXTPORT1, name=u'txtPort1',
              parent=self.pnlCentralina, pos=wx.Point(101, 24), size=wx.Size(36,
              21), style=0, value=u'3500')

        self.txtport2 = wx.TextCtrl(id=wxID_FRAME1TXTPORT2, name=u'txtport2',
              parent=self.pnlCentralina, pos=wx.Point(140, 24), size=wx.Size(36,
              21), style=0, value=u'3365')

        self.btnTest = wx.Button(id=wxID_FRAME1BTNTEST, label=u'Stato?',
              name=u'btnTest', parent=self.pnlCentralina, pos=wx.Point(10, 48),
              size=wx.Size(64, 23), style=0)
        self.btnTest.Bind(wx.EVT_BUTTON, self.OnBtnTestButton,
              id=wxID_FRAME1BTNTEST)

        self.txtStatus = wx.TextCtrl(id=wxID_FRAME1TXTSTATUS, name=u'txtStatus',
              parent=self.pnlCentralina, pos=wx.Point(75, 48), size=wx.Size(106,
              21), style=0, value=u'')
        self.txtStatus.SetEditable(False)
        self.txtStatus.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.btnLista = wx.Button(id=wxID_FRAME1BTNLISTA, label=u'Lista Dir.',
              name=u'btnLista', parent=self.pnlCentralina, pos=wx.Point(10,
              236), size=wx.Size(56, 23), style=0)
        self.btnLista.Enable(False)
        self.btnLista.Bind(wx.EVT_BUTTON, self.OnBtnListaButton,
              id=wxID_FRAME1BTNLISTA)

        self.lstDir = wx.ListCtrl(id=wxID_FRAME1LSTDIR, name=u'lstDir',
              parent=self.pnlCentralina, pos=wx.Point(71, 236),
              size=wx.Size(104, 204), style=wx.LC_REPORT)
        self.lstDir.Enable(False)
        self._init_coll_lstDir_Columns(self.lstDir)
        self.lstDir.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnLstDirListItemSelected, id=wxID_FRAME1LSTDIR)

        self.txtIDEN = wx.TextCtrl(id=wxID_FRAME1TXTIDEN, name=u'txtIDEN',
              parent=self.pnlCentralina, pos=wx.Point(10, 74), size=wx.Size(170,
              21), style=0, value=u'')
        self.txtIDEN.SetEditable(False)
        self.txtIDEN.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.txtPERIH = wx.TextCtrl(id=wxID_FRAME1TXTPERIH, name=u'txtPERIH',
              parent=self.pnlCentralina, pos=wx.Point(83, 97), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtPERIH.SetEditable(True)
        self.txtPERIH.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIH.SetMaxLength(2)
        self.txtPERIH.Enable(False)

        self.txtPERIM = wx.TextCtrl(id=wxID_FRAME1TXTPERIM, name=u'txtPERIM',
              parent=self.pnlCentralina, pos=wx.Point(115, 97), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtPERIM.SetEditable(True)
        self.txtPERIM.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIM.SetMaxLength(2)
        self.txtPERIM.Enable(False)

        self.txtPERIS = wx.TextCtrl(id=wxID_FRAME1TXTPERIS, name=u'txtPERIS',
              parent=self.pnlCentralina, pos=wx.Point(147, 97), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtPERIS.SetEditable(True)
        self.txtPERIS.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIS.SetMaxLength(2)
        self.txtPERIS.Enable(False)

        self.staticText20 = wx.StaticText(id=wxID_FRAME1STATICTEXT20,
              label=u'Periodo H:M:S', name='staticText20',
              parent=self.pnlCentralina, pos=wx.Point(10, 104), size=wx.Size(69,
              13), style=0)

        self.txtSAMP = wx.TextCtrl(id=wxID_FRAME1TXTSAMP, name=u'txtSAMP',
              parent=self.pnlCentralina, pos=wx.Point(83, 123), size=wx.Size(61,
              21), style=0, value=u'')
        self.txtSAMP.SetEditable(True)
        self.txtSAMP.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtSAMP.SetMaxLength(4)
        self.txtSAMP.Enable(False)

        self.staticText21 = wx.StaticText(id=wxID_FRAME1STATICTEXT21,
              label=u'N\xb0 Campioni', name='staticText21',
              parent=self.pnlCentralina, pos=wx.Point(10, 128), size=wx.Size(59,
              13), style=0)

        self.btnSavePERI_SAM = wx.Button(id=wxID_FRAME1BTNSAVEPERI_SAM,
              label=u'Imposta Periodo e N\xb0 Campioni',
              name=u'btnSavePERI_SAM', parent=self.pnlCentralina,
              pos=wx.Point(8, 152), size=wx.Size(168, 23), style=0)
        self.btnSavePERI_SAM.Enable(False)
        self.btnSavePERI_SAM.Bind(wx.EVT_BUTTON, self.OnBtnSavePERI_SAMButton,
              id=wxID_FRAME1BTNSAVEPERI_SAM)

        self.btnACQUSTART = wx.Button(id=wxID_FRAME1BTNACQUSTART,
              label=u'Avvia Sched.', name=u'btnACQUSTART',
              parent=self.pnlCentralina, pos=wx.Point(10, 179),
              size=wx.Size(168, 23), style=0)
        self.btnACQUSTART.Enable(False)
        self.btnACQUSTART.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnACQUSTART.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnACQUSTART.Bind(wx.EVT_BUTTON, self.OnBtnACQUSTARTButton,
              id=wxID_FRAME1BTNACQUSTART)

        self.btnACQUSTOP = wx.Button(id=wxID_FRAME1BTNACQUSTOP,
              label=u'Ferma Acquisizione', name=u'btnACQUSTOP',
              parent=self.pnlCentralina, pos=wx.Point(10, 206),
              size=wx.Size(168, 23), style=0)
        self.btnACQUSTOP.Enable(False)
        self.btnACQUSTOP.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnACQUSTOP.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnACQUSTOP.Bind(wx.EVT_BUTTON, self.OnBtnACQUSTOPButton,
              id=wxID_FRAME1BTNACQUSTOP)

        self.btnImportSCHE = wx.Button(id=wxID_FRAME1BTNIMPORTSCHE,
              label=u'Importa', name=u'btnImportSCHE',
              parent=self.pnlCentralina, pos=wx.Point(10, 261), size=wx.Size(56,
              23), style=0)
        self.btnImportSCHE.Enable(False)
        self.btnImportSCHE.Bind(wx.EVT_BUTTON, self.OnBtnImportSCHEButton,
              id=wxID_FRAME1BTNIMPORTSCHE)

        self.btnExportFile = wx.Button(id=wxID_FRAME1BTNEXPORTFILE,
              label=u'Exp. File', name=u'btnExportFile',
              parent=self.pnlCentralina, pos=wx.Point(10, 286), size=wx.Size(56,
              23), style=0)
        self.btnExportFile.Enable(False)
        self.btnExportFile.Bind(wx.EVT_BUTTON, self.OnBtnExportFileButton,
              id=wxID_FRAME1BTNEXPORTFILE)

        self.btnCanellaTutto = wx.Button(id=wxID_FRAME1BTNCANELLATUTTO,
              label=u'Cancella Memoria', name=u'btnCanellaTutto',
              parent=self.pnlCentralina, pos=wx.Point(10, 444),
              size=wx.Size(158, 23), style=0)
        self.btnCanellaTutto.Enable(False)
        self.btnCanellaTutto.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.btnCanellaTutto.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnCanellaTutto.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnCanellaTutto.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.btnCanellaTutto.Bind(wx.EVT_BUTTON, self.OnBtnCanellaTuttoButton,
              id=wxID_FRAME1BTNCANELLATUTTO)

        self.txtNodeIp = wx.TextCtrl(id=wxID_FRAME1TXTNODEIP, name=u'txtNodeIp',
              parent=self.panelNode, pos=wx.Point(10, 276), size=wx.Size(94,
              21), style=0, value=u'')

        self.txtPortInput = wx.TextCtrl(id=wxID_FRAME1TXTPORTINPUT,
              name=u'txtPortInput', parent=self.panelNode, pos=wx.Point(108,
              276), size=wx.Size(36, 21), style=0, value=u'')

        self.txtPortOutput = wx.TextCtrl(id=wxID_FRAME1TXTPORTOUTPUT,
              name=u'txtPortOutput', parent=self.panelNode, pos=wx.Point(154,
              276), size=wx.Size(36, 21), style=0, value=u'')

        self.pnlScpiConf = wx.Panel(id=wxID_FRAME1PNLSCPICONF,
              name=u'pnlScpiConf', parent=self.panelNode, pos=wx.Point(8, 304),
              size=wx.Size(304, 64), style=wx.TAB_TRAVERSAL)

        self.staticText25 = wx.StaticText(id=wxID_FRAME1STATICTEXT25,
              label=u'Periodo H:M:S', name='staticText25',
              parent=self.pnlScpiConf, pos=wx.Point(10, 5), size=wx.Size(69,
              13), style=0)

        self.txtConfHH = wx.TextCtrl(id=wxID_FRAME1TXTCONFHH, name=u'txtConfHH',
              parent=self.pnlScpiConf, pos=wx.Point(83, 5), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtConfHH.SetEditable(True)
        self.txtConfHH.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtConfHH.SetMaxLength(2)
        self.txtConfHH.Enable(True)

        self.txtConfMM = wx.TextCtrl(id=wxID_FRAME1TXTCONFMM, name=u'txtConfMM',
              parent=self.pnlScpiConf, pos=wx.Point(115, 5), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtConfMM.SetEditable(True)
        self.txtConfMM.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtConfMM.SetMaxLength(2)
        self.txtConfMM.Enable(True)

        self.txtConfSS = wx.TextCtrl(id=wxID_FRAME1TXTCONFSS, name=u'txtConfSS',
              parent=self.pnlScpiConf, pos=wx.Point(147, 5), size=wx.Size(29,
              21), style=0, value=u'')
        self.txtConfSS.SetEditable(True)
        self.txtConfSS.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtConfSS.SetMaxLength(2)
        self.txtConfSS.Enable(True)

        self.staticText24 = wx.StaticText(id=wxID_FRAME1STATICTEXT24,
              label=u'N\xb0 Campioni', name='staticText24',
              parent=self.pnlScpiConf, pos=wx.Point(10, 36), size=wx.Size(59,
              13), style=0)

        self.txtConfSamples = wx.TextCtrl(id=wxID_FRAME1TXTCONFSAMPLES,
              name=u'txtConfSamples', parent=self.pnlScpiConf, pos=wx.Point(83,
              36), size=wx.Size(61, 21), style=0, value=u'')
        self.txtConfSamples.SetEditable(True)
        self.txtConfSamples.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtConfSamples.SetMaxLength(4)
        self.txtConfSamples.Enable(True)

        self.btnIPAD = wx.Button(id=wxID_FRAME1BTNIPAD,
              label=u'Imposta indirizzo IP', name=u'btnIPAD',
              parent=self.pnlCentralina, pos=wx.Point(10, 472),
              size=wx.Size(158, 23), style=0)
        self.btnIPAD.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.btnIPAD.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnIPAD.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'Tahoma'))
        self.btnIPAD.Enable(False)
        self.btnIPAD.Bind(wx.EVT_BUTTON, self.OnBtnIPADButton,
              id=wxID_FRAME1BTNIPAD)

        self.chkByNode = wx.CheckBox(id=wxID_FRAME1CHKBYNODE,
              label=u'Filtra per Node', name=u'chkByNode', parent=self.panel3,
              pos=wx.Point(24, 64), size=wx.Size(96, 13), style=0)
        self.chkByNode.SetValue(False)
        self.chkByNode.Bind(wx.EVT_CHECKBOX, self.OnChkByNodeCheckbox,
              id=wxID_FRAME1CHKBYNODE)

        self.btnUpdateCode = wx.Button(id=wxID_FRAME1BTNUPDATECODE,
              label=u'Aggiorna', name=u'btnUpdateCode',
              parent=self.panelDatastream, pos=wx.Point(48, 222),
              size=wx.Size(72, 23), style=0)
        self.btnUpdateCode.Bind(wx.EVT_BUTTON, self.OnBtnUpdateCodeButton,
              id=wxID_FRAME1BTNUPDATECODE)

        self.chkAllDs = wx.CheckBox(id=wxID_FRAME1CHKALLDS,
              label=u'applica a tutto', name=u'chkAllDs',
              parent=self.panelDatastream, pos=wx.Point(128, 224),
              size=wx.Size(80, 16), style=0)
        self.chkAllDs.SetValue(False)
        self.chkAllDs.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'MS Shell Dlg 2'))
        self.chkAllDs.Bind(wx.EVT_CHECKBOX, self.OnChkAllDsCheckbox,
              id=wxID_FRAME1CHKALLDS)

        self.staticLine1 = wx.StaticLine(id=wxID_FRAME1STATICLINE1,
              name='staticLine1', parent=self.panelDatastream, pos=wx.Point(17,
              250), size=wx.Size(303, 1), style=0)

        self.txtCh = wx.TextCtrl(id=wxID_FRAME1TXTCH, name=u'txtCh',
              parent=self.panelDatastream, pos=wx.Point(272, 224),
              size=wx.Size(56, 21), style=0, value=u'')
        self.txtCh.SetEditable(False)

        self.staticText26 = wx.StaticText(id=wxID_FRAME1STATICTEXT26,
              label=u'Canale', name='staticText26', parent=self.panelDatastream,
              pos=wx.Point(232, 224), size=wx.Size(34, 16), style=0)

        self.btnRandomGen = wx.Button(id=wxID_FRAME1BTNRANDOMGEN,
              label=u'Genera Random', name=u'btnRandomGen',
              parent=self.panelNode, pos=wx.Point(16, 408), size=wx.Size(96,
              23), style=0)
        self.btnRandomGen.Bind(wx.EVT_BUTTON, self.OnBtnRandomGenButton,
              id=wxID_FRAME1BTNRANDOMGEN)

        self.staticLine2 = wx.StaticLine(id=wxID_FRAME1STATICLINE2,
              name='staticLine2', parent=self.panelNode, pos=wx.Point(9, 392),
              size=wx.Size(311, 2), style=0)

        self.txtNumRandom = wx.TextCtrl(id=wxID_FRAME1TXTNUMRANDOM,
              name=u'txtNumRandom', parent=self.panelNode, pos=wx.Point(120,
              408), size=wx.Size(56, 21), style=0, value=u'')

        self.staticText27 = wx.StaticText(id=wxID_FRAME1STATICTEXT27,
              label=u'...n\xb0 totale di campioni', name='staticText27',
              parent=self.panelNode, pos=wx.Point(184, 413), size=wx.Size(109,
              13), style=0)

        self._init_coll_notebook1_Pages(self.notebook1)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.selected_entity = 1
        self.selected_entity_id = 0
        self.databaseBrowseButton.changeCallback = self.dbCallback
        self.workingDirBrowseButton.changeCallback = self.WorkingDirCallback
        self.fileBrowseButton1.changeCallback = self.imgCallback 
        if not os.path.exists(settings.gibedatafolder_path ):
            os.mkdir(settings.gibedatafolder_path )
            os.mkdir(settings.gibedatafolder_path + settings.environment_name)
            os.mkdir(settings.gibedatafolder_path + settings.environment_name+ "\\db")
        if not os.path.exists(settings.gibeimportfolder_path ):
            os.mkdir(settings.gibeimportfolder_path )
        self.logger = logging.getLogger("NrsWXAppLog")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(settings.gibelogfile_path)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("NrsWXApp Started on %s" % settings.gibeimportfolder_path)
        self.logger.info("NrsWXApp Database: %s" % settings.database)
        self.logger.info("NrsWXApp Working Folder: %s" %settings.gibeimportfolder_path)
        self.workingDirBrowseButton.SetValue(settings.gibedatafolder_path)    
        self.txtCtrlCentralina.SetValue(settings.first_node);
        self.textCtrlCantiere.SetValue(settings.environment_name)
        self.LoadEnvDirs()
        self.databaseBrowseButton.SetValue(settings.database)
        self.CheckDB()
        self.SelectDefaultItems()
        self.logger.info("NrsWXApp Init terminated")
    
    def setMyCursor(self, cur):
        self.SetCursor(cur)
    
    def OnButton1Button(self, event):
        self.logger.info("starting import")
        mycur = self.GetCursor();        
        self.staticTextMessage.SetLabel("Elaborazione...in corso!");
        self.setMyCursor(self.stockCursor1)
        sMeasureFile = self.measureFileBrowseButton.GetValue()
        self.LoadEnvDirs()
        sEnvCode = self.textCtrlCantiere.GetValue()
        sNodeCode = self.txtCtrlCentralina.GetValue()
        filetstamp = time.strftime('%Y%m%d%H%M%S')
        shutil.copy(sMeasureFile,os.path.join( self.NodeDir, sEnvCode+"_"+sNodeCode+"_"+filetstamp+".csv"))
        settings.gibeimportfolder_path = self.EnvDir
        self.logfilepath = os.path.join(self.EnvDir , settings.gibelogfile_name)
        settings.gibelogfile_path = self.logfilepath  
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.logfilepath)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        self.run_main()
        self.CheckDB()
        #time.sleep(1)
        self.setMyCursor(mycur)
        self.staticTextMessage.SetLabel("Elaborazione...terminata!");
        self.Info("Importazione completata, verificare la cartella di lavoro %s " % self.EnvDir, "Import Data")
        self.logger.info("Importazione completata, verificare la cartella di lavoro %s " % self.EnvDir)
        event.Skip()
        
    def run_main(self):
        self.logger.info("GibeNRSApp Started on %s" % settings.gibeimportfolder_path)
        item = self.txtCtrlCentralina.GetValue()
        if os.path.isdir(settings.gibeimportfolder_path+"/"+item) == True:
          csv_folder = settings.gibeimportfolder_path+"/"+item
          gibe2nrs = GibeToNrs(self.e_uid,item,csv_folder,self.logger)
          gibe2nrs.run()

    def LoadFilenames(self,nodeId):
        bFilterNodeIsChecked = self.chkByNode.IsChecked();
        self.imgPath = os.path.join( settings.gibeimportfolder_path, "img");
        if nodeId>0:
            self.listCtrlImages.DeleteAllItems()
            items = self.LoadDatastreamPicturesByNode(nodeId)
            if os.path.exists(self.imgPath) == True:
                for file_name in glob(os.path.join( self.imgPath ,"*.png")):
                    x=0
                    sFile_name = os.path.basename(file_name)
                    for item in items:
                        if sFile_name == item[0]:
                            self.listCtrlImages.InsertStringItem(x,sFile_name)
                            mod_date, date2 = self.get_info(file_name)
                            self.listCtrlImages.SetStringItem(x,1,u'%s' % mod_date)
                            x=x+1 
                            break
            
    def setImageToPreview(self, imgPath):
        Img = wx.Image(imgPath, wx.BITMAP_TYPE_PNG)
        self.wximgMap = Img
        W = Img.GetWidth()
        H = Img.GetHeight()
        fH = float(H)
        fW = float(W)
        fRate = fH / fW
        if fRate + 0.01 < 0.75 or fRate - 0.01 > 0.75:
            self.Info("Attenzione l'immagine non ha formato 4:3 (%d:%d)!\n Potrebbero verificarsi dei problemi nella visualizzazione." % (int(3.0/fRate),3), "Formato immagine non corretto!")
        if W > H:
            NewW = 280
            NewH = 280 * H / W
        else:
            NewH = 210
            NewW = 210 * W / H
        Img = Img.Scale(NewW,NewH)
        self.imgMap.SetBitmap(wx.BitmapFromImage(Img))
        self.Refresh()

            
    def imgCallback(self, event):
        imgFilePath = self.fileBrowseButton1.GetValue()
        self.imgPath = os.path.join( settings.gibeimportfolder_path, "img");
        if not os.path.exists(self.imgPath ):
            os.mkdir(self.imgPath )
        imgNewFilePath = os.path.join( self.imgPath , os.path.basename(imgFilePath) )
        if imgFilePath == imgNewFilePath:
            imgNewFilePath = imgFilePath
        else:
            shutil.copy(imgFilePath , imgNewFilePath  )
        self.setImageToPreview(imgNewFilePath)
        self.imgFileName = os.path.basename(imgFilePath)
        self.imgFilePath = imgNewFilePath
        self.LoadFilenames(self.nodeselected_id)
        event.Skip()
    
    def dbCallback(self,event):
        self.CheckDB()
    
    def WorkingDirCallback(self,event):
        self.LoadEnvDirs()
    
    def LoadEnvDirs(self):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        self.logger.info("LoadEnvDirs starting...")
        sDir = self.workingDirBrowseButton.GetValue()
        if settings.gibedatafolder_path != sDir:
            self.logger.info("Changing Working Folder from %s to %s" % (settings.gibedatafolder_path,sDir))
            settings.gibedatafolder_path = sDir
        if not os.path.exists(sDir ):
            self.logger.info("Creating new Working Folder %s" % sDir)
            os.mkdir(sDir )
        sEnvCode = self.textCtrlCantiere.GetValue()
        if settings.environment_name != sEnvCode:
           self.logger.info("Changing Environment Name from %s to %s" % (settings.environment_name,sEnvCode))
           settings.environment_name = sEnvCode
        self.e_uid = sEnvCode
        sNodeCode = self.txtCtrlCentralina.GetValue()
        if settings.first_node != sNodeCode:
           self.logger.info("Changing First Node from %s to %s" % (settings.first_node,sNodeCode))
           settings.first_node = sNodeCode        
        self.EnvDir = os.path.join( sDir, sEnvCode)
        if settings.gibeimportfolder_path != self.EnvDir:
            self.logger.info("Changing new Import Folder from %s to %s" % (settings.gibeimportfolder_path,self.EnvDir))
            settings.gibeimportfolder_path = self.EnvDir
        if not os.path.exists(self.EnvDir ):
            self.logger.info("Creating new folder %s for Environment %s" % (self.EnvDir,sEnvCode))
            os.mkdir(self.EnvDir )            
        self.NodeDir = os.path.join( self.EnvDir , sNodeCode)
        if not os.path.exists(self.NodeDir ):
            self.logger.info("Creating new folder %s for node %s" % (self.NodeDir,sNodeCode))
            os.mkdir(self.NodeDir)
        self.logger.info("LoadEnvDirs terminated...")
        self.setMyCursor(mycur)

    def OnBtnCheckDBButton(self, event):
        self.logger.info("Verifica DB...in corso")
        self.staticTextMessage.SetLabel("Verifica DB...in corso");
        self.CheckDB()
        self.staticTextMessage.SetLabel("Verifica DB...terminata!");
        self.logger.info("Verifica DB...terminata")
        event.Skip()
        
    def CheckDB(self):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        self.logger.info("CheckDB...starting")
        self.database_file = self.databaseBrowseButton.GetValue()
        if settings.database != self.database_file:
            self.logger.info("Changing Database from %s to %s" % (settings.database,self.database_file))
            settings.database = self.database_file
        self.listCtrl1.DeleteAllItems()
        self.listCtrlEnv.DeleteAllItems()
        self.listCtrlNode.DeleteAllItems()
        self.listCtrlDatastream.DeleteAllItems()
        sAt_from , sAt_to = self.GetAdminDatetimeLimits() 
        sDataFiltering = " WHERE 1=1"
        if self.checkBox1.IsChecked() or self.checkBox2.IsChecked():
            sDataFiltering = " WHERE updated >= '%s' AND updated <= '%s'" % ( sAt_from , sAt_to )
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT count(*) as cnt, max(updated)
            FROM nrs_environment %s
        """ % sDataFiltering
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = row[0]       
        else:
            return_value = 0
        self.listCtrl1.InsertStringItem(0,u'Environment')
        self.listCtrl1.SetStringItem(0,1,"%d" % return_value)
        if row[1]!=None:
            self.listCtrl1.SetStringItem(0,2,row[1])
        else:            
            self.listCtrl1.SetStringItem(0,2,u'None')
        sQuery = """
            SELECT count(*) as cnt, max(updated)
            FROM nrs_node %s 
        """  % sDataFiltering
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = row[0]       
        else:
            return_value = 0
        self.listCtrl1.InsertStringItem(1,u'Node')
        self.listCtrl1.SetStringItem(1,1,"%d" % return_value)
        if row[1]!=None:
            self.listCtrl1.SetStringItem(1,2,row[1])
        else:            
            self.listCtrl1.SetStringItem(1,2,u'None')
        sQuery = """
            SELECT count(*) as cnt, max(updated)
            FROM nrs_datastream %s 
        """  % sDataFiltering
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = row[0]       
        else:
            return_value = 0
        self.listCtrl1.InsertStringItem(2,u'Datastream')
        self.listCtrl1.SetStringItem(2,1,"%d" % return_value)
        if row[1]!=None:
            self.listCtrl1.SetStringItem(2,2,row[1])
        else:            
            self.listCtrl1.SetStringItem(2,2,u'None')
        sQuery = """
            SELECT count(*) as cnt, max(updated)
            FROM nrs_datapoint %s 
        """  % sDataFiltering
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = row[0]       
        else:
            return_value = 0
        self.listCtrl1.InsertStringItem(3,u'Datapoint')
        self.listCtrl1.SetStringItem(3,1,"%d" % return_value)
        if row[1]!=None:
            self.listCtrl1.SetStringItem(3,2,row[1])
        else:            
            self.listCtrl1.SetStringItem(3,2,u'None')
        db_conn.close()
        self.LoadEnv()
        if self.listCtrlEnv.GetItemCount > 0:
            id=self.listCtrlEnv.GetItemData(0)
            if id>0:
                self.txtEnvNode.SetValue(u'%s' % self.listCtrlEnv.GetItem(0,1).GetText())
                self.LoadNode(id)
                id=self.listCtrlNode.GetItemData(0)
                if id>0:
                    self.LoadFilenames(id)
                    self.txtNodeDatastream.SetValue(u'%s' % self.listCtrlNode.GetItem(0,1).GetText())
                    self.LoadDataFilter(id)
                    self.LoadDistinctDatastreamUpdated2(id)
                    self.nodeselected_id = id
                    self.LoadDatastream(id)
        self.setMyCursor(mycur)
        self.logger.info("CheckDB...terminated")
    
    def LoadEnv(self):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        self.listCtrlEnv.DeleteAllItems()
         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT title, environment_uid, location_name, updated, id
            FROM nrs_environment
            ORDER BY updated DESC
        """
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        x=0
        for row in rows:
            self.listCtrlEnv.InsertStringItem(x,row[0])
            self.listCtrlEnv.SetStringItem(x,1,row[1])
            self.listCtrlEnv.SetStringItem(x,2,row[3])
            self.listCtrlEnv.SetItemData(x,row[4])
            x=x+1
            
        
        db_conn.close()


    def LoadNode(self, env_id):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        self.listCtrlNode.DeleteAllItems()
         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT title, node_uid, updated, id
            FROM nrs_node
            WHERE nrs_environment_id = %d
            ORDER BY updated DESC
        """ % env_id
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        x=0
        for row in rows:
            self.listCtrlNode.InsertStringItem(x,row[0])
            self.listCtrlNode.SetStringItem(x,1,row[1])
            self.listCtrlNode.SetStringItem(x,2,row[2])
            self.listCtrlNode.SetItemData(x,row[3])
            x=x+1
        db_conn.close()

    def LoadDatastream(self, node_id):
        self.logger.info("Starting LoadDatastream for Node with id %s ...." % node_id)
        self.listCtrlDatastream.DeleteAllItems()
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT title, datastream_uid, nrs_datastream.updated,nrs_datastream.id, factor_title, MAX(datetime_at), MIN(datetime_at), nrs_datastream.nrs_node_id , lambda_value
            FROM nrs_datastream 
			LEFT JOIN nrs_datapoint ON nrs_datapoint.nrs_datastream_id = nrs_datastream.id
            WHERE nrs_datastream.nrs_node_id = %d 
            GROUP BY title, datastream_uid, nrs_datastream.updated,nrs_datastream.id, factor_title
            ORDER BY title ASC
        """ % node_id
        self.logger.info("LoadDatastream sQuery \n %s " % sQuery)
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        x=0
        dsData={}
        bFirst = True
        self.datastreamslist = []
        for row in rows:
            self.datastreamslist.append(row)
            self.listCtrlDatastream.InsertStringItem(x,row[0])
            if row[4]==None:
                row[4]=""
            self.listCtrlDatastream.SetStringItem(x,1,row[1])
            self.listCtrlDatastream.SetStringItem(x,2,str(row[8]))
            self.listCtrlDatastream.SetStringItem(x,3,row[2])
            self.listCtrlDatastream.SetItemData(x,row[3])
            if bFirst:
                dsData['max_date'] = row[5]
                dsData['min_date'] = row[6]
                bFirst = False
            else:
                if row[5] > dsData['max_date']:
                    dsData['max_date'] = row[5] 
                if row[6] < dsData['min_date']:
                    dsData['min_date'] = row[6] 
            x=x+1
        if dsData['max_date'] != None:
			max_date=datetime.strptime(dsData['max_date'],'%Y%m%d%H%M%S%f')
			wxmaxdate = wx.DateTimeFromDMY(max_date.day, max_date.month - 1, max_date.year, 0, 0, 0)        
			self.dtTo.SetValue(wxmaxdate)
        if dsData['min_date'] != None:
			min_date=datetime.strptime(dsData['min_date'],'%Y%m%d%H%M%S%f')
			wxmindate = wx.DateTimeFromDMY(min_date.day, min_date.month - 1, min_date.year, 0, 0, 0)
			self.dtFrom.SetValue(wxmindate)
        db_conn.close()
        self.logger.info("LoadDatastream terminated")

    def LoadAllDatastreams(self):
        self.logger.info("Staring LoadAllDatastreams... ")
        self.listCtrlDatastream.DeleteAllItems()
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT title, datastream_uid, nrs_datastream.updated,nrs_datastream.id, factor_title, MAX(datetime_at), MIN(datetime_at), nrs_datastream.nrs_node_id , nrs_datastream.lambda_value 
            FROM nrs_datastream 
			LEFT JOIN nrs_datapoint ON nrs_datapoint.nrs_datastream_id = nrs_datastream.id
            GROUP BY title, datastream_uid, nrs_datastream.updated,nrs_datastream.id, factor_title
            ORDER BY title ASC
        """
        self.logger.info("LoadAllDatastreams sQuery \n %s " % sQuery)
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        x=0
        dsData={}
        bFirst = True
        self.datastreamslist = []
        for row in rows:
            self.datastreamslist.append(row)
            self.listCtrlDatastream.InsertStringItem(x,row[0])
            if row[4]==None:
                row[4]=""
            self.listCtrlDatastream.SetStringItem(x,1,row[1])
            self.listCtrlDatastream.SetStringItem(x,2,str(row[8]))
            self.listCtrlDatastream.SetStringItem(x,3,row[2])
            self.listCtrlDatastream.SetItemData(x,row[3])
            if bFirst:
                dsData['max_date'] = row[5]
                dsData['min_date'] = row[6]
                bFirst = False
            else:
                if row[5] > dsData['max_date']:
                    dsData['max_date'] = row[5] 
                if row[6] < dsData['min_date']:
                    dsData['min_date'] = row[6] 
            x=x+1
        if dsData['max_date'] != None:
			max_date=datetime.strptime(dsData['max_date'],'%Y%m%d%H%M%S%f')
			wxmaxdate = wx.DateTimeFromDMY(max_date.day, max_date.month - 1, max_date.year, 0, 0, 0)        
			self.dtTo.SetValue(wxmaxdate)
        if dsData['min_date'] != None:
			min_date=datetime.strptime(dsData['min_date'],'%Y%m%d%H%M%S%f')
			wxmindate = wx.DateTimeFromDMY(min_date.day, min_date.month - 1, min_date.year, 0, 0, 0)
			self.dtFrom.SetValue(wxmindate)
        db_conn.close()
        self.logger.info("LoadAllDatastreams terminated!")


    def LoadDistinctDatastreamUpdated2(self, node_id, from_date=None, to_date=None):
        #controllare formula danzi.tn@20140702
        return_value = -99
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        self.listCtrlDatapoint.DeleteAllItems()
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sextra = "1=1"
        if from_date!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at >= '%s'" % from_date
        if to_date!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at <= '%s'" % to_date
        sQuery = """
            SELECT DISTINCT 
            nrs_datastream.id, 
            nrs_datastream.datastream_uid, 
            max(nrs_datapoint.updated), 
            AVG(value_at) AS avg_value_at,
            COUNT(sample_no) as cnt_samples,
            nrs_datastream.title
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            FROM nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND nrs_datastream.nrs_node_id = %d AND %s
            GROUP BY 
            nrs_datastream.id, 
            nrs_datastream.datastream_uid,
            nrs_datastream.title
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            ORDER BY nrs_datastream.datastream_uid
        """ % (node_id, sextra)
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        xx=0
        for row in rows:
            at_val = float(row[3])
            const = row[6] #constant_value
            lambda_val = float(row[7]) #lambda_value
            first = row[8] #factor_value
            second = row[9] #factor_value_2
            sFormula = row[10]
            delta_val = at_val - lambda_val
            x = delta_val
            #resVal = second*x*x + first*x + const
            return_value = eval(sFormula)
            self.listCtrlDatapoint.InsertStringItem(xx,row[5])
            self.listCtrlDatapoint.SetStringItem(xx,1,row[2])
            self.listCtrlDatapoint.SetStringItem(xx,2,u'%f'%return_value)
            self.listCtrlDatapoint.SetStringItem(xx,3,u'%d'%row[4])
            self.listCtrlDatapoint.SetItemData(xx,row[0])
            xx=xx+1
        db_conn.close()
    
    def LoadDatapointAvg2(self, datastream_id, date_from=None, date_to=None):
        #controllare formula danzi.tn@20140702
        return_value = -99
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sextra = "1=1"
        if date_from!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at >= '%s'" % date_from
        if date_to!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at <= '%s'" % date_to
        sQuery = """
            SELECT 
            AVG(value_at) AS avg_value_at 
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            FROM  nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND 
            nrs_datastream_id = %d AND %s
            GROUP BY 
            nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
        """ % (datastream_id, sextra)
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()
        if row:
            at_val = float(row[0])
            const = row[1] #constant_value
            lambda_val = float(row[2]) #lambda_value
            first = row[3] #factor_value
            second = row[4] #factor_value_2
            sFormula = row[5]
            delta_val = at_val - lambda_val
            x = delta_val
            #resVal = second*x*x + first*x + const
            return_value = eval(sFormula)
        db_conn.close()
        return return_value

    def LoadDatapoints2(self, datastream_id, avg_val, date_from=None, date_to=None):
        # controllare formula danzi.tn@20140702
        return_value = -99
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sextra = "1=1"
        if date_from!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at >= '%s'" % date_from
        if date_to!=None:
            sextra = sextra + " AND nrs_datapoint.datetime_at <= '%s'" % date_to
        sQuery = """
            SELECT DISTINCT datetime_at
            ,  sample_no 
            , value_at
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula            
            FROM  nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND 
            nrs_datastream_id = %d AND %s
            ORDER BY  datetime_at
        """ % (datastream_id, sextra)
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        xx=0
        val=[]
        dta=[]
        lbl=[]
        avg=[]
        ddatetime=[]
        tmpavg = avg_val
        if avg_val == None:
            tmpavg = 0
        for row in rows:
            xx = xx + 1
            at_val = float(row[2])
            const = row[3]
            lambda_val = float(row[4])
            first = row[5]
            second = row[6]
            sFormula = row[7]
            delta_val = at_val - lambda_val
            x = delta_val
            #resVal = second*x*x + first*x + const
            resVal = eval(sFormula)
            #val.append(row[0])
            val.append(resVal)
            sDate = row[0]
            dtt=datetime.strptime(sDate,'%Y%m%d%H%M%S%f')
            sAt_from = dtt.strftime('%Y-%m-%d %H:%M:%S')
            #x = int(time.mktime(dtt.timetuple()))
            dta.append(sAt_from)
            ddatetime.append(dtt)
            lbl.append(xx)
            avg.append(tmpavg)
        db_conn.close()
        return_value={'val':val,'dta':dta,'lbl':lbl,'avg':avg,'datetime':ddatetime}
        return return_value   

    def GetEnv(self,id):
        return_value = {}
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT id, title, environment_uid, location_name, updated,
            location_disposition, location_exposure, location_latitude, location_longitude, location_elevation
            FROM nrs_environment
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = {'id':row[0],'title':row[1],'environment_uid':row[2],'location_name':row[3],'updated':row[4]} 
        
        db_conn.close()
        return return_value

    def GetNode(self,id):
        return_value = {}
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT id, title, node_uid, updated, ipaddress, portin, portout, confhh, confmm, confss, confsamples
            FROM nrs_node
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = {'id':row[0],'title':row[1],'node_uid':row[2],'updated':row[3],'ipaddress':row[4],'portin':row[5],'portout':row[6],'hh':row[7],'mm':row[8],'ss':row[9],'samp':row[10]} 
        
        db_conn.close()
        return return_value
    

    def GetDatastream(self,id):
        return_value = {}
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT  nrs_datastream.id, 
                    nrs_datastream.title, 
                    nrs_datastream.datastream_uid, 
                    nrs_datastream.updated, 
                    factor_value, 
                    lambda_value, 
                    constant_value, 
                    factor_title, 
                    max( nrs_datapoint.datetime_at) as max_date,  
                    min( nrs_datapoint.datetime_at) as min_date , 
                    factor_value_2, 
                    ds_formula, 
                    nrs_node.node_uid as nrs_node_uid, 
                    nrs_datastream.ch as ds_channell
            FROM nrs_datastream 
            JOIN nrs_node ON nrs_node.id = nrs_datastream.nrs_node_id
			LEFT JOIN nrs_datapoint ON nrs_datastream.id = nrs_datapoint.nrs_datastream_id
            WHERE 
            nrs_datastream.id = %d
            GROUP BY 
                    nrs_datastream.id, 
                    nrs_datastream.title, 
                    nrs_datastream.datastream_uid, 
                    nrs_datastream.updated, 
                    factor_value, 
                    lambda_value, 
                    constant_value, 
                    factor_title, 
                    factor_value_2, 
                    ds_formula, 
                    nrs_node.node_uid, 
                    nrs_datastream.ch
        """ % id
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = {'id':row[0],'title':row[1],'datastream_uid':row[2],'updated':row[3],'den':row[4],'lambda':row[5],'const':row[6],'ds_len':row[7],'max_date':row[8],'min_date':row[9],'second':row[10],'formula':row[11],'node_uid':row[12],'ds_channell':row[13]} 
        db_conn.close()
        return return_value
    

    def OnListCtrlEnvListItemSelected(self, event):
        self.selected_entity = 1
        idx = event.m_itemIndex
        id=self.listCtrlEnv.GetItemData(idx)
        self.logger.info("Selected Environment with id %s" % id)
        envData = self.GetEnv(id)
        self.selected_entity_id = id
        self.txtEnvTitle.Clear()
        self.txtEnvTitle.SetValue(envData['title'])
        self.logger.info("Environment title is %s" % envData['title'])
        self.txtEnvCod.Clear()
        self.txtEnvCod.SetValue(envData['environment_uid'])
        self.logger.info("Environment uid is %s" % envData['environment_uid'])
        if settings.environment_name!= envData['environment_uid']:
            self.logger.info("Changing Environment from %s to %s" % (settings.environment_name, envData['environment_uid']))
            settings.environment_name = envData['environment_uid']
            self.textCtrlCantiere.SetValue(envData['environment_uid'])
        self.txtEnvLocation.Clear()
        if envData['location_name']==None:
            envData['location_name'] = "Nessuna"
        self.txtEnvLocation.SetValue(u'%s' % envData['location_name'])
        self.logger.info("Environment location is %s" % envData['location_name'])
        self.LoadNode(self.selected_entity_id)
        self.txtEnvNode.SetValue(self.txtEnvCod.GetValue())
        event.Skip()

    def OnButtonSaveButton(self, event):
        if self.selected_entity == 1:
            sTitle = self.txtEnvTitle.GetValue()
            sLocation = self.txtEnvLocation.GetValue()
            env_item = {'id': self.selected_entity_id, 'title':sTitle,'location_name':sLocation}
            ret = self.UpdatetEnv(env_item)
        if self.selected_entity == 2:
            sTitle = self.txtNodeName.GetValue()
            node_item = {'id': self.selected_entity_id, 'title':sTitle, 'ipaddress': self.txtNodeIp.GetValue(), 'portin':self.txtPortInput.GetValue() ,'portout':self.txtPortOutput.GetValue(),'hh':self.txtConfHH.GetValue(),'mm':self.txtConfMM.GetValue(),'ss':self.txtConfSS.GetValue(),'samples':self.txtConfSamples.GetValue() }
            ret = self.UpdatetNode(node_item)
        if self.selected_entity == 3:
            sDen = self.txtDen.GetValue()
            sConst = self.txtConst.GetValue()
            sLambda = self.txtLambda.GetValue()
            sSecond = self.txtSecond.GetValue()
            sTitle = self.txtDsTitle.GetValue()
            sFormula = self.txtFormula.GetValue()
            sDen = sDen.replace(',','.')
            sConst = sConst.replace(',','.')
            sLambda = sLambda.replace(',','.')
            sSecond = sSecond.replace(',','.')
            sFormula = sFormula.replace(',','.')
            ds_item = {'id': self.selected_entity_id, 'den':sDen,'const':sConst,'lambda':sLambda,'title':sTitle,'second':sSecond,'formula':sFormula}
            ret = self.UpdatetDs(ds_item)
        event.Skip()
    
    def UpdatetEnv(self,env_item):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
        sQuery = """
            UPDATE 
            nrs_environment
            SET
            title = '%s' , location_name = '%s', updated= '%s'
            WHERE id = %d
        """ % (env_item['title'],env_item['location_name'],sUpdated, env_item['id'])
        retVal = db_cur.execute(sQuery)
        db_conn.commit()
        db_conn.close()
        self.CheckDB()
        return retVal
    
    def UpdatetNode(self,node_item):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
        sQuery = """
            UPDATE 
            nrs_node
            SET
            title = '%s' , updated= '%s', ipaddress = '%s',portin = '%s',portout = '%s',confhh = '%s',confmm = '%s',confss = '%s',confsamples = '%s'
            WHERE id = %d
        """ % (node_item['title'],sUpdated, node_item['ipaddress'], node_item['portin'], node_item['portout'], node_item['hh'], node_item['mm'], node_item['ss'], node_item['samples'], node_item['id'])
        retVal = db_cur.execute(sQuery)
        db_conn.commit()
        db_conn.close()
        self.CheckDB()
        return retVal

    def UpdatetDs(self,ds_item):         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
        sQuery = """
            UPDATE 
            nrs_datastream
            SET
            factor_value = %s , lambda_value= %s, constant_value=%s, updated='%s', title='%s' , factor_value_2=%s, ds_formula='%s'
            WHERE id = %d
        """ % (ds_item['den'], ds_item['lambda'], ds_item['const'],sUpdated,ds_item['title'],ds_item['second'],ds_item['formula'],ds_item['id'])
        retVal = db_cur.execute(sQuery)
        db_conn.commit()
        db_conn.close()
        self.CheckDB()
        return retVal
    
    def DelEnv(self,id):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            DELETE 
            FROM nrs_environment
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_node
            WHERE nrs_environment_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_datastream
            WHERE nrs_environment_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_datapoint
            WHERE nrs_environment_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal
    
    def DelNode(self,id):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            DELETE 
            FROM nrs_node
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_datastream
            WHERE nrs_node_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_datapoint
            WHERE nrs_node_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal
    
    def DelDs(self,id):
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            DELETE 
            FROM nrs_datastream
            WHERE id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        sQuery = """
            DELETE 
            FROM nrs_datapoint
            WHERE nrs_datastream_id = %d
        """ % id
        retVal = db_cur.execute(sQuery)
        db_conn.commit()      
        db_conn.close()
        return retVal

    def OnButtonDeleteButton(self, event):
        if self.selected_entity == 1:
            self.DelEnv(self.selected_entity_id)
        if self.selected_entity == 2:
            self.DelNode(self.selected_entity_id)
        if self.selected_entity == 3:
            self.DelDs(self.selected_entity_id)
        if self.selected_entity == 5:
            self.DelDsPicture()
        self.CheckDB()
        event.Skip()

    def OnListCtrlNodeListItemSelected(self, event):
        mycur = self.GetCursor()
        self.setMyCursor(self.stockCursor1)
        self.selected_entity = 2
        idx = event.m_itemIndex
        id=self.listCtrlNode.GetItemData(idx)
        self.logger.info("Selected Node with id %s" % id )
        nodeData = self.GetNode(id)
        self.selected_entity_id = id
        self.nodeselected_id = id
        self.txtNodeName.Clear()
        self.txtNodeName.SetValue(nodeData['title'])
        self.logger.info("Selected Node with title %s" % nodeData['title'] )
        self.txtNodeCode.Clear()
        sNodeUid = nodeData['node_uid']
        self.logger.info("Selected Node with uid %s" % sNodeUid )
        sNodeFolder = sNodeUid[len(self.e_uid):]
        if settings.first_node != sNodeFolder:
            self.logger.info("First Node changed from %s to %s" % (settings.first_node, sNodeFolder ))
            settings.first_node = sNodeFolder
        self.NodeDir = os.path.join( self.EnvDir , sNodeFolder)
        if not os.path.exists(self.NodeDir ):
            self.logger.info("Creating new folder %s for node %s" % (self.NodeDir,sNodeFolder))
            os.mkdir(self.NodeDir)
        self.txtCtrlCentralina.SetValue(sNodeFolder)
        self.txtNodeCode.SetValue(sNodeUid)
        self.txtNodeIp.Clear() 
        self.txtNodeIp.SetValue(nodeData['ipaddress'])
        self.txtPortInput.Clear() 
        self.txtPortInput.SetValue(nodeData['portin'])
        self.txtPortOutput.Clear() 
        self.txtPortOutput.SetValue(nodeData['portout'])
        self.txtConfHH.Clear() 
        self.txtConfHH.SetValue(nodeData['hh'])
        self.txtConfMM.Clear() 
        self.txtConfMM.SetValue(nodeData['mm'])
        self.txtConfSS.Clear() 
        self.txtConfSS.SetValue(nodeData['ss'])
        self.txtConfSamples.Clear() 
        self.txtConfSamples.SetValue(nodeData['samp'])
        self.LoadDatastream(self.selected_entity_id)     
        self.LoadFilenames(id)   
        sAt_from , sAt_to = self.GetDatapointDatetimeLimits()
        valChck = self.chkDataFilter.IsChecked()
        if not valChck:
            sAt_from = None
            sAt_to = None
        self.LoadDistinctDatastreamUpdated2(self.selected_entity_id,sAt_from,sAt_to)
        self.nodeselected_id = self.selected_entity_id
        self.LoadDataFilter(self.selected_entity_id)
        self.txtNodeDatastream.SetValue(self.txtNodeCode.GetValue())
        self.loadConnectionInfo()
        self.setMyCursor(mycur)
        event.Skip()

    def loadConnectionInfo(self):
        self.txtIP.SetValue(self.txtNodeIp.GetValue());
        self.txtPort1.SetValue(self.txtPortInput.GetValue());
        self.txtport2.SetValue(self.txtPortOutput.GetValue());
        self.txtPERIH.SetValue(self.txtConfHH.GetValue());
        self.txtPERIM.SetValue(self.txtConfMM.GetValue());
        self.txtPERIS.SetValue(self.txtConfSS.GetValue());
        self.txtSAMP.SetValue(self.txtConfSamples.GetValue());

    def OnListCtrlDatastreamListItemSelected(self, event):
        self.selected_entity = 3
        idx = event.m_itemIndex
        id = self.listCtrlDatastream.GetItemData(idx)
        dsData = self.GetDatastream(id)
        self.selected_entity_id = id
        self.selected_datastream_id = id
        self.txtDsCode.Clear()
        self.txtDsCode.SetValue(dsData['datastream_uid'])
        self.txtDsLen.Clear()
        self.txtDsLen.SetValue(u'%s' % dsData['ds_len'])
        self.txtDsTitle.Clear()
        self.txtDsTitle.SetValue(u'%s' % dsData['title'])
        self.txtConst.Clear()
        self.txtConst.SetValue(u'%f' % dsData['const'])
        self.txtLambda.Clear()
        self.txtLambda.SetValue(u'%f' % dsData['lambda'])
        self.txtDen.Clear()
        self.txtDen.SetValue(u'%f' % dsData['den'])
        self.txtSecond.Clear()
        self.txtSecond.SetValue(u'%f' % dsData['second'])
        self.txtFormula.Clear()
        self.txtFormula.SetValue(u'%s' % dsData['formula'])
        self.txtCh.Clear()
        self.txtCh.SetValue(u'%d' % dsData['ds_channell'])
        if dsData['max_date']!= None:
			max_date=datetime.strptime(dsData['max_date'],'%Y%m%d%H%M%S%f')
			wxmaxdate = wx.DateTimeFromDMY(max_date.day, max_date.month - 1, max_date.year, 0, 0, 0)     
			self.dtTo.SetValue(wxmaxdate)
        if dsData['min_date']!= None:
			min_date=datetime.strptime(dsData['min_date'],'%Y%m%d%H%M%S%f')
			wxmindate = wx.DateTimeFromDMY(min_date.day, min_date.month - 1, min_date.year, 0, 0, 0)
			self.dtFrom.SetValue(wxmindate)   
        #self.LoadDatapoint(self.selected_entity_id)
        #self.txtDatastreamDatapoint.SetValue(self.txtDsCode.GetValue())
        event.Skip()

    def OnListCtrlDatapointListItemSelected(self, event):
        idx = event.m_itemIndex
        self.ProcessImage(idx)
        event.Skip()

    def ProcessImage(self,idx):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        id=self.listCtrlDatapoint.GetItemData(idx)
        updated=self.listCtrlDatapoint.GetItem(idx,1).GetText()  
        sAt_from , sAt_to = self.GetDatapointDatetimeLimits()
        valChck = self.chkDataFilter.IsChecked()
        if not valChck:
            sAt_from = None
            sAt_to = None
        avgVal = self.LoadDatapointAvg2(id, sAt_from , sAt_to)
        retVal = self.LoadDatapoints2(id, avgVal, sAt_from , sAt_to)
        if avgVal== None:
            self.txtAvg.SetValue(u'ND')
        else:
            self.txtAvg.SetValue(u'%f' % avgVal)
        x1 = retVal['lbl']
        y1 = retVal['avg']
        x2 = retVal['lbl']
        y2 = retVal['val']
        plt.clf()
        plt.tick_params(axis='y', labelsize=8)
        plt.tick_params(axis='x', labelsize=8,labelleft=True)
        plt.plot(x1, y1,'r--')
        plt.plot( x2, y2,'b-')
        locs, labels = plt.xticks()
        new_labels = []
        for loc in locs:
            idx = int(loc)
            if idx < len(retVal['dta']):
              sText = retVal['dta'][int(loc)]
            else:
              sText = ""
            new_labels.append(sText )
        plt.xticks(locs, new_labels,rotation=17)
        plt.grid(which='major', axis='x')
        dt=datetime.strptime(updated,u'%Y-%m-%d %H:%M:%S')
        sAt = dt.strftime('%Y%m%d%H%M%S')    
        imagefname=os.path.join(self.EnvDir,"%d_%s_plot.png" % (id,sAt))
        plt.savefig(imagefname,format='png')
        Img = wx.Image(imagefname, wx.BITMAP_TYPE_PNG)
        self.wximg = Img
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = 320
            NewH = 320 * H / W
        else:
            NewH = 320
            NewW = 320 * W / H
        Img = Img.Scale(NewW,NewH)
        self.imgChart.SetBitmap(wx.BitmapFromImage(Img))
        self.Refresh()
        self.setMyCursor(mycur)


    def OnBtnExportButton(self, event):
        self.LoadEnvDirs()
        datastream_id=self.selected_entity_id
        dsItem = self.GetDatastream(datastream_id)
        sDtFrom = self.dtFrom.GetValue().Format('%Y-%m-%d')
        sDtTo = self.dtTo.GetValue().Format('%Y-%m-%d')
        sHHFrom = self.txtHHFrom.GetValue()
        sMMFrom = self.txtMMFrom.GetValue()
        sSSFrom = self.txtSSFrom.GetValue()
        sHHTo = self.txtHH.GetValue()
        sMMTo = self.txtMMTo.GetValue()
        sSSTo = self.txtSSTo.GetValue()
        sDtFrom = "%s %s:%s:%s.000000" % (sDtFrom,sHHFrom,sMMFrom,sSSFrom)
        sDtTo = "%s %s:%s:%s.000000" % (sDtTo,sHHTo,sMMTo,sSSTo)
        dtf=datetime.strptime(sDtFrom,"%Y-%m-%d %H:%M:%S.%f")
        dtt=datetime.strptime(sDtTo,"%Y-%m-%d %H:%M:%S.%f")
        sAt_from = dtf.strftime('%Y%m%d%H%M%S%f')  
        sAt_to = dtt.strftime('%Y%m%d%H%M%S%f')
        bulk_export_rows = self.ExportDatapoints(self.nodeselected_id, datastream_id, sAt_from,sAt_to)
        bulk_export_grouped_rows = self.ExportGroupedDatapoints(self.nodeselected_id, datastream_id, sAt_from,sAt_to)
        sExported = time.strftime('%Y%m%d%H%M%S') #timestamp for unique file name
        sFileName = "export_%d_%s.csv" % (self.nodeselected_id,sExported) #filename for the standard export
        sGroupedFileName = "export_grouped_%d_%s.csv" % (self.nodeselected_id,sExported) #filename for the grouped export
        sExportFilePath = os.path.join(self.EnvDir,sFileName)
        sExportGroupedFilePath = os.path.join(self.EnvDir,sGroupedFileName)
        with open(sExportFilePath,'wb') as exportcsvfile:
            writer = csv.writer(exportcsvfile,delimiter=';')
            writer.writerows(bulk_export_rows)
        with open(sExportGroupedFilePath,'wb') as exportgroupedcsvfile:
            writer = csv.writer(exportgroupedcsvfile,delimiter=';')
            writer.writerows(bulk_export_grouped_rows)            
        self.Info("export completati disponibili in:\n%s\n%s" % (sExportFilePath,sExportGroupedFilePath), "Export Data")
        event.Skip()

    def ExportGroupedDatapoints(self, node_id, datastream_id, datetime_from,datetime_to):
        #controllare formula danzi.tn@20140702
        sFormat = self.chkFormat.GetStringSelection()
        if sFormat=="aaaa-mm-gg":
            sFormat = "%Y-%m-%d %H:%M:%S"
        if sFormat=="mm/gg/aaaa":
            sFormat = "%m/%d/%Y %H:%M:%S"
        if sFormat=="gg/mm/aaaa":
            sFormat = "%d/%m/%Y %H:%M:%S"
        bulk_export_rows = []
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        
        sQueryDates = """
            SELECT 
            substr(datetime_at,0,9) as date_at, 
            count(value_at) as cnt_samples , 
            max( nrs_datapoint.updated) AS dp_updated
            FROM  nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND
            nrs_datapoint.nrs_node_id = %d AND nrs_datapoint.datetime_at <= '%s' AND nrs_datapoint.datetime_at >= '%s' 
            GROUP BY date_at
            ORDER BY date_at ASC""" % (node_id, datetime_to,datetime_from)
        
        retVal = db_cur.execute(sQueryDates)
        rows = retVal.fetchall()
        len_dates = len(rows)
        grouped_dates = {}
        header = []
        header.append('Sensore')
        j=1
        for row in rows:
            dtt = datetime.strptime(row[0],'%Y%m%d')
            sAt = dtt.strftime(sFormat)  
            grouped_dates[row[0]] = (sAt,j)
            header.append(sAt)
            j=j+1
        
        sQueryGrouped = """
            SELECT nrs_datastream.title AS ds_title, 
            AVG(value_at) as avg_value, 
            substr(datetime_at,0,9) as date_at, 
            count(value_at) as cnt_samples , 
            max(nrs_datapoint.updated) AS dp_updated
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            FROM  nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND
            nrs_datapoint.nrs_node_id = %d AND nrs_datapoint.datetime_at <= '%s' AND nrs_datapoint.datetime_at >= '%s' 
            GROUP BY 
            ds_title, 
            date_at
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            ORDER BY ds_title, date_at ASC
        """ % (node_id, datetime_to,datetime_from)
        
        retVal = db_cur.execute(sQueryGrouped)
        rows = retVal.fetchall()
        body=[] # Title=>row[0] e N sValue_at
        bLastGroup = False
        bFirst = True
        sLastDs = "ND"
        bulk_export_rows.append(header)
        sValue_Zero = "0.0"
        if self.rbtComma.GetValue():
            sValue_Zero = sValue_Zero.replace('.',',')
        body.append("TITLE")
        for key, value in grouped_dates.items():
            body.append(sValue_Zero)
        for row in rows:
            sTitle = row[0]
            if bFirst:
                sLastDs = sTitle
                bFirst = False
            dtt=datetime.strptime(row[2],'%Y%m%d')
            sAt = dtt.strftime(sFormat) 
            at_val = float(row[1])
            const = row[5] #constant_value
            lambda_val = float(row[6]) #lambda_value
            first = row[7] #factor_value
            second = row[8] #factor_value_2
            sFormula = row[9]
            delta_val = at_val - lambda_val
            x = delta_val
            #resVal = second*x*x + first*x + const
            retVal = eval(sFormula) 
            sValue_at = "%f" % retVal
            if self.rbtComma.GetValue():
                sValue_at = sValue_at.replace('.',',')
            if sTitle != sLastDs:                    
                bulk_export_rows.append(body)
                body=[]
                body.append("TITLE")
                for key, value in grouped_dates.items():
                    body.append(sValue_Zero)
            body[0] = sTitle
            if row[2] in grouped_dates:
                body[grouped_dates[row[2]][1]] = sValue_at
            sLastDs = sTitle                   
        bulk_export_rows.append(body)
        db_conn.close()        
        return bulk_export_rows
    
    def ExportDatapoints(self, node_id, datastream_id, datetime_from,datetime_to):
        sFormat = self.chkFormat.GetStringSelection()
        if sFormat=="aaaa-mm-gg":
            sFormat = "%Y-%m-%d %H:%M:%S"
        if sFormat=="mm/gg/aaaa":
            sFormat = "%m/%d/%Y %H:%M:%S"
        if sFormat=="gg/mm/aaaa":
            sFormat = "%d/%m/%Y %H:%M:%S"
        bulk_export_rows = []
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        
        sQuery = """
            SELECT  nrs_datastream.title, nrs_datastream.constant_value+(value_at - nrs_datastream.lambda_value)/nrs_datastream.factor_value AS calc_value_at , datetime_at,  sample_no, nrs_datapoint.updated
            FROM  nrs_datastream, nrs_datapoint
            WHERE nrs_datapoint.nrs_datastream_id = nrs_datastream.id AND 
            nrs_datastream.nrs_node_id = %d AND nrs_datapoint.datetime_at <= '%s' AND nrs_datapoint.datetime_at >= '%s'
            ORDER BY nrs_datastream.title, nrs_datapoint.updated DESC, datetime_at ASC
        """ % (node_id, datetime_to,datetime_from)
                
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        bulk_export_rows.append(('nome','valore','timestamp','campione','data'))
        for row in rows:
            dtt=datetime.strptime(row[2],'%Y%m%d%H%M%S%f')
            dt_updated=datetime.strptime(row[4],'%Y-%m-%d %H:%M:%S')
            sAt =dtt.strftime(sFormat)  
            sUpdated = dt_updated.strftime(sFormat)  
            #bulk_export_rows.append((row[0],row[1],sA,row[3],row[4]))
            sValue_at = "%f" % row[1]
            if self.rbtComma.GetValue():
                sValue_at = sValue_at.replace('.',',')
            bulk_export_rows.append((row[0],sValue_at,sAt,row[3],sUpdated))
        db_conn.close()        
        return bulk_export_rows
    
    def Info(parent, message, caption = 'Insert program title'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnImgChartLeftDclick(self, event):
        imgBox = Messaggio(self,self.wximg)
        imgBox.ShowModal()
        imgBox.Destroy()
        event.Skip()

    def OnBtnCloseButton(self, event):
        self.Close()
        event.Skip()

    def OnListCtrlDatapointLeftDclick(self, event):
        imgBox = Messaggio(self,self.wximg)
        imgBox.ShowModal()
        imgBox.Destroy()
        event.Skip()
        
    def LoadDataFilter(self, nrs_node_id):
        ret_max = None
        ret_min = None
        self.wxMinDatetime_at = None
        self.wxMaxDatetime_at = None
        self.database_file = self.databaseBrowseButton.GetValue()
        settings.database = self.database_file
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT MAX(datetime_at) 
            FROM  nrs_datapoint
            WHERE nrs_datapoint.nrs_node_id = %d 
        """ % (nrs_node_id)
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            ret_max = row[0]
            if ret_max:        
                max_date=datetime.strptime(ret_max,'%Y%m%d%H%M%S%f')
                wxmaxdate = wx.DateTimeFromDMY(max_date.day, max_date.month - 1, max_date.year, 0, 0, 0)
                self.dateTo.SetValue(wxmaxdate)   
                self.wxMaxDatetime_at = wxmaxdate
        sQuery = """
            SELECT MIN(datetime_at) 
            FROM  nrs_datapoint
            WHERE nrs_datapoint.nrs_node_id = %d 
        """ % (nrs_node_id)
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            ret_min = row[0]   
            if ret_min:       
                min_date=datetime.strptime(ret_min,'%Y%m%d%H%M%S%f')
                wxmindate = wx.DateTimeFromDMY(min_date.day, min_date.month - 1, min_date.year, 0, 0, 0)
                self.dateFrom.SetValue(wxmindate)
                self.wxMinDatetime_at = wxmindate
        db_conn.close()        
        return ret_min, ret_max
    
    def LoadDatastreamPictures(self):
        sQuery = """
            SELECT nrs_datastream_picture.id, nrs_datastream.id, nrs_datastream.title, nrs_datastream_picture.filename, nrs_datastream_picture.description, nrs_datastream.factor_title, nrs_datastream_picture.px, nrs_datastream_picture.py , nrs_datastream.lambda_value
            FROM nrs_datastream_picture, nrs_datastream
            WHERE
            nrs_datastream_picture.datastream_id = nrs_datastream.id
            AND
            nrs_datastream_picture.filename = '%s'
        """ % self.imgFileName
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        retVal = db_cur.execute(sQuery)    
        rows = retVal.fetchall()
        self.nrs_datastream_pictures = []
        for row in rows:
            self.nrs_datastream_pictures.append(row)
        db_conn.close() 
        
    def LoadDatastreamPicturesByNode(self,nodeID):
        bFilterNodeIsChecked = self.chkByNode.IsChecked();
        results = []
        sQuery = """
                SELECT DISTINCT nrs_datastream_picture.filename 
                FROM nrs_datastream_picture, nrs_datastream
                WHERE
                nrs_datastream_picture.datastream_id = nrs_datastream.id
        """ 
        if bFilterNodeIsChecked:
            sQuery = """
                SELECT DISTINCT nrs_datastream_picture.filename 
                FROM nrs_datastream_picture, nrs_datastream
                WHERE
                nrs_datastream_picture.datastream_id = nrs_datastream.id AND nrs_datastream.nrs_node_id = %d
            """ % nodeID
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        retVal = db_cur.execute(sQuery)    
        rows = retVal.fetchall()
        self.nrs_datastream_pictures = []
        for row in rows:
            results.append(row)
        db_conn.close() 
        return results
    

    def DeleteDatastreamPictures(self):
         #passo la lista dei datastream associati
        sQuery = """
            DELETE
            FROM nrs_datastream_picture 
            WHERE
            nrs_datastream_picture.filename = '%s'
        """ % self.imgFileName
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        retVal = db_cur.execute(sQuery)
        db_conn.commit()
        db_conn.close()   

    def OnListCtrlImagesListItemSelected(self, event):
        self.selected_entity = 5
        idx = event.m_itemIndex
        self.imgFileName=self.listCtrlImages.GetItem(idx,0).GetText()
        updated=self.listCtrlImages.GetItem(idx,1).GetText()
        self.imgFilePath = os.path.join( self.imgPath , self.imgFileName )
        self.setImageToPreview(self.imgFilePath)
        #passo la lista dei datastream associati
        self.LoadDatastreamPictures()           
        event.Skip()
    
    def DelDsPicture(self):
        self.imgFilePath = self.imgFilePath
        self.imgFileName = self.imgFileName
        os.remove(self.imgFilePath)
        #delefe file
        self.DeleteDatastreamPictures()
        self.LoadFilenames(self.nodeselected_id)
        #self.imgMap.SetBitmap(wx.BitmapFromImage(wx.EmptyImage()))
    
    def get_info(self, file_name):
        time_format = "%Y-%m-%d %H:%M:%S"
        file_stats = os.stat(file_name)
        modification_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_MTIME]))
        access_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_ATIME]))
        return modification_time, access_time

    def OnImgMapLeftDclick(self, event):
        mycur = self.GetCursor()
        self.setMyCursor(self.stockCursor1)
        if not self.chkByNode.IsChecked():
            self.LoadAllDatastreams()
        imgBox = imgAssociation(self)
        imgBox.setParameters(self.wximgMap,self.nrs_datastream_pictures,self.datastreamslist,self.imgFileName,self.imgFilePath, settings.database,self.wxMinDatetime_at,self.wxMaxDatetime_at, self.EnvDir)
        self.setMyCursor(mycur)
        imgBox.ShowModal()
        imgBox.Destroy()
        self.LoadDatastreamPictures()
        self.LoadFilenames(self.nodeselected_id)
        event.Skip()

    def OnListCtrlImagesLeftDclick(self, event):
        mycur = self.GetCursor()
        self.setMyCursor(self.stockCursor1)
        if not self.chkByNode.IsChecked():
            self.LoadAllDatastreams()
        imgBox = imgAssociation(self)
        imgBox.setParameters(self.wximgMap,self.nrs_datastream_pictures,self.datastreamslist,self.imgFileName, self.imgFilePath,settings.database,self.wxMinDatetime_at,self.wxMaxDatetime_at, self.EnvDir)        
        self.setMyCursor(mycur)
        imgBox.ShowModal()
        imgBox.Destroy()
        self.LoadDatastreamPictures()
        self.LoadFilenames(self.nodeselected_id)
        event.Skip()

    def OnDateFromDateChanged(self, event):
        idx = self.listCtrlDatapoint.GetFirstSelected()
        if idx == -1:
            idx=0
            self.listCtrlDatapoint.Select(idx)            
        if self.listCtrlDatapoint.GetItemCount() > 0:
            self.ProcessImage(idx)     
        sAt_from , sAt_to = self.GetDatapointDatetimeLimits()
        valChck = self.chkDataFilter.IsChecked()
        if not valChck:
            sAt_from = None
            sAt_to = None
        self.LoadDistinctDatastreamUpdated2(self.nodeselected_id,sAt_from,sAt_to)
        self.listCtrlDatapoint.Select(idx)
        event.Skip()

    def OnDateToDateChanged(self, event):
        idx = self.listCtrlDatapoint.GetFirstSelected()
        if idx == -1:
            idx=0
            self.listCtrlDatapoint.Select(idx)            
        if self.listCtrlDatapoint.GetItemCount() > 0:
            self.ProcessImage(idx)     
        sAt_from , sAt_to = self.GetDatapointDatetimeLimits()
        valChck = self.chkDataFilter.IsChecked()
        if not valChck:
            sAt_from = None
            sAt_to = None
        self.LoadDistinctDatastreamUpdated2(self.nodeselected_id,sAt_from,sAt_to)
        self.listCtrlDatapoint.Select(idx)
        event.Skip()

    def OnChkDataFilterCheckbox(self, event):
        idx = self.listCtrlDatapoint.GetFirstSelected()
        if idx == -1:
            idx=0
            self.listCtrlDatapoint.Select(idx)            
        if self.listCtrlDatapoint.GetItemCount() > 0:
            self.ProcessImage(idx)     
        sAt_from , sAt_to = self.GetDatapointDatetimeLimits()
        valChck = self.chkDataFilter.IsChecked()
        if not valChck:
            sAt_from = None
            sAt_to = None
        self.LoadDistinctDatastreamUpdated2(self.nodeselected_id,sAt_from,sAt_to)
        self.listCtrlDatapoint.Select(idx)
        event.Skip()
    
    def GetDatapointDatetimeLimits(self):
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
        return sAt_from, sAt_to
    
    def GetAdminDatetimeLimits(self):
        sDtFrom = self.datePickerCtrl1.GetValue().Format('%Y-%m-%d')
        sDtTo = self.datePickerCtrl2.GetValue().Format('%Y-%m-%d')
        sHHFrom = "00"
        sMMFrom = "00"
        sSSFrom = "00"
        sHHTo = "23"
        sMMTo = "59"
        sSSTo = "59"
        sAt_from = "%s %s:%s:%s" % (sDtFrom,sHHFrom,sMMFrom,sSSFrom)
        sAt_to = "%s %s:%s:%s" % (sDtTo,sHHTo,sMMTo,sSSTo)
        return sAt_from, sAt_to

    def OnDatePickerCtrl1DateChanged(self, event):
        self.CheckDB()
        event.Skip()

    def OnDatePickerCtrl2DateChanged(self, event):
        self.CheckDB()
        event.Skip()

    def OnCheckBox1Checkbox(self, event):
        valChck = self.checkBox1.IsChecked()
        if valChck:
            self.checkBox2.SetValue(True)
        self.CheckDB()
        event.Skip()

    def OnCheckBox2Checkbox(self, event):
        self.CheckDB()
        event.Skip()

    def OnBtnDeleteAdminButton(self, event):
        sAt_from , sAt_to = self.GetAdminDatetimeLimits() 
        sDataFiltering = " WHERE updated >= '%s' AND updated <= '%s'" % ( sAt_from , sAt_to )
        # delete datastream adn datapoint
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        valChck = self.checkBox1.IsChecked()
        if valChck:
            sQuery = """
                DELETE 
                FROM nrs_datastream %s 
            """  % sDataFiltering
            retVal = db_cur.execute(sQuery)
            sQuery = """
                DELETE 
                FROM nrs_datapoint %s 
            """  % sDataFiltering
            retVal = db_cur.execute(sQuery) 
            db_conn.commit()
        valChck = self.checkBox2.IsChecked()
        if valChck:
            # delete only datapoint
            sQuery = """
                DELETE 
                FROM nrs_datapoint %s 
            """  % sDataFiltering
            retVal = db_cur.execute(sQuery)
            db_conn.commit()
        db_conn.close()
        self.CheckDB()
        event.Skip()

    def OnNotebook1NotebookPageChanged(self, event):
        idx = event.GetSelection()
        if idx == 0:
            self.selected_entity = 1
        if idx == 1:
            self.selected_entity = 2
        if idx == 2:
            self.selected_entity = 3
        if idx == 3:
            self.selected_entity = 4
        if idx == 4:
            self.selected_entity = 5
        event.Skip()

    def OnNotebook1NotebookPageChanging(self, event):
        event.Skip()

    def OnBtnTestButton(self, event):    
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        sIP= self.txtIP.GetValue()
        sPort1= self.txtPort1.GetValue()
        sPort2= self.txtport2.GetValue()
        bValidate = True
        splittedIp = sIP.split('.')
        self.btnLista.Enabled = False
        self.btnSavePERI_SAM.Enabled = False
        self.btnACQUSTOP.Enabled = False
        self.btnACQUSTART.Enabled = False
        self.btnCanellaTutto.Enabled = False
        self.btnImportSCHE.Enabled = False
        self.btnExportFile.Enabled = False
        self.txtPERIH.Enabled = False
        self.btnIPAD.Enabled = False
        self.txtPERIM.Enabled = False
        self.txtPERIS.Enabled = False
        self.txtSAMP.Enabled = False     
        self.lstDir.Enabled = False   
        if len(splittedIp) !=4:
            bValidate = False
        if not sPort1.isdigit():
            bValidate = False
        if not sPort2.isdigit():
            bValidate = False
        if bValidate:
            self.scpi = SCPICli(sIP,int(sPort1), int(sPort2))
            res = self.scpi.getIDEN()
            if res != None:
                self.txtIDEN.SetValue(res)
                res=self.scpi.getSTAT()
                self.txtStatus.SetValue(res)
                if self.scpi.status == -1:
                    self.txtStatus.SetBackgroundColour(wx.Colour(192, 192, 192));
                if self.scpi.status == 0:
                    self.txtStatus.SetBackgroundColour(wx.Colour(255, 0, 0));
                if self.scpi.status == 1: #ready
                    self.txtStatus.SetBackgroundColour(wx.Colour(0, 255, 0));
                    self.btnLista.Enabled = True
                    self.btnSavePERI_SAM.Enabled = True
                    self.txtPERIH.Enabled = True
                    self.btnIPAD.Enabled = True
                    self.txtPERIM.Enabled = True
                    self.txtPERIS.Enabled = True
                    self.txtSAMP.Enabled = True
                    self.btnACQUSTOP.Enabled = False
                    self.btnACQUSTART.Enabled = True  
                    self.lstDir.Enabled = True   
                    self.btnCanellaTutto.Enabled = True
                    self.retrieveSCPIParm()
                    self.listDirs()
                if self.scpi.status == 2:
                    self.txtStatus.SetBackgroundColour(wx.Colour(255, 0, 255));
                    self.btnACQUSTOP.Enabled = True
                if self.scpi.status == 3:
                    self.txtStatus.SetBackgroundColour(wx.Colour(255, 255, 0));
                    self.btnACQUSTOP.Enabled = True
                if self.scpi.status == 4:
                    self.txtStatus.SetBackgroundColour(wx.Colour(0, 255, 255));
                    self.btnACQUSTOP.Enabled = True
                if self.scpi.status == 5:
                    self.txtStatus.SetBackgroundColour(wx.Colour(255, 165, 0));
                    
                self.txtIDEN.SetBackgroundColour(self.txtStatus.GetBackgroundColour());
                self.setMyCursor(mycur)
            else:
                self.setMyCursor(mycur)
                self.Info("Impossibile connettersi a %s:%s" % (sIP,sPort1))
        else:
            self.setMyCursor(mycur)
            self.Info("Formato dell'indirizzo IP e delle porte NON Valido ")
        self.Refresh()
        event.Skip()
    
    
    def listDirs(self):
        self.lstDir.DeleteAllItems();
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            resItems = self.scpi.getDIRE()
            x=0
            for item in resItems:
                self.lstDir.InsertStringItem(x,item)
                x=x+1

    def retrieveSCPIParm(self):
        res=self.scpi.getPERI()
        splitted = res.split(":")
        if len(splitted) == 3:
            self.txtPERIH.SetValue(splitted[0])
            self.txtPERIM.SetValue(splitted[1])
            self.txtPERIS.SetValue(splitted[2])
        res=self.scpi.getSAMP()
        self.txtSAMP.SetValue(res)

    def OnBtnSavePERI_SAMButton(self, event):
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            mycur = self.GetCursor();
            self.setMyCursor(self.stockCursor1)
            sH = self.txtPERIH.GetValue()
            sM = self.txtPERIM.GetValue()
            sS = self.txtPERIS.GetValue()
            nSampl = self.txtSAMP.GetValue()
            if sH.isdigit() and sM.isdigit() and sS.isdigit() and nSampl.isdigit():
                sOK = self.scpi.setPERI("%d:%d:%d" % (int(sH),int(sM),int(sS)))
                if sOK == 'OK':
                    sOK = self.scpi.setSAMP("%d" % int(nSampl))
                if sOK == 'OK':
                    self.retrieveSCPIParm()
                    self.setMyCursor(mycur)
                    self.Info("Parametri \"Periodo=%d:%d:%d\"\n\"No Campioni=%d\"\nsalvati con successo!" % (int(sH),int(sM),int(sS),int(nSampl)))
                else:
                    self.setMyCursor(mycur)
                    self.Info("Errore durante il salvataggio dei parametri")                    
            else:
                self.setMyCursor(mycur)
                self.Info("Formato dei parametri NON Valido")
        else:
                self.txtPERIH.Enabled = False
                self.txtPERIM.Enabled = False
                self.txtPERIS.Enabled = False
                self.txtSAMP.Enabled = False   
                self.btnIPAD.Enabled = False
                self.btnACQUSTART.Enabled = False
                self.lstDir.Enabled = False   
                self.btnCanellaTutto.Enabled = False
                self.btnImportSCHE.Enabled = False
                self.btnExportFile.Enabled = False
                self.Info("Stato delle centralina NON Valido")
        event.Skip()

    def OnBtnACQUSTARTButton(self, event):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        res=self.scpi.getSTAT()
        if self.scpi.status == 1: 
            res = self.scpi.startSCHEDULE()
            if res == 'OK':
                self.setMyCursor(mycur)
                #self.Info("Schedulazione avviata correttamente")
                self.OnBtnTestButton(event)
            else:
                self.setMyCursor(mycur)
                self.Info("Errore nell'avvio della schedulazione")
        else:
            self.txtPERIH.Enabled = False
            self.txtPERIM.Enabled = False
            self.txtPERIS.Enabled = False
            self.txtSAMP.Enabled = False     
            self.btnACQUSTART.Enabled = False
            self.lstDir.Enabled = False      
            self.btnIPAD.Enabled = False
            self.btnCanellaTutto.Enabled = False
            self.btnImportSCHE.Enabled = False
            self.btnExportFile.Enabled = False
            self.setMyCursor(mycur)
            self.Info("Stato delle centralina NON Valido")
        

    def OnBtnACQUSTOPButton(self, event):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        res=self.scpi.getSTAT()
        if self.scpi.status == 2 or self.scpi.status == 3 or self.scpi.status == 4: 
            res = self.scpi.stopACQU()    
            if res == 'OK':  
                self.setMyCursor(mycur)
                #self.Info("Schedulazione interrotta correttamente")
                self.OnBtnTestButton(event)
            else:
                self.setMyCursor(mycur)
                self.Info("Errore durante l'interruzzione della schedulazione")        
        else:
            self.setMyCursor(mycur)
            self.Info("Stato delle centralina NON Valido")

    def OnBtnListaButton(self, event):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        self.listDirs()
        self.setMyCursor(mycur)
        event.Skip()

    def OnLstDirListItemSelected(self, event):
        idx = event.m_itemIndex
        if idx >= 0 and self.lstDir.GetSelectedItemCount() > 0 :
            self.btnImportSCHE.Enabled = True
            self.btnExportFile.Enabled = True
        event.Skip()

    def OnBtnCanellaTuttoButton(self, event):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            self.scpi.deleteMEMO()
            self.listDirs()
            self.Info("Cancellazione della memoria avvenuta correttamente")
        self.setMyCursor(mycur)
        event.Skip()

    def OnBtnImportSCHEButton(self, event):
        if self.tryDBConnect():
            mycur = self.GetCursor();
            self.setMyCursor(self.stockCursor1)
            retItems = self.getDataFromDevice()
            if len(retItems) > 0:
                gibe2nrs = GibeToNrs(self.e_uid,self.txtCtrlCentralina.GetValue(),self.NodeDir,self.logger)
                gibe2nrs.run_itemlist(retItems)
            else:
                self.Info("Non ci sono dati da esportare")
            self.setMyCursor(mycur)
            self.CheckDB()
            self.Info("Operazione completata, %d campioni importati!" % len(retItems), "Import Data")
            event.Skip()

    def OnBtnExportFileButton(self, event):
        mycur = self.GetCursor();
        self.setMyCursor(self.stockCursor1)
        #retItems = ['1\tadad\tkjlkj\tkjkljh','2\tadad\tkjlkj\tkjkljh','3\tadad\tkjlkj\tkjkljh',]
        retItems = self.getDataFromDevice()
        if len(retItems) > 0:
            csv_file = time.strftime('%Y%m%d%H%M%S')
            sFileName = "scpi_" + csv_file + ".csv"
            sFilePath = self.NodeDir+"/tmp/" + sFileName
            #with open(sFilePath, 'wb') as importcsvfile:
            #    importcsvfile.writelines(retItems)
            self.saveAs(self.NodeDir,sFileName,retItems)
            self.setMyCursor(mycur)
            self.Info("Operazione completata, %d campioni esporati su file!" % len(retItems), "Export data to file")
        else:
            self.setMyCursor(mycur)
            self.Info("Non ci sono dati da esportare")
        event.Skip()
    
    def saveAs(self,dirName,fileName,retItems):
        ret = False
        dlg = wxFileDialog(self, "Save As", dirName, fileName,
                           "CSV Files (*.csv)|*.csv|All Files|*.*", wxSAVE)
        if (dlg.ShowModal() == wxID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.fileSave(dirName,fileName,retItems):
                self.SetTitle("FBG " + " - [" + fileName + "]")
                ret = True
        dlg.Destroy()
        return ret
    
    def fileSave(self,dirName,fileName,retItems):
        try:
            f = file(os.path.join(dirName,fileName), 'w')
            f.writelines(retItems)
            #self.Info("Saved file.")
            f.close()
            return True
        except:
            self.Info("Error in saving file.")
            return False
    
    def getDataFromDevice(self):
        retItems = []
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            nCount = self.lstDir.GetSelectedItemCount()
            if nCount > 0:
                selection = []
                index = self.lstDir.GetFirstSelected()
                itemText = self.lstDir.GetItemText(index)
                items = self.scpi.getDATA(itemText)
                retItems = retItems + items
                selection.append(index)
                while len(selection) != nCount:
                    index = self.lstDir.GetNextSelected(index)
                    itemText = self.lstDir.GetItemText(index)
                    items = self.scpi.getDATA(itemText)
                    retItems = retItems + items
                    selection.append(itemText)        
        return retItems
    
    def tryDBConnect(self):
        s_database_file = self.databaseBrowseButton.GetValue()
        if len(s_database_file) == 0:
            self.Info('Percorso del DATABASE non valido','DB non corretto')
            return False
        settings.database = s_database_file
        try:
            db_conn = sqlite3.connect(settings.database)
            db_cur = db_conn.cursor()
            db_conn.close()
            return True 
        except Exception, e:
            self.Info('something\'s wrong with %s:%d. Exception type is %s' % (self.host, self.port, `e`),'DB non corretto')
            return False

    def OnBtnIPADButton(self, event):
        res = self.scpi.getSTAT()
        if self.scpi.status == 1:
            sIPAD = self.txtNodeIp.GetValue()
            sSM = "255.0.0.0"
            sGW = "0.0.0.0"
            self.scpi.setIPAD(self,sIPAD,sSM,sGW)
            self.Info('Configurazione della scheda di rete della centralina eseguita! Attendere il riavvio','Configurazione di rete')

    def OnChkByNodeCheckbox(self, event):
        self.LoadFilenames(self.nodeselected_id)

    def OnBtnUpdateCodeButton(self, event):
        self.logger.info("Inizio aggiornamento dei codici datastream...")
        if self.chkAllDs.IsChecked():
            self.logger.info("...per tutti i datastream del nodo corrente (%s)" % self.nodeselected_id)
            self.updateAllDatastreamUidByNodeId(self.nodeselected_id)
        else:
            self.logger.info("...per il datastream corrente (%s)" % self.selected_datastream_id)
            self.updateDatastreamUid(self.selected_datastream_id)
        self.logger.info("Aggiornamento dei codici datastream terminato")
        event.Skip()

      
    def updateDatastreamUid(self,ds_id):
        self.logger.info("...per il datastream corrente (%s)" % self.selected_datastream_id)
        dsData = self.GetDatastream(ds_id)
        f_lambda = dsData['lambda']
        node_uid = dsData['node_uid']
        ds_prefix_no = 0
        prefix = "_%02d." % dsData['ds_channell']
        datastream_uid = "%s%s%09.03f" % (node_uid, prefix, f_lambda)
        self.txtDsCode.SetValue(datastream_uid)
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
        sQuery = """
            UPDATE 
            nrs_datastream
            SET
            datastream_uid = '%s',
            updated = '%s'
            WHERE id = %d
        """ % (datastream_uid,sUpdated, ds_id)
        self.logger.info(sQuery)
        retVal = db_cur.execute(sQuery)
        db_conn.commit()
        db_conn.close()
        self.CheckDB()

    def OnChkAllDsCheckbox(self, event):
        event.Skip()
    
    
    def SelectDefaultItems(self):
        iEnvCount = self.listCtrlEnv.GetItemCount()
        iNodeCount = self.listCtrlNode.GetItemCount()
        sFirstNodeCode = settings.environment_name + settings.first_node
        iEnv = 0
        while iEnv < iEnvCount:
            itemEnvData = self.listCtrlEnv.GetItem(iEnv,1).GetText()
            if itemEnvData == settings.environment_name:
                self.listCtrlEnv.Select(iEnv)
            iEnv = iEnv +1
        iNode = 0
        while iNode < iNodeCount:
            itemNodeData = self.listCtrlNode.GetItem(iNode,1).GetText()
            if itemNodeData == sFirstNodeCode:
                self.listCtrlNode.Select(iNode)
            iNode = iNode +1
    
    
    def _getSelectedIndices( self, wxList, state =  wx.LIST_STATE_SELECTED):
        indices = []
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
        return indices
    
    
    def updateAllDatastreamUidByNodeId(self,node_id):
        indices = self._getSelectedIndices(self.listCtrlDatastream)
        sQuery = """
            SELECT  
            nrs_datastream.id
            FROM nrs_datastream
            WHERE  nrs_datastream.nrs_node_id = %d
            ORDER BY nrs_datastream.ch, lambda_value
        """ % node_id
        self.logger.info(sQuery)
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        items=[]
        for row in rows:
            items.append(row[0])
        db_conn.close()
        for item in items:
            self.updateDatastreamUid(item)
        self.listCtrlDatastream.Select(indices[0])

    def OnBtnRandomGenButton(self, event):
        nRandom = int(self.txtNumRandom.GetValue())
        nHH = int(self.txtConfHH.GetValue())
        nMM = int(self.txtConfMM.GetValue())
        nSS = int(self.txtConfSS.GetValue())
        nSamples = int(self.txtConfSamples.GetValue())
        fRandom = float(nRandom)
        fSamples= (nSamples)
        fRate = fRandom / fSamples
        nTotSec = nHH*3600+nMM*60+nSS
        self.Info("Saranno necessarie %d rilevazioni di %d campioni ogni %d secondi" % (fRate,fSamples, nTotSec))
        iCount = 1
        dt_now = datetime.now()
        s_date_now = dt_now.strftime('%d/%m/%Y') #%H%M%S%f
        delta_1 = timedelta(seconds=1)
        delta_t = timedelta(seconds=nTotSec)      
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT   nrs_datastream.title
            , nrs_datastream.constant_value
            , nrs_datastream.lambda_value
            , nrs_datastream.factor_value
            , nrs_datastream.factor_value_2
            , nrs_datastream.ds_formula
            , nrs_datastream.ch
            FROM nrs_datastream 
            WHERE nrs_datastream.nrs_node_id = %d 
            ORDER BY  ch , nrs_datastream.lambda_value 
        """ % self.nodeselected_id
        retVal = db_cur.execute(sQuery)
        rows = retVal.fetchall()
        db_conn.close()
        bulk_export_rows = []
        while nRandom >= iCount:
            if iCount%(nSamples+1) == 0:
                dt_now = dt_now + delta_t
            else:
                dt_now = dt_now + delta_1
            sTmpVal = ""
            csvrow = []
            csvrow.append(s_date_now)
            csvrow.append(dt_now.strftime('%H:%M:%S'))
            for row in rows:
                fTemp = random.uniform(19.8,27.5)
                const = float(row[1]) #constant_value
                lambda_val = float(row[2]) #lambda_value
                first = float(row[3]) #factor_value
                second = float(row[4]) #factor_value_2
                return_value = (fTemp - const) + first*lambda_val
                return_value = return_value/first
                return_value = round(return_value,4)
                csvrow.append("%0.4f" % return_value)
                sTmpVal = "%s\t%0.4f" % (sTmpVal,return_value)
            self.logger.info("%d\t%s\t%s%s" % (iCount,s_date_now,dt_now.strftime('%H:%M:%S'), sTmpVal ))
            bulk_export_rows.append(csvrow)
            iCount = iCount + 1
        sExported = time.strftime('%Y%m%d%H%M%S') #timestamp for unique file name
        sFileName = "export_random_%d_%s.csv" % (self.nodeselected_id,sExported) #filename for the standard export
        sExportFilePath = os.path.join(self.EnvDir,sFileName)
        with open(sExportFilePath,'wb') as exportcsvfile:
            writer = csv.writer(exportcsvfile,delimiter='\t')
            writer.writerows(bulk_export_rows)
        event.Skip()

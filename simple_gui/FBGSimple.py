#Boa:Frame:FBGSimple

import wx
import wx.lib.buttons
import wx.lib.filebrowsebutton
import shutil, sqlite3, time, os, csv
import settings
import logging, os, stat
import time
import ConfigParser
from GibeToNrsWin32_new import GibeToNrs
from scpi_client import SCPICli

def create(parent):
    return FBGSimple(parent)

[wxID_FBGSIMPLE, wxID_FBGSIMPLEBTNACQUSTART, wxID_FBGSIMPLEBTNACQUSTOP, 
 wxID_FBGSIMPLEBTNCANELLATUTTO, wxID_FBGSIMPLEBTNCLOSE, 
 wxID_FBGSIMPLEBTNCONNECT, wxID_FBGSIMPLEBTNEXPORTFILE, 
 wxID_FBGSIMPLEBTNIMPORTSCHE, wxID_FBGSIMPLEBTNIMPOSTASAMPL, 
 wxID_FBGSIMPLEBTNIPAD, wxID_FBGSIMPLEBTNM1, wxID_FBGSIMPLEBTNM2, 
 wxID_FBGSIMPLEBTNM3, wxID_FBGSIMPLEBTNM4, wxID_FBGSIMPLEBTNSALVADB, 
 wxID_FBGSIMPLELSTDIR, wxID_FBGSIMPLESTATICTEXT20, wxID_FBGSIMPLESTATICTEXT21, 
 wxID_FBGSIMPLETXTIDEN, wxID_FBGSIMPLETXTIP, wxID_FBGSIMPLETXTPERIH, 
 wxID_FBGSIMPLETXTPERIM, wxID_FBGSIMPLETXTPERIS, wxID_FBGSIMPLETXTPORT1, 
 wxID_FBGSIMPLETXTPORT2, wxID_FBGSIMPLETXTSAMP, wxID_FBGSIMPLETXTSTATUS, 
] = [wx.NewId() for _init_ctrls in range(27)]

class FBGSimple(wx.Frame):
    def _init_coll_lstDir_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Memoria', width=72)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FBGSIMPLE, name=u'FBGSimple',
              parent=prnt, pos=wx.Point(522, 179), size=wx.Size(472, 383),
              style=wx.DEFAULT_FRAME_STYLE, title=u'FBG Importer')
        self.SetClientSize(wx.Size(456, 345))

        self.btnM1 = wx.lib.buttons.GenToggleButton(id=wxID_FBGSIMPLEBTNM1,
              label=u'M1', name=u'btnM1', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(101, 64), style=0)
        self.btnM1.SetToggle(False)
        self.btnM1.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.btnM1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.btnM1.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnM1.Bind(wx.EVT_BUTTON, self.OnBtnM1Button,
              id=wxID_FBGSIMPLEBTNM1)

        self.btnM2 = wx.lib.buttons.GenToggleButton(id=wxID_FBGSIMPLEBTNM2,
              label=u'M2', name=u'btnM2', parent=self, pos=wx.Point(120, 8),
              size=wx.Size(101, 64), style=0)
        self.btnM2.SetToggle(False)
        self.btnM2.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.btnM2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.btnM2.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnM2.Bind(wx.EVT_BUTTON, self.OnBtnM2Button,
              id=wxID_FBGSIMPLEBTNM2)

        self.btnM3 = wx.lib.buttons.GenToggleButton(id=wxID_FBGSIMPLEBTNM3,
              label=u'M3', name=u'btnM3', parent=self, pos=wx.Point(232, 8),
              size=wx.Size(101, 64), style=0)
        self.btnM3.SetToggle(False)
        self.btnM3.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.btnM3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.btnM3.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnM3.Bind(wx.EVT_BUTTON, self.OnBtnM3Button,
              id=wxID_FBGSIMPLEBTNM3)

        self.btnM4 = wx.lib.buttons.GenToggleButton(id=wxID_FBGSIMPLEBTNM4,
              label=u'M4', name=u'btnM4', parent=self, pos=wx.Point(344, 8),
              size=wx.Size(101, 64), style=0)
        self.btnM4.SetToggle(False)
        self.btnM4.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.btnM4.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.btnM4.SetHelpText(u'')
        self.btnM4.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnM4.Bind(wx.EVT_BUTTON, self.OnBtnM4Button,
              id=wxID_FBGSIMPLEBTNM4)

        self.txtPERIH = wx.TextCtrl(id=wxID_FBGSIMPLETXTPERIH, name=u'txtPERIH',
              parent=self, pos=wx.Point(83, 109), size=wx.Size(29, 21), style=0,
              value=u'')
        self.txtPERIH.SetEditable(True)
        self.txtPERIH.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIH.SetMaxLength(2)
        self.txtPERIH.Enable(False)

        self.txtPERIM = wx.TextCtrl(id=wxID_FBGSIMPLETXTPERIM, name=u'txtPERIM',
              parent=self, pos=wx.Point(115, 109), size=wx.Size(29, 21),
              style=0, value=u'')
        self.txtPERIM.SetEditable(True)
        self.txtPERIM.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIM.SetMaxLength(2)
        self.txtPERIM.Enable(False)

        self.txtPERIS = wx.TextCtrl(id=wxID_FBGSIMPLETXTPERIS, name=u'txtPERIS',
              parent=self, pos=wx.Point(147, 109), size=wx.Size(29, 21),
              style=0, value=u'')
        self.txtPERIS.SetEditable(True)
        self.txtPERIS.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtPERIS.SetMaxLength(2)
        self.txtPERIS.Enable(False)

        self.txtSAMP = wx.TextCtrl(id=wxID_FBGSIMPLETXTSAMP, name=u'txtSAMP',
              parent=self, pos=wx.Point(251, 109), size=wx.Size(50, 21),
              style=0, value=u'')
        self.txtSAMP.SetEditable(True)
        self.txtSAMP.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.txtSAMP.SetMaxLength(4)
        self.txtSAMP.Enable(False)

        self.staticText21 = wx.StaticText(id=wxID_FBGSIMPLESTATICTEXT21,
              label=u'N\xb0 Campioni', name='staticText21', parent=self,
              pos=wx.Point(186, 112), size=wx.Size(59, 13), style=0)

        self.staticText20 = wx.StaticText(id=wxID_FBGSIMPLESTATICTEXT20,
              label=u'Periodo H:M:S', name='staticText20', parent=self,
              pos=wx.Point(10, 112), size=wx.Size(69, 13), style=0)

        self.txtIP = wx.TextCtrl(id=wxID_FBGSIMPLETXTIP, name=u'txtIP',
              parent=self, pos=wx.Point(304, 80), size=wx.Size(58, 21), style=0,
              value=u'')

        self.txtPort1 = wx.TextCtrl(id=wxID_FBGSIMPLETXTPORT1, name=u'txtPort1',
              parent=self, pos=wx.Point(365, 80), size=wx.Size(36, 21), style=0,
              value=u'')

        self.txtport2 = wx.TextCtrl(id=wxID_FBGSIMPLETXTPORT2, name=u'txtport2',
              parent=self, pos=wx.Point(404, 80), size=wx.Size(36, 21), style=0,
              value=u'')

        self.txtStatus = wx.TextCtrl(id=wxID_FBGSIMPLETXTSTATUS,
              name=u'txtStatus', parent=self, pos=wx.Point(8, 80),
              size=wx.Size(109, 21), style=0, value=u'')
        self.txtStatus.SetEditable(False)
        self.txtStatus.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.txtIDEN = wx.TextCtrl(id=wxID_FBGSIMPLETXTIDEN, name=u'txtIDEN',
              parent=self, pos=wx.Point(120, 80), size=wx.Size(181, 21),
              style=0, value=u'')
        self.txtIDEN.SetEditable(False)
        self.txtIDEN.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.btnACQUSTART = wx.Button(id=wxID_FBGSIMPLEBTNACQUSTART,
              label=u'Avvia Sched.', name=u'btnACQUSTART', parent=self,
              pos=wx.Point(194, 138), size=wx.Size(126, 23), style=0)
        self.btnACQUSTART.Enable(False)
        self.btnACQUSTART.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnACQUSTART.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnACQUSTART.Bind(wx.EVT_BUTTON, self.OnBtnACQUSTARTButton,
              id=wxID_FBGSIMPLEBTNACQUSTART)

        self.btnACQUSTOP = wx.Button(id=wxID_FBGSIMPLEBTNACQUSTOP,
              label=u'Ferma Acquisizione', name=u'btnACQUSTOP', parent=self,
              pos=wx.Point(322, 138), size=wx.Size(126, 23), style=0)
        self.btnACQUSTOP.Enable(False)
        self.btnACQUSTOP.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnACQUSTOP.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnACQUSTOP.Bind(wx.EVT_BUTTON, self.OnBtnACQUSTOPButton,
              id=wxID_FBGSIMPLEBTNACQUSTOP)

        self.btnConnect = wx.Button(id=wxID_FBGSIMPLEBTNCONNECT,
              label=u'Connetti', name=u'btnConnect', parent=self,
              pos=wx.Point(322, 109), size=wx.Size(126, 23), style=0)
        self.btnConnect.Enable(False)
        self.btnConnect.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnConnect.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnConnect.Bind(wx.EVT_BUTTON, self.OnBtnConnectButton,
              id=wxID_FBGSIMPLEBTNCONNECT)

        self.btnImpostaSampl = wx.Button(id=wxID_FBGSIMPLEBTNIMPOSTASAMPL,
              label=u'Imposta Periodo e N\xb0 Campioni',
              name=u'btnImpostaSampl', parent=self, pos=wx.Point(10, 138),
              size=wx.Size(182, 23), style=0)
        self.btnImpostaSampl.Enable(False)
        self.btnImpostaSampl.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.btnImpostaSampl.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnImpostaSampl.Bind(wx.EVT_BUTTON, self.OnBtnImpostaSampling,
              id=wxID_FBGSIMPLEBTNIMPOSTASAMPL)

        self.btnCanellaTutto = wx.Button(id=wxID_FBGSIMPLEBTNCANELLATUTTO,
              label=u'Cancella Memoria', name=u'btnCanellaTutto', parent=self,
              pos=wx.Point(138, 164), size=wx.Size(150, 52), style=0)
        self.btnCanellaTutto.Enable(False)
        self.btnCanellaTutto.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.btnCanellaTutto.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.btnCanellaTutto.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnCanellaTutto.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.btnCanellaTutto.Bind(wx.EVT_BUTTON, self.OnBtnCanellaTuttoButton,
              id=wxID_FBGSIMPLEBTNCANELLATUTTO)

        self.btnIPAD = wx.Button(id=wxID_FBGSIMPLEBTNIPAD,
              label=u'Imposta indirizzo IP', name=u'btnIPAD', parent=self,
              pos=wx.Point(298, 164), size=wx.Size(150, 52), style=0)
        self.btnIPAD.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.btnIPAD.SetForegroundColour(wx.Colour(255, 255, 255))
        self.btnIPAD.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'Tahoma'))
        self.btnIPAD.Enable(False)
        self.btnIPAD.Bind(wx.EVT_BUTTON, self.OnBtnIPADButton,
              id=wxID_FBGSIMPLEBTNIPAD)

        self.btnClose = wx.Button(id=wxID_FBGSIMPLEBTNCLOSE, label=u'Chiudi',
              name=u'btnClose', parent=self, pos=wx.Point(298, 284),
              size=wx.Size(150, 52), style=0)
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FBGSIMPLEBTNCLOSE)

        self.btnImportSCHE = wx.Button(id=wxID_FBGSIMPLEBTNIMPORTSCHE,
              label=u'Importa misure nel DB', name=u'btnImportSCHE',
              parent=self, pos=wx.Point(138, 224), size=wx.Size(150, 52),
              style=0)
        self.btnImportSCHE.Enable(False)
        self.btnImportSCHE.Bind(wx.EVT_BUTTON, self.OnBtnImportSCHEButton,
              id=wxID_FBGSIMPLEBTNIMPORTSCHE)

        self.btnExportFile = wx.Button(id=wxID_FBGSIMPLEBTNEXPORTFILE,
              label=u'Esporta misure su file', name=u'btnExportFile',
              parent=self, pos=wx.Point(298, 224), size=wx.Size(150, 52),
              style=0)
        self.btnExportFile.Enable(False)
        self.btnExportFile.Bind(wx.EVT_BUTTON, self.OnBtnExportFileButton,
              id=wxID_FBGSIMPLEBTNEXPORTFILE)

        self.lstDir = wx.ListCtrl(id=wxID_FBGSIMPLELSTDIR, name=u'lstDir',
              parent=self, pos=wx.Point(10, 164), size=wx.Size(122, 172),
              style=wx.LC_REPORT)
        self.lstDir.Enable(False)
        self._init_coll_lstDir_Columns(self.lstDir)
        self.lstDir.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnLstDirListItemSelected, id=wxID_FBGSIMPLELSTDIR)

        self.btnSalvaDB = wx.Button(id=wxID_FBGSIMPLEBTNSALVADB,
              label=u'Salva copia DB', name=u'btnSalvaDB', parent=self,
              pos=wx.Point(138, 284), size=wx.Size(150, 52), style=0)
        self.btnSalvaDB.Bind(wx.EVT_BUTTON, self.OnBtnSalvaDBButton,
              id=wxID_FBGSIMPLEBTNSALVADB)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.cfg = ConfigParser.ConfigParser()
        res = self.cfg.read('settings.conf')
        settings.gibedatafolder_path = self.cfg.get('Common','gibedatafolder_path')
        settings.gibelogfile_path = self.cfg.get('Common','gibelogfile_path')
        settings.gibeimportfolder_path = self.cfg.get('Common','gibeimportfolder_path')
        settings.database = self.cfg.get('Common','database')
        if self.checkSettings():
            self.logger = logging.getLogger("FBGSimpleAppLog")
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler = logging.FileHandler(settings.gibelogfile_path)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.info("FBGSimpleWXApp Started on %s" % settings.gibeimportfolder_path)
            self.checkDB()
            
        
    def checkSettings(self):
        if not os.path.isdir(settings.gibedatafolder_path):
            self.Error("La cartella %s non esiste.\n Configurazione sbagliata, verificare il file settings.conf" % settings.gibedatafolder_path)
            return False
        if not os.path.isdir(settings.gibeimportfolder_path):
            self.Error("La cartella %s non esiste.\n Configurazione sbagliata, verificare il file settings.conf" % settings.gibeimportfolder_path)    
            return False
        if not os.path.isfile(settings.database):
            self.Error("Il file %s non esiste.\n Configurazione sbagliata, verificare il file settings.conf" % settings.database)
            return False
        return True
    
    def checkDB(self):
        self.logger.info("CheckDB...starting")
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT count(*) as cnt, max(updated)
            FROM nrs_environment
        """
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = row[0]   
            self.logger.info("DB %s ok!" % settings.database)
        else:
            return_value = 0
            self.logger.error("CheckDB query=%s, nothing found!" % sQuery)
            self.Error("Sembra che il DB sia vuoto!")
        self.logger.info("CheckDB terminated")
    
    def GetNode(self,uid):
        return_value = {}         
        db_conn = sqlite3.connect(settings.database)
        db_cur = db_conn.cursor()
        sQuery = """
            SELECT nrs_node.id, nrs_node.title, nrs_node.node_uid, nrs_node.updated, nrs_node.ipaddress, portin, portout, confhh, confmm, confss, confsamples, nrs_environment.environment_uid, nrs_environment.id
            FROM nrs_node
            JOIN nrs_environment ON nrs_environment.id = nrs_node.nrs_environment_id
            WHERE node_uid = '%s'
        """ % uid
        retVal = db_cur.execute(sQuery)
        row = retVal.fetchone()  
        if row:
            return_value = {'id':row[0],'title':row[1],'node_uid':row[2],'updated':row[3],'ipaddress':row[4],'portin':row[5],'portout':row[6],'hh':row[7],'mm':row[8],'ss':row[9],'samp':row[10],'e_uid':row[11],'e_id':row[12]} 
        db_conn.close()
        return return_value
    
    def setNodeData(self, nodedata):
        self.nodedata = nodedata
        nodeuid = self.nodedata['node_uid']
        envuid = self.nodedata['e_uid']
        nodedir = nodeuid[len(envuid):]
        nodedir = os.path.join(settings.gibeimportfolder_path,nodedir)
        if not os.path.exists(nodedir):
            os.mkdir(nodedir)
        self.nodedata['node_dir'] = nodedir
        self.logger.info("Getting node data for node %s with id %d" % (nodedata['title'],nodedata['id']))
        self.txtIP.SetValue(nodedata['ipaddress'])
        self.txtPERIH.SetValue(nodedata['hh'])
        self.txtPERIM.SetValue(nodedata['mm'])
        self.txtPERIS.SetValue(nodedata['ss'])
        self.txtPort1.SetValue(nodedata['portin'])
        self.txtport2.SetValue(nodedata['portout'])
        self.txtSAMP.SetValue(nodedata['samp'])
        self.SetTitle("FBG Importer (%s)" % nodedata['title'] )
        self.btnConnect.Enable(True)
    
    def clearNodeData(self):
        self.btnConnect.Enable(False)
        self.txtIP.Clear()
        self.txtPERIH.Clear()
        self.txtPERIM.Clear()
        self.txtPERIS.Clear()
        self.txtPort1.Clear()
        self.txtport2.Clear()
        self.txtSAMP.Clear()
        self.txtIDEN.Clear()
        self.txtStatus.Clear()
        self.SetTitle("FBG Importer"  )
        self.setDefaultsBeforeConnect()

    
    def OnBtnM1Button(self, event):
        self.clearNodeData()
        if self.btnM1.GetToggle() == True:
            self.btnM2.SetToggle(False)
            self.btnM3.SetToggle(False)
            self.btnM4.SetToggle(False)
            nodedata = self.GetNode("GIBE3M1")
            if nodedata:
                self.setNodeData(nodedata)
            else:
                self.logger.error("GetNode on GIBE3M1 failed!")
                self.Error("Impossibile recuperare i dati della centralina M1")

    def OnBtnM2Button(self, event):
        self.clearNodeData()
        if self.btnM2.GetToggle() == True:
            self.btnM1.SetToggle(False)
            self.btnM3.SetToggle(False)
            self.btnM4.SetToggle(False)
            nodedata = self.GetNode("GIBE3M2")
            if nodedata:
                self.setNodeData(nodedata)
            else:
                self.logger.error("GetNode on GIBE3M2 failed!")
                self.Error("IMpossibile recuperare i dati della centralina M2")

    def OnBtnM3Button(self, event):
        self.clearNodeData()
        if self.btnM3.GetToggle() == True:
            self.btnM2.SetToggle(False)
            self.btnM1.SetToggle(False)
            self.btnM4.SetToggle(False)
            nodedata = self.GetNode("GIBE3M3")
            if nodedata:
                self.setNodeData(nodedata)
            else:
                self.logger.error("GetNode on GIBE3M3 failed!")
                self.Error("Impossibile recuperare i dati della centralina M3")

    def OnBtnM4Button(self, event):
        self.clearNodeData()
        if self.btnM4.GetToggle() == True:
            self.btnM2.SetToggle(False)
            self.btnM3.SetToggle(False)
            self.btnM1.SetToggle(False)
            nodedata = self.GetNode("GIBE3M4")
            if nodedata:
                self.setNodeData(nodedata)
            else:
                self.logger.error("GetNode on GIBE3M4 failed!")
                self.Error("Impossibile recuperare i dati della centralina M4")


    def OnBtnImpostaSampling(self, event):
        mycur = self.GetCursor();
        self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
        sH = self.txtPERIH.GetValue()
        sM = self.txtPERIM.GetValue()
        sS = self.txtPERIS.GetValue()
        nSampl = self.txtSAMP.GetValue()
        self.setPeriodAndSamplig(sH,sM,sS,nSampl)
        self.SetCursor(mycur)

    def OnBtnACQUSTARTButton(self, event):
        mycur = self.GetCursor();
        self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
        self.startSampling()
        self.SetCursor(mycur)

    def OnBtnACQUSTOPButton(self, event):
        mycur = self.GetCursor();
        self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
        self.stopSampling()
        self.SetCursor(mycur)
        
    def Info(parent, message, caption = 'Notifica'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
         
    def Error(parent, message, caption = 'Errore'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def Confirm(parent, message, caption = 'Conferma'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        bRet = False
        if result == wx.ID_OK:
            bRet = True
        return bRet

    def OnBtnConnectButton(self, event):
        self.logger.info("OnBtnConnectButton starting...")
        self.setDefaultsBeforeConnect()
        sIP= self.txtIP.GetValue()
        sPort1= self.txtPort1.GetValue()
        sPort2= self.txtport2.GetValue()
        splittedIp = sIP.split('.')
        if len(splittedIp) !=4:
            self.logger.error("OnBtnConnectButton, wrong IP address format (%s)" % sIP )
            self.Error("Indirizzo IP con formato errato (%s)" % sIP)
        else:
            mycur = self.GetCursor();
            self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
            self.scpi = SCPICli(sIP,int(sPort1), int(sPort2))
            res = self.scpi.getIDEN()
            if res != None:
                self.txtIDEN.SetValue(res)
                res=self.scpi.getSTAT()
                self.logger.info("Successfully connected to %s:%s" % (sIP,sPort1))
                self.txtStatus.SetValue(res)
                self.setWidgetsOnStatus(self.scpi.status)
                self.SetCursor(mycur)
            else:
                self.SetCursor(mycur)
                self.Info("Impossibile connettersi a %s:%s" % (sIP,sPort1))
                self.logger.error("Connection not available on %s:%s" % (sIP,sPort1))
        self.logger.info("OnBtnConnectButton terminated!")

    def checkScpiStat(self):
        self.setDefaultsBeforeConnect()
        res = self.scpi.getIDEN()
        if res != None:
            self.txtIDEN.SetValue(res)
            res=self.scpi.getSTAT()
            self.txtStatus.SetValue(res)
            self.setWidgetsOnStatus(self.scpi.status)

    def setDefaultsBeforeConnect(self):
        self.txtStatus.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.txtIDEN.SetBackgroundColour(wx.Colour(192, 192, 192));
        self.btnImpostaSampl.Enabled = False
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
        self.lstDir.DeleteAllItems();   
        self.lstDir.Enabled = False
        self.txtIDEN.Refresh()
        self.txtStatus.Refresh()
    
    def setWidgetsOnStatus(self, status):
        if status == -1:
            self.txtStatus.SetBackgroundColour(wx.Colour(192, 192, 192));
            self.txtIDEN.SetBackgroundColour(wx.Colour(192, 192, 192));
        if status == 0:
            self.txtStatus.SetBackgroundColour(wx.Colour(255, 0, 0));
            self.txtIDEN.SetBackgroundColour(wx.Colour(255, 0, 0));
        if status == 1: #ready
            self.txtStatus.SetBackgroundColour(wx.Colour(0, 255, 0));
            self.txtIDEN.SetBackgroundColour(wx.Colour(0, 255, 0));
            self.btnImpostaSampl.Enabled = True
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
        if status == 2:
            self.txtStatus.SetBackgroundColour(wx.Colour(255, 0, 255));
            self.txtIDEN.SetBackgroundColour(wx.Colour(255, 0, 255));
            self.btnACQUSTOP.Enabled = True
        if status == 3:
            self.txtStatus.SetBackgroundColour(wx.Colour(255, 255, 0));
            self.txtIDEN.SetBackgroundColour(wx.Colour(255, 255, 0));
            self.btnACQUSTOP.Enabled = True
        if status == 4:
            self.txtStatus.SetBackgroundColour(wx.Colour(0, 255, 255));
            self.txtIDEN.SetBackgroundColour(wx.Colour(0, 255, 255));
            self.btnACQUSTOP.Enabled = True
        if status == 5:
            self.txtStatus.SetBackgroundColour(wx.Colour(255, 165, 0));
            self.txtIDEN.SetBackgroundColour(wx.Colour(255, 165, 0));
        self.txtIDEN.Refresh()
        self.txtStatus.Refresh()
        
    def retrieveSCPIParm(self):
        res=self.scpi.getPERI()
        splitted = res.split(":")
        if len(splitted) == 3:
            self.txtPERIH.SetValue(splitted[0])
            self.txtPERIM.SetValue(splitted[1])
            self.txtPERIS.SetValue(splitted[2])
        res=self.scpi.getSAMP()
        self.txtSAMP.SetValue(res)

    def setPeriodAndSamplig(self,sH,sM,sS,nSampl):
        if sH.isdigit() and sM.isdigit() and sS.isdigit() and nSampl.isdigit():
            sOK = self.scpi.setPERI("%d:%d:%d" % (int(sH),int(sM),int(sS)))
            if sOK == 'OK':
                sOK = self.scpi.setSAMP("%d" % int(nSampl))
            if sOK == 'OK':
                self.retrieveSCPIParm()
                self.Info("Parametri \"Periodo=%d:%d:%d\"\n\"No Campioni=%d\"\nsalvati con successo!" % (int(sH),int(sM),int(sS),int(nSampl)))
                self.logger.info("Setting of sampling parameters succedeed: H:M:S=%s:%s:%s, Samples No=%s" % (sH,sM,sS,nSampl))
            else:
                self.Info("Errore durante il salvataggio dei parametri")                    
        else:
            self.Error("Formato dei parametri NON Valido")
            self.logger.error("Invalid sampling parameters: H:M:S=%s:%s:%s, Samples No=%s" % (sH,sM,sS,nSampl))

    def stopSampling(self):
        res = self.scpi.stopACQU()    
        if res == 'OK':            
            self.logger.info("scpi ACQU stopped!")
            self.checkScpiStat()            
        else:
            self.Info("Errore durante l'interruzione della schedulazione")  

    def startSampling(self):
        res = self.scpi.startSCHEDULE()
        if res == 'OK':              
            self.logger.info("Starting scpi SCHEDULE...")
            self.checkScpiStat()            
        else:
            self.Info("Errore nell'avvio della schedulazione")

    def OnBtnCanellaTuttoButton(self, event):
        bOk = self.Confirm("Sei sicuro di voler cancellare la memoria della centralina?")
        if bOk:
            mycur = self.GetCursor();
            self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
            self.clearMemory()
            self.SetCursor(mycur)

    def clearMemory(self):
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            self.scpi.deleteMEMO()        
            self.logger.info("scpi delete MEMO completed!")
            self.Info("Cancellazione della memoria avvenuta correttamente", "Cancellazione Memoria")

    def OnBtnIPADButton(self, event):
        sIPAD = self.txtIP.GetValue()
        bOk = self.Confirm("Sei sicuro di voler cambiare \nl'indirizzo IP in %s?" % sIPAD)
        if bOk:
            mycur = self.GetCursor();
            self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
            self.setIPAddress(sIPAD)
            self.SetCursor(mycur)

    def setIPAddress(self,sIPAD):
        res = self.scpi.getSTAT()
        if self.scpi.status == 1:
            sSM = "255.0.0.0"
            sGW = "0.0.0.0"
            self.scpi.setIPAD(sIPAD,sSM,sGW)
            self.logger.info("Network configuration has been modified: %s %s %s" % (sIPAD,sSM,sGW))
            self.Info('Configurazione della scheda di rete della centralina eseguita! Attendere il riavvio','Configurazione di rete')

    def OnBtnCloseButton(self, event):
        self.logger.info("FBGSimpleWXApp is shutting down!")
        self.Destroy()

    def OnBtnImportSCHEButton(self, event):
        bOk = self.Confirm("Sei sicuro di voler importare \ni dati delle %d cartelle selezionate nel DB?" % self.lstDir.GetSelectedItemCount())
        if bOk:
            mycur = self.GetCursor();
            self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
            i_samples, num_items = self.importDataFromSelectedListDir()
            self.logger.info("Data import completed, %d/%d samples imported!" % (i_samples,num_items))
            self.Info("Operazione completata, %d campioni importati su totali %d!" % (i_samples,num_items), "Import Data")
            self.SetCursor(mycur)

    def OnBtnExportFileButton(self, event):
        bOk = self.Confirm("Sei sicuro di voler esportare su file\ni dati delle %d cartelle selezionate?" % self.lstDir.GetSelectedItemCount())
        if bOk:
            mycur = self.GetCursor();
            self.SetCursor(wx.StockCursor(id=wx.CURSOR_WAIT))
            num_items, sFilename = self.exportDataFromSelectedListDir()
            self.logger.info("Data export completed, %d samples exported to %s!" % (num_items,sFilename))
            self.Info("Operazione completata, %d campioni esportati sul file\n%s!" % (num_items,sFilename), "Export Data")
            self.SetCursor(mycur)

    def OnLstDirListItemSelected(self, event):
        self.btnImportSCHE.Enabled = True
        self.btnExportFile.Enabled = True
    
    def listDirs(self):
        self.logger.info("Starting scpi listDirs...")
        self.lstDir.DeleteAllItems();
        res=self.scpi.getSTAT()
        if self.scpi.status == 1:
            resItems = self.scpi.getDIRE()
            x=0
            for item in resItems:
                self.lstDir.InsertStringItem(x,item.strip())
                self.logger.info("scpi DIRE %s" % item.strip())
                x=x+1
        self.logger.info("scpi listDirs terminated")


    def getDataFromDevice(self, dir_items): 
        self.logger.info("Starting getDataFromDevice...")
        retItems = []
        res = self.scpi.getSTAT()
        if self.scpi.status == 1:
            for dir_item in dir_items:
                items = self.scpi.getDATA(dir_item.strip())
                self.logger.info("getDataFromDevice: scpi DATA retrieved for %s folder, tot items = %d" % (dir_item,len(items)))
                retItems = retItems + items
        self.logger.info("getDataFromDevice Terminated!")
        return retItems
    
    
    def getDataFromSelectedListDir(self):
        idxes, ids = self._getSelectedIndices(self.lstDir)
        dir_items = []
        for idx in idxes:
            itemText = self.lstDir.GetItemText(idx)
            dir_items.append(itemText.strip())
        retItems = self.getDataFromDevice(dir_items)
        return retItems
    
    def importDataFromSelectedListDir(self):
        iSamples = 0
        retItems = self.getDataFromSelectedListDir()
        if len(retItems) > 0:
            gibe2nrs = GibeToNrs(self.nodedata['e_uid'],self.nodedata['node_uid'],self.nodedata['node_dir'],self.logger,self.nodedata['id'])
            iSamples = gibe2nrs.import_itemlist(retItems)
        return iSamples, len(retItems)        
    
    
    def exportDataFromSelectedListDir(self):
        retItems = self.getDataFromSelectedListDir()
        sFilePath = "ND"
        if len(retItems) > 0:
            csv_file = time.strftime('%Y%m%d%H%M%S')
            sFileName = "scpi_" + csv_file + ".csv"
            sFilePath = os.path.join( self.nodedata['node_dir'], sFileName)
            sFilePath = self.saveAs(self.nodedata['node_dir'],sFileName,retItems)
        return len(retItems) , sFilePath
    
    
    def saveAs(self,dirName,fileName,retItems):
        ret = ""
        dlg = wx.FileDialog(self, "Save As", dirName, fileName,
                           "CSV Files (*.csv)|*.csv|All Files|*.*", wx.FD_SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.fileSave(dirName,fileName,retItems):
                ret = os.path.join(dirName, fileName)
        dlg.Destroy()
        return ret
    
    def fileSave(self,dirName,fileName,retItems):
        try:
            f = file(os.path.join(dirName,fileName), 'w')
            f.writelines(retItems)
            f.close()
            return True
        except:
            self.Info("Error in saving file %s." % os.path.join(dirName,fileName))
            return False
        
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

    def OnBtnSalvaDBButton(self, event):
        dirName = settings.gibeimportfolder_path
        fileName = os.path.basename(settings.database)
        fileName = "copy_" + fileName
        dlg = wx.FileDialog(self, "Save As", dirName, fileName,
                           "DB Files (*.db)|*.db|All Files|*.*", wx.FD_SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.dbSave(dirName,fileName):
                ret = True
        dlg.Destroy()



    def dbSave(self,dirName,fileName):
        try:
            destDB = os.path.join(dirName,fileName)
            if settings.database == destDB:
                self.Error("Stai sovrascivrndo il database in uso %s!\nOperazione non permessa!" % destDB)
                return False
            else:
                shutil.copy(settings.database,destDB)
                return True
        except Exception, e:
            self.Error("Errore nel salvataggio del file %s. (%s)" % (os.path.join(dirName,fileName),str(e)))
            return False

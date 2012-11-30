#Boa:Dialog:Messaggio

import wx

def create(parent):
    return Messaggio(parent)

[wxID_MESSAGGIO, wxID_MESSAGGIOBUTTON1, wxID_MESSAGGIOPANEL1, 
 wxID_MESSAGGIOSTATICBITMAP1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class Messaggio(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_MESSAGGIO, name=u'Messaggio',
              parent=prnt, pos=wx.Point(351, 49), size=wx.Size(850, 702),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Messaggio')
        self.SetClientSize(wx.Size(834, 664))

        self.button1 = wx.Button(id=wxID_MESSAGGIOBUTTON1, label=u'Close',
              name='button1', parent=self, pos=wx.Point(752, 632),
              size=wx.Size(75, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_MESSAGGIOBUTTON1)

        self.panel1 = wx.Panel(id=wxID_MESSAGGIOPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(816, 648),
              style=wx.TAB_TRAVERSAL)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_MESSAGGIOSTATICBITMAP1, name='staticBitmap1',
              parent=self.panel1, pos=wx.Point(0, 0), size=wx.Size(800, 640),
              style=0)

    def __init__(self, parent,wximage):
        self._init_ctrls(parent)
        self.wximage = wximage
        self.staticBitmap1.SetBitmap(wx.BitmapFromImage(self.wximage))
        self.Refresh()

    def OnButton1Button(self, event):
        self.Close()
        event.Skip()

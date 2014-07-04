#!/usr/bin/env python
#Boa:App:BoaApp

import wx
import settings
import nrs_frame
import logging, os
import time
import matplotlib
import scipy
import mpl_toolkits
from sets import Set

modules ={u'GibeToNrsWin32_new': [0, '', u'GibeToNrsWin32_new.py'],
 u'img_frame': [0, '', u'img_frame.py'],
 u'nrs_frame': [1, 'Main frame of Application', u'nrs_frame.py'],
 u'nrs_message': [0, '', u'nrs_message.py'],
 u'settings': [0, '', u'settings.conf']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = nrs_frame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()

"""
Image viewer that pans and zooms.
The pan and zoom mechanism is comparable to Google Maps.
No scrollbar is implemented.

Heavily inspired by demo code at
https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414

"""


import wx
import cv2

import wx.lib.inspection



### Class ViewerPanel (where all the action is!!) ----------------------

class ViewerPanel(wx.Panel):
    def __init__(self, parent, image_file):
        wx.Panel.__init__(self, parent, -1)
        pass
    
    
    ## Normalisation methods --------------------------------------------
    
    def NormaliseEventPosition(self, evt_pos):
        pass
    
    ## Paint methods ----------------------------------------------------
    
    def OnSize(self, event):
        self.Refresh()
        
        
    def GetBitmapPosition(self):
        """Determine bitmap draw location on panel as function of panel 
        size and image size.
        Want centre of image to be drawn on panel_centre.
        """
        pass
    
    
    def GetBitmapSize(self):
        """Want to rescale based on panel height and width."""
        pass
        
    
    def DoDrawCanvas(self, gc):
        pass
        
        
    def OnPaint(self, event):
        pass
        
    
    
    ### Pan methods ----------------------------------------------------
    
    def ProcessPan(self, position, do_refresh):
        self.in_prog_vec = self.in_prog_start - position
        if do_refresh:
            self.Refresh()
    
    
    def FinishPan(self, do_refresh):
        pass
        
    
    def OnLeftUp(self, event):
        self.ProcessPan(event.GetPosition(), False)
        self.FinishPan(False)
    
    
    def OnMotion(self, event):
        self.ProcessPan(event.GetPosition(), True)
    
    
    def OnCaptureLost(self, event):
        self.FinishPan(True)
    
    
    def OnLeftDown(self, event):
        # Turn the cursor into a hand cursor
        pass
    
    
    
    ### Zoom methods ---------------------------------------------------
    
    def OnZoom(self, a, b, position):
        """a is the normalised old zoom; b is the normalised new zoom"""
        pass
    
        
    def OnPinch(self, event):
        pass
    
        
    def OnDoubleClick(self, event):
        """Zoom in by 50%"""
        pass
        




### Base class supporting ViewerPanel ----------------------------------

class Base(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        
        


def main():
    app = wx.App(False)
    base = Base(None, wx.ID_ANY)
    base.Show()
    
    #wx.lib.inspection.InspectionTool().Show()
    
    app.MainLoop()

if __name__ == '__main__':
    main()
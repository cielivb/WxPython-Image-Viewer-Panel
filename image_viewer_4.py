"""
Image viewer that pans and zooms.
The pan and zoom mechanism is comparable to Google Maps.
No scrollbar is implemented.

Heavily inspired by demo code at
https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414

"""


import wx
import cv2
import numpy as np

import wx.lib.inspection



### Class ViewerPanel (where all the action is!!) ----------------------

class ViewerPanel(wx.Panel):
    def __init__(self, image_file, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)
        
        self.InitGraphicsAttr(image_file)
        self.InitVecAttr()
        self.SetBindings()
        
        
    ### Initialisation methods -----------------------------------------
    
    def InitGraphicsAttr(self, image_file):
        """ Initialise window attributes related to graphics """
        self.image_file = image_file
        self.image = wx.Bitmap(self.image_file)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.zoom_factor = 1        
    
    def InitVecAttr(self):
        """ Initialise pan vector and related attributes """
        self.pan_vec = np.array([0,0]) # Current pan position
        self.in_prog_vec = np.array([0,0]) # Difference between pan_vec and actual pan position
        self.is_panning = False # Whether pan is currently in progress    
        
    def SetBindings(self):
        pass
        
    
    ## Normalisation methods --------------------------------------------
    
    def NormaliseEventPosition(self, evt_pos):
        pass
    
    ## Paint methods ----------------------------------------------------
    
    def OnSize(self, event):
        print('size')
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
        
    
    def DrawCanvas(self, gc):
        image = gc.CreateBitmap(self.image)
        height, width = 300, 300 # Implement auto-adjust function later
        gc.DrawBitmap(image, 0, 0, 300, 300)
        
        
    def OnPaint(self, event):
        """ Paint the image onto the ViewerPanel """
        # Initialise paint device context
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        
        # Set to start painting from centre of window        
        size_x, size_y = self.GetClientSize()
        dc.SetDeviceOrigin(int(size_x/2), int(size_y/2))
        
        # Create graphics context from Paint DC
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            # Position view according to pan
            total_pan = self.pan_vec + self.in_prog_vec
            gc.Translate(-total_pan[0], -total_pan[1])
            
            # Scale x and y axes equally according to zoom factor
            gc.Scale(self.zoom_factor, self.zoom_factor)
            
            self.DrawCanvas(gc)
        
        del(gc)
    
    
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

class BasePanel(wx.Panel):
    """ Base panel to support ViewerPanel and Zoom buttons """
    def __init__(self, image_file, *args, **kw):
        super().__init__(*args, **kw)
        self.image_file = image_file
        self.InitUI()
        self.SetBindings()
    
    def InitUI(self):
        """ Add ViewerPanel and Zoom button widgets to self """
        # Create panel components
        viewer_panel = ViewerPanel(image_file=self.image_file, 
                                   parent=self,
                                   id=wx.ID_ANY)
        self.zoom_out_btn = wx.Button(self, label='-', size=(30,30))
        self.zoom_in_btn = wx.Button(self, label='+', size=(30,30))
        
        # Add viewer panel to main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(viewer_panel, 20, wx.EXPAND)
        
        # Add zoom buttons to button sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.zoom_out_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.zoom_in_btn, 0, wx.ALL, 5)
        
        # Finalise main sizer
        main_sizer.Add(btn_sizer, 1, wx.ALIGN_CENTRE, 5)
        self.SetSizer(main_sizer)
        
    
    def SetBindings(self):
        """ Bind zoom buttons to their event handlers """
        self.zoom_out_btn.Bind(wx.EVT_BUTTON, self.OnZoomOut)
        self.zoom_in_btn.Bind(wx.EVT_BUTTON, self.OnZoomIn)
    
    def OnZoomOut(self, event):
        """ Zoom out by 50% """
        print('Zoom out button pressed')
    
    def OnZoomIn(self, event):
        """ Zoom in by 50% """
        print('Zoom in button pressed')
        

class Base(wx.Frame):
    """ Base frame to support Base Panel """
    def __init__(self, image_file, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        panel = BasePanel(image_file=image_file, parent=self,
                          id=wx.ID_ANY)
        
        # Set frame size limits
        self.SetMinSize((300,300))
        self.SetMaxSize(wx.DisplaySize())
        
        self.Show()


        
def main(image_file):
    """ Open and run image viewer, which will display given image file """
    app = wx.App(False)
    base = Base(image_file=image_file, parent=None, 
                id=wx.ID_ANY, title='Image Viewer',
                pos=wx.DefaultPosition, size=(300,300),
                style=wx.DEFAULT_FRAME_STYLE,
                name='ImageViewer')
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


if __name__ == '__main__':
    main(image_file = 'images/medium.jpg')
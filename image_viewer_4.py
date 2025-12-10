"""
Image viewer that pans and zooms.
The pan and zoom mechanism is comparable to Google Maps.
No scrollbar is implemented.

Heavily inspired by demo code at
https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414

"""


import wx
import cv2



class ViewerPanel(wx.Panel):
    def __init__(self, parent, image_file):
        wx.Panel.__init__(self, parent, -1)
        self.image_file = image_file
        self.image_height = cv2.imread(image_file).shape[0]        
        self.image_width = cv2.imread(image_file).shape[1]
        self.SetSize(self.image_width, self.image_height)
        
        self.old_frame_width = self.image_width
        self.old_frame_height = self.image_height
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.zoom_factor = 100
        self.pan_vec = wx.Point2D(0,0)
        self.in_prog_start = wx.Point(0,0)
        self.in_prog_vec = wx.Point2D(0,0)
        self.pan_in_prog = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_GESTURE_ZOOM, self.OnPinch)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    
    def OnSize(self, event):
        #print('Size event!', self.GetParent().GetSize())
        #self.SetSize(self.GetParent().GetSize())
        """Pan and zoom image according to resize"""
        print('Size event!', event.GetSize())
        height_diff = event.GetSize()[0] - self.old_frame_height
        width_diff = event.GetSize()[1] - self.old_frame_width
        
        
    
    def DoDrawCanvas(self, gc):
        image = gc.CreateBitmap(wx.Bitmap(self.image_file))
        height, width = cv2.imread(self.image_file).shape[0:2]
        #x, y = self.GetBitmapPosition()
        gc.DrawBitmap(image, 0, 0, width, height)
        
    def OnPaint(self, event):
        # Create Paint DC
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        
        # Create graphics context from Paint DC
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            a = self.zoom_factor / 100
            
            # Add self.pan_vec and self.in_prog_vec together
            panvec_tuple = self.pan_vec.Get()
            inprogvec_tuple = self.in_prog_vec.Get()
            total_x = panvec_tuple[0] + inprogvec_tuple[0]
            total_y = panvec_tuple[1] + inprogvec_tuple[1]
            total_pan = wx.Point2D(total_x, total_y)
            
            gc.Translate(-total_pan[0], -total_pan[1])
            gc.Scale(a, a)
            self.DoDrawCanvas(gc)
        
        del(gc)
        
    
    def ProcessPan(self, position, do_refresh):
        self.in_prog_vec = self.in_prog_start - position
        if do_refresh:
            self.Refresh()
    
    def FinishPan(self, do_refresh):
        if self.pan_in_prog:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.HasCapture():
            self.ReleaseMouse()
            
        self.Unbind(wx.EVT_LEFT_UP)
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        
        # Update pan vector (+= in_prog_vec)
        panvec_tuple = self.pan_vec.Get()
        inprogvec_tuple = self.in_prog_vec.Get()
        sum_x = panvec_tuple[0] + inprogvec_tuple[0]
        sum_y = panvec_tuple[1] + inprogvec_tuple[1]
        self.pan_vec = wx.Point2D(sum_x, sum_y)
        
        self.in_prog_pan_vec = wx.Point2D(0,0)
        self.pan_in_prog = False
        
        if do_refresh: self.Refresh()
        
    
    def OnLeftUp(self, event):
        self.ProcessPan(event.GetPosition(), False)
        self.FinishPan(False)
    
    def OnMotion(self, event):
        self.ProcessPan(event.GetPosition(), True)
    
    def OnCaptureLost(self, event):
        self.FinishPan(True)
    
    
    def OnLeftDown(self, event):
        # Turn the cursor into a hand cursor
        cursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(cursor)
        
        self.in_prog_start = event.GetPosition()
        self.in_prog_vec = wx.Point2D(0,0)
        self.pan_in_prog = True
        
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnCaptureLost)
        
        self.CaptureMouse()
    
    
    
    def OnZoom(self, a, b, position):
        """a is the normalised old zoom; b is the normalised new zoom"""
        # Set panvec so the point below the cursor in the new scaled/panned
        # corresponds to the same point that is currently below it
        
        # st_pt = event.GetPosition() + self.pan_vec
        pan_vec_tuple = self.pan_vec.Get()
        event_pos_tuple = position
        sum_x = pan_vec_tuple[0] + event_pos_tuple[0]
        sum_y = event_pos_tuple[1] + pan_vec_tuple[1]
        st_pt = (sum_x, sum_y)
        
        xy_pt = (st_pt[0]/a, st_pt[1]/a)
        new_st_pt = (b*xy_pt[0], b*xy_pt[1])
        
        #self.panvec = new_st_pt - event.GetPosition()
        diff_x = new_st_pt[0] - event_pos_tuple[0]
        diff_y = new_st_pt[1] - event_pos_tuple[1]
        self.pan_vec = wx.Point2D(diff_x, diff_y)
        
        self.Refresh()
        
    def OnPinch(self, event):
        if self.pan_in_prog : self.FinishPan(False)
        oldzoom = self.zoom_factor        
        self.zoom_factor = event.GetZoomFactor()*100
        
        # The following snippet accounts for sudden zoom factor shifts
        if abs(oldzoom - self.zoom_factor) > 20:
            if oldzoom > self.zoom_factor:
                self.zoom_factor = oldzoom - 5
            else:
                self.zoom_factor = oldzoom + 5
        
        a = oldzoom / 100
        b = self.zoom_factor / 100
        self.OnZoom(a, b, event.GetPosition())
        
    def OnDoubleClick(self, event):
        """Zoom in by 50%"""
        oldzoom = self.zoom_factor
        self.zoom_factor = oldzoom * 1.5
        a = oldzoom / 100
        b = self.zoom_factor / 100
        self.OnZoom(a, b, event.GetPosition())
        



class Base(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #self.panel = ViewerPanel(self, 'images/small.png')
        self.panel = ViewerPanel(self, 'images/medium.jpg')
        #self.panel = ViewerPanel(self, 'images/big.gif') #SHOWS FIRST SCENE ONLY
        #self.panel = ViewerPanel(self, 'images/nebula.webp') #FAILS
        self.SetSize(self.panel.GetSize())
        self.SetMinSize((300,300))
        
        self.zoom_out_button = wx.Button(self, label='-', size=(30,30))
        self.zoom_in_button = wx.Button(self, label='+', size=(30,30))
        self.zoom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.zoom_sizer.Add(self.zoom_out_button, 1, wx.ALL, 5)
        self.zoom_sizer.Add(self.zoom_in_button, 1, wx.ALL, 5)
        
        sizer.Add(self.panel, 20, wx.EXPAND)
        sizer.Add(self.zoom_sizer, 1, wx.ALIGN_CENTRE, 5)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


def main():
    app = wx.App(False)
    base = Base(None, wx.ID_ANY)
    base.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
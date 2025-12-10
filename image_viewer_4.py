"""
Image viewer that pans and zooms

Heavily inspired by demo code at
https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414

Next steps:
- centre image at startup
"""


import wx
import wx.lib.scrolledpanel as scrolled
import cv2



class ViewerPanel(wx.Panel):
    def __init__(self, parent, image_file):
        wx.Panel.__init__(self, parent, -1)
        self.image_file = image_file
        
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
    
    
    def DoDrawCanvas(self, gc):
        image = gc.CreateBitmap(wx.Bitmap(self.image_file))
        height, width = cv2.imread(self.image_file).shape[0:2]
        gc.DrawBitmap(image, 10, 10, width, height)
        print('Zoom factor = ', self.zoom_factor)
        #print('pan_vec = ', self.pan_vec)
        #print('in_prog_start = ', self.in_prog_start)
        #print('in_prog_vec = ', self.in_prog_vec)
        #print('pan_in_prog = ', self.pan_in_prog)
        
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
        self.panel = ViewerPanel(self, 'images/stack.png')


def main():
    app = wx.App(False)
    base = Base(None, wx.ID_ANY)
    base.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
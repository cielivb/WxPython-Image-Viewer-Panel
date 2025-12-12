"""
Image viewer with a pan and zoom mechanism comparable to Google Maps.

This script is designed to be portable into a larger GUI application.
Simply import this module into your script and call
ImageViewer.view(self, image_file) where image_file is a string
representing the relative file path of the image you wish to display.

"""
import os

import wx
import numpy as np

from PIL import Image as PILImage




### Class _ViewerPanel (where all the action is!!) ----------------------

class _ViewerPanel(wx.Panel):
    """ Panel onto which the image is drawn """
    def __init__(self, image_file, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self._init_graphics_attr(image_file)
        self._init_vec_attr()
        self._set_bindings()



    ### Initialisation methods -----------------------------------------

    def _init_graphics_attr(self, image_file):
        """ Initialise window attributes related to graphics """
        self.image_file = image_file
        self.image = self._load_image(self.image_file)
        self.scaled_img_dims = (self.image.GetWidth(),
                                self.image.GetHeight())
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.zoom_factor = 1


    def _init_vec_attr(self):
        """ Initialise pan vector and related attributes """
        self.pan_vec = np.array([0,0]) # Current pan position

        # Pan start position (updated in _on_left_down to represent event position)
        self.in_prog_start = np.array([0,0])

        # Difference between pan_vec and actual pan position
        self.in_prog_vec = np.array([0,0])

        self.is_panning = False # Whether pan is currently in progress


    def _set_bindings(self):
        """ Set permanent _ViewerPanel bindings """
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_PAINT, self._on_paint)

        # Zoom bindings
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_double_click)
        self.Bind(wx.EVT_GESTURE_ZOOM, self._on_zoom_gesture)
        self.Bind(wx.EVT_BUTTON, self._on_zoom_out_button, id=1)
        self.Bind(wx.EVT_BUTTON, self._on_zoom_in_button, id=2)

        # Pan binding
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)

        # Reset binding
        self.Bind(wx.EVT_BUTTON, self._on_reset_button, id=3)



    ## Utility methods --------------------------------------------

    def _get_viewer_panel_centre(self):
        """ Get centre position relative to top left corner """
        panel_size = self.GetSize()
        panel_centre = (panel_size[0] / 2,
                        panel_size[1] / 2) # w x h
        return panel_centre


    def _on_reset_button(self, event):
        """ Restore _ViewerPanel to initial state """
        self._init_graphics_attr(self.image_file)
        self._init_vec_attr()
        self.Refresh()


    def _load_image(self, image_file):
        """ Load image file as wx.Image object """

        # Convert .webp image file to .png file
        if image_file.endswith('.webp'):
            image = PILImage.open(image_file)
            filename = image_file.split('/')[-1] # Just filename with ext
            filename = filename.split('.')[0] + '.png' # Replace extension
            filename = os.path.join(os.path.dirname(__file__), 'temp', filename)
            image.save(filename, 'PNG')
            self.GetParent().GetParent().temp_file = filename
            return wx.Image(filename)

        else:
            return wx.Image(self.image_file)



    ## Paint methods ----------------------------------------------------

    def _on_size(self, event):
        """ Refresh background when _ViewerPanel size changes """
        self.Refresh()


    def _get_bitmap_position(self):
        """Determine bitmap draw location on panel as function of panel 
        size and image size.
        Want centre of image to be drawn on panel_centre.
        By default, the image drawing begins at the top left corner, hence
        need to calculate this position.
        """
        # Get viewer panel centre position (width x height)
        panel_centre_tuple = self._get_viewer_panel_centre()
        panel_centre = np.array([panel_centre_tuple[0],
                                 panel_centre_tuple[1]])

        # Get scaled image centre
        image_centre = np.array([self.scaled_img_dims[0]/2,
                                 self.scaled_img_dims[1]/2])

        # Get draw start coordinates (panel centre - image_centre)
        start_coords = panel_centre - image_centre

        return (start_coords[0], start_coords[1])


    def _get_bitmap_size(self):
        """ Get display image dimensions based on panel height and width. """

        # Get panel and scaled image dimensions
        panel_width = self.GetSize()[0]
        panel_height = self.GetSize()[1]
        image_width = self.image.GetWidth()
        image_height = self.image.GetHeight()

        if image_height > panel_height or image_width > panel_width:

            # If original image is larger in any dimension than the panel,
            # check what % larger each dimension of image is than panel,
            # and scale down both dimensions by the larger % difference.
            # Do not directly scale original image. Return only scaled
            # image dimensions.

            prop_diff_width = (image_width - panel_width) / panel_width
            prop_diff_height = (image_height - panel_height) / panel_height
            scale = max(prop_diff_width, prop_diff_height)

            self.scaled_img_dims = (image_width/scale, image_height/scale)

            # If the either of the scaled image dimensions exceed original
            # image size, reset scaled image dimensions to original image
            # dimensions
            if self.scaled_img_dims[0] > image_width or self.scaled_img_dims[1] > image_height:
                self.scaled_img_dims = (image_width, image_height)

        else:

            # The image fits neatly in the panel. Use original image
            # dimensions as scaled image dimensions.
            self.scaled_image_dims = (image_width, image_height)

        return self.scaled_img_dims


    def _draw_canvas(self, gc):
        """ Draw image onto _ViewerPanel """
        image = gc.CreateBitmap(wx.Bitmap(self.image))
        width, height = self._get_bitmap_size()
        start_coords = self._get_bitmap_position()
        gc.DrawBitmap(image, start_coords[0], start_coords[1],
                      width, height)


    def _on_paint(self, event):
        """ Prepare to draw on _ViewerPanel """
        # Initialise paint device context
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        # Create graphics context from Paint DC
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            # Position view according to pan
            total_pan = self.pan_vec + self.in_prog_vec
            gc.Translate(-total_pan[0], -total_pan[1])

            # Scale x and y axes equally according to zoom factor
            gc.Scale(self.zoom_factor, self.zoom_factor)

            self._draw_canvas(gc)

        del gc
    
    
    
    ### Pan methods ----------------------------------------------------

    def _process_pan(self, position, do_refresh):
        """ Update in progress vector then refresh display """
        self.in_prog_vec = self.in_prog_start - position
        if do_refresh:
            self.Refresh()


    def _finish_pan(self, do_refresh):
        """ Restore attributes and bindings to pre-panning state """
        # Restore cursor to arrow and release mouse capture
        if self.is_panning:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.HasCapture():
            self.ReleaseMouse()

        # Remove bindings associated with left mouse down
        self.Unbind(wx.EVT_LEFT_UP)
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)

        # Update pan vector
        self.pan_vec += self.in_prog_vec

        # Restore self.in_prog_vec and self.is_panning
        self.in_prog_vec = np.array([0,0])
        self.is_panning = False

        # Refresh viewer panel if required
        if do_refresh: self.Refresh()


    def _on_left_up(self, event):
        """ Process last pan event then finish pan """
        event_position = np.array([event.GetPosition()[0],
                                   event.GetPosition()[1]])
        self._process_pan(event_position, False)
        self._finish_pan(False)


    def _on_motion(self, event):
        """ Signal to process current pan event """
        event_position = np.array([event.GetPosition()[0],
                                   event.GetPosition()[1]])
        self._process_pan(event_position, True)


    def _on_capture_lost(self, event):
        """ Finish pan if mouse capture is lost """
        self._finish_pan(True)


    def _on_left_down(self, event):
        """ Initiate pan """

        # Turn the cursor into a hand cursor
        cursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(cursor)

        # Initialise class pan attributes
        self.in_prog_start = np.array([event.GetPosition()[0],
                                       event.GetPosition()[1]])
        self.in_prog_vec = np.array([0,0])
        self.is_panning = True

        # Set bindings
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._on_capture_lost)

        # Let cursor exit frame while performing pan
        self.CaptureMouse()



    ### Zoom methods ---------------------------------------------------

    def _on_zoom(self, old_zoom, new_zoom, evt_pos):
        """ Set self.pan_vec such that the point below the cursor (i.e,
        evt_pos) is the new absolute pan site """

        # Convert evt_pos from tuple to numpy array
        pos = np.array([evt_pos[0], evt_pos[1]])

        # Add pos to self.pan_vec
        st_pt = self.pan_vec + pos

        # I don't fully understand how this works but it works
        xy_pt = st_pt / old_zoom
        new_st_pt = xy_pt * new_zoom
        self.pan_vec = new_st_pt - pos

        self.Refresh()


    def _on_zoom_gesture(self, event):
        """ Process pinch zoom gesture """
        if self.is_panning: self._finish_pan(False)
        old_zoom = self.zoom_factor
        new_zoom_factor = event.GetZoomFactor()

        # Smooth out sudden zoom factor shifts
        if abs(old_zoom - new_zoom_factor) > 10:
            if old_zoom > new_zoom_factor: # Zooming out
                new_zoom_factor = old_zoom - 2
            else: # Zooming in
                new_zoom_factor = old_zoom + 2

        self.zoom_factor = new_zoom_factor
        self._on_zoom(old_zoom, self.zoom_factor, event.GetPosition())


    def _on_double_click(self, event):
        """ Zoom in by 50% """
        old_zoom = self.zoom_factor
        self.zoom_factor = old_zoom * 1.5
        self._on_zoom(old_zoom, self.zoom_factor, event.GetPosition())


    def _on_zoom_out_button(self, event):
        """ Zoom out by 50% """
        old_zoom = self.zoom_factor
        self.zoom_factor = old_zoom * 0.5
        centre = self._get_viewer_panel_centre()
        self._on_zoom(old_zoom, self.zoom_factor, centre)


    def _on_zoom_in_button(self, event):
        """ Zoom in by 50% """
        old_zoom = self.zoom_factor
        self.zoom_factor = old_zoom * 1.5
        centre = self._get_viewer_panel_centre()
        self._on_zoom(old_zoom, self.zoom_factor, centre)




### _Base class supporting _ViewerPanel ----------------------------------

class _BasePanel(wx.Panel):
    """ _Base panel to support _ViewerPanel and Zoom buttons """

    def __init__(self, image_file, *args, **kw):
        super().__init__(*args, **kw)
        self.image_file = image_file
        self._init_ui()
        self._set_bindings()


    def _init_ui(self):
        """ Add _ViewerPanel and Zoom button widgets to self """

        # Create panel components
        viewer_panel = _ViewerPanel(image_file=self.image_file,
                                   parent=self,
                                   id=wx.ID_ANY)
        self.zoom_out_btn = wx.Button(self, label='-',
                                      size=(30,30), id=1)
        self.zoom_in_btn = wx.Button(self, label='+',
                                     size=(30,30), id=2)
        self.reset_btn = wx.Button(self, label='Reset',
                                      size=(30,30), id=3)

        # Add viewer panel to main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(viewer_panel, 20, wx.EXPAND)

        # Add zoom buttons to button sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.zoom_out_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.zoom_in_btn, 0, wx.ALL, 5)

        # Add items to bottom bar
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(btn_sizer, 2, wx.ALL, 5)
        bottom_sizer.Add(self.reset_btn, 1, wx.ALL|wx.ALIGN_CENTRE, 5)

        # Finalise main sizer
        main_sizer.Add(bottom_sizer, 1, wx.ALIGN_CENTRE, 5)
        self.SetSizer(main_sizer)


    def _set_bindings(self):
        """ Bind zoom buttons to their event handlers """
        self.zoom_out_btn.Bind(wx.EVT_BUTTON, self._on_zoomOut)
        self.zoom_in_btn.Bind(wx.EVT_BUTTON, self._on_zoomIn)
        self.reset_btn.Bind(wx.EVT_BUTTON, self._on_reset)


    def _on_zoomOut(self, event):
        """ Post Zoom Out Button event to _ViewerPanel """
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId,
                                self.zoom_out_btn.Id)
        viewer_panel = self.GetChildren()[0]
        viewer_panel.GetEventHandler().ProcessEvent(event)


    def _on_zoomIn(self, event):
        """ Post Zoom In Button event to _ViewerPanel """
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId,
                                self.zoom_in_btn.Id)
        viewer_panel = self.GetChildren()[0]
        viewer_panel.GetEventHandler().ProcessEvent(event)


    def _on_reset(self, event):
        """ Post Reset Button event to _ViewerPanel """
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId,
                                self.reset_btn.Id)
        viewer_panel = self.GetChildren()[0]
        viewer_panel.GetEventHandler().ProcessEvent(event)



class _Base(wx.Frame):
    """ _Base frame to support _Base Panel """

    def __init__(self, image_file, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.temp_file = None
        panel = _BasePanel(image_file=image_file, parent=self,
                          id=wx.ID_ANY)

        # Set frame size limits
        self.SetMinSize((300,300))
        self.SetMaxSize(wx.DisplaySize())

        self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.Layout()
        self.Show()


    def OnExit(self, event):
        """ Discard temp image file if present before closing """
        if self.temp_file is not None:
            os.remove(self.temp_file)
        self.Destroy()




### Execution functions -------------------------------------------------


def view(parent, image_file):
    """ Open and run image viewer, which will display given image file.
    This function should be called from a currently running wxpython app.
    """
    wx.InitAllImageHandlers()
    base = _Base(image_file=image_file, parent=parent,
                id=wx.ID_ANY, title='Image Viewer',
                pos=wx.DefaultPosition, size=(400,300),
                style=wx.DEFAULT_FRAME_STYLE)



def main(image_file):
    """ Initialises wx app to use ImageViewer """
    app = wx.App(False)
    wx.InitAllImageHandlers()
    base = _Base(image_file=image_file, parent=None,
                id=wx.ID_ANY, title='Image Viewer',
                pos=wx.DefaultPosition, size=(400,300),
                style=wx.DEFAULT_FRAME_STYLE)
    app.MainLoop()

if __name__ == '__main__':
    main('images/medium.jpg')
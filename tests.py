

import ImageViewer as iv
import wx



class TestPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        buttons = []
        btn1 = wx.Button(self, label='small.png', id=1)
        btn2 = wx.Button(self, label='medium.jpg', id=2)
        btn3 = wx.Button(self, label='medium_vertical.jpg', id=3)
        btn4 = wx.Button(self, label='nebula.webp', id=4)
        buttons.append(btn1)
        buttons.append(btn2)
        buttons.append(btn3)
        buttons.append(btn4)
        
        sizer = wx.GridSizer(cols=2)        
        for button in buttons:
            self.Bind(wx.EVT_BUTTON, self.OpenViewer, button)
            sizer.Add(button, 0, wx.ALIGN_CENTRE, 5)
        self.SetSizer(sizer)
    
    def OpenViewer(self, event):
        if event.GetId() == 1: iv.view('images/small.png')
        elif event.GetId() == 2: iv.view('images/medium.jpg')
        elif event.GetId() == 3: iv.view('images/medium_vertical.jpg')
        elif event.GetId() == 4: iv.view('images/nebula.webp')
    
        
class TestFrame(wx.Frame):
    def __init__(self, parent, size):
        wx.Frame.__init__(self, parent, size=size)
        panel = TestPanel(self)
        self.SetAutoLayout(False)
        self.Show()

if __name__ == '__main__':
    test_app = wx.App(False)
    frame = TestFrame(None, size=(300,100))
    test_app.MainLoop()
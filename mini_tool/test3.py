import wx

mainframe_svg = '<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><rect fill="#F2F2F7" x="2" y="2" height="20" width="20" rx="4"/><g transform="translate(2.4, 2.4) scale(0.8)><path fill="#FF4530" d="M14.06,9.94L12,9l2.06-0.94L15,6l0.94,2.06L18,9l-2.06,0.94L15,12L14.06,9.94z"/> <path fill="#34C759" d="M4,14l0.94-2.06L7,11l-2.06-0.94L4,8 l-0.94,2.06L1,11l2.06,0.94L4,14z"/> <path fill="#FF9500" d="M8.5,9l1.09-2.41L12,5.5L9.59,4.41L8.5,2L7.41,4.41L5,5.5l2.41,1.09L8.5,9z"/> <path fill="#0A84FF" d="M4.5,20.5l6-6.01l4,4 L23,8.93l-1.41-1.41l-7.09,7.97l-4-4L3,19L4.5,20.5z"/></g></svg>'

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 300))

    def on_tool_click(self, event):
        print('Tool clicked!')


app = wx.App(False)
frame = MyFrame(None, 'Demo')
frame.Show(True)
app.MainLoop()

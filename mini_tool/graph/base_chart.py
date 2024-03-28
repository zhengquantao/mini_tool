import os
import wx
import wx.html2

from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:38121/static/"

from pyecharts import options as opts
from pyecharts.charts import *


class ChartFrame(wx.MDIChildFrame):
    def __init__(self, parent, title="", html_name=""):
        wx.MDIChildFrame.__init__(self, parent, -1, title=title, size=(700, 500))
        # Create html name
        self.html_name = html_name
        # Create HTML container
        self.THML_CONTAINER = wx.html2.WebView.New(self)
        # self.html_container.LoadPage(c)
        self.THML_CONTAINER.LoadURL(f"file:///{self.read_html()}")

        # Add container to Frame sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.THML_CONTAINER, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def read_html(self):
        pass

    def on_close(self, event):
        if os.path.exists(self.html_name):
            print("del successful")
            os.remove(self.html_name)

        # 调用基类的Close方法来处理关闭
        event.Skip()

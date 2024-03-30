import wx


class ScatterDialog(wx.Dialog):
    def __init__(self, parent, title=u"Bar Chart"):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(350, 260),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        wSizer3 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText45 = wx.StaticText(self, wx.ID_ANY, u"选择需要Y轴的字段：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText45.Wrap(-1)

        wSizer3.Add(self.m_staticText45, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.ylist = wx.CheckListBox(self, size=(170, 130), choices=parent.data_df.columns, style=wx.TC_MULTILINE)

        wSizer3.Add(self.ylist, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(wSizer3, 0, 0, 5)

        wSizer4 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText46 = wx.StaticText(self, wx.ID_ANY, u"选择需要X轴的字段：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText46.Wrap(-1)

        wSizer4.Add(self.m_staticText46, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.xlist = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, 30),
                                 choices=parent.data_df.columns)
        self.xlist.AutoComplete(parent.data_df.columns)
        wSizer4.Add(self.xlist, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(wSizer4, 0, 0, 5)

        wSizer6 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer6.Add(self.m_button1, 0, wx.ALL, 10)

        self.m_button2 = wx.Button(self, wx.ID_OK, u"画图", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer6.Add(self.m_button2, 0, wx.ALL, 10)

        bSizer3.Add(wSizer6, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button1.Bind(wx.EVT_LEFT_UP, self.m_button1OnLeftUp)
        # self.m_button2.Bind(wx.EVT_LEFT_UP, self.m_button2OnLeftUp)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def __del__(self):
        pass

    def on_close(self, event):
        self.Destroy()

    # Virtual event handlers, overide them in your derived class
    def m_button2OnLeftUp(self, event):
        self.on_close(event)
        # event.Skip()

    def m_button1OnLeftUp(self, event):
        self.on_close(event)
        # event.Skip()

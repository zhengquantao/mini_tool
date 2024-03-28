import wx


class LineDialog(wx.Dialog):
    def __init__(self, parent, title=u"Line"):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(350, 235),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        wSizer3 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText45 = wx.StaticText(self, wx.ID_ANY, u"智能写作API：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText45.Wrap(-1)

        wSizer3.Add(self.m_staticText45, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(215, -1), 0)
        wSizer3.Add(self.m_textCtrl2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(wSizer3, 0, 0, 5)

        wSizer4 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText46 = wx.StaticText(self, wx.ID_ANY, u"自动排版API：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText46.Wrap(-1)

        wSizer4.Add(self.m_staticText46, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(215, -1), 0)
        wSizer4.Add(self.m_textCtrl3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(wSizer4, 0, 0, 5)

        wSizer5 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText47 = wx.StaticText(self, wx.ID_ANY, u"智能标题API：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText47.Wrap(-1)

        wSizer5.Add(self.m_staticText47, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(215, -1), 0)
        wSizer5.Add(self.m_textCtrl4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(wSizer5, 0, 0, 5)

        wSizer6 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer6.Add(self.m_button1, 0, wx.ALL, 10)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer6.Add(self.m_button2, 0, wx.ALL, 10)

        bSizer3.Add(wSizer6, 0, wx.ALIGN_RIGHT, 5)

        wSizer7 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_staticText48 = wx.StaticText(self, wx.ID_ANY, u"API说明请访问小发猫官网。", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText48.Wrap(-1)

        wSizer7.Add(self.m_staticText48, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        bSizer3.Add(wSizer7, 0, 0, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)
        self.filename = 'config.json'


        self.m_button1.Bind(wx.EVT_LEFT_UP, self.m_button1OnLeftUp)
        self.m_button2.Bind(wx.EVT_LEFT_UP, self.m_button2OnLeftUp)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __del__(self):
        pass

    def OnClose(self, event):
        self.Destroy()

    # Virtual event handlers, overide them in your derived class
    def m_button2OnLeftUp(self, event):
        rewrite_url = self.m_textCtrl2.GetValue()
        title_url = self.m_textCtrl4.GetValue()
        type_url = self.m_textCtrl3.GetValue()
        self.OnClose(event)
        # event.Skip()

    def m_button1OnLeftUp(self, event):
        self.OnClose(event)
        # event.Skip()


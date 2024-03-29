import datetime
import uuid
from functools import wraps
import wx
import wx.svg


def svg_to_bitmap(svg, size=None, win=None):
    if size is None:
        if wx.Platform == '__WXMSW__':
            size = (18, 18)
        else:
            size = (16, 16)
    bmp = wx.svg.SVGimage.CreateFromBytes(str.encode(svg))
    bmp = bmp.ConvertToScaledBitmap(size, win)
    if win:
        bmp.SetScaleFactor(win.GetContentScaleFactor())
    return bmp


def random_name(f_type="html"):
    return f"date{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{f_type}"


def check_graph_df(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not hasattr(self, "data_df"):
            wx.MessageBox("缺数据支撑画图，请选择文件", "错误", wx.YES_NO | wx.ICON_WARNING)
            return

        return func(self, *args, **kwargs)
    return inner

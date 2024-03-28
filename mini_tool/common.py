import datetime
import uuid
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
    return f"date{datetime.datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex}.{f_type}"


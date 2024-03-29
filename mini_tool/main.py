import datetime
from concurrent.futures.thread import ThreadPoolExecutor
import wx
import wx.grid
import pandas as pd

from mini_tool import constants as cs
from mini_tool.common import svg_to_bitmap, check_graph_df
from mini_tool.graph.bar_chart import BarChart
from mini_tool.graph.bar_dialog import BarDialog
from mini_tool.graph.d3_chart import D3Chart
from mini_tool.graph.line_chart import LineChart
from mini_tool.graph.line_dialog import LineDialog
from mini_tool.graph.scatter_chart import ScatterChart

from mini_tool.html_server import run_server

THREAD_POOL = ThreadPoolExecutor(cs.thread_num)


class ChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, title):
        wx.MDIChildFrame.__init__(self, parent, -1, title)

        # 监听HTML服务
        THREAD_POOL.submit(run_server)

        # 创建静态文本控件
        self.static_text = wx.TextCtrl(
            self, -1, value=f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ———————————————————— "
                            f"\n 欢迎━(*｀∀´*)ノ亻!",
            style=wx.TE_MULTILINE)
        self.static_text.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))

        # 将静态文本控件添加到 MDIChildFrame 窗口中
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.static_text, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    #     self.Bind(wx.EVT_ICONIZE, self.on_iconize)
    #
    # def on_iconize(self, event):
    #     if self.IsIconized():
    #         self.SetPosition((0, self.GetParent().GetSize()[1] - self.GetSize()[1]))


class ChildFrameTable(wx.MDIChildFrame):
    def __init__(self, parent, title):
        wx.MDIChildFrame.__init__(self, parent, -1, title)
        self.grid = wx.grid.Grid(self)
        # 开启虚拟滚动
        self.grid.EnableScrolling(True, True)
        self.grid.CreateGrid(1000, 100)  # 创建一个n行n列的表格

        # 边框颜色
        self.grid.SetGridLineColour(wx.LIGHT_GREY)
        # 创建一个sizer对象
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)

        self.SetSizer(sizer)
    #     self.Bind(wx.EVT_ICONIZE, self.on_iconize)
    #
    # def on_iconize(self, event):
    #     if self.IsIconized():
    #         self.SetPosition((0, self.GetParent().GetSize()[1] - self.GetSize()[1]))

    def show_data(self, data):
        # Clear old data
        self.grid.ClearGrid()

        # Get the current number of rows and columns
        num_rows = self.grid.GetNumberRows()
        num_cols = self.grid.GetNumberCols()

        # Calculate the number of additional rows and columns needed
        additional_rows = data.shape[0] - num_rows
        additional_cols = data.shape[1] - num_cols

        # Append additional rows and columns if needed
        if additional_rows > 0:
            self.grid.AppendRows(additional_rows)
        if additional_cols > 0:
            self.grid.AppendCols(additional_cols)

        for col, val in enumerate(data.columns):
            self.grid.SetCellValue(0, col, str(val))
            self.grid.SetCellAlignment(0, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        self.grid.BeginBatch()
        for row in range(1, data.shape[0]):
            for col in range(data.shape[1]):
                self.grid.SetCellValue(row, col, str(data.iat[row, col]))
                self.grid.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.grid.EndBatch()


class MainFrame(wx.MDIParentFrame):
    TITLE = cs.main_title

    def __init__(self):
        sz = wx.DisplaySize()
        # 减去导航栏
        sz = (sz[0], sz[1] - 45)
        wx.MDIParentFrame.__init__(self, None, title=self.TITLE, size=sz)
        icon = wx.Icon()
        icon.CopyFromBitmap(svg_to_bitmap(cs.icon_svg,  win=self))
        self.SetIcon(icon)
        self.filename = ""

        # 创建一个工具栏
        toolbar = self.CreateToolBar()
        toolbar.SetToolBitmapSize((20, 20))
        # 添加一个文本按钮
        open_file_tool = toolbar.AddTool(wx.ID_ANY, 'TextTool', wx.Bitmap(svg_to_bitmap(cs.of_svg)), "打开文件")
        open_project_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.op_svg)), "打开项目")
        save_tool = toolbar.AddTool(wx.ID_ANY, 'TextTool', wx.Bitmap(svg_to_bitmap(cs.save_svg)), "保存")
        back_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.back_svg)), "返回")
        exit_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.exit_svg)), "退出")
        copy_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.copy_svg)), "复制")
        paste_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.paste_svg)), "粘贴")
        cut_tool = toolbar.AddTool(wx.ID_ANY, 'IconTool', wx.Bitmap(svg_to_bitmap(cs.cut_svg)), "剪切")

        self.Bind(wx.EVT_TOOL, self.on_tool_click, open_file_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, exit_tool)

        # Menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        graphMenu = wx.Menu()
        editMenu = wx.Menu()
        toolMenu = wx.Menu()
        helpMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        menubar.Append(graphMenu, '&Graph')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(toolMenu, '&Tools')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        # 创建 FileHistory 对象
        self.filehistory = wx.FileHistory(8)
        self.config = wx.Config(self.TITLE, style=wx.CONFIG_USE_LOCAL_FILE)
        self.filehistory.Load(self.config)
        recent = wx.Menu()
        self.filehistory.UseMenu(recent)
        self.filehistory.AddFilesToMenu()

        # File menu items
        open_item = fileMenu.Append(wx.ID_OPEN, '&Open File', 'Open a file')
        project_item = fileMenu.Append(wx.ID_ANY, '&Open Project', 'Open a Project')
        save_item = fileMenu.Append(wx.ID_SAVE, '&Save', 'Save a file')
        recent_item = fileMenu.Append(wx.ID_ANY, '&Recent Files', recent)
        quit_item = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        # Event bindings
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_project, project_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_quit, quit_item)
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)

        # Graph menu items
        # 柱状图
        bar_chart_item = graphMenu.Append(wx.ID_ANY, 'Bar Chart', 'Generate a bar chart')
        # 折线图
        line_plot_item = graphMenu.Append(wx.ID_ANY, 'Line Plot', 'Generate a line plot')
        # 3D图
        d3_plot_item = graphMenu.Append(wx.ID_ANY, '3D Plot', 'Generate 3D plot')
        # 散点图
        scatter_plot_item = graphMenu.Append(wx.ID_ANY, 'scatter Plot', 'Generate scatter plot')
        # 3D散点图
        d3_scatter_plot_item = graphMenu.Append(wx.ID_ANY, 'scatter 3D Plot', 'Generate 3D scatter plot')
        # 极坐标图
        polar_plot_item = graphMenu.Append(wx.ID_ANY, 'polar Plot', 'Generate polar plot')
        # 雷达图
        radar_plot_item = graphMenu.Append(wx.ID_ANY, 'radar Plot', 'Generate radar plot')
        # 数据集
        dataset_plot_item = graphMenu.Append(wx.ID_ANY, 'dataset Plot', 'Generate dataset plot')
        # 关系图
        graph_plot_item = graphMenu.Append(wx.ID_ANY, 'graph Plot', 'Generate graph plot')
        # Event bindings
        self.Bind(wx.EVT_MENU, self.on_bar_chart, bar_chart_item)
        self.Bind(wx.EVT_MENU, self.on_line_plot, line_plot_item)
        self.Bind(wx.EVT_MENU, self.on_3D_plot, d3_plot_item)
        self.Bind(wx.EVT_MENU, self.on_scatter_plot, scatter_plot_item)
        self.Bind(wx.EVT_MENU, self.on_d3_scatter_plot, d3_scatter_plot_item)
        self.Bind(wx.EVT_MENU, self.on_polar_plot, polar_plot_item)
        self.Bind(wx.EVT_MENU, self.on_radar_plot, radar_plot_item)
        self.Bind(wx.EVT_MENU, self.on_dataset_plot, dataset_plot_item)
        self.Bind(wx.EVT_MENU, self.on_graph_plot, graph_plot_item)

        # Graph menu items
        help_item = helpMenu.Append(wx.ID_ANY, '&Help', 'Help')
        contact_item = helpMenu.Append(wx.ID_ANY, '&Contact Us', 'Contact Us')
        about_item = helpMenu.Append(wx.ID_ANY, '&About', 'About Gui')
        self.Bind(wx.EVT_MENU, self.on_help, help_item)
        self.Bind(wx.EVT_MENU, self.on_contact, contact_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        # Parent
        toolbar.Realize()
        self.Show()
        self.create_child_frames()

    def on_tool_click(self, event):
        pass

    def on_file_history(self, event):
        file_num = event.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(file_num)
        self.filehistory.AddFileToHistory(path)
        # reopen file
        self.read_file(path)

    def create_child_frames(self):
        self.top_child_frame = ChildFrame(self, "main")
        self.bottom_child_frame = ChildFrameTable(self, "table")
        self.bottom_child_frame.Show()
        self.top_child_frame.Show()
        # Set child frames to tile HORIZONTAL
        self.Tile(wx.HORIZONTAL)

    def read_file(self, filename):
        # 将文件路径添加到 FileHistory 中
        self.filehistory.AddFileToHistory(filename)
        self.filehistory.Save(self.config)
        self.config.Flush()
        self.data_df = pd.read_csv(filename)
        THREAD_POOL.submit(self.bottom_child_frame.show_data, self.data_df)
        # self.bottom_child_frame.show_data(self.data_df)

    def on_open(self, event):
        wildcard = "CSV files (*.csv)|*.csv"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename = dialog.GetPath()
            self.read_file(self.filename)

    def on_project(self, event):
        pass

    def on_save(self, event):
        pass

    def on_help(self, event):
        wx.MessageBox("这个是使用指导", "帮助", wx.OK | wx.ICON_INFORMATION)
        pass

    def on_contact(self, event):
        wx.MessageBox("请联系xxx-xxxx-xxxx", "提示", wx.OK | wx.ICON_INFORMATION)
        pass

    def on_quit(self, event):
        if wx.MessageBox("是否确认要对出", "警告", wx.YES_NO | wx.ICON_WARNING) == wx.YES:
            self.Close()

    def on_about(self, event):
        pass

    @check_graph_df
    def on_bar_chart(self, event):
        dlg = BarDialog(self)
        result = dlg.ShowModal()
        if result != wx.ID_OK:
            dlg.Destroy()
            return
        y_list = dlg.ylist.GetSelections()
        checks = dlg.ylist.GetCheckedItems()
        x_num = dlg.xlist.GetSelection()
        y_list.extend(checks)
        selected_items = []
        for sel in y_list:
            # 使用GetStringSelection获取选中项的文本
            selected_items.append(dlg.ylist.GetString(sel))
        dlg.Destroy()

        bar = BarChart(self, x=self.data_df.iloc[:, x_num], y=self.data_df.iloc[:, y_list])
        bar.Show()

    @check_graph_df
    def on_line_plot(self, event):
        # dialog = wx.MultiChoiceDialog(self, 'Choose columns', 'Line Plot', self.data_df.columns)
        # if dialog.ShowModal() == wx.ID_OK:
        #     selections = dialog.GetSelections()
        #     columns = [self.data_df.columns[index] for index in selections]
        #     self.data_df[columns].plot(kind='line')
        #     plt.show()

        dlg = LineDialog(self)
        result = dlg.ShowModal()
        if result != wx.ID_OK:
            dlg.Destroy()
            return
        y_list = dlg.ylist.GetSelections()
        checks = dlg.ylist.GetCheckedItems()
        x_num = dlg.xlist.GetSelection()
        y_list.extend(checks)
        selected_items = []
        for sel in y_list:
            # 使用GetStringSelection获取选中项的文本
            selected_items.append(dlg.ylist.GetString(sel))
        dlg.Destroy()

        line = LineChart(self, x=self.data_df.iloc[:, x_num], y=self.data_df.iloc[:, y_list])
        line.Show()

    def on_3D_plot(self, event):
        dlg = D3Chart(self)
        dlg.Show()

    def on_scatter_plot(self, event):
        dlg = ScatterChart(self)
        dlg.Show()

    def on_d3_scatter_plot(self, event):
        pass

    def on_polar_plot(self, event):
        pass

    def on_radar_plot(self, event):
        pass

    def on_dataset_plot(self, event):
        pass

    def on_graph_plot(self, event):
        pass


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

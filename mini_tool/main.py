import os
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


class ChildTableFrame(wx.MDIChildFrame):
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


class TreeFrame(wx.MDIChildFrame):

    def __init__(self, parent, title="目录", path=None):
        wx.MDIChildFrame.__init__(self, parent, -1, title, pos=(0, 0), size=(300, 500))
        self.tree = wx.TreeCtrl(self)
        root = self.tree.AddRoot('ProjectRoot', data=path)

        self.tree.SetItemData(root, path)
        self.build_tree(path, root)
        self.tree.Expand(root)

        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.on_item_expanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.on_item_collapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.on_sel_changing)
        self.Layout()
        self.Show()

    def build_tree(self, dir_path, parent_item):
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                new_item = self.tree.AppendItem(parent_item, item)
                self.tree.SetItemData(new_item, item_path)
                self.build_tree(item_path, new_item)
            else:
                new_item = self.tree.AppendItem(parent_item, item)
                self.tree.SetItemData(new_item, item_path)

    def on_right_click(self, event):
        menu = wx.Menu()
        delete_item = menu.Append(wx.ID_ANY, 'Delete')
        open_item = menu.Append(wx.ID_ANY, 'Open')
        rename_item = menu.Append(wx.ID_ANY, 'Rename')

        self.Bind(wx.EVT_MENU, self.on_delete, delete_item)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_rename, rename_item)

        self.PopupMenu(menu)

    def on_delete(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Delete clicked, path: {path}")

    def on_open(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Open clicked, path: {path}")

    def on_rename(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Rename clicked, path: {path}")

    def on_item_expanded(self, event):
        print("Item expanded!")

    def on_item_collapsed(self, event):
        print("Item collapsed!")

    def on_sel_changed(self, event):
        print("Selection changed")

    def on_sel_changing(self, event):
        print("Selection changing")


class InitDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "初始化APP", size=(300, 200))
        self.main_windows = parent
        # 创建位图
        # new_project_bitmap = wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, wx.ART_BUTTON, size=(100, 100))
        # open_project_bitmap = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, size=(100, 100))
        new_project_bitmap = wx.Bitmap(svg_to_bitmap(cs.init1_svg, size=(90, 90)))
        open_project_bitmap = wx.Bitmap(svg_to_bitmap(cs.init2_svg, size=(90, 90)))
        # 创建带有图标的按钮
        new_project_button = wx.BitmapButton(self, wx.ID_ANY, new_project_bitmap, size=(100, 100))
        open_project_button = wx.BitmapButton(self, wx.ID_ANY, open_project_bitmap,  size=(100, 100))

        # 设置按钮的提示信息
        new_project_button.SetToolTip("新建项目")
        open_project_button.SetToolTip("打开项目")

        # 创建一个水平方向的布局管理器
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 将按钮添加到布局管理器中
        sizer.Add(new_project_button, 0, wx.ALL, 20)
        sizer.Add(open_project_button, 0, wx.ALL, 20)

        new_project_button.Bind(wx.EVT_LEFT_UP, self.on_new_project)
        open_project_button.Bind(wx.EVT_LEFT_UP, self.on_open_project)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Center()
        self.SetSizer(sizer)
        self.Layout()

    def on_close(self, event):
        self.main_windows.Destroy()

    def on_new_project(self, event):
        # event.Skip()
        self.EndModal(wx.ID_NEW)

    def on_open_project(self, event):
        # event.Skip()
        self.EndModal(wx.ID_OPEN)
        pass


class CreateDirectoryDialog(wx.Dialog):
    def __init__(self, parent, title="新建项目"):
        wx.Dialog.__init__(self, parent, title=title, size=(250, 150))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label="请输入项目名:")
        vbox.Add(self.label, flag=wx.EXPAND | wx.ALL, border=5)

        self.directory_name_text = wx.TextCtrl(panel)
        vbox.Add(self.directory_name_text, flag=wx.EXPAND | wx.ALL, border=5)

        self.button = wx.Button(panel, label="保存")
        self.button.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(self.button, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Center()

    def on_save(self, event):
        self.EndModal(wx.ID_OK)


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
        self.project_path = "./"

        # 创建一个工具栏
        toolbar = self.CreateToolBar(id=wx.ID_ANY, style=wx.TB_TEXT | wx.TB_HORIZONTAL)
        toolbar.SetToolBitmapSize((20, 20))
        # 添加一个文本按钮
        directory_tool = toolbar.AddTool(wx.ID_ANY, 'List', wx.Bitmap(svg_to_bitmap(cs.List_svg)), "打开目录")
        open_file_tool = toolbar.AddTool(wx.ID_ANY, 'File', wx.Bitmap(svg_to_bitmap(cs.of_svg)), "打开文件")
        open_project_tool = toolbar.AddTool(wx.ID_ANY, 'Project', wx.Bitmap(svg_to_bitmap(cs.op_svg)), "打开项目")
        save_tool = toolbar.AddTool(wx.ID_ANY, 'Save', wx.Bitmap(svg_to_bitmap(cs.save_svg)), "保存")
        back_tool = toolbar.AddTool(wx.ID_ANY, 'Back', wx.Bitmap(svg_to_bitmap(cs.back_svg)), "返回")
        exit_tool = toolbar.AddTool(wx.ID_ANY, 'Exit', wx.Bitmap(svg_to_bitmap(cs.exit_svg)), "退出")
        copy_tool = toolbar.AddTool(wx.ID_ANY, 'Copy', wx.Bitmap(svg_to_bitmap(cs.copy_svg)), "复制")
        paste_tool = toolbar.AddTool(wx.ID_ANY, 'Paste', wx.Bitmap(svg_to_bitmap(cs.paste_svg)), "粘贴")
        cut_tool = toolbar.AddTool(wx.ID_ANY, 'Cut', wx.Bitmap(svg_to_bitmap(cs.cut_svg)), "剪切")

        self.Bind(wx.EVT_TOOL, self.on_directory_click, directory_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, open_file_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, open_project_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, save_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, back_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, exit_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, copy_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, paste_tool)
        self.Bind(wx.EVT_TOOL, self.on_tool_click, cut_tool)

        # Menu
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        graph_menu = wx.Menu()
        edit_menu = wx.Menu()
        tool_menu = wx.Menu()
        help_menu = wx.Menu()
        menubar.Append(file_menu, '&File')
        menubar.Append(graph_menu, '&Graph')
        menubar.Append(edit_menu, '&Edit')
        menubar.Append(tool_menu, '&Tools')
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)

        # 创建 FileHistory 对象
        self.filehistory = wx.FileHistory(8)
        self.config = wx.Config(self.TITLE, style=wx.CONFIG_USE_LOCAL_FILE)
        self.filehistory.Load(self.config)
        recent = wx.Menu()
        self.filehistory.UseMenu(recent)
        self.filehistory.AddFilesToMenu()

        # File menu items
        new_project_item = file_menu.Append(wx.ID_ANY, '&New Project', 'New a Project')
        open_project_item = file_menu.Append(wx.ID_ANY, '&Open Project', 'Open a Project')
        open_item = file_menu.Append(wx.ID_OPEN, '&Open File', 'Open a file')
        save_item = file_menu.Append(wx.ID_SAVE, '&Save', 'Save a file')
        recent_item = file_menu.Append(wx.ID_ANY, '&Recent Files', recent)
        quit_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        # Event bindings
        self.Bind(wx.EVT_MENU, self.on_new_project, new_project_item)
        self.Bind(wx.EVT_MENU, self.on_open_project, open_project_item)
        self.Bind(wx.EVT_MENU, self.on_open_file, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_quit, quit_item)
        self.Bind(wx.EVT_MENU_RANGE, self.on_project_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)

        # Graph menu items
        # 柱状图
        bar_chart_item = graph_menu.Append(wx.ID_ANY, 'Bar Chart', 'Generate a bar chart')
        # 折线图
        line_plot_item = graph_menu.Append(wx.ID_ANY, 'Line Plot', 'Generate a line plot')
        # 3D图
        d3_plot_item = graph_menu.Append(wx.ID_ANY, '3D Plot', 'Generate 3D plot')
        # 散点图
        scatter_plot_item = graph_menu.Append(wx.ID_ANY, 'scatter Plot', 'Generate scatter plot')
        # 3D散点图
        d3_scatter_plot_item = graph_menu.Append(wx.ID_ANY, 'scatter 3D Plot', 'Generate 3D scatter plot')
        # 极坐标图
        polar_plot_item = graph_menu.Append(wx.ID_ANY, 'polar Plot', 'Generate polar plot')
        # 雷达图
        radar_plot_item = graph_menu.Append(wx.ID_ANY, 'radar Plot', 'Generate radar plot')
        # 数据集
        dataset_plot_item = graph_menu.Append(wx.ID_ANY, 'dataset Plot', 'Generate dataset plot')
        # 关系图
        graph_plot_item = graph_menu.Append(wx.ID_ANY, 'graph Plot', 'Generate graph plot')
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
        help_item = help_menu.Append(wx.ID_ANY, '&Help', 'Help')
        contact_item = help_menu.Append(wx.ID_ANY, '&Contact Us', 'Contact Us')
        about_item = help_menu.Append(wx.ID_ANY, '&About', 'About Gui')
        self.Bind(wx.EVT_MENU, self.on_help, help_item)
        self.Bind(wx.EVT_MENU, self.on_contact, contact_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        # Parent
        toolbar.Realize()
        self.Show()
        self.create_child_frames()
        self.load_recent_project()
        # 监听HTML服务
        THREAD_POOL.submit(run_server)

    def create_child_frames(self):
        self.top_child_frame = ChildFrame(self, "main")
        self.bottom_child_frame = ChildTableFrame(self, "table")
        self.bottom_child_frame.Show()
        self.top_child_frame.Show()
        # Set child frames to tile HORIZONTAL
        self.Tile(wx.HORIZONTAL)

    def load_recent_project(self):
        recent_project_path = self.get_recent_project_path()
        if recent_project_path:
            self.open_project(recent_project_path)
        else:
            init_dialog = InitDialog(self)
            result = init_dialog.ShowModal()
            # 创建并打开项目
            if result == wx.ID_NEW:
                n_res = self.new_project_dialog()
                n_res or self.load_recent_project()

            # 打开项目
            init_dialog.Destroy()
            o_res = self.open_project_dialog()
            o_res or self.load_recent_project()

    def new_project_dialog(self) -> bool:
        create_dialog = CreateDirectoryDialog(self)
        if create_dialog.ShowModal() == wx.ID_OK:
            directory_name = create_dialog.directory_name_text.GetValue()
            if not directory_name:
                return False

            select_dialog = wx.DirDialog(self, "请选择文件保存路径：", style=wx.DD_DEFAULT_STYLE)
            if select_dialog.ShowModal() != wx.ID_OK:
                return False
            path = os.path.join(select_dialog.GetPath(), directory_name)
            print(f"Chosen directory: {path}")
            os.makedirs(path)
            self.add_history(path)
            self.open_project(path)
            return True

        create_dialog.Destroy()
        return False

    def open_project_dialog(self) -> bool:
        dialog = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            print(f"Chosen directory: {path}")
            self.add_history(path)
            self.open_project(path)
            return True
        return False

    def create_and_open_project(self):
        pass

    def get_recent_project_path(self) -> str:

        if not self.filehistory.GetCount():
            return ""

        path = self.filehistory.GetHistoryFile(0)
        return path

    def read_file(self, filename: str):
        self.data_df = pd.read_csv(filename)
        THREAD_POOL.submit(self.bottom_child_frame.show_data, self.data_df)
        # self.bottom_child_frame.show_data(self.data_df)

    def open_project(self, path: str):
        # 打开项目
        TreeFrame(self, title=path, path=path)
        pass

    def add_history(self, path: str):
        # 将项目路径添加到 FileHistory 中
        self.filehistory.AddFileToHistory(path)
        self.filehistory.Save(self.config)
        self.config.Flush()

    def on_directory_click(self, event):
        tree_frame = TreeFrame(self, title=self.project_path, path=self.project_path)

    def on_tool_click(self, event):
        pass

    def on_project_history(self, event):
        file_num = event.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(file_num)
        self.filehistory.AddFileToHistory(path)
        # reopen project
        self.open_project(path)

    def on_open_file(self, event):
        wildcard = "CSV files (*.csv)|*.csv"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            self.read_file(filename)
        dialog.Destroy()

    def on_new_project(self, event):
        self.new_project_dialog()

    def on_open_project(self, event):
        self.open_project_dialog()

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
            self.Destroy()

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

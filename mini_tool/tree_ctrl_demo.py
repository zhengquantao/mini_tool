import wx
import os


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(300, 300))

        self.tree = wx.TreeCtrl(self)
        root = self.tree.AddRoot('Root')
        self.tree.SetItemData(root, os.getcwd())
        self.buildTree(os.getcwd(), root)
        self.tree.Expand(root)

        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging)

        self.Centre()
        self.Show(True)

    def buildTree(self, dirPath, parentItem):
        for item in os.listdir(dirPath):
            itemPath = os.path.join(dirPath, item)
            if os.path.isdir(itemPath):
                newItem = self.tree.AppendItem(parentItem, item)
                self.tree.SetItemData(newItem, itemPath)
                self.buildTree(itemPath, newItem)
            else:
                newItem = self.tree.AppendItem(parentItem, item)
                self.tree.SetItemData(newItem, itemPath)

    def OnRightClick(self, event):
        menu = wx.Menu()
        delete_item = menu.Append(wx.ID_ANY, 'Delete')
        open_item = menu.Append(wx.ID_ANY, 'Open')
        rename_item = menu.Append(wx.ID_ANY, 'Rename')

        self.Bind(wx.EVT_MENU, self.OnDelete, delete_item)
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        self.Bind(wx.EVT_MENU, self.OnRename, rename_item)

        self.PopupMenu(menu)

    def OnDelete(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Delete clicked, path: {path}")

    def OnOpen(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Open clicked, path: {path}")

    def OnRename(self, event):
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        print(f"Rename clicked, path: {path}")

    def OnItemExpanded(self, event):
        print("Item expanded!")

    def OnItemCollapsed(self, event):
        print("Item collapsed!")

    def OnSelChanged(self, event):
        print("Selection changed")

    def OnSelChanging(self, event):
        print("Selection changing")


app = wx.App()
Mywin(None, "TreeCtrl Demo")
app.MainLoop()

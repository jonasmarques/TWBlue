# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import wx
import widgetUtils
from multiplatform_widgets import widgets

class listViewer(widgetUtils.BaseDialog):

    def __init__(self, *args, **kwargs):
        super(listViewer, self).__init__(parent=None, *args, **kwargs)
        self.SetTitle(_(u"Lists manager"))
        panel = wx.Panel(self)
        label = wx.StaticText(panel, -1, _(u"Lists"))
        self.lista = widgets.list(panel, _(u"List"), _(u"Description"), _(u"Owner"), _(u"Members"), _(u"mode"), size=(800, 800), style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.lista.list.SetFocus()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label)
        sizer.Add(self.lista.list)
        self.createBtn = wx.Button(panel, wx.ID_ANY, _(u"Create a new list"))
        self.editBtn = wx.Button(panel, -1, _(u"Edit"))
        self.deleteBtn = wx.Button(panel, -1, _(u"Remove"))
        self.view = wx.Button(panel, -1, _(u"Open in buffer"))
#  self.members = wx.Button(panel, -1, _(u"View members"))
#  self.members.Disable()
#  self.subscriptors = wx.Button(panel, -1, _(u"View subscribers"))
#  self.subscriptors.Disable()
#  self.get_linkBtn = wx.Button(panel, -1, _(u"Get link for the list"))
#  self.get_linkBtn.Bind(wx.EVT_BUTTON, self.onGetLink)
        self.cancelBtn = wx.Button(panel, wx.ID_CANCEL)
        btnSizer = wx.BoxSizer()
        btnSizer.Add(self.createBtn)
        btnSizer.Add(self.editBtn)
        btnSizer.Add(self.cancelBtn)
        panel.SetSizer(sizer)

    def populate_list(self, lists, clear=False):
        if clear == True:
            self.clear()
        for item in lists:
            self.lista.insert_item(False, *item)

    def get_item(self):
        return self.lista.get_selected()

    def clear(self):
        self.lista.clear()

class userListViewer(listViewer):
    def __init__(self, username, *args, **kwargs):
        self.username = username
        super(userListViewer, self).__init__(*args, **kwargs)
        self.SetTitle(_(u"Viewing lists for %s") % (self.username))
        self.createBtn.SetLabel(_(u"Subscribe"))
        self.deleteBtn.SetLabel(_(u"Unsubscribe"))
        self.editBtn.Disable()
        self.view.Disable()

class createListDialog(widgetUtils.BaseDialog):

    def __init__(self, *args, **kwargs):
        super(createListDialog, self).__init__(parent=None, *args, **kwargs)
        self.SetTitle(_(u"Create a new list"))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        name = wx.StaticText(panel, -1, _(u"Name (20 characters maximun)"))
        self.name = wx.TextCtrl(panel, -1)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(name)
        nameSizer.Add(self.name)
        description = wx.StaticText(panel, -1, _(u"Description"))
        self.description = wx.TextCtrl(panel, -1)
        descriptionSizer = wx.BoxSizer(wx.HORIZONTAL)
        descriptionSizer.Add(description)
        descriptionSizer.Add(self.description)
        mode = wx.StaticText(panel, -1, _(u"Mode"))
        self.public = wx.RadioButton(panel, -1, _(u"Public"), style=wx.RB_GROUP)
        self.private = wx.RadioButton(panel, -1, _(u"Private"))
        modeBox = wx.BoxSizer(wx.HORIZONTAL)
        modeBox.Add(mode)
        modeBox.Add(self.public)
        modeBox.Add(self.private)
        ok = wx.Button(panel, wx.ID_OK)
        ok.SetDefault()
        cancel = wx.Button(panel, wx.ID_CANCEL)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(ok)
        btnBox.Add(cancel)
        sizer.Add(nameSizer)
        sizer.Add(descriptionSizer)
        sizer.Add(modeBox)
        sizer.Add(btnBox)

class editListDialog(createListDialog):

    def __init__(self, list, *args, **kwargs):
        super(editListDialog, self).__init__(*args, **kwargs)
        self.SetTitle(_(u"Editing the list %s") % (list.name))
        self.name.ChangeValue(list.name)
        self.description.ChangeValue(list.description)
        if list.mode == "public":
            self.public.SetValue(True)
        else:
            self.private.SetValue(True)

class addUserListDialog(listViewer):
    def __init__(self, *args, **kwargs):
        super(addUserListDialog, self).__init__(*args, **kwargs)
        self.SetTitle(_(u"Select a list to add the user"))
        self.createBtn.SetLabel(_(u"Add"))
        self.createBtn.SetDefault()
        self.createBtn.Bind(wx.EVT_BUTTON, self.ok)
        self.editBtn.Disable()
        self.view.Disable()
#  self.subscriptors.Disable()
#  self.members.Disable()
        self.deleteBtn.Disable()
        widgetUtils.connect_event(self.lista.list, widgetUtils.KEYPRESS, self.on_keypress)

    def on_keypress(self, event):
        """Catch return and execute ok()"""
        if event.GetKeyCode() == wx.WXK_RETURN:
            return self.ok()
        event.Skip()

    def ok(self, *args, **kwargs):
        self.EndModal(wx.ID_OK)

class removeUserListDialog(listViewer):
    def __init__(self, *args, **kwargs):
        super(removeUserListDialog, self).__init__(*args, **kwargs)
        self.SetTitle(_(u"Select a list to remove the user"))
        self.createBtn.SetLabel(_(u"Remove"))
        self.createBtn.SetDefault()
        self.createBtn.SetId(wx.ID_OK)
        self.editBtn.Disable()
        self.view.Disable()
#  self.subscriptors.Disable()
#  self.members.Disable()
        self.deleteBtn.Disable()
        widgetUtils.connect_event(self.lista.list, widgetUtils.KEYPRESS, self.on_keypress)

    def on_keypress(self, event):
        """Catch return and execute EndModal()"""
        if event.GetKeyCode() == wx.WXK_RETURN:
            return self.EndModal(wx.ID_OK)
        event.Skip()

def remove_list():
    return wx.MessageDialog(None, _("Do you really want to delete this list?"), _("Delete"), wx.YES_NO).ShowModal()


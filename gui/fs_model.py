from PyQt5.QtWidgets import QFileSystemModel
from PyQt5 import QtCore, QtGui
from enum import Enum

# class CheckedDirState(Enum):
#     SET_BY_PARENT = 0
#     SET_BY_CHILD = 1
#     UNCHECKED = 2
#     CHECKED = 3


def get_num_index_children(index):
    return index.model().rowCount(index)

def get_children(index):
    num_children = get_num_index_children(index)
    return (index.child(ii, 0) for ii in range(num_children))

def get_siblings(index):
    ii = 0
    while True:
        sibling = index.sibling(ii, 0)
        if not sibling.isValid():
            break
        yield sibling
        ii += 1


class CheckedStateModel(object):
    def __init__(self):
        self.__checked_nodes = set()

    def is_explicitly_checked(self, index):
        return index in self.__checked_nodes

    def uncheck(self, index):
        if self.is_explicitly_checked(index):
            self.__checked_nodes.remove(index)

    def is_parent_checked(self, index):
        parent = index.parent()
        if not parent.isValid():
            return False
        elif self.is_explicitly_checked(parent):
            return True
        else:
            return self.is_parent_checked(parent)

    def is_any_child_checked(self, index):
        children = get_children(index)
        direct_child_checked = any(self.is_explicitly_checked(c) for c in children)

        # need to call get_children() again, otherwise the children
        # iterator is already been iteratred through.
        children = get_children(index)
        return direct_child_checked or any(self.is_any_child_checked(c) for c in children)

    def get_checked_state(self, index):
        if self.is_explicitly_checked(index):
            return QtCore.Qt.Checked
        elif self.is_parent_checked(index):
            return QtCore.Qt.Checked
        elif self.is_any_child_checked(index):
            return QtCore.Qt.PartiallyChecked
        else:
            return QtCore.Qt.Unchecked

    def uncheck_recursive(self, index):
        self.uncheck(index)
        for c in get_children(index):
            self.uncheck_recursive(c)

    def normalize_unchecked(self, index):
        siblings = list(get_siblings(index))
        if all(self.is_explicitly_checked(s) for s in siblings):
            parent = index.parent()
            if parent.isValid():
                for s in siblings:
                    self.uncheck(s)
                self.mark_explicit_checked(parent)
                self.normalize_unchecked(parent)

    def normalize_partial(self, index):
        self.uncheck_recursive(index)

    def find_root_checked_node(self, index):
        if not index.isValid() or self.is_explicitly_checked(index):
            return index
        else:
            return self.find_root_checked_node(index.parent())

    def normalize_checked(self, index):
        self.uncheck_recursive(index)
        root_checked = self.find_root_checked_node(index)
        if root_checked.isValid():
            self.uncheck(root_checked)
            for s in get_siblings(index):
                if s != index:
                    self.mark_explicit_checked(s)

    def mark_explicit_checked(self, index):
        self.__checked_nodes.add(index)

def get_name(index):
    return index.model().data(index, QtCore.Qt.DisplayRole)

class CheckedFsModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = CheckedStateModel()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.CheckStateRole:
            return super().data(index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        flags = super().flags(index)
        flags |= QtCore.Qt.ItemIsUserCheckable
        flags |= QtCore.Qt.ItemIsTristate
        return flags

    def checkState(self, index):
        return self.state.get_checked_state(index)

    def __unchecked_to_checked(self, index):
        self.state.mark_explicit_checked(index)
        self.state.normalize_unchecked(index)

    def __partial_to_checked(self, index):
        self.state.normalize_partial(index)
        self.state.mark_explicit_checked(index)

    def __checked_to_unchecked(self, index):
        self.state.normalize_checked(index)

    def setData(self, index, value, role):
        if (role == QtCore.Qt.CheckStateRole) and (index.column() == 0):
            old_state = self.checkState(index)
            if old_state == QtCore.Qt.Unchecked:
                self.__unchecked_to_checked(index)
            elif old_state == QtCore.Qt.PartiallyChecked:
                self.__partial_to_checked(index)
            elif old_state == QtCore.Qt.Checked:
                self.__checked_to_unchecked(index)
            ii = index
            while ii.parent().isValid():
                ii = ii.parent()
            self.dataChanged.emit(ii, index)

            return True
        
        return super().setData(index, value, role)


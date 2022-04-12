import sys
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide.QtCore import *
from PySide.QtGui import *
#from PyQt4.QtSql import *
from log import *
from model import Models
from model import Traveller
from resources import qrc_resources

MAC = "qt_mac_set_native_menubar" in dir()

##NAME = 0
##COL = 1
##ROW = 2
##STARPORT = 3

ACQUIRED = 1


class WorldDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(WorldDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)
        if index.column() == Models.STARPORT:
            myoption.displayAlignment |= Qt.AlignRight|Qt.AlignVCenter
        QStyledItemDelegate.paint(self, painter, myoption, index)

    @logmethod
    def createEditor(self, parent, option, index):
        if index.column() == Models.ROW:
            editor = Traveller.RowSpinBox(parent)
            editor.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return editor
        elif index.column() == Models.COL:
            editor = Traveller.ColumnSpinBox(parent)
            editor.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return editor
        elif index.column() == Models.STARPORT:
            editor = Traveller.StarportComboBox(parent)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent,
                                                       option, index)
    @logmethod
    def setEditorData(self, editor, index):
        if index.column() == Models.ROW:
            num, ok = index.data(Qt.DisplayRole).toInt()
            editor.setValue(num)
        elif index.column() == Models.COL:
            num,  ok = index.data(Qt.DisplayRole).toInt()
            editor.setValue(num)
        elif index.column() == Models.STARPORT:
            portref, ok = index.data(Qt.EditRole).toInt()
            editor.setCurrentIndex(portref)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    @logmethod
    def setModelData(self, editor, model, index):
        if index.column() == Models.ROW:
            debug_log("Row index " + str(index) +
                      " Value " + str(editor.value()))
            model.setData(index, editor.value())
        elif index.column() == Models.COL:
            debug_log("Col index " + str(index) +
                      " Value " + str(editor.value()))
            model.setData(index, editor.value())
        elif index.column() == Models.STARPORT:
            debug_log("Starport index " + str(index) +
                      " Value " + str(editor.currentIndex()))
            model.setData(index, editor.currentIndex(), Qt.EditRole)
        else:
            debug_log("Other field index " + str(index))
            QStyledItemDelegate.setModelData(self, editor, model, index)


class WorldBrowser(QDialog):

    def __init__(self, world_model, parent=None):
        super(WorldBrowser, self).__init__(parent)

        info_log("Initialising WorldBrowser")

        self.worldModel = world_model

        self.worldView = QTableView()
        self.worldView.setModel(self.worldModel)
        self.worldView.setItemDelegate(WorldDelegate(self))
        self.worldView.setSelectionMode(QTableView.SingleSelection)
        self.worldView.setSelectionBehavior(QTableView.SelectRows)
        #self.worldView.setColumnHidden(ID, True)
        self.worldView.resizeColumnsToContents()
        worldLabel = QLabel("W&orlds")
        worldLabel.setBuddy(self.worldView)

        self.addWorldButton = QPushButton("&Add World")
        self.deleteWorldButton = QPushButton("&Delete World")
        self.quitButton = QPushButton("&Quit")
        for button in (addWorldButton, deleteWorldButton, quitButton):
            if MAC:
                button.setDefault(False)
                button.setAutoDefault(False)
            else:
                button.setFocusPolicy(Qt.NoFocus)

        dataLayout = QVBoxLayout()
        dataLayout.addWidget(self.worldView, 1)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.addWorldButton)
        buttonLayout.addWidget(self.deleteWorldButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.quitButton)
        layout = QHBoxLayout()
        layout.addLayout(dataLayout, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

##        self.connect(addWorldButton, SIGNAL("clicked()"),
##                     self.addWorld)
##        self.connect(deleteWorldButton, SIGNAL("clicked()"),
##                     self.deleteWorld)
##        self.connect(quitButton, SIGNAL("clicked()"), self.done)

        self.addWorldButton.clicked.connect(self.addWorld)
        self.deleteWorldButton.clicked.connect(self.deleteWorld)
        self.quitButton.clicked.connect(self.done)

        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        self.setWindowTitle("World Manager")


    def done(self, result=1):
        QDialog.done(self, 1)

    @logmethod
    def worldChanged(self, index):
        pass


    @logmethod
    def addWorld(self):
        row = self.worldView.currentIndex().row() \
            if self.worldView.currentIndex().isValid() else 0

        self.worldModel.insertRandomWorld(row)
        index = self.worldModel.index(row, Models.NAME)
        self.worldView.setCurrentIndex(index)

        self.worldView.edit(index)

    #@logmethod
    def deleteWorld(self):
        index = self.worldView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.worldModel.removeRows(row)



if __name__ == '__main__':
    model = Models.WorldModel()
    
    for world in Models.generateTestWorlds():
        model.worlds.append(world)

    model.reset()
    model.dirty = False
    
    app = QApplication(sys.argv)
    form = WorldBrowser(model)
    form.show()
    app.exec_()

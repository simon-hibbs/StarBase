#!/usr/bin/env python

#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)


import os
import sys
import math
from PySide import QtCore, QtGui
#from PyQt4 import QtOpenGL
from model import Models
from starmap import MapGlyphs
from starmap import MapScene
from projects import ProjectManager
from forms import WorldBrowser
from forms import AllegianceEditor
from forms import Trade
from categories import WorldGenerator
from yapsy.PluginManager import PluginManager
#from forms import Trade
from resources import starmap_rc
import log

log.set_logger()

InsertTextButton = 10

class OccurrenceSpinBox(QtGui.QSpinBox):
    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        self.setMinimum(-2)
        self.setMaximum(2)
        self.setValue(0)
        self.lineEdit().setReadOnly(True)

    def textFromValue(self, value):
        if value >= 0:
            text = '+' + str(value)
            return text
        elif value < 0:
            text = str(value)
            return text

class MapView(QtGui.QGraphicsView):
    
    changeZoomLevel = QtCore.Signal(QtGui.QWheelEvent)
    
    def __init__(self,  scene=None):
        QtGui.QGraphicsView.__init__(self,  scene)
        #self.setViewportUpdateMode(self.SmartViewportUpdate)
        self.setViewportUpdateMode(self.FullViewportUpdate)
        #self.setViewport(QtOpenGL.QGLWidget())
        self.hzsb = self.horizontalScrollBar()
        self.vtsb = self.verticalScrollBar()
        #self.connect(hzsb,
        #             QtCore.SIGNAL("valueChanged(int)"),
        #             scene.viewMoveDetected)
        self.hzsb.valueChanged[int].connect(scene.viewMoveDetected)
        #self.connect(hzsb,
        #             QtCore.SIGNAL("valueChanged(int)"),
        #             scene.viewMoveDetected)
        self.vtsb.valueChanged[int].connect(scene.viewMoveDetected)

    def wheelEvent(self,  event):
        view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        self.centerOn(scene_pos)
        self.changeZoomLevel.emit(event)

    def setupMatrix(self, ml):
        self.setMatrix(QtGui.QMatrix(ml[0], ml[1], ml[2], ml[3], ml[4], ml[5]))


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.model = Models.WorldModel()

        self.createActions()
        self.createMenus()
        #self.createToolBox()

        self.worldItemView = MapScene.WorldItemView(self.model)
        self.scene = self.worldItemView.scene

        self.beginCreateGroup = False
        self.createToolbars()

        layout = QtGui.QHBoxLayout()
        #layout.addWidget(self.toolBox)
        self.view = MapView(self.scene)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing)
        
        layout.addWidget(self.view)
        self.view.changeZoomLevel.connect(self.wheelScrollZoom)

        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("StarBase")
        self.pointerGroupClicked(1)

        self.sceneScaleCombo.setCurrentIndex(self.model.initialZoomLevel)
        self.sceneScaleChanged(self.sceneScaleCombo.currentText())
        
        self.view.horizontalScrollBar().setValue(self.model.horizontalScroll)
        self.view.verticalScrollBar().setValue(self.model.verticalScroll)
        #self.view.setupMatrix(self.model.initalDisplayMatrix)
        self.selectionTypeCombo.setCurrentIndex(0)
        self.selectionTypeChanged(self.selectionTypeCombo.currentText())

        self.projectManager()

        self.scene.setFromTradeWorld.connect(self.setFromTradeWorld)
        self.scene.setToTradeWorld.connect(self.setToTradeWorld)
        #self.generateCargoButton.clicked.connect(self.generateCargo)
        self.tradeButton.clicked.connect(self.openTradeDialog)
        
        

    def setWorldOccurrenceDM(self, value):
        self.model.worldOccurrenceDM = value

    def toggleAutoName(self, flag):
        if flag == QtCore.Qt.Checked:
            self.model.toggleAutoName(True)
        else:
            self.model.toggleAutoName(False)

    def toggleAllegianceDisplay(self, flag):
        if flag == QtCore.Qt.Checked:
            self.scene.toggleAllegianceDisplay(True)
        else:
            self.scene.toggleAllegianceDisplay(False)

    def pointerGroupClicked(self, i):
        if self.pointerTypeGroup.checkedId() == self.scene.SELECT_MODE:
            self.view.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.view.setInteractive(True)
            self.scene.setMode(self.pointerTypeGroup.checkedId())
            
        elif self.pointerTypeGroup.checkedId() == self.scene.RUBBER_BAND_MODE:
            self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.view.setInteractive(True)
            self.scene.setMode(self.pointerTypeGroup.checkedId())
            
        elif self.pointerTypeGroup.checkedId() == self.scene.HAND_DRAG_MODE:
            self.view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.view.setInteractive(False)
            #self.scene.setCellsSelectable(False)
            self.scene.setMode(self.pointerTypeGroup.checkedId())
            
        else:
            self.view.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.view.setInteractive(True)
            self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if len(self.scene.selectedItems()) == 0:
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() >= zValue and
                isinstance(item, StarMap.MapItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if len(self.scene.selectedItems()) == 0:
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and
                isinstance(item, StarMap.MapItem)):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

##    def itemInserted(self, item):
##        self.scene.setMode(self.pointerTypeGroup.checkedId())
##        self.buttonGroup.button(item.diagramType).setChecked(False)
##
##    def textInserted(self, item):
##        self.buttonGroup.button(InsertTextButton).setChecked(False)
##        self.scene.setMode(pointerTypeGroup.checkedId())

##    def currentFontChanged(self, font):
##        self.handleFontChange()
##
##    def fontSizeChanged(self, font):
##        self.handleFontChange()

    def wheelScrollZoom(self,  event):
        index = self.sceneScaleCombo.currentIndex()
        if event.delta() > 0:
            if index < 16:
                index = index + 1 
        elif event.delta() < 0:
            if index >0:
                index = index - 1
        self.sceneScaleCombo.setCurrentIndex(index)

    def sceneScaleChanged(self, scale):
        #newScale = scale.left(scale.indexOf("%")).toDouble()[0] / 100.0
        newScale = float(scale[0:scale.index('%')]) / 100.0
        #self.scene.rebuild(newScale)
        oldMatrix = self.view.matrix()
        self.view.resetMatrix()
        self.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.scene.setScale(newScale)
        self.view.scale(newScale, newScale)


    def projectManager(self):
        projectManager = ProjectManager.ProjectManager(self.model, self)
        result = projectManager.exec_()
        app.processEvents()

        if result == 1:
            self.worldItemView = MapScene.WorldItemView(self.model)
            self.scene = self.worldItemView.scene

            self.view.setScene(self.scene)
            self.view.changeZoomLevel.connect(self.wheelScrollZoom)
            self.pointerGroupClicked(1)
            self.sceneScaleCombo.setCurrentIndex(self.model.initialZoomLevel)
            self.sceneScaleChanged(self.sceneScaleCombo.currentText())
            self.view.horizontalScrollBar().setValue(self.model.horizontalScroll)
            self.view.verticalScrollBar().setValue(self.model.verticalScroll)
            self.selectionTypeCombo.setCurrentIndex(0)
            self.selectionTypeChanged(self.selectionTypeCombo.currentText())
            self.refreshGroupComboBox()
            self.refreshWorldGeneratorsCombo()
            
        elif result == 0:
            log.debug_log('Application closing. No project opened.')
            sys.exit()

    #@QtCore.pyqtSlot(str)
    def setFromTradeWorld(self):
        name = self.model.getWorld(self.model.fromTradeWorldPmi).name
        self.tradeFromWorldName.setText(name)

    def setToTradeWorld(self):
        name = self.model.getWorld(self.model.toTradeWorldPmi).name
        self.tradeToWorldName.setText(name)

    def generateCargo(self):
        pass
##        fromWorld = self.model.getWorld(self.model.fromTradeWorldPmi)
##        toWorld = self.model.getWorld(self.model.toTradeWorldPmi)
##        log.debug_log('Trade from ' + fromWorld.name + ' to ' + toWorld.name)
##        self.tradeDialog = Trade.TradeDialog(self.model, self.scene)
##        self.tradeDialog.show()
##        self.tradeDialog.activateWindow()
##        app.processEvents()

    def openTradeDialog(self):
        self.tradeDialog = Trade.MerchantDetailsDialog(self.model, self)
        self.tradeDialog.show()
        self.tradeDialog.activateWindow()
        app.processEvents()

    def selectGroup(self, index):
        if self.beginCreateGroup == False:
            self.scene.selectGroup(index)
        self.model.selectedGroup = index

    def createGroup(self):
        # Temporarily disable clearing of currently selected hexes
        self.beginCreateGroup = True
        #ok = 0
        group_name, ok = QtGui.QInputDialog.getText(self, 'Crate New Group',
                                                'New Group Name:',
                                                QtGui.QLineEdit.Normal)
        if ok and group_name:
            self.model.addNewGroup(str(group_name))
            #debug_log('App: New group "' + str(group_name) + '" added')
            self.refreshGroupComboBox()
            last_item = self.groupSelectionCombo.count() - 1
            self.groupSelectionCombo.setCurrentIndex(last_item)
            self.beginCreateGroup = False
        else:
            self.beginCreateGroup = False
            log.debug_log('App: Adding new group failed. Name: ' + str(group_name))

    def updateGroup(self):
        index = self.groupSelectionCombo.currentIndex()
        if index != 0:
            self.scene.addCellsToGroup(index)

    def disbandGroup(self):
        index = self.groupSelectionCombo.currentIndex()
        self.model.disbandGroup(index)
        self.refreshGroupComboBox()

    def refreshGroupComboBox(self):
        self.groupSelectionCombo.clear()
        self.groupSelectionCombo.addItems(self.model.groupNames)

    def setWorldGenerator(self):
        self.model.currentWorldGeneratorName = str(self.worldGeneratorsCombo.currentText())

    def refreshWorldGeneratorsCombo(self):
        self.worldGeneratorsCombo.clear()
        self.model.worldGenerators = {}
        #print self.model.manager.getPluginsOfCategory('WorldGenerators')
        for plugin in self.model.manager.getPluginsOfCategory('WorldGenerators'):
            log.debug_log('Setting up plugin ' + plugin.plugin_object.name)
            # plugin.plugin_object is an instance of the plugin
            self.worldGeneratorsCombo.addItem(plugin.plugin_object.name)
            self.model.worldGenerators[plugin.plugin_object.name] = plugin.plugin_object
            if plugin.plugin_object.name == self.model.defaultWorldGeneratorName:
                default_index = self.worldGeneratorsCombo.count() - 1
        self.worldGeneratorsCombo.setCurrentIndex(default_index)
        

    def save(self):
        self.model.storeZoomLevel(self.sceneScaleCombo.currentIndex())
        h = self.view.horizontalScrollBar().value()
        v = self.view.verticalScrollBar().value()
        self.model.storeHorizontalScroll(h)
        self.model.storeVerticalScroll(v)
        self.model.save()

    def selectionTypeChanged(self, selectionType):
        self.scene.setSelectionType(selectionType)


    def about(self):
        QtGui.QMessageBox.about(self, ("About StarBase"),
            ("<b>StarBase</b>, the science fiction star mapping application by Simon D. Hibbs."))


    def createActions(self):

        # File Menu actions
        projectManagerAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "&Project Manager", self)
        projectManagerAction.setShortcut("Ctrl+M")
        projectManagerAction.setStatusTip("Open the Project Manager")
        #self.connect(projectManagerAction,
        #             QtCore.SIGNAL("triggered()"),
        #             self.projectManager)
        projectManagerAction.triggered.connect(self.projectManager)
        self.projectManagerAction = projectManagerAction
        
        saveWorldDataAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "&Save World Data", self)
        saveWorldDataAction.setShortcut("Ctrl+S")
        saveWorldDataAction.setStatusTip("Save the World Data")
        #self.connect(saveWorldDataAction,
        #             QtCore.SIGNAL("triggered()"),
        #             self.save)
        saveWorldDataAction.triggered.connect(self.save)
        self.saveWorldDataAction = saveWorldDataAction


        worldBrowserAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "&World Browser", self)
        worldBrowserAction.setShortcut("Ctrl+W")
        worldBrowserAction.setStatusTip("Open the World Browser")
        #self.connect(worldBrowserAction, QtCore.SIGNAL("triggered()"),
        #        self.openWorldBrowser)
        worldBrowserAction.triggered.connect(self.openWorldBrowser)
        self.worldBrowserAction = worldBrowserAction

        ###
        sectorBrowserAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "&Sector Browser", self)
        sectorBrowserAction.setShortcut("Ctrl+W")
        sectorBrowserAction.setStatusTip("Open the Sector Browser")
        #self.connect(sectorBrowserAction, QtCore.SIGNAL("triggered()"),
        #        self.openSectorBrowser)
        sectorBrowserAction.triggered.connect(self.openSectorBrowser)
        self.sectorBrowserAction = sectorBrowserAction

        subsectorBrowserAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "S&ubsector Browser", self)
        subsectorBrowserAction.setShortcut("Ctrl+W")
        subsectorBrowserAction.setStatusTip("Open the Subsector Browser")
        #self.connect(subsectorBrowserAction, QtCore.SIGNAL("triggered()"),
        #        self.openSubsectorBrowser)
        subsectorBrowserAction.triggered.connect(self.openSubsectorBrowser)
        self.subsectorBrowserAction = subsectorBrowserAction

	###
        allegianceEditorAction = QtGui.QAction(QtGui.QIcon(":/images/undefined.png"),
                                    "Allegiance Colors", self)
        allegianceEditorAction.setShortcut("Ctrl+A")
        allegianceEditorAction.setStatusTip("Open the Allegiance Editor")
        #self.connect(allegianceEditorAction, QtCore.SIGNAL("triggered()"),
        #        self.openAllegianceEditor)
        allegianceEditorAction.triggered.connect(self.openAllegianceEditor)
        self.allegianceEditorAction =  allegianceEditorAction

        exitAction = QtGui.QAction("E&xit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.setStatusTip("Quit StarBase")
        #self.connect(exitAction, QtCore.SIGNAL("triggered()"), self.exitApp)
        exitAction.triggered.connect(self.exitApp)
        self.exitAction = exitAction

        aboutAction = QtGui.QAction("A&bout", self)
        aboutAction.setShortcut("Ctrl+B")
        #self.connect(aboutAction, QtCore.SIGNAL("triggered()"),
        #        self.about)
        aboutAction.triggered.connect(self.about)
        self.aboutAction = aboutAction

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        #self.fileMenu.addAction(self.projectManagerAction)
        self.fileMenu.addAction(self.saveWorldDataAction)
        self.fileMenu.addAction(self.exitAction)

        self.configMenu = self.menuBar().addMenu("&Config")
        self.configMenu.addAction(self.allegianceEditorAction)

##        self.itemMenu = self.menuBar().addMenu("&Item")
##        self.itemMenu.addAction(self.addWorldAction)
##        self.itemMenu.addAction(self.deleteWorldAction)
##
##        self.dataMenu = self.menuBar().addMenu("&Data")
##        self.dataMenu.addAction(self.worldBrowserAction)
##        self.dataMenu.addAction(self.subsectorBrowserAction)
##        self.dataMenu.addAction(self.sectorBrowserAction)
        
        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutAction)

    def createToolbars(self):
        # Pointers
        self.selectionTypeCombo = QtGui.QComboBox()
        selectionTypes = ['Hexes', 'Subsectors', 'Sectors']
        self.selectionTypeCombo.addItems(selectionTypes)
        self.selectionTypeCombo.currentIndexChanged[str].connect(self.selectionTypeChanged)
        
        pointerButton = QtGui.QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QtGui.QIcon(":/images/pointer.png"))

        rubberBandPointerButton = QtGui.QToolButton()
        rubberBandPointerButton.setCheckable(True)
        rubberBandPointerButton.setIcon(QtGui.QIcon(":/images/rubber_band.png"))
        
        handDragPointerButton = QtGui.QToolButton()
        handDragPointerButton.setCheckable(True)
        handDragPointerButton.setIcon(QtGui.QIcon(":/images/grab_hand.png"))

        pointerTypeGroup = QtGui.QButtonGroup()
        pointerTypeGroup.addButton(pointerButton,
                                    int(MapScene.MapScene.SELECT_MODE))
        pointerTypeGroup.addButton(rubberBandPointerButton,
                                    int(MapScene.MapScene.RUBBER_BAND_MODE))
        pointerTypeGroup.addButton(handDragPointerButton,
                                    int(MapScene.MapScene.HAND_DRAG_MODE))
        pointerTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)
        self.pointerTypeGroup = pointerTypeGroup

        self.sceneScaleCombo = QtGui.QComboBox()
        #scales = ["3%","6%","12%","25%", "50%", "65%", "75%", "100%", "133%", "200%"]
        scales = ['3%', '5%', '8%', '12%', '18%', '25%', '37%', '50%', '60%', '70%', \
                   '80%', '90%', '100%', '120%', '140%', '160%', '200%']
        self.sceneScaleCombo.addItems(scales)
        self.sceneScaleCombo.currentIndexChanged[str].connect(self.sceneScaleChanged)

        pointerToolbar = self.addToolBar("Pointer type")
        pointerToolbar.addWidget(QtGui.QLabel('Select:  '))
        pointerToolbar.addWidget(self.selectionTypeCombo)
        pointerToolbar.addWidget(QtGui.QLabel('   Pointer Mode: '))
        pointerToolbar.addWidget(pointerButton)
        #pointerToolbar.addWidget(rubberBandPointerButton)
        pointerToolbar.addWidget(handDragPointerButton)
        pointerToolbar.addWidget(QtGui.QLabel(' Zoom level: '))
        pointerToolbar.addWidget(self.sceneScaleCombo)
        self.pointerToolbar = pointerToolbar

        occurrenceSpinBox = OccurrenceSpinBox()
        #self.connect(occurrenceSpinBox,
        #             QtCore.SIGNAL("valueChanged(int)"),
        #             self.setWorldOccurrenceDM)
        occurrenceSpinBox.valueChanged[int].connect(self.setWorldOccurrenceDM)
        self.worldGeneratorsCombo = QtGui.QComboBox()
        self.worldGeneratorsCombo.currentIndexChanged.connect(self.setWorldGenerator)        
        worldsToolbar = self.addToolBar("Worlds Toolbar")
        worldsToolbar.addWidget(QtGui.QLabel('World Occurrence:  '))
        worldsToolbar.addWidget(occurrenceSpinBox)
        worldsToolbar.addWidget(QtGui.QLabel('  World Generator:  '))
        worldsToolbar.addWidget(self.worldGeneratorsCombo)

        autoNameCheckBox = QtGui.QCheckBox('AutoName')
        autoNameCheckBox.setToolTip('World names are randomly chosen from a list,\ninstead of based on their grid coordinates.')
        autoNameCheckBox.setChecked(self.model.auto_name)
        autoNameCheckBox.stateChanged[int].connect(self.toggleAutoName)
        worldsToolbar.addWidget(autoNameCheckBox)

        self.worldsToolbar = worldsToolbar

        allegianceCheckBox = QtGui.QCheckBox('Display Allegiances')
        #self.connect(allegianceCheckBox,
        #             QtCore.SIGNAL("stateChanged(int)"),
        #             self.toggleAllegianceDisplay)
        allegianceCheckBox.stateChanged[int].connect(self.toggleAllegianceDisplay)
        displayToolbar = self.addToolBar("Display Toolbar")
        displayToolbar.addWidget(allegianceCheckBox)

        self.displayToolbar = displayToolbar

        self.addToolBarBreak()

        groupsToolbar = self.addToolBar("Groups Toolbar")
        groupsToolbar.addWidget(QtGui.QLabel('Select Hex Group: '))
        self.groupSelectionCombo = QtGui.QComboBox()
        self.groupSelectionCombo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        #self.groupSelectionCombo.currentIndexChanged[int].connect(self.selectGroup)
        self.groupSelectionCombo.activated[int].connect(self.selectGroup)
        groupsToolbar.addWidget(self.groupSelectionCombo)
        
        self.createGroupButton = QtGui.QPushButton('New (empty)')
        self.createGroupButton.clicked.connect(self.createGroup)
        groupsToolbar.addWidget(self.createGroupButton)

        self.updateGroupButton = QtGui.QPushButton('Update')
        self.updateGroupButton.clicked.connect(self.updateGroup)
        groupsToolbar.addWidget(self.updateGroupButton)
        
        self.disbandGroupButton = QtGui.QPushButton('Disband')
        self.disbandGroupButton.clicked.connect(self.disbandGroup)
        groupsToolbar.addWidget(self.disbandGroupButton)

        self.tradeFromWorldName = QtGui.QLineEdit()
        self.tradeFromWorldName.setMaximumWidth(100)
        self.tradeFromWorldName.setReadOnly(True)
        
        self.tradeToWorldName = QtGui.QLineEdit()
        self.tradeToWorldName.setMaximumWidth(100)
        self.tradeToWorldName.setReadOnly(True)
        
        #self.generateCargoButton = QtGui.QPushButton('Generate Cargo')
        self.tradeButton = QtGui.QPushButton('Trade')

        tradeToolbar = self.addToolBar("Trade Toolbar")
        tradeToolbar.addWidget(QtGui.QLabel('Trade From:'))
        tradeToolbar.addWidget(self.tradeFromWorldName)
        tradeToolbar.addWidget(QtGui.QLabel('To:'))
        tradeToolbar.addWidget(self.tradeToWorldName)
        #tradeToolbar.addWidget(self.generateCargoButton)
        tradeToolbar.addWidget(self.tradeButton)

        self.tradeToolbar = tradeToolbar


    def createBackgroundCellWidget(self, text, image):
        button = QtGui.QToolButton()
        button.setText(text)
        button.setIcon(QtGui.QIcon(image))
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.backgroundButtonGroup.addButton(button)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createCellWidget(self, text, diagramType):
        item = StarMap.MapItem(diagramType, self.dataMenu)
        icon = QtGui.QIcon(item.image())

        button = QtGui.QToolButton()
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.buttonGroup.addButton(button, diagramType)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createColorMenu(self, slot, defaultColor):
        colors = [QtCore.Qt.black, QtCore.Qt.white, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

        colorMenu = QtGui.QMenu(self)
        for color, name in zip(colors, names):
            action = QtGui.QAction(name, self)
            #need to specifically create a QColor from "color", since the "color" is a GlobalColor
            # and not a QColor object
            action.setData(QtGui.QColor(color))
            #action.setData(QtCore.QVariant(QtGui.QColor(color)))
            action.setIcon(self.createColorIcon(color))
            self.connect(action, QtCore.SIGNAL("triggered()"), slot)
            colorMenu.addAction(action)
            if color == defaultColor:
                colorMenu.setDefaultAction(action)
        return colorMenu

    def createColorToolButtonIcon(self, imageFile, color):
        pixmap = QtGui.QPixmap(50, 80)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        image = QtGui.QPixmap(imageFile)
        target = QtCore.QRect(0, 0, 50, 60)
        source = QtCore.QRect(0, 0, 42, 42)
        painter.fillRect(QtCore.QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()
        return QtGui.QIcon(pixmap)

    def setScrollHandDragAction(self):
        self.view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def setRubberBandDragAction(self):
        self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def createColorIcon(self, color):
        pixmap = QtGui.QPixmap(20, 20)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.NoPen)
        painter.fillRect(QtCore.QRect(0, 0, 20, 20), color)
        painter.end()
        return QtGui.QIcon(pixmap)

    def openAllegianceEditor(self):
        self.allegianceEditor = AllegianceEditor.AllegianceEditor(
            self.model, self.scene, self)
        self.allegianceEditor.show()
        self.allegianceEditor.activateWindow()
        #app.processEvents()
        

    def openWorldBrowser(self):
        self.worldBrowser = WorldBrowser.WorldBrowser(self.model, self)
        #worldBrowser.exec_()
        self.worldBrowser.show()
        #worldBrowser.raise()
        self.worldBrowser.activateWindow()
        
        app.processEvents()
    
    def openSectorBrowser(self):
        sectorBrowser = SectorBrowser.SectorBrowser(sector_model)
        sectorBrowser.exec_()
        app.processEvents()
    
    def openSubsectorBrowser(self):
        subsectorBrowser = SubsectorBrowser.SubsectorBrowser(subsector_model)
        subsectorBrowser.exec_()
        app.processEvents()

    def exitApp(self):
        saveDialog = QtGui.QMessageBox()
        saveDialog.setText('Do you want to save any changes before exiting?')
        saveDialog.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        saveDialog.setDefaultButton(QtGui.QMessageBox.Save)
        ret = saveDialog.exec_()
        if ret == QtGui.QMessageBox.Save:
            self.save()
            self.close()
        elif ret == QtGui.QMessageBox.Discard:
            self.close()
        elif ret == QtGui.QMessageBox.Cancel:
            app.processEvents()
            
            
        


if __name__ == "__main__":

    log.info_log("=== Application Started ===")
    app = QtGui.QApplication(sys.argv)

    #worlds_model = Models.WorldModel()
    #subsector_model = Models.SubsectorModel()
    #sector_model = Models.SectorModel()
    #worlds_model = Models.WorldModel()

    #for world in Models.generateTestWorlds():
    #    worlds_model.worlds.append(world)
        # set convenience lists in model here: states, regions, etc
    #worlds_model.reset()
    #worlds_model.dirty = False

    #worlds_model.removeRows(2)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 900, 600)
    mainWindow.show()

    sys.exit(app.exec_())

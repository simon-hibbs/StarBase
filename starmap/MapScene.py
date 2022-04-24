#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

import sys
import os
import math
from PySide import QtCore, QtGui
from log import *
from model import Models
from starmap import MapGlyphs
from starmap import MapGrid
from forms import WorldDialogs
from reports import PreviewMap
from reports import WorldReport
from reports import SubsectorReport
from reports import StatisticsDialog

WORLDS = 0
CELLS = 1
SUBSECTORS = 2
SECTORS = 3

class MapScene(QtGui.QGraphicsScene):
    # TODO: INSERT_TEXT_MODE and MOVE_ITEM_MODE not yet implemented
    SELECT_MODE, RUBBER_BAND_MODE, HAND_DRAG_MODE, INSERT_TEXT_MODE, MOVE_ITEM_MODE  = list(range(5))

    changeCellsSelectable = QtCore.Signal(bool)
    setFromTradeWorld = QtCore.Signal()
    setToTradeWorld = QtCore.Signal()

    def __init__(self, model, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

        self.model = model
        self.myMode = self.SELECT_MODE
        self.selectionType = 'Worlds'

        self.dialogs = {}
        self.lastScale = 0.12

        self.grid = MapGrid.Grid(self.model.secsWide, self.model.secsHigh)
        self.addItem(self.grid)
        self.grid.config()

        for subsector in self.model.getSubsectorList():
            self.setSubsectorData(subsector.name,
                                  subsector.subsectorCol,
                                  subsector.subsectorRow)

        for sector in self.model.getSectorList():
            self.setSectorData(sector.name,
                                  sector.sectorCol,
                                  sector.sectorRow)


    def setSubsectorData(self, name, subsectorCol, subsectorRow):
        self.grid.setSubsectorData(name, subsectorCol, subsectorRow)

    def setSectorData(self, name, sectorCol, sectorRow):
        self.grid.setSectorData(name, sectorCol, sectorRow)

    def worldChanged(self, row):
        self.grid.worldChanged(row)

    def insertWorld(self, pmi):
        # Used for all addition and updating of world data.
        if self.selectionType == 'Worlds':
            selectable = True
        else:
            selectable = False
        self.grid.insertWorld(pmi, selectable)

    def removeWorld(self, row):
        self.grid.removeWorld(row)

    def clearWorlds(self):
        self.grid.clearWorlds()

    def setCellsSelectable(self, flag):
        self.changeCellsSelectable.emit(flag)

    def selectGroup(self, index):
        if index <= (len(self.model.groupNames) - 1):
            self.setCellsSelectable(False)
            self.setCellsSelectable(True)
            self.grid.selectCells(self.model.groupCells[index])
        else:
            debug_log('Group index ' + str(index) + ' not valid.')
            debug_log('model.groupNames: ' + str(self.model.groupNames))

##    def focusOutEvent(self, event):
##        self.clearSelection()
##        QGraphicsScene.focusOutEvent(event)

    def toggleAllegianceDisplay(self, checked):
        self.grid.toggleAllegianceDisplay(checked)

    def setAllegiance(self, code):
        cell_list = []
        
        if self.selectionType == 'Hexes':
            for cell in self.selectedItems():
                cell_list.append(cell)

        elif self.selectionType == 'Sectors':
            for sector in self.selectedItems():
                cell_list = cell_list + sector.cells

        elif self.selectionType == 'Subsectors':
            for subsector in self.selectedItems():
                cell_list = cell_list + subsector.cells

        for cell in cell_list:
            pmi = self.grid.worldPmiAt(cell.col, cell.row)
            if pmi is not None:
                self.model.setAllegianceCode(pmi, code)


    def viewMoveDetected(self, value):
        pass
        #print 'View Moved!', value

    def setMode(self, mode):
        self.myMode = mode

    def setScale(self, scale):
        if scale > 0.12:
            self.grid.setHexGridVisible(True)
        else:
            self.grid.setHexGridVisible(False)

        if scale >= 0.80:
            self.grid.setCoordsVisible(True)
        else:
            self.grid.setCoordsVisible(False)

        if scale > 0.18:
            self.grid.showWorldDetails(True)
        else:
            self.grid.showWorldDetails(False)
        
        if 0.18 <= scale <= 0.37:
            self.grid.showSubsectorNames(True)
        else:
            self.grid.showSubsectorNames(False)

        if scale < 0.18:
            self.grid.showSectorNames(True)
        else:
            self.grid.showSectorNames(False)

        self.lastScale = scale

    def setSelectionType(self, selectionType):
        self.selectionType = selectionType
        for item in list(self.items()):
            item.setSelected(False)
            item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

            try:
                if selectionType == 'Hexes' \
                   and item.itemType == MapGlyphs.GRID_CELL_TYPE:
                    item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
                elif selectionType == 'Subsectors' \
                   and item.itemType == MapGlyphs.SUBSECTOR_GLYPH_TYPE:
                    item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
                elif selectionType == 'Sectors' \
                   and item.itemType == MapGlyphs.SECTOR_GLYPH_TYPE:
                    item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
            except:
                pass

##    def addCellsToGroup(self, cell_list):
##        coord_list = []
##        for cell in cell_list:
##            coord_list.append((cell.col, cell.row))
##        self.model.addCellsToSelectedGroup(coord_list)

    def addCellsToGroup(self, index):
        if self.selectionType == 'Hexes':
            cell_list = []
            for cell in self.selectedItems():
                cell_list.append(cell)

        coord_list = []
        for cell in cell_list:
            coord_list.append((cell.col, cell.row))
        self.model.addCellsToGroup(index, coord_list)

    def populateCells(self, cell_list, random_occurrence=True):
        progress = QtGui.QProgressDialog('Populating selected region',
                                                     'Abort',
                                                     0,
                                                     len(cell_list))
        progress.setWindowTitle('World Generation')
        count = 0
        for cell in cell_list:
            pmi = self.grid.worldPmiAt(cell.col, cell.row)
            if pmi != None:
                self.model.removeRow(pmi.row())
            
            if self.model.rollToPopulate() or not random_occurrence:
                last_row = self.model.rowCount()
                self.model.currentCell =(cell.col, cell.row)
                self.model.insertRandomWorld(last_row)

            count = count + 1
            progress.setValue(count)
        

    def contextMenuEvent(self, event):

        if len(self.selectedItems()) == 0:
            return

        if self.selectionType == 'Hexes':
            
            cell_list = []
            for cell in self.selectedItems():
                cell_list.append(cell)

            # Single cell selected
            if len(cell_list) == 1:
                
                x = cell_list[0].col
                y = cell_list[0].row
                pmi = self.grid.worldPmiAt(x, y)

                menu = QtGui.QMenu()
                addWorld = False
                editWorld = False
                worldReport = False
                tradeFrom = False
                tradeTo = False
                removeWorld = False

                if pmi is not None:
                    editWorld = menu.addAction('Edit World')
                    worldReport = menu.addAction('View Report')
                    tradeFrom = menu.addAction('Trade From Here')
                    tradeTo = menu.addAction('Trade To Here')
                    separator = menu.addSeparator()
                    removeWorld = menu.addAction('Remove World')
                else:
                    addWorld = menu.addAction('Add World')

                selectedAction = menu.exec_(event.screenPos())
        
                if selectedAction == editWorld:
                    myView = self.views()[0]
                    self.dialog = WorldDialogs.EditWorldDialog(
                                                pmi,
                                                parent=myView)
                    self.dialog.show()
                    self.dialog.raise_()
                    self.dialog.activateWindow()

##                    # Clean up dead edit dialogs, needs to be automatic
##                    for key, value in self.dialogs.items():
##                        try:
##                            hidden = value.isHidden()
##                        except:
##                            del self.dialogs[key]

                elif selectedAction == worldReport:
                    myView = self.views()[0]
                    self.dialog = WorldReport.WorldReportDialog(pmi,
                                                                      parent=myView)
                    self.dialog.show()
                    self.dialog.raise_()
                    self.dialog.activateWindow()

                elif selectedAction == tradeFrom:
                    self.model.fromTradeWorldPmi = pmi
                    self.setFromTradeWorld.emit()

                elif selectedAction == tradeTo:
                    self.model.toTradeWorldPmi = pmi
                    self.setToTradeWorld.emit()

                elif selectedAction == addWorld:
                    self.populateCells(cell_list, False)
##                    self.dialogs[(x,y)] = \
##                            WorldDialogs.AddWorldDialog(self.model, x, y)
##                    self.dialogs[(x,y)].show()

                elif selectedAction == removeWorld:
                    self.model.removeRow(pmi.row())

            # Multiple cells selected
            elif len(cell_list) > 1:
                
                pmi_list = []
                for cell in cell_list:
                    pmi = self.grid.worldPmiAt(cell.col, cell.row)
                    if pmi is not None:
                        pmi_list.append(pmi)

                menu = QtGui.QMenu()

                removeLink = False
                addLink = False
                generateRegion = False
                deleteWorlds = False
                reGenerateWorlds = False
                reGenerateRegion = False
                statistics = False

                if len(pmi_list) == 2 and len(cell_list) == 2:
                    row1 = pmi_list[0].row()
                    row2 = pmi_list[1].row()
##                    if self.model.linkExists(row1, row2):
##                        removeLink = menu.addAction('Remove Link')
##                    else:
##                        addLink = menu.addAction('Create Link')

                if len(pmi_list) == 0:
                    generateRegion = menu.addAction('Generate Region')
                    populateAll = menu.addAction('Populate All Hexes')
                else:
                    deleteWorlds = menu.addAction('Delete Selected Worlds')
                    populateAll = menu.addAction('Populate All Hexes')
                    reGenerateWorlds = menu.addAction('Re-Generate Selected Worlds')
                    reGenerateRegion = menu.addAction('Re-Generate Region')
                    statistics = menu.addAction('Statistics')

                selectedAction = menu.exec_(event.screenPos())

##                if selectedAction == removeLink:
##                    self.model.removeLink(row1, row2)
##                    # Also need to remove from map
##                
##                elif selectedAction == addLink:
##                    self.model.addLink(row1, row2)
##                    # Also need to add to map

                if selectedAction == populateAll:
                    self.populateCells(cell_list, random_occurrence=False)

                if selectedAction == generateRegion \
                        or selectedAction == reGenerateRegion:
                    self.populateCells(cell_list, random_occurrence=True)

                elif selectedAction == deleteWorlds:
                    for pmi in pmi_list:
                        self.model.removeRow(pmi.row())

                elif selectedAction == reGenerateWorlds:
                    for pmi in pmi_list:
                        pmi.model().regenerateWorld(pmi.row())

                elif selectedAction == statistics:
                    myView = self.views()[0]
                    self.dialog = StatisticsDialog.StatisticsDialog(
                                             pmi_list,
                                             len(cell_list),
                                             '',
                                             parent=myView)
                    self.dialog.show()
                    self.dialog.raise_()
                    self.dialog.activateWindow()

##                    # Clean up dead edit dialogs, needs to be automatic
##                    for key, value in self.dialogs.items():
##                        try:
##                            hidden = value.isHidden()
##                        except:
##                            del self.dialogs[key]


        elif self.selectionType == 'Sectors':
            sector_list = []
            for sector in self.selectedItems():
                sector_list.append(sector)

            menu = QtGui.QMenu()
            renameSector = False
            previewMap = False
            populateSector = False
            deleteWorlds = False
            statistics = False
            importSec = False
            
            if len(sector_list) == 1:
                renameSector = menu.addAction('Rename Sector')
                previewMap = menu.addAction('Preview Map')
                populateSector = menu.addAction('Generate Sector')
                deleteWorlds = menu.addAction('Delete Worlds')
                statistics = menu.addAction('Show Statistics')
                importSEC = menu.addAction('Import SEC file')

            elif len(sector_list) > 1:
                populateSector = menu.addAction('Generate Sectors')
                deleteWorlds = menu.addAction('Delete Worlds')
                statistics = menu.addAction('Show Statistics')
                
            selectedAction = menu.exec_(event.screenPos())

            if selectedAction == renameSector:
                sector = sector_list[0]
                col = sector.sectorCol
                row = sector.sectorRow
                myView = self.views()[0]
                new_name, ok = QtGui.QInputDialog.getText(myView,
                                                    'New Sector Name',
                                                    'Sector Name:',
                                                    QtGui.QLineEdit.Normal,
                                                    sector.name)
                self.model.renameSector(col, row, new_name)
                self.setSectorData(new_name, col, row)
                
            elif selectedAction == previewMap:
                col = sector_list[0].sectorCol
                row = sector_list[0].sectorRow
                myView = self.views()[0]
                self.dialog = PreviewMap.PreviewDialog(
                                         old_glyph=sector_list[0],
                                         region_type=PreviewMap.SECTOR, 
                                         model=self.model,
                                         parent=myView)
                self.dialog.show()
                self.dialog.raise_()
                self.dialog.activateWindow()

##                # Clean up dead edit dialogs, needs to be automatic
##                for key, value in self.dialogs.items():
##                    try:
##                        hidden = value.isHidden()
##                    except:
##                        del self.dialogs[key]

            if selectedAction == populateSector:
                cell_list = []
                for sector in sector_list:
                    cell_list = cell_list + sector.cells
                self.populateCells(cell_list, random_occurrence=True)

            elif selectedAction == deleteWorlds:
                cell_list = []
                for sector in sector_list:
                    for cell in sector.cells:
                        x = cell.col
                        y = cell.row
                        pmi = self.grid.worldPmiAt(x, y)
                        if pmi != None:
                            self.model.removeRow(pmi.row())

            elif selectedAction == statistics:
                cell_list = []
                for sector in sector_list:
                    cell_list = cell_list + sector.cells
                pmi_list = []
                for cell in cell_list:
                    pmi = self.model.getPmiAt(cell.col, cell.row)
                    if pmi != None:
                        pmi_list.append(pmi)
                if len(pmi_list) > 0:
                    myView = self.views()[0]
                    self.dialog = StatisticsDialog.StatisticsDialog(
                                             pmi_list,
                                             len(cell_list),
                                             '',
                                             parent=myView)
                    self.dialog.show()
                    self.dialog.raise_()
                    self.dialog.activateWindow()

##                # Clean up dead edit dialogs, needs to be automatic
##                for key, value in self.dialogs.items():
##                    try:
##                        hidden = value.isHidden()
##                    except:
##                        del self.dialogs[key]

            elif selectedAction == importSEC:
                sector = sector_list[0]
                myView = self.views()[0]
                default_path = self.model.project_path
                filename = QtGui.QFileDialog.getOpenFileName(myView,
                                                'Open .SEC file',
                                                default_path,
                                                'SEC Files (*.SEC)')
                self.model.importSEC(filename,
                                     sector.sectorCol,
                                     sector.sectorRow)
                debug_log('SEC import complete')


        elif self.selectionType == 'Subsectors':
            subsector_list = []
            for subsector in self.selectedItems():
                subsector_list.append(subsector)

            menu = QtGui.QMenu()
            renameSubsector = False
            previewMap = False
            subsectorReport = False
            populateSubsector = False
            deleteWorlds = False
            statistics = False

            if len(subsector_list) == 1:
                renameSubsector = menu.addAction('Rename Subsector')
                previewMap = menu.addAction('Preview Map')
                subsectorReport = menu.addAction('Subsector Report')
                populateSubsector = menu.addAction('Generate Subsector')
                deleteWorlds = menu.addAction('Delete Worlds')
                statistics = menu.addAction('Show Statistics')

            elif len(subsector_list) > 1:
                populateSubsector = menu.addAction('Generate Subsector')
                deleteWorlds = menu.addAction('Delete Worlds')
                statistics = menu.addAction('Show Statistics')
                
            selectedAction = menu.exec_(event.screenPos())

            if selectedAction == renameSubsector:
                subsector = subsector_list[0]
                col = subsector.subsectorCol
                row = subsector.subsectorRow
                myView = self.views()[0]
                new_name, ok = QtGui.QInputDialog.getText(myView,
                                                    'New Subsector Name',
                                                    'Subsector Name:',
                                                    QtGui.QLineEdit.Normal,
                                                    subsector.name)
                self.model.renameSubsector(col, row, new_name)
                self.setSubsectorData(new_name, col, row)

            elif selectedAction == previewMap:
                col = subsector_list[0].subsectorCol
                row = subsector_list[0].subsectorRow
                myView = self.views()[0]
                self.dialog = PreviewMap.PreviewDialog(
                                         old_glyph=subsector_list[0],
                                         region_type=PreviewMap.SUBSECTOR, 
                                         model=self.model,
                                         parent=myView)
                self.dialog.show()
                self.dialog.raise_()
                self.dialog.activateWindow()

##                # Clean up dead edit dialogs, needs to be automatic
##                for key, value in self.dialogs.items():
##                    try:
##                        hidden = value.isHidden()
##                    except:
##                        del self.dialogs[key]

            elif selectedAction == subsectorReport:
                pmi_list = []
                for subsector in subsector_list:
                     for cell in subsector.cells:
                        x = cell.col
                        y = cell.row
                        pmi = self.grid.worldPmiAt(x, y)
                        if pmi != None:
                            pmi_list.append(pmi)
                myView = self.views()[0]
                col = subsector_list[0].subsectorCol
                row = subsector_list[0].subsectorRow
                self.dialog = SubsectorReport.SubsectorReportDialog(
                                    subsector_glyph=subsector_list[0],
                                    pmi_list=pmi_list,
                                    model=self.model,
                                    parent=myView)
                self.dialog.show()
                self.dialog.raise_()
                self.dialog.activateWindow()

##                # Clean up dead edit dialogs, needs to be automatic
##                for key, value in self.dialogs.items():
##                    try:
##                        hidden = value.isHidden()
##                    except:
##                        del self.dialogs[key]
            
            elif selectedAction == populateSubsector:
                cell_list = []
                for subsector in subsector_list:
                    cell_list = cell_list + subsector.cells
                self.populateCells(cell_list, random_occurrence=True)

            elif selectedAction == deleteWorlds:
                cell_list = []
                for subsector in subsector_list:
                    for cell in subsector.cells:
                        x = cell.col
                        y = cell.row
                        pmi = self.grid.worldPmiAt(x, y)
                        if pmi != None:
                            self.model.removeRow(pmi.row())

            elif selectedAction == statistics:
                cell_list = []
                for subsector in subsector_list:
                    cell_list = cell_list + subsector.cells
                pmi_list = []
                for cell in cell_list:
                    pmi = self.model.getPmiAt(cell.col, cell.row)
                    if pmi != None:
                        pmi_list.append(pmi)
                myView = self.views()[0]
                self.dialog = StatisticsDialog.StatisticsDialog(
                                         pmi_list,
                                         len(cell_list),
                                         '',
                                         parent=myView)
                self.dialog.show()
                self.dialog.raise_()
                self.dialog.activateWindow()

##                # Clean up dead edit dialogs, needs to be automatic
##                for key, value in self.dialogs.items():
##                    try:
##                        hidden = value.isHidden()
##                    except:
##                        del self.dialogs[key]


    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            return

        if self.myMode == self.SELECT_MODE:
            QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)

        elif self.myMode == self.RUBBER_BAND_MODE:
            pass    # Don't propagate mouse events to the default handler
            #QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)
        elif self.myMode == self.HAND_DRAG_MODE:
            pass    # Don't propagate mouse events to the default handler
##        elif self.myMode == self.INSERT_TEXT_MODE:
##            textItem = MapTextItem()
##            textItem.setFont(self.myFont)
##            textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
##            textItem.setZValue(1000.0)
##            self.connect(textItem, QtCore.SIGNAL("lostFocus"),
##                    self.editorLostFocus)
##            self.connect(textItem, QtCore.SIGNAL("selectedChange"),
##                    self, QtCore.SIGNAL("itemSelected(QGraphicsItem *)"))
##            
##            self.addItem(textItem)
##            textItem.setDefaultTextColor(self.myTextColor)
##            textItem.setPos(mouseEvent.scenePos())
##            self.emit(QtCore.SIGNAL("textInserted"), textItem)
##            QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)
        else:
            QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False


class WorldItemView(QtGui.QAbstractItemView):
    """ Hidden view which interfaces between the model and the scene.
    """
    def __init__(self, model, parent=None):
        QtGui.QAbstractItemView.__init__(self, parent)
        self.hide()
        self.setModel(model)
        self.my_model = model
        self.scene = MapScene(self.my_model)
        self.resetWorlds()

    def dataChanged(self, topLeft, bottomRight):
        top_row = topLeft.row()
        bottom_row = bottomRight.row()
        #debug_log("Top row " + str(top_row) + " Bottom row " + str(bottom_row))
        for row in range(top_row, (bottom_row + 1)):
            self.scene.worldChanged(row)

    def rowsInserted(self, parent, start, end):
        for row in range(start, (end + 1) ):
            pmi = self.my_model.getPMI(row)
            self.scene.insertWorld(pmi)

    def rowsAboutToBeRemoved(self, parent, start, end):
        for row in range(start, (end + 1)):
            self.scene.removeWorld(row)

    def resetWorlds(self):
        self.scene.clearWorlds()
        # Add worlds to scene
        last_row = self.my_model.rowCount() - 1
        self.rowsInserted(None, 0, last_row)

from PySide.QtCore import *
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide.QtGui import *
import os
from model import Models
from model import Traveller
from starmap import MapGlyphs
from starmap import MapGrid
from log import *


TITLE_FONT = 16
UPP_FONT = 10
HEADING_FONT = 11
BODY_FONT = 9


class WorldReportDialog(QDialog):
    def __init__(self, pmi, parent=None):
        super(WorldReportDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('World Report')

        self.worldReport = WorldReport(pmi)
        
        editor = QTextEdit()
        editor.setDocument(self.worldReport.document)

        #saveButton = QPushButton('Save')
        self.pdfButton = QPushButton('Save As PDF')
        self.closeButton = QPushButton('Close')

        buttonLayout = QVBoxLayout()
        #buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(self.pdfButton)
        buttonLayout.addWidget(self.closeButton)
##        buttonLayout.addWidget(self.view)
        buttonLayout.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(editor)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #self.connect(pdfButton, SIGNAL("clicked()"),
        #             self.exportToPdf)
        self.pdfButton.clicked.connect(self.exportToPdf)
        #self.connect(closeButton, SIGNAL("clicked()"),
        #             self.closeButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        


    def exportToPdf(self):
        #filename = 'World report.pdf'
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        default_path = os.path.join(self.worldReport.model.project_path,
                                    self.worldReport.model.slugify(self.worldReport.world.name))
        filename = QFileDialog.getSaveFileName(self, 'Save as PDF',
                                               default_path,
                                               'PDF Files (*.pdf)')
        printer.setOutputFileName(filename)
        
        self.worldReport.document.print_(printer)


    def closeButtonClicked(self):
        self.close()



class BoundaryRectangle(QGraphicsPolygonItem):
    def __init__(self, rectF=QRectF(), parent=None):
        QGraphicsPolygonItem.__init__(self, parent)
        self.rectF = rectF
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.transparent)
        self.setPen(pen)
        self.setBrush(Qt.transparent)
        myPolygon = QPolygonF(rectF)
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)

    def boundingRect(self):
        return self.rectF

                  
class MicroGridRoot(QGraphicsItem):
    def __init__(self, pmi, parent=None):
        QGraphicsItem.__init__(self, parent)

        self.hex_root = MapGrid.HexRoot(self,
                                        hexes_wide=1,
                                        hexes_high=1,
                                        hex_color=Qt.black)
        self.hex_root.setCellsSelectable(False)
        self.hex_root.setParentItem(self)
        self.model = pmi.model()

        model_row = pmi.row()
        world = pmi.model().getWorld(pmi)
        glyph = MapGlyphs.PlanetGlyph(pmi)
        glyph.configurePlanetGlyph(True)
        glyph.setParentItem(self)
        px, py = 0, 0
        MapGrid.gridToPix((world.col), (world.row))
        glyph.setPos(px, py)
        glyph.setFlag(QGraphicsItem.ItemIsSelectable, False)

        self.world_glyph = glyph


    def addBorder(self, rectF):
        self.boundary = BoundaryRectangle(rectF, self)

    def setCoordsVisible(self, flag):
        self.hex_root.setCoordsVisible(flag)

    def paint(self, painter=None, option=None, widget=None):
        pass

    def boundingRect(self):
        return QRectF()




class WorldReport(object):
    def __init__(self, pmi):

        self.pmi = pmi
        self.model = pmi.model()
        self.world = self.model.getWorld(pmi)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.scene.model = self.model

        self.grid = MicroGridRoot(pmi)
        self.scene.addItem(self.grid)
        self.grid.setCoordsVisible(True)

        self.mapRect = self.scene.sceneRect()
        self.mapRect.adjust(-30, -0, -13, 0)
        #rect = self.mapRect.toRect()
        self.grid.addBorder(self.mapRect)

        image = QImage(262, 200, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene.render(painter)
        painter.end()
        self.image_file = self.model.storeWorldImage(self.world.name, image)

##        self.view = QGraphicsView(self.scene)
##        self.view.setRenderHints(QPainter.Antialiasing)
##        self.view.setViewportUpdateMode(self.view.FullViewportUpdate)

        self.document = self.createDocument()



    def createDocument(self):
        
        worldReport = QTextDocument()
        cursor = QTextCursor(worldReport)

        title_text_format = QTextCharFormat()
        title_text_format.setFont(QFont('Helvetica',
                                        TITLE_FONT,
                                        QFont.Bold))
        title_block_format = QTextBlockFormat()
        title_block_format.setTopMargin(TITLE_FONT)

        region_text_format = QTextCharFormat()
        region_text_format.setFont(QFont('Helvetica',
                                          HEADING_FONT,
                                          QFont.Bold))

        upp_text_format = QTextCharFormat()
        font = QFont('Courier New', UPP_FONT, QFont.Bold)
        upp_text_format.setFont(font)
        upp_block_format = QTextBlockFormat()
        upp_block_format.setTopMargin(0)
        upp_block_format.setBottomMargin(0)

        heading_text_format = QTextCharFormat()
        heading_text_format.setFont(QFont('Helvetica',
                                          HEADING_FONT,
                                          QFont.Bold))
        heading_block_format = QTextBlockFormat()
        heading_block_format.setTopMargin(HEADING_FONT)
        heading_block_format.setBottomMargin(HEADING_FONT)
        heading_block_format.setIndent(0)

        body_text_format = QTextCharFormat()
        body_text_format.setFont(QFont('Helvetica',
                                      BODY_FONT,
                                      QFont.Normal))
        body_block_format = QTextBlockFormat()
        body_block_format.setAlignment(Qt.AlignTop)
        body_block_format.setBottomMargin(0)
        body_block_format.setIndent(1)

        table_constraints = [QTextLength(QTextLength.PercentageLength, 50),
                             QTextLength(QTextLength.PercentageLength, 50)]
        title_table_format = QTextTableFormat()
        title_table_format.setCellSpacing(0)
        title_table_format.setCellPadding(5)
        title_table_format.setBorderBrush(QBrush(Qt.transparent))
        title_table_format.setColumnWidthConstraints(table_constraints)

        table_constraints = [QTextLength(QTextLength.PercentageLength, 25),
                             QTextLength(QTextLength.PercentageLength, 30),
                             QTextLength(QTextLength.PercentageLength, 25),
                             QTextLength(QTextLength.PercentageLength, 20)]
        form_table_format = QTextTableFormat()
        form_table_format.setCellSpacing(0)
        form_table_format.setCellPadding(3)
        form_table_format.setBorderBrush(QBrush(Qt.transparent))
        form_table_format.setColumnWidthConstraints(table_constraints)

        details_table_format = QTextTableFormat()
        details_table_format.setCellSpacing(0)
        details_table_format.setCellPadding(7)
        details_table_format.setBorderBrush(QBrush(Qt.transparent))

        # World name title
        #cursor.setBlockFormat(title_block_format)
        #cursor.insertText(self.world.name, title_text_format)
        table = cursor.insertTable(1, 2, title_table_format)
        
        cell = table.cellAt(0, 0)
        cellCursor = cell.firstCursorPosition()
        cellCursor.insertText(self.world.name + '                   ',
                              title_text_format)

        image_format = QTextImageFormat()
        image_format.setHeight(100)
        image_format.setWidth(131)
        image_format.setName(self.image_file)
##        image_format.setWidth(200)
##        image_format.setHeight(200)
        
        cell = table.cellAt(0, 1)
        cellCursor = cell.firstCursorPosition()
        cellCursor.insertImage(image_format)

        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)

        # UPP
        cursor.insertBlock()
        cursor.setBlockFormat(upp_block_format)
        upp_header = self.model.getUWP(None)
        upp_text =  self.model.getUWP(self.pmi.row())
        cursor.insertText(upp_header, upp_text_format)
        cursor.insertBlock()
        cursor.setBlockFormat(upp_block_format)
        cursor.insertText(upp_text, upp_text_format)


        #Table of Details
        cursor.insertBlock()
        cursor.setBlockFormat(heading_block_format)
        cursor.insertText('System Information', heading_text_format)

        info = self.getSystemInfo()
        table = cursor.insertTable(len(info), 4, form_table_format)
        for row in info:
            cell = table.cellAt(info.index(row), 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[0], body_text_format)

            cell = table.cellAt(info.index(row), 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[1], body_text_format)

            cell = table.cellAt(info.index(row), 2)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[2], body_text_format)

            cell = table.cellAt(info.index(row), 3)
            cellCursor = cell.firstCursorPosition()
            if row[3] != '':
                cellCursor.insertText(row[3], body_text_format)
        table.mergeCells(1, 3, 2, 1)
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)


        cursor.insertBlock()
        cursor.setBlockFormat(heading_block_format)
        cursor.insertText('Starport Facilities', heading_text_format)

        info = self.getStarportInfo()
        table = cursor.insertTable(len(info), 4, form_table_format)
        for row in info:
            cell = table.cellAt(info.index(row), 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[0], body_text_format)

            cell = table.cellAt(info.index(row), 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[1], body_text_format)

            cell = table.cellAt(info.index(row), 2)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[2], body_text_format)

            cell = table.cellAt(info.index(row), 3)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[3], body_text_format)
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        debug_log('Finished starport info table')


        cursor.insertBlock()
        cursor.setBlockFormat(heading_block_format)
        cursor.insertText('Mainworld Attributes', heading_text_format)

        info = self.getMainworldInfo()
        table = cursor.insertTable(len(info), 4, form_table_format)
        for row in info:
            cell = table.cellAt(info.index(row), 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[0], body_text_format)

            cell = table.cellAt(info.index(row), 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[1], body_text_format)

            cell = table.cellAt(info.index(row), 2)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[2], body_text_format)

            cell = table.cellAt(info.index(row), 3)
            cellCursor = cell.firstCursorPosition()
            if row[3] != '':
                cellCursor.insertText(row[3], body_text_format)
        table.mergeCells(4, 3, 5, 1)
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)


        cursor.insertBlock()
        cursor.setBlockFormat(heading_block_format)
        cursor.insertText('Mainworld Description', heading_text_format)

        info = self.getMainworldDescription()
        table = cursor.insertTable(len(info), 2, details_table_format)
        for row in info:
            cell = table.cellAt(info.index(row), 0)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[0], body_text_format)

            cell = table.cellAt(info.index(row), 1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(row[1], body_text_format)
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)

        return worldReport


    def getSystemInfo(self):
        table_data = []

        sector = self.model.owningSector(self.world.col,
                                         self.world.row)
        table_data.append(['Sector:', sector, 'Travel Code:',
                           self.world.travelCode.code])
        
        subsector = self.model.owningSubsector(self.world.col,
                                               self.world.row)
        bases = []
        if self.world.starport.hasNavyBase:
            bases.append('Navy Base')
        if self.world.starport.hasScoutBase:
            bases.append('Scout base')
        if self.world.starport.hasResearchBase:
            bases.append('Research Facility')
        if self.world.starport.hasTas:
            bases.append('TAS Hostel')
        if self.world.starport.hasConsulate:
            bases.append('Imperial Consulate')
        if self.world.starport.hasPirateBase:
            bases.append('Pirate Base')
        
        if len(bases) == 0:
            bases = 'None'
        else:
            bases = '\n'.join(bases)
        table_data.append(['Subsector:', subsector, 'Bases:', bases])

        secX, secY = self.model.gridToSector(self.world.col,
                                                self.world.row)
        sector_coords = str(secX).zfill(2) + str(secY).zfill(2) 
        table_data.append(['Coordinates:', sector_coords, '', ''])

        return table_data


    def getStarportInfo(self):
        table_data = []

        if self.world.starport.hasFullRepair:
            repair = 'Full'
        elif self.world.starport.hasLimitedRepair:
            repair = 'Limited'
        else:
            repair = 'None'
        
        table_data.append(['Berthing cost (Cr):',
                           str(self.world.starport.berthingCost),
                           'Repair capability:',
                           repair])

        fuel = 'None'
        if self.world.starport.hasUnrefined :
            fuel = 'Unrefined'
        if self.world.starport.hasRefined :
            if fuel ==  'Unrefined':
                fuel = fuel + '\nRefined'
            else:
                fuel = 'Refined'
        if self.world.hasGasGiant:
            if fuel == 'None':
                fuel = 'Gas Giant refueling only'
            else:
                fuel = fuel + '\nGas giant refueling'

        yards = []
        if self.world.starport.hasStarshipYard:
            yards.append('Starships')
        if self.world.starport.hasSpacecraftYard:
                yards.append('Spacecraft')
        if self.world.starport.hasSmallCraftYard:
                yards.append('Small Craft')

        if len(yards) == 0:
            yards = 'None'
        else:
            yards = '\n'.join(yards)
        
        table_data.append(['Fuel availability:', fuel,
                           'Shipyards:', yards])

        return table_data


    def getMainworldInfo(self):
        debug_log('Called getMainworldInfo.')
        table_data = []

        port_label = Traveller.starport_labels[self.world.starport.index]
        table_data.append(['Starport Quality:',
                           port_label,
                           'Surface pressure:',
                           str(self.world.atmosphere.pressure) + ' atm'])

        
        size_label = Traveller.size_labels[self.world.size.index]
        table_data.append(['World Size:',
                           size_label,
                           'Average temperature:',
                           str(self.world.temperature.avg_temp) + ' C'])

        hydro_label = Traveller.hydrographics_labels[self.world.hydrographics.index]
        table_data.append(['Hydrographics:',
                           hydro_label,
                           'Water coverage:',
                           str(self.world.hydrographics.percentage)])

        
        atmo_label = Traveller.atmosphere_labels[self.world.atmosphere.index]
        def splitThousands(s, sep=','):
            if len(s) <= 3: return s
            return splitThousands(s[:-3], sep) + sep + s[-3:]
        table_data.append(['Atmosphere:',
                           atmo_label,
                           'Inhabitants:',
                           splitThousands(str(self.world.population.inhabitants))])

        equipment = []
        if self.world.atmosphere.requiresVacc:
            equipment.append('Vacc. Suit')
        if self.world.atmosphere.requiresRespirator:
            equipment.append('Respirator')
        if self.world.atmosphere.requiresFilter:
            equipment.append('Air filter')
        if self.world.atmosphere.requiresAir:
            equipment.append('Air supply')
        if self.world.atmosphere.requirementsVary:
            equipment = ['Non-standard requirements']
        equipment = '\n'.join(equipment)
        if len(equipment) == 0:
            equipment = 'None'
        pop_label = Traveller.population_labels[self.world.population.index]
        table_data.append(['Population:', pop_label,
                           'Required equipment:', equipment])

        gov_label = Traveller.government_labels[self.world.government.index]
        table_data.append(['Government:', gov_label, '', ''])
        law_label = Traveller.law_level_labels[self.world.lawLevel.index]
        table_data.append(['Law Level:', law_label, '', ''])
        tech_label = Traveller.tech_level_labels[self.world.techLevel.index]
        table_data.append(['Technology Level:', tech_label, '', ''])
        table_data.append(['Temperature:', self.world.temperature.code, '', ''])

        return table_data


    def getMainworldDescription(self):
        table_data = []

        if self.world.temperature.userText != '':
            table_data.append(['Climate:', self.world.temperature.userText])
        else:
            table_data.append(['Climate:', self.world.temperature.description])

        if self.world.hydrographics.userText != '':
            table_data.append(['Geography:', self.world.hydrographics.userText])
        else:
            table_data.append(['Geography:', self.world.hydrographics.description])

        if self.world.population.userText != '':
            table_data.append(['Settlement pattern:', self.world.population.userText])
        else:
            table_data.append(['Settlement pattern:', self.world.population.description])

        if self.world.government.userText != '':
            table_data.append(['Government System:', self.world.government.userText])
        else:
            table_data.append(['Government System:', self.world.government.description])

        # Law Level
        if self.world.lawLevel.userText != '':
            table_data.append(['Legal Restrictions:', self.world.lawLevel.userText])
        else:
            table_data.append(['Legal Restrictions:', self.world.lawLevel.description])

        #Tech Level
        if self.world.techLevel.userText != '':
            table_data.append(['Technology:', self.world.techLevel.userText])
        else:
            table_data.append(['Technology:', self.world.techLevel.description])

        return table_data





#Deprecated
    def getInfo(self):
        table_data = []


        # Regions
        sector = self.model.owningSector(self.world.col,
                                         self.world.row)
        subsector = self.model.owningSubsector(self.world.col,
                                               self.world.row)
        table_data.append(['Sector:', sector])
        table_data.append(['Subsector:', subsector])

        #Travel Code
        table_data.append(['Travel Code:', self.world.travelCode.code])

        # Mainworld Attributes
        port_label = Traveller.starport_labels[self.world.starport.index]
        table_data.append(['Starport Quality:', port_label])
        size_label = Traveller.size_labels[self.world.size.index]
        table_data.append(['World Size:', size_label])
        hydro_label = Traveller.hydrographics_labels[self.world.hydrographics.index]
        table_data.append(['Hydrographics:', hydro_label])
        atmo_label = Traveller.atmosphere_labels[self.world.atmosphere.index]
        table_data.append(['Atmosphere:', atmo_label])
        pop_label = Traveller.population_labels[self.world.population.index]
        table_data.append(['Population:', pop_label])
        gov_label = Traveller.government_labels[self.world.government.index]
        table_data.append(['Government:', gov_label])
        law_label = Traveller.law_level_labels[self.world.lawLevel.index]
        table_data.append(['Law Level:', law_label])
        tech_label = Traveller.tech_level_labels[self.world.techLevel.index]
        table_data.append(['Technology Level:', tech_label])
        table_data.append(['Temperature:', self.world.temperature.code])
        
        table_data.append(['Berthing cost (Cr):', self.world.starport.berthingCost])
        
        fuel = 'None'
        if self.world.starport.hasUnrefined :
            fuel = 'Unrefined'
        if self.world.starport.hasRefined :
            if fuel ==  'Unrefined':
                fuel = fuel + '\nRefined'
            else:
                fuel = 'Refined'
        if self.world.hasGasGiant:
            if fuel == 'None':
                fuel = 'Gas Giant refueling only'
            else:
                fuel = fuel + '\nGas giant refueling'
        table_data.append(['Fuel availability:', fuel])
        
        yards = []
        if self.world.starport.hasStarshipYard:
            yards.append('Starships')
        if self.world.starport.hasSpacecraftYard:
                yards.append('Spacecraft')
        if self.world.starport.hasSmallCraftYard:
                yards.append('Small Craft')

        if len(yards) == 0:
            yards = 'None'
        else:
            yards = '\n'.join(yards)
        table_data.append(['Shipyards:', yards])
        
        if self.world.starport.hasFullRepair:
            repair = 'Full'
        elif self.world.starport.hasLimitedRepair:
            repair = 'Limited'
        else:
            repair = 'None'
        table_data.append(['Repair capability:', repair])

        # Bases
        bases = []
        if self.world.starport.hasNavyBase:
            bases.append('Navy Base')
        if self.world.starport.hasScoutBase:
            bases.append('Scout base')
        if self.world.starport.hasResearchBase:
            bases.append('Research Facility')
        if self.world.starport.hasTas:
            bases.append('TAS Hostel')
        if self.world.starport.hasConsulate:
            bases.append('Imperial Consulate')
        if self.world.starport.hasPirateBase:
            bases.append('Pirate Base')
        
        if len(bases) == 0:
            bases = ['None']
        else:
            bases = '\n'.join(bases)
        table_data.append(['Bases:', bases])

        #Size
        table_data.append(['Diameter:', str(self.world.size.diameter) + ' km'])
        table_data.append(['Surface gravity:', str(self.world.size.gravity) + ' G'])
        if self.world.size.userText != '':
            table_data.append(['Description:', self.world.size.userText])
        else:
            table_data.append(['Description:', self.world.size.description])
            
        #Atmosphere
        table_data.append(['Surface pressure:',
                           str(self.world.atmosphere.pressure) + ' atm'])
        equipment = []
        if self.world.atmosphere.requiresVacc:
            equipment.append('Vacc. Suit')
        if self.world.atmosphere.requiresRespirator:
            equipment.append('Respirator')
        if self.world.atmosphere.requiresFilter:
            equipment.append('Air filter')
        if self.world.atmosphere.requiresAir:
            equipment.append('Air supply')
        if self.world.atmosphere.requirementsVary:
            equipment = ['Non-standard requirements']
        equipment = '\n'.join(equipment)
        if len(equipment) == 0:
            equipment = 'None'

        table_data.append(['Required equipment:', equipment])

        if self.world.atmosphere.userText != '':
            table_data.append(['Atmosphere type:', self.world.atmosphere.userText])
        else:
            table_data.append(['Atmosphere type:', self.world.atmosphere.description])


        # Temperature
        table_data.append(['Temperature category:', self.world.temperature.category])
        table_data.append(['Average temperature:',
                           str(self.world.temperature.avg_temp) + ' C'])
            
        if self.world.temperature.userText != '':
            table_data.append(['Temperature details:', self.world.temperature.userText])
        else:
            table_data.append(['Temperature details:', self.world.temperature.description])


        # Hydrographics
        table_data.append(['Water coverage:',
                           str(self.world.hydrographics.percentage)])

        if self.world.hydrographics.userText != '':
            table_data.append(['Hydrographic Summary:', self.world.hydrographics.userText])
        else:
            table_data.append(['Hydrographic Summary:', self.world.hydrographics.description])

        # Population
        def splitThousands(s, sep=','):
            if len(s) <= 3: return s
            return splitThousands(s[:-3], sep) + sep + s[-3:]

        table_data.append(['Inhabitants:',
                           splitThousands(str(self.world.population.inhabitants))])

        if self.world.population.userText != '':
            table_data.append(['Settlement pattern:', self.world.population.userText])
        else:
            table_data.append(['Settlement pattern:', self.world.population.description])

        # Government
        if self.world.government.userText != '':
            table_data.append(['Description:', self.world.government.userText])
        else:
            table_data.append(['Description:', self.world.government.description])

        # Law Level
        if self.world.lawLevel.userText != '':
            table_data.append(['Legal restrictions:', self.world.lawLevel.userText])
        else:
            table_data.append(['Legal restrictions:', self.world.lawLevel.description])

        #Tech Level
        if self.world.techLevel.userText != '':
            table_data.append(['Technical achievements:', self.world.techLevel.userText])
        else:
            table_data.append(['Technical achievements:', self.world.techLevel.description])


        return table_data

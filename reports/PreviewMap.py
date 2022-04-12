from PySide.QtCore import *
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide.QtGui import *
#from PyQt4.QtSvg import *
import os
from model import Models
from starmap import MapGlyphs
from starmap import MapGrid

SUBSECTOR = 1
SECTOR = 2

class BoundaryRectangle(QGraphicsPolygonItem):
    def __init__(self, rectF=QRectF(), parent=None):
        QGraphicsPolygonItem.__init__(self, parent)
        self.rectF = rectF
        pen = QPen()
        pen.setWidth(2)
        self.setPen(pen)
        self.setBrush(Qt.transparent)
        myPolygon = QPolygonF(rectF)
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)

    def boundingRect(self):
        return self.rectF


class PreviewGridRoot(QGraphicsItem):
    def __init__(self, old_glyph, region_type,  model, parent=None):
        QGraphicsItem.__init__(self, parent)
        
        if region_type == SUBSECTOR:
            width=8
            height=10
        elif region_type == SECTOR:
            width=32
            height=40

        self.hex_root = MapGrid.HexRoot(self,
                                        hexes_wide=width,
                                        hexes_high=height,
                                        hex_color=Qt.black)
        self.hex_root.setCellsSelectable(False)
        self.hex_root.setParentItem(self)

        self.worlds_glyphs = []

        self.model = model
        
        if region_type == SUBSECTOR:
            col_offset = old_glyph.subsectorCol * width
            row_offset = old_glyph.subsectorRow * height
        elif region_type == SECTOR:
            col_offset = old_glyph.sectorCol * width
            row_offset = old_glyph.sectorRow * height

        for cell in old_glyph.cells:
            pmi = self.model.getPmiAt(cell.col, cell.row)
            if pmi != None:
                model_row = pmi.row()
                world = pmi.model().getWorld(pmi)
                glyph = MapGlyphs.PlanetGlyph(pmi)
                glyph.configurePlanetGlyph(True)
                glyph.setParentItem(self)
                px, py = MapGrid.gridToPix((world.col - col_offset),
                                           (world.row - row_offset))
                glyph.setPos(px, py)
                glyph.setFlag(QGraphicsItem.ItemIsSelectable, False)
                self.worlds_glyphs.insert(model_row, glyph)


    def addBorder(self, rectF):
        self.boundary = BoundaryRectangle(rectF, self)

    def setCoordsVisible(self, flag):
        self.hex_root.setCoordsVisible(flag)

    def paint(self, painter=None, option=None, widget=None):
        pass

    def boundingRect(self):
        return QRectF()


class PreviewDialog(QDialog):
    def __init__(self, old_glyph,  region_type,  model, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Preview Map')
        
        self.region_type = region_type
        self.old_glyph = old_glyph

        self.model = model
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.scene.model = self.model

        self.grid = PreviewGridRoot(old_glyph, region_type,  model)
        self.scene.addItem(self.grid)
        self.grid.setCoordsVisible(True)
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(self.view.FullViewportUpdate)
        
        self.mapRect = self.scene.sceneRect()
        self.mapRect.adjust(-30, -0, -10, 0)
        #self.scene.setSceneRect(rectF)
        rect = self.mapRect.toRect()
        #self.view.setSceneRect(rectF)
        self.view.setGeometry(rect)
        self.grid.addBorder(self.mapRect)

        printButton = QPushButton('Print')
        pngButton = QPushButton('Save As PNG')
##        svgButton = QPushButton('Save As SVG')
        closeButton = QPushButton('Close')
        self.decorateCB = QCheckBox('Decorate')

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(printButton)
        buttonLayout.addWidget(pngButton)
##        buttonLayout.addWidget(svgButton)
        buttonLayout.addWidget(closeButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.decorateCB)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #self.connect(printButton, SIGNAL("clicked()"),
        #             self.printMap)
        printButton.clicked.connect(self.printMap)
        #self.connect(pngButton, SIGNAL("clicked()"),
        #             self.saveMapPNG)
        pngButton.clicked.connect(self.saveMapPNG)
##        self.connect(svgButton, SIGNAL("clicked()"),
##                     self.saveMapSvg)
        #self.connect(closeButton, SIGNAL("clicked()"),
        #             self.closeDialog)
        closeButton.clicked.connect(self.closeDialog)
        #self.connect(self.decorateCB, SIGNAL("stateChanged(int)"),
        #             self.redrawMap)
        self.decorateCB.stateChanged[int].connect(self.redrawMap)
        
        self.view.scale(0.6, 0.6)
        
        self.decorateCB.setChecked(True)


    def showName(self, flag):
        pass

    def redrawMap(self, flag):

        if flag == Qt.Checked:

            self.scene.clear()
            self.scene.setBackgroundBrush(Qt.white)
            self.scene.model = self.model
            self.grid = PreviewGridRoot(self.old_glyph,
                                        self.region_type,
                                        self.model)
            self.scene.addItem(self.grid)
            self.grid.setCoordsVisible(True)
            self.view.setScene(self.scene)

            #self.mapRect = self.scene.sceneRect()
            #self.mapRect.adjust(-30, -0, -10, 0)
            #rect = self.mapRect.toRect()
            #self.view.setGeometry(rect)
            self.grid.addBorder(self.mapRect)

            if self.region_type == SUBSECTOR:
                self.view.scale(0.6, 0.6)
                subX = self.old_glyph.subsectorCol
                subY = self.old_glyph.subsectorRow
                north = self.model.getSubsectorAt(subX, subY - 1)
                east = self.model.getSubsectorAt(subX + 1, subY)
                south = self.model.getSubsectorAt(subX, subY + 1)
                west = self.model.getSubsectorAt(subX - 1, subY)
                name = self.old_glyph.name
                fontsize = 12
            elif self.region_type == SECTOR:
                self.view.scale(0.5, 0.5)
                secX = self.old_glyph.sectorCol
                secY = self.old_glyph.sectorRow
                north = self.model.getSectorAt(secX, secY - 1)
                east = self.model.getSectorAt(secX + 1, secY)
                south = self.model.getSectorAt(secX, secY + 1)
                west = self.model.getSectorAt(secX - 1, secY)
                name = self.old_glyph.name
                fontsize = 50

            self.north_text = QGraphicsSimpleTextItem(north)
            self.scene.addItem(self.north_text)
            self.north_text.setFont(QFont('Helvetica', fontsize, QFont.Bold))
            woffset = self.north_text.boundingRect().width()/2
            hoffset = self.north_text.boundingRect().height()
            self.north_text.setBrush(Qt.black)
            self.north_text.setPos((self.mapRect.width() / 2) - woffset - 70,
                                   -55 - hoffset)

            self.east_text = QGraphicsSimpleTextItem(east)
            self.scene.addItem(self.east_text)
            self.east_text.setFont(QFont('Helvetica', fontsize, QFont.Bold))
            woffset = self.east_text.boundingRect().width()/2
            hoffset = self.east_text.boundingRect().height()
            self.east_text.setBrush(Qt.black)
            self.east_text.setRotation(+90)
            self.east_text.setPos(self.mapRect.width() - 55 + hoffset,
                                  (self.mapRect.height() / 2) - woffset - 45)

            self.south_text = QGraphicsSimpleTextItem(south)
            self.scene.addItem(self.south_text)
            self.south_text.setFont(QFont('Helvetica', fontsize, QFont.Bold))
            woffset = self.south_text.boundingRect().width()/2
            name_offset = self.south_text.boundingRect().height()
            self.south_text.setBrush(Qt.black)
            self.south_text.setPos((self.mapRect.width() / 2) - woffset - 70,
                                   self.mapRect.height() - 45 + 0)

            self.west_text = QGraphicsSimpleTextItem(west)
            self.scene.addItem(self.west_text)
            self.west_text.setFont(QFont('Helvetica', fontsize, QFont.Bold))
            woffset = self.west_text.boundingRect().width()/2
            hoffset = self.west_text.boundingRect().height()
            self.west_text.setBrush(Qt.black)
            self.west_text.setRotation(-90)
            self.west_text.setPos(-75 - hoffset,
                                  (self.mapRect.height() / 2) + woffset - 45)

            self.name_text = QGraphicsSimpleTextItem(name)
            self.scene.addItem(self.name_text)
            self.name_text.setFont(QFont('Helvetica', fontsize * 2, QFont.Bold))
            woffset = self.name_text.boundingRect().width()/2
            self.name_text.setBrush(Qt.black)
            self.name_text.setPos((self.mapRect.width() / 2) - woffset - 70,
                                   self.mapRect.height() - 35 + name_offset)

            self.update()

        else:
            self.scene.clear()
            self.scene.setBackgroundBrush(Qt.white)
            self.scene.model = self.model
            self.grid = PreviewGridRoot(self.old_glyph,
                                        self.region_type,
                                        self.model)
            self.scene.addItem(self.grid)
            self.grid.setCoordsVisible(True)
            #self.view.setScene(self.scene)

            #self.mapRect = self.scene.sceneRect()
            #self.mapRect.adjust(-30, -0, -10, 0)
            #rect = self.mapRect.toRect()
            #self.view.setGeometry(rect)
            self.grid.addBorder(self.mapRect)

            self.update()


# Doesn't work yet
    def printMap(self):
        if self.region_type == SUBSECTOR:
            filename = 'Subsector.pdf'
        elif self.region_type == SECTOR:
            filename = 'Sector.pdf'
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        
        painter = QPainter(printer)
        painter.setBackgroundMode(Qt.OpaqueMode)
        painter.setBrush(Qt.SolidPattern)
        self.scene.render(painter)
        painter.end()
        
##    def saveMapSvg(self):
##        if self.region_type == SUBSECTOR:
##            image_width = 1668
##            image_height = 2106
##        elif self.region_type == SECTOR:
##            image_width = 3336
##            image_height = 4212
##        generator = QSvgGenerator()
##        name = self.old_glyph.name
##        default_path = os.path.join(self.model.project_path,
##                                    self.model.slugify(name)) + \
##                                    '.svg'
##        filename = QFileDialog.getSaveFileName(self, 'Save As SVG',
##                                               default_path,
##                                               'SVG Files (*.svg)')
##        generator.setFileName(filename)
##        generator.setSize(QSize(image_width, image_height))
##        generator.setTitle(name)
##        generator.setDescription('StarBase generated region map')
##        painter = QPainter(generator)
##        painter.setBackgroundMode(Qt.OpaqueMode)
##        painter.setBrush(Qt.SolidPattern)
##        self.scene.render(painter)
##        painter.end()
        

        
##        printDialog = QPrintDialog(printer, self)
##        printDialog.setWindowTitle('Print Subsector Map')
##        if printDialog.exec_() == QDialog.Accepted:
##            painter.begin(printer)
##            painter.save()
##            painter.restore()
##            painter.end()

    def saveMapPNG(self):
        if self.region_type == SUBSECTOR:
            image_width = 1668
            image_height = 2106
            filename = 'Subsector.png'
        elif self.region_type == SECTOR:
            #image_width = 3336
            #image_height = 4212
            image_width = 4448
            image_height = 5616
            filename = 'Sector.png'

        name = self.old_glyph.name
        default_path = os.path.join(self.model.project_path,
                                    self.model.slugify(name)) + \
                                    '.png'
        filename = QFileDialog.getSaveFileName(self, 'Save As PNG',
                                               default_path,
                                               'PNG Files (*.png)')
        image = QImage(image_width, image_height, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene.render(painter)
        painter.end()
        image.save(filename,  'PNG')




    def closeDialog(self):
        QDialog.done(self, 0)

#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui
import math
import binascii
from model import Models
from model import Traveller
#import WorldDialogs
from log import *

CELLSIZE = 100
HEX_DELTA = float(abs(math.tan(math.radians(30))) * 25.0)

userType = QtGui.QGraphicsItem.UserType

SECTOR_ROOT_TYPE = userType
SUBSECTOR_ROOT_TYPE = userType + 1
HEX_ROOT_TYPE = userType +2
GRID_TYPE = userType + 3

SECTOR_RECTANGLE_TYPE = userType + 4
SECTOR_GLYPH_TYPE = userType + 5
SUBSECTOR_RECTANGLE_TYPE = userType + 6
SUBSECTOR_GLYPH_TYPE = userType + 7
GRID_HEX_TYPE = userType + 8
GRID_CELL_TYPE = userType + 9
PLANET_CIRCLE_TYPE = userType + 10
PLANET_GLYPH_TYPE = userType + 11
TZ_CIRCLE_TYPE = userType + 12
GAS_GIANT_TYPE = userType + 13
GAS_GIANT_RING_TYPE = userType + 14
BASE_GLYPH_TYPE = userType + 15

def gridToPix(gx, gy):
    px = CELLSIZE * gx
    py = CELLSIZE * gy
    if gx%2 != 0:
        py += CELLSIZE / 2.0
    return int(px), int(py)

def gridToHEX(gx, gy):
    # Convert x,y coords to H,E,X three-axis coordinates
    H = int(math.floor( 2.0 * gy))
    E = int(math.floor(math.sqrt(3.0) * gx - gy))
    X = int(math.floor(math.sqrt(3.0) * gx + gy))
    return H, E, X

def targetXY(angle, distance):
    theta = math.radians(angle)
    dx = distance * math.cos(theta)
    dy = distance * math.sin(theta)
    return dx, dy

# deprecated
##def gridToSecRelText(gx, gy):
##    xtext = str((gx % 32) + 1).zfill(2)
##    ytext = str((gy % 40) + 1).zfill(2)
##    return xtext + ytext



class SectorRectangle(QtGui.QGraphicsPolygonItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsPolygonItem.__init__(self, parent)
        self._type = SECTOR_RECTANGLE_TYPE
        pen = QtGui.QPen()
        pen.setWidth(5)
        #pen.setColor(QtCore.Qt.darkGray)
        self.setPen(pen)
        self.setBrush(QtCore.Qt.transparent)
        # 0,0 is the centre of the top-left hex in the sector
        myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-50, -50), QtCore.QPointF(3150, -50),
                    QtCore.QPointF(3150,3950), QtCore.QPointF(-50, 3950),
                    QtCore.QPointF(-50, -50)])
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

    @property
    def itemType(self):
        return self._type

    def image(self):
        pixmap = QtGui.QPixmap(250, 250)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.myPolygon)
        return pixmap

    def boundingRect(self):
        return QtCore.QRectF(-50, -50, 3150, 3950)


class SectorGlyph(QtGui.QGraphicsItem):
    def __init__(self, col, row, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = SECTOR_GLYPH_TYPE
        self.boundary_glyph = SectorRectangle(self)
        self.sectorCol = col
        self.sectorRow = row
        self.cells = []
        
        self.name_text = QtGui.QGraphicsSimpleTextItem(self)
        self.name_text.hide()
        self.name_text.setFont(QtGui.QFont('Helvetica', 250, QtGui.QFont.Bold))
        self.name_text.setBrush(QtCore.Qt.darkGray)
        self.setName('Unknown')

    @property
    def itemType(self):
        return self._type

    def paint(self, painter=None, option=None, widget=None):
        pass

    def boundingRect(self):
        return QtCore.QRectF(-50, -50, 3150, 3950)

    def setName(self, name):
        self.name = name
        self.name_text.setText(name)
        offset = -1.0 * (self.name_text.boundingRect().width()/2)
        self.name_text.setPos((offset + 1550), 1740.0)

    def showName(self, flag):
        self.name_text.setVisible(flag)

    def itemChange(self, change, value):
        #Temporary feature to test cell selection/display
        if change == QtGui.QGraphicsItem.ItemSelectedHasChanged:
            if value == True:
                self.boundary_glyph.setBrush(QtCore.Qt.lightGray)
                self.boundary_glyph.setOpacity(0.7)
            else:
                self.boundary_glyph.setBrush(QtCore.Qt.transparent)
        else:
            #print 'NoSelectionChange'
            return value



class SubSectorRectangle(QtGui.QGraphicsPolygonItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsPolygonItem.__init__(self, parent)
        self._type = SUBSECTOR_RECTANGLE_TYPE
        pen = QtGui.QPen()
        pen.setWidth(2)
        #pen.setColor(QtCore.Qt.darkGray)
        self.setPen(pen)
        self.setBrush(QtCore.Qt.transparent)
        # 0,0 is the centre of the top-left hex in the sector
        myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-50, -50), QtCore.QPointF(750, -50),
                    QtCore.QPointF(750,950), QtCore.QPointF(-50, 950),
                    QtCore.QPointF(-50, -50)])
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

    @property
    def itemType(self):
        return self._type

    def boundingRect(self):
        return QtCore.QRectF(-50, -50, 750, 950)


class SubSectorGlyph(QtGui.QGraphicsItemGroup):
    def __init__(self, col, row, parent=None):
        QtGui.QGraphicsItemGroup.__init__(self, parent)
        self._type = SUBSECTOR_GLYPH_TYPE
        self.boundary_glyph = SubSectorRectangle(self)
        self.subsectorCol = col
        self.subsectorRow = row
        self.cells = []
        
        self.name_text = QtGui.QGraphicsSimpleTextItem(self)
        self.name_text.hide()
        self.name_text.setFont(QtGui.QFont('Helvetica', 50, QtGui.QFont.Bold))
        self.name_text.setBrush(QtGui.QColor(85,85,85,170))
        self.setName('Unknown')

    @property
    def itemType(self):
        return self._type

    def setName(self, name):
        self.name = name
        self.name_text.setText(name)
        offset = -1.0 * (self.name_text.boundingRect().width()/2)
        self.name_text.setPos((offset + 350), 410.0)

    def showName(self, flag):
        self.name_text.setVisible(flag)

    def itemChange(self, change, value):
        #Temporary feature to test cell selection/display
        if change == QtGui.QGraphicsItem.ItemSelectedHasChanged:
            if value == True:
                self.boundary_glyph.setBrush(QtCore.Qt.lightGray)
                self.boundary_glyph.setOpacity(0.7)
            else:
                self.boundary_glyph.setBrush(QtCore.Qt.transparent)
        else:
            #print 'NoSelectionChange'
            return value


class GridHex(QtGui.QGraphicsPolygonItem):

    def __init__(self, parent=None,
                 hex_color=QtCore.Qt.darkGray,
                 hex_brush=QtCore.Qt.transparent):
        QtGui.QGraphicsPolygonItem.__init__(self, parent)
        self._type = GRID_HEX_TYPE
        # path = QtGui.QPainterPath()
        self.pen = QtGui.QPen()
        self.pen.setWidth(0)
        self.pen.setColor(hex_color)
        self.setPen(self.pen)
        self.setBrush(hex_brush)
        topleft = ((HEX_DELTA - 50.0), -50.0)
        topright = ((50.0 - HEX_DELTA), -50.0)
        midright = ((50.0 + HEX_DELTA), 0.0)
        lowright = ((50.0 - HEX_DELTA), 50.0)
        lowleft = ((HEX_DELTA - 50.0), 50.0)
        midleft = ((-50.0 - HEX_DELTA), 0.0)
        myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(topleft[0], topleft[1]),
                    QtCore.QPointF(topright[0], topright[1]),
                    QtCore.QPointF(midright[0], midright[1]),
                    QtCore.QPointF(lowright[0], lowright[1]),
                    QtCore.QPointF(lowleft[0], lowleft[1]),
                    QtCore.QPointF(midleft[0], midleft[1]),
                    QtCore.QPointF(topleft[0], topleft[1])])
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

    @property
    def itemType(self):
        return self._type

    def boundingRect(self):
        return QtCore.QRectF((HEX_DELTA - 50.0), -50, (100 + HEX_DELTA), 100)

    def image(self):
        pixmap = QtGui.QPixmap(250, 250)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.lightGray, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.myPolygon)
        return pixmap


class GridCell(QtGui.QGraphicsItemGroup):
    def __init__(self, x, y, hex_color=QtCore.Qt.darkGray, parent=None):
        QtGui.QGraphicsItemGroup.__init__(self, parent)
        self._type = GRID_CELL_TYPE
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

        self.col = x
        self.row = y
        
        self.grid_poly = GridHex(self, hex_color)
        self.selection_poly = GridHex(self, hex_color)
        
        self.grid_text = QtGui.QGraphicsSimpleTextItem(self)
        self.grid_text.setBrush(QtCore.Qt.darkGray)
        self.allegianceColor = QtCore.Qt.transparent
        #self.grid_text.setFont(QtGui.QFont('Helvetica', 10, QtGui.QFont.Bold))

    @property
    def itemType(self):
        return self._type

    def setAllegianceColor(self, color):
        self.allegianceColor = color
        self.grid_poly.setBrush(color)
        #self.grid_poly.paint()

    def displayGridCoordText(self, flag):
        if flag:
            #text = gridToSecRelText(self.col, self.row)
            sectorX, sectorY = self.scene().model.gridToSector(
                                                    self.col, self.row)
            text = str(sectorX).zfill(2) + str(sectorY).zfill(2)
            #text = 'temp'
            self.grid_text.setText(text)
            offset = -1.0 * (self.grid_text.boundingRect().width()/2)
            self.grid_text.setPos(offset, -50.0)
            self.grid_text.show()
        else:
            self.grid_text.hide()

    def displayGlobalGridCoordText(self, flag):
        if flag:
            text = str(self.col) + ' ' + str(self.row)
            #text = 'temp'
            self.grid_text.setText(text)
            offset = -1.0 * (self.grid_text.boundingRect().width()/2)
            self.grid_text.setPos(offset, -45.0)
            self.grid_text.show()
        else:
            self.grid_text.hide()

    def itemChange(self, change, value):
        #Temporary feature to test cell selection/display
        if change == QtGui.QGraphicsItem.ItemSelectedHasChanged:
            if value == True:
                self.selection_poly.setBrush(QtCore.Qt.darkGray)
                self.selection_poly.setOpacity(0.7)
                self.scene().model.currentCell = (self.col, self.row)
            else:
                self.grid_poly.setBrush(self.allegianceColor)
                self.selection_poly.setBrush(QtCore.Qt.transparent)
        else:
            #print 'NoSelectionChange'
            return value


    def boundingRect(self):
        # Required for rubber band drag selection
        return QtCore.QRectF((HEX_DELTA - 50.0), -50, (100 + HEX_DELTA), 100)

##    def contextMenuEvent(self, event):
##        
##        #if len(self.scene().selectedItems()) > 1:
##        
##        if self.isSelected():
##            if len(self.scene().selectedItems()) > 1:
##                debug_log('Multiple cells context menu not implemented.')
##                return
##            else:
##                menu = QtGui.QMenu()
##                if self._pmi != None:
##                    editWorld = menu.addAction('Edit')
##                    addWorld = False
##                    removeWorld = menu.addAction('Remove World')
##                else:
##                    addWorld = menu.addAction('Add World')
##                    removeWorld = False
##                selectedAction = menu.exec_(event.screenPos())
##
##            if selectedAction == removeWorld:
##                self._pmi.model().removeRow(self._pmi.row())
##            elif selectedAction == editWorld:
##                self.dialog = EditWorldDialog.EditWorldDialog(self._pmi)
##                self.dialog.show()
##                self.dialog.raise_()
##                self.dialog.activateWindow()



class PlanetCircle(QtGui.QGraphicsItem):

    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = PLANET_CIRCLE_TYPE
        self.planet_color = QtCore.Qt.darkBlue
        self.sky_color = QtGui.QColor('#55AAFF')
        
        #self.setCursor(QtCore.Qt.OpenHandCursor)

    @property
    def itemType(self):
        return self._type

    def boundingRect(self):
        return QtCore.QRectF(-10.5, -10.5, 22, 22)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        #painter.setBrush(QtCore.Qt.cyan)
        painter.setBrush(self.sky_color)
        painter.drawEllipse(-12, -12, 24, 24)
        #painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.planet_color))
        painter.drawEllipse(-8, -8, 16, 16)

    def setPlanetColor(self, color):
        self.planet_color = color
        self.update()

    def setSkyColor(self, color):
        self.sky_color = color
        self.update()

    def setSelectionColour(self, flag):
        if flag == True:
            self.color = QtCore.Qt.green
        else:
            self.color = QtCore.Qt.blue
        self.update()


class GasGiantGlyph(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = GAS_GIANT_TYPE
        self.hide()

    @property
    def itemType(self):
        return self._type

    def boundingRect(self):
        return QtCore.QRectF(-6, -6, 12, 12)

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
        painter.drawEllipse(-3, -3, 6, 6)
        painter.rotate(70.0)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.75))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.transparent))
        painter.drawEllipse(-1, -7, 2, 14)


class BaseGlyphs(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = BASE_GLYPH_TYPE
        self.fontSize = 9
        #self.hide()
        self.backgrounds = {}

        # Build backgrounds dictionary
        # Backgrounds first so they are drawn first - behind symbols

        outlinePen = QtGui.QPen(QtGui.QBrush(QtCore.Qt.white), 1.0)
        #outlinePen = QtGui.QPen()
        
        #char = QtCore.QChar(0xAB)
        char = binascii.unhexlify('AB')
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Wingdings', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(char)
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['navy'] = symbol
        
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Helvetica', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(u'\u25B2')
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['scout'] = symbol
        
        #char = QtCore.QChar(0x70)
        char = binascii.unhexlify('70')
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Symbol', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(str(char))
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['research'] = symbol
        
        #char = QtCore.QChar(0x52)
        char = binascii.unhexlify('52')
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Wingdings', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(str(char))
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['tas'] = symbol
        
        #char = QtCore.QChar(0x6E)
        char = binascii.unhexlify('6E')
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Wingdings', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(str(char))
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['consulate'] = symbol
        
        #char = QtCore.QChar(0x4E)
        char = binascii.unhexlify('4E')
        symbol = QtGui.QGraphicsSimpleTextItem(self)
        symbol.setFont(QtGui.QFont('Wingdings', self.fontSize,
                                   QtGui.QFont.Normal, False))
        symbol.setText(str(char))
        symbol.setPen(outlinePen)
        symbol.hide()
        self.backgrounds['pirate'] = symbol

        self.symbols = {}
        for (base_type, symbol) in self.backgrounds.iteritems():
            new_symbol = QtGui.QGraphicsSimpleTextItem(self)
            new_symbol.setText(symbol.text())
            new_symbol.setFont(symbol.font())
            new_symbol.font().setPointSize(self.fontSize)
            new_symbol.setBrush(QtCore.Qt.black)
            new_symbol.hide()
            self.symbols[base_type] = new_symbol

        self.config()

    @property
    def itemType(self):
        return self._type

    def hideGlyphs(self):
        for symbol in self.symbols.itervalues():
            symbol.hide()
        for background in self.backgrounds.itervalues():
            background.hide()

    def config(self, navy=False, scout=False, research=False,
               tas=False, consulate=False, pirate=False):
        for symbol in self.symbols.itervalues():
            symbol.hide()
        for background in self.backgrounds.itervalues():
            background.hide()
        
        display_list = []
        if navy:
            display_list.append((self.backgrounds['navy'],
                                self.symbols['navy']))
        if scout:
            display_list.append((self.backgrounds['scout'],
                                self.symbols['scout']))
        if research:
            display_list.append((self.backgrounds['research'],
                                 self.symbols['research']))
        if tas:
            display_list.append((self.backgrounds['tas'],
                                self.symbols['tas']))
        if consulate:
            display_list.append((self.backgrounds['consulate'],
                                self.symbols['consulate']))
        if pirate:
            display_list.append((self.backgrounds['pirate'],
                                self.symbols['pirate']))

        if len(display_list) > 0:
            start_angle = 240
            count = 0
            for symbols in display_list:
                angle = start_angle - (count * 25)
                x, y = targetXY(angle, 35)
                for symbol in symbols:
                    dx = symbol.boundingRect().width() / 2
                    dy = symbol.boundingRect().height() / 2
                    symbol.setPos(x - dx, y - dy)
                    symbol.show()
                count = count + 1

    def boundingRect(self):
        return QtCore.QRectF(-6, -6, 12, 12)

    def paint(self, painter=None, option=None, widget=None):
        pass



class TravelCodeCircle(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = TZ_CIRCLE_TYPE
        self.hide()
        self.code = 'Green'
        
    @property
    def itemType(self):
        return self._type

    def boundingRect(self):
        return QtCore.QRectF(-35, -35, 70, 70)

    def paint(self, painter, option, widget):
        if self.code == 'Green':
            painter.setPen(QtGui.QPen(QtCore.Qt.green, 1))
            painter.setBrush(QtGui.QBrush(QtCore.Qt.transparent))
            painter.drawEllipse(-35, -35, 70, 70)
        elif self.code == 'Amber':
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 191, 0), 3))
            painter.setBrush(QtGui.QBrush(QtCore.Qt.transparent))
            painter.drawEllipse(-35, -35, 70, 70)
        elif self.code == 'Red':
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 128)))
            painter.drawEllipse(-35, -35, 70, 70)

    def setTravelCode(self, zone):
        self.code = zone
        if self.code == 'Green':
            self.hide()
        elif self.code == 'Amber':
            self.show()
        elif self.code == 'Red':
            self.show()
        self.update()


class PlanetGlyph(QtGui.QGraphicsItem):
    def __init__(self, pmi, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self._type = PLANET_GLYPH_TYPE
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.travel_code = TravelCodeCircle(self)
        self.planet_image = PlanetCircle(self)
        self.gasGiantGlyph = GasGiantGlyph(self)
        self.gasGiantGlyph.setPos(30, -17)
        self.baseGlyphs = BaseGlyphs(self)
        self.name_text = QtGui.QGraphicsSimpleTextItem(self)
        self.display_code = QtGui.QGraphicsSimpleTextItem(self)

        self._pmi = pmi
        self.configurePlanetGlyph(False)

    @property
    def itemType(self):
        return self._type

    def itemChange(self, change, value):
        #Temporary feature to test cell selection/display
        if change == QtGui.QGraphicsItem.ItemSelectedHasChanged:
            if value == True:
                self.planet_image.setSelectionColour(True)
            else:
                self.planet_image.setSelectionColour(False)
        else:
            #print 'NoSelectionChange'
            return value

    def paint(self, painter=None, option=None, widget=None):
        pass

    def boundingRect(self):
        # Required for rubber band drag selection
        return QtCore.QRectF(-25, -25, 50, 50)

    def configurePlanetGlyph(self, show_details):
        if show_details:

            if self._pmi != None:
                world = self.pmi.model().getWorld(self.pmi)
                
                self.name_text.setFont(QtGui.QFont('Helvetica', 10, QtGui.QFont.Bold))
                self.name_text.setText(world.name)
                offset = -1.0 * (self.name_text.boundingRect().width()/2)
                self.name_text.setPos(offset, 30.0)

                code_value = world.starport.code
                self.display_code.setFont(QtGui.QFont('Helvetica', 10, QtGui.QFont.Bold))
                self.display_code.setText(str(code_value))
                offset = -1.0 * (self.display_code.boundingRect().width()/2)
                self.display_code.setPos(offset, -30)

                self.travel_code.setTravelCode(world.travelCode.code)
                
                if world.hasGasGiant:
                    self.gasGiantGlyph.show()
                else:
                    self.gasGiantGlyph.hide()

                
                self.planet_image

                self.baseGlyphs.config(navy=world.starport.hasNavyBase,
                                       scout=world.starport.hasScoutBase,
                                       research=world.starport.hasResearchBase,
                                       tas=world.starport.hasTas,
                                       consulate=world.starport.hasConsulate,
                                       pirate=world.starport.hasPirateBase)
                
                self.name_text.show()
                self.planet_image.show()
                self.display_code.show()

        else:
            self.planet_image.show()
            self.gasGiantGlyph.hide()
            self.baseGlyphs.hideGlyphs()
            self.name_text.hide()
            self.display_code.hide()
            self.travel_code.hide()
            

    def getPMI(self):
        return self._pmi
    def setPMI(self, pmi):
        self._pmi = pmi
        self.configurePlanetGlyph()
    def delPMI(self):
        del self._pmi
    pmi = property(getPMI, setPMI, delPMI, "The Planet's pmi property")

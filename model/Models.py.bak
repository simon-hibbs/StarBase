
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

import platform
from PySide.QtCore import *
from PySide.QtGui import *
import os
import shutil
import csv
from ConfigParser import SafeConfigParser
from log import *
import random
import math
#import richtextlineedit
import unicodedata
import re
from model import Traveller
from model import Merchant
from categories import WorldGenerator
from yapsy.PluginManager import PluginManager
try:
    import cPickle as pickle
except:
    import pickle



NAME = 0
COL = 1
ROW = 2
SECTOR_COORDS = 3
STARPORT = 4
STARPORT_TEXT = 5
SIZE = 6
SIZE_TEXT = 7
ATMOSPHERE = 8
ATMOSPHERE_TEXT = 9
HYDROGRAPHICS = 10
WATER_TEXT = 11
POPULATION = 12
POPULATION_TEXT = 13
GOVERNMENT = 14
GOVERNMENT_TEXT = 15
LAW_LEVEL = 16
LAW_LEVEL_TEXT = 17
TECH_LEVEL = 18
TECH_LEVEL_TEXT = 19
TEMPERATURE = 20
TEMPERATURE_TEXT = 21
OWNING_SECTOR = 22
OWNING_SUBSECTOR = 23
TRAVEL_CODE = 24
GAS_GIANT = 25
BERTHING_COST = 26
REFINED_FUEL = 27
UNREFINED_FUEL = 28
STARSHIP_YARD = 29
SPACECRAFT_YARD = 30
SMALL_CRAFT_YARD = 31
FULL_REPAIR = 32
LIMITED_REPAIR = 33
NAVY_BASE = 34
SCOUT_BASE = 35
RESEARCH_BASE = 36
TAS = 37
CONSULATE = 38
PIRATE_BASE = 39
DIAMETER = 40
GRAVITY = 41
PRESSURE = 42
REQ_VACC = 43
REQ_RESPIRATOR = 44
REQ_FILTER = 45
REQ_AIR = 46
WATER_PERCENT = 47
INHABITANTS = 48
AGRICULTURAL = 49
ASTEROID = 50
BARREN = 51
DESERT = 52
FLUID_OCEAN = 53
GARDEN = 54
HIGH_POP = 55
HIGH_TECH = 56
ICE_CAPPED = 57
INDUSTRIAL = 58
LOW_POP = 59
LOW_TECH = 60
NON_AGRICULTURAL = 61
NON_INDUSTRIAL = 62
POOR = 63
RICH = 64
VACUUM = 65
WATER_WORLD = 66
ALLEGIANCE_CODE = 67
ALLEGIANCE_NAME = 68
COMMUNICATIONS_LINKS = 69

LAST = 69

def gridToSlant(gx, gy):
    sx = gx
    sy = gy + math.ceil(float(gx) / 2)
    return int(sx), int(sy)


def gridToHEX(gx, gy):
    # Convert x,y coords to H,E,X three-axis coordinates
    H = int(math.floor( 2.0 * gy))
    E = int(math.floor(math.sqrt(3.0) * gx - gy))
    X = int(math.floor(math.sqrt(3.0) * gx + gy))
    return H, E, X


FIELD_NAMES = ('World Name', 'Column', 'Row',
                          'Starport', 'Size', 'Atmosphere',
                          'Hydrographics', 'Population', 'Government',
                          'Law Level', 'Tech Level', 'Temperature',
                          'Gas Giant', 'Travel Code', 'Berthing Cost',
                          'Naval Base', 'Scout Base', 'Research Base',
                          'TAS', 'Imperial Consulate', 'Pirate Base',
                          'Hydro. %', 'Allegiance',
                          'Ag', 'As', 'Ba', 'De', 'Fl', 'Ga', 'Hi',
                          'Ht', 'IC', 'In', 'Lo', 'Lt', 'Na', 'NI',
                          'Po', 'Ri', 'Va', 'Wa')

ACQUIRED = 1


class WorldModel(QAbstractTableModel):

    def __init__(self):
        super(WorldModel, self).__init__()

        self.secsWide = 1
        self.secsHigh = 1

        self.project_path = ''
        self.sectors_file = ''
        self.subsectors_file = ''
        self.worlds_file = ''
        
        self.initialZoomLevel = 3
        self.horizontalScroll = 0
        self.verticalScroll = 0

        self.worldOccurrenceDM = 0
        self.dirty = False
        
        self.sectors = []
        self.subsectors = []
        self.worlds = []
        self.deleted_worlds= []
        self.merchant = Merchant.MerchantData()
        self.fromTradeWorldPmi = None
        self.toTradeWorldPmi = None
        self.groupNames = ['None']
        self.groupCells = [[]]
        self.selectedGroupIndex = 0

        self.manager = PluginManager(categories_filter={ "WorldGenerators": WorldGenerator})
        self.manager.setPluginPlaces(['plugins'])
        self.manager.locatePlugins()
        self.manager.loadPlugins()

        #The following is a placeholder and is actualy initialised by
        #refreshWorldGeneratorsCombo in the main starbase.py script
        #so that the combo is correctly populated.
        self.currentWorldGeneratorName = 'None'

        # This needs to go into the project config file
        self.auto_name = True
        self.world_name_list = []
    
        self._col = -1
        self._row = -1



    def loadProjectData(self, project_path):
        self.project_path = project_path
        debug_log('Loading project: ' + str(project_path))

        self.config_file = os.path.join(self.project_path ,  'starbase.ini')

        self.config = SafeConfigParser()
        self.config.read(self.config_file)

        self.secsWide = self.config.getint('Map', 'SectorGridWidth')
        self.secsHigh = self.config.getint('Map', 'SectorGridHeight')

        self.sectors_file = os.path.join(self.project_path, 
                                         self.config.get('Files', 'SectorsFile'))
        self.subsectors_file = os.path.join(self.project_path, 
                                            self.config.get('Files', 'SubsectorsFile'))
        self.worlds_file = os.path.join(self.project_path,
                                        self.config.get('Files', 'WorldsFile'))
        
        self.initialZoomLevel = self.config.getfloat('Display', 'ZoomLevel')
        self.horizontalScroll = self.config.getfloat('Display', 'HorizontalScroll')
        self.verticalScroll = self.config.getfloat('Display', 'VerticalScroll')

        if os.path.isfile('WorldNames.txt'):
            with open('WorldNames.txt', 'r') as f:
                self.world_name_list = f.readlines()
                debug_log('Using default WorldNames.txt file with ' + str(len(self.world_name_list)) + ' names')
        else:
            debug_log('World Model: World names file not found.')
            self.toggleAutoName(False)
            
        #Allegiance defaults defined in Traveller, but maintained in the model.
        #World objects just store the allegiance index into these lists.
        try:
            allegiance_codes = self.config.get('Overrides', 'allegiancecodes')
            allegiance_names = self.config.get('Overrides', 'allegiancenames')
            Traveller.allegiance_codes = allegiance_codes.split(',')
            Traveller.allegiance_names = allegiance_names.split(',')
            debug_log('Allegiance codes overriden.')
        except:
            debug_log('Allegiance codes not overriden, using defaults.')

        try:
            allegiance_colors = self.config.get('Overrides', 'allegiancecolors')
            Traveller.allegiance_colors = allegiance_colors.split(',')
        except:
            debug_log('Allegiance colors not overriden, using defaults.')

        try:
            self.defaultWorldGeneratorName = self.config.get('Overrides', 'worldgeneratorname')
        except:
            self.defaultWorldGeneratorName = 'Blank'
            debug_log('Default world generator name not found.')

        self.worldOccurrenceDM = 0
        self.dirty = False
        
        self.sectors = []
        self.subsectors = []
        self.worlds = []
        self.deleted_worlds= []

        self.loadSectors()
        self.loadSubsectors()
        self.loadWorlds()

    def addFactions(self, pmi):
        row = pmi.row()
        self.worlds[row].addFactions()
        modelIndex1 = self.index(row, GOVERNMENT_TEXT)
        modelIndex2 = self.index(row, GOVERNMENT_TEXT)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                    modelIndex1, modelIndex2)
        

    def addNewGroup(self, group_name):
        if group_name not in self.groupNames:
            self.groupNames.append(group_name)
            self.groupCells.append([])
            debug_log('Group "' + group_name + '" added.')
        else:
            debug_log('Duplicate group name: ' + group_name)

    def addCellsToGroup(self, index, coord_list):
        for xy in coord_list:
            if xy not in self.groupCells[index]:
                self.groupCells[index].append(xy)

    def disbandGroup(self, index):
        if len(self.groupNames) > index > 0:
            del self.groupNames[index]
            del self.groupCells[index]
            debug_log('Group disbanded.')
            if index <= self.selectedGroupIndex:
                self.selectedGroupIndex -= 1
        else:
            debug_log('Group "' + self.groupNames[index]+ '" not disbanded')

    def getCurrentCell(self):
        return self._col, self._row

    def setCurrentCell(self, cell_xy):
        col = cell_xy[0]
        row = cell_xy[1]
        if (self.secsWide * 32) > col >= 0:
            if (self.secsHigh * 40) > row >= 0:
                self._col = col
                self._row = row
            else:
                debug_log('Model.setCurrentCell: Row outside grid ' + \
                          str(col) + ' ' + str(row))
        else:
            debug_log('Model.setCurrentCell: Column outside grid ' + \
                      str(col) + ' ' + str(row))

    def delCurrentCell(self):
        del self._col
        del self._row
    currentCell = property(getCurrentCell, setCurrentCell, delCurrentCell,
             "Current cell coordinates")

    def getSubsectorList(self):
        return self.subsectors

    def getSectorList(self):
        return self.sectors

    def getAllegianceIndex(self, code):
        if code in Traveller.allegiance_codes:
            return Traveller.allegiance_codes.index(code)
        else:
            debug_log('Index for invalid allegiance code requested: ' + str(code))
            return 0

    def getAllegianceInfo(self, pmi):
        world = self.worlds[pmi.row()]
        color = QColor(Traveller.allegiance_colors[world.allegiance.index])
        color.setAlpha(128)
        return world.col, world.row, color

    def setAllegianceCode(self, pmi, code):
        if pmi != None:
            allegiance_index = Traveller.allegiance_codes.index(code)
            codeModelIndex = self.index(pmi.row(), ALLEGIANCE_CODE)
            nameModelIndex = self.index(pmi.row(), ALLEGIANCE_NAME)
            self.setData(codeModelIndex, allegiance_index)
            self.setData(nameModelIndex, allegiance_index)

    def allegianceCodeToName(self, code):
        if code in Traveller.allegiance_codes:
            index = Traveller.allegiance_codes.index(code)
            if 0 <= index < len(Traveller.allegiance_names):
                return Traveller.allegiance_names[index]
            else:
                debug_log('Allegiance names and codes lists do not match.')
                debug_log(str(Traveller.allegiance_codes))
                debug_log(str(Traveller.allegiance_names))
                return 'Non-alligned'
        else:
            debug_log('Allegiance code ' + str(code) + ' not found in list.')
            return 'Non-alligned'

##    def generateLinks(self, pmi=None):
##        if pmi != None:
##            # Generate links for just that world
##            pass
##        else:
##            self.links = []
##            

    def renameSubsector(self, col, row, text):
        #Setting the name in the map needs to be done seperately
        for subsector in self.subsectors:
            if subsector.subsectorCol == col and subsector.subsectorRow == row:
                subsector.name = text

    def renameSector(self, col, row, text):
        #Setting the name in the map needs to be done seperately
        for sector in self.sectors:
            if sector.sectorCol == col and sector.sectorRow == row:
                sector.name = text

    def allegianceDataChanged(self):
        modelIndex1 = self.index(0, ALLEGIANCE_CODE)
        modelIndex2 = self.index((len(self.worlds) - 1), ALLEGIANCE_NAME)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                    modelIndex1, modelIndex2)

    def mergeAllegiance(self, merge_from, merge_to):
        if merge_from in Traveller.allegiance_names and \
           merge_to in Traveller.allegiance_names:
            debug_log('Codes: ' + str(Traveller.allegiance_codes))
            debug_log('Merge From: ' + merge_from)
            debug_log('Merge To: ' + merge_to)
            
            from_index = Traveller.allegiance_names.index(merge_from)
            from_code = Traveller.allegiance_codes[from_index]
            debug_log('From Index: ' + str(from_index))
            debug_log('From Code: ' + from_code)

            to_index = Traveller.allegiance_names.index(merge_to)
            to_code = Traveller.allegiance_codes[to_index]
            debug_log('To Index: ' + str(to_index))
            debug_log('To Code: ' + to_code)

            for world in self.worlds:
                if world.allegiance.code == from_code:
                    world_index = self.worlds.index(world)
                    debug_log('Merging world ' + str(world.name) + ' from ' + \
                              world.allegiance.code)
                    world.allegiance.code = to_code
                    debug_log('To ' + world.allegiance.code)
                    debug_log('Index ' + str(world.allegiance.index))
                    
                    modelIndex1 = self.index(world_index, ALLEGIANCE_CODE)
                    modelIndex2 = self.index(world_index, ALLEGIANCE_NAME)
                    self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                              modelIndex1, modelIndex2)
            
            debug_log('Current codes: ')
            debug_log(str(Traveller.allegiance_codes))
            del Traveller.allegiance_codes[from_index]
            debug_log('New codes: ')
            debug_log(str(Traveller.allegiance_codes))
            del Traveller.allegiance_names[from_index]
            del Traveller.allegiance_colors[from_index]

            for world in self.worlds:
                if world.allegiance.index > from_index:
                    world_index = self.worlds.index(world)
                    world.allegiance.index = world.allegiance.index - 1

                    modelIndex1 = self.index(world_index, ALLEGIANCE_CODE)
                    modelIndex2 = self.index(world_index, ALLEGIANCE_NAME)
                    self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                              modelIndex1, modelIndex2)

        else:
            debug_log('Allegiance merge error in Models')
            debug_log('From: ' + merge_from)
            debug_log('To: ' + merge_to)
            debug_log('Codes: ' + str(Traveller.allegiance_codes))


    # Converts global grid coords to sector relative coords for grid display
    def gridToSector(self, gx, gy):
        sec_x = (gx % 32) + 1
        sec_y = (gy % 40) + 1
        return sec_x, sec_y

    def owningSector(self, gx, gy):
        sec_x = int(math.floor(float(gx) / 32.0))
        sec_y = int(math.floor(float(gy) / 40.0))

        for sector in self.sectors:
            if sec_x == sector.sectorCol \
               and sec_y == sector.sectorRow:
                return sector.name

    def owningSubsector(self, gx, gy):
        sub_x = int(math.floor(float(gx) / 8.0))
        sub_y = int(math.floor(float(gy) / 10.0))

        for sub in self.subsectors:
            if sub_x == sub.subsectorCol \
               and sub_y == sub.subsectorRow:
                return sub.name

    def getSubsectorAt(self, subX, subY):
        for subsector in self.subsectors:
            if subsector.subsectorCol == subX and \
               subsector.subsectorRow == subY:
                return subsector.name
        return None

    def getSectorAt(self, secX, secY):
        for sector in self.sectors:
            if sector.sectorCol == secX and \
               sector.sectorRow == secY:
                return sector.name
        return None

    def getUWP(self, row):

        if row == None:
            return 'Name              ' + \
                   'Hex ' + \
                   '  ' + \
                   'Statistics ' + \
                   'Bases   ' + \
                   'Remarks'
        
        world = self.worlds[row]
        sec_X, sec_Y = self.gridToSector(world.col, world.row)
        sector_xy = str(sec_X).zfill(2) + str(sec_Y).zfill(2)

        name = str(world.name)
        if len(name) > 16:
            name = name[0:15].ljust(18)
        else:
            name = name.ljust(18)

        upp = name + \
              sector_xy + \
              '  ' + \
              world.starport.code + \
              world.size.code + \
              world.atmosphere.code + \
              world.hydrographics.code + \
              world.population.code + \
              world.government.code + \
              world.lawLevel.code + \
              '-' + \
              world.techLevel.code + \
              '  '

        bases = ''
        if world.starport.hasNavyBase:
            bases = bases + 'N'
        if world.starport.hasScoutBase:
            bases = bases + 'S'
        if world.starport.hasResearchBase:
            bases = bases + 'R'
        if world.starport.hasTas:
            bases = bases + 'T'
        if world.starport.hasConsulate:
            bases = bases + 'C'
        if world.starport.hasPirateBase:
            bases = bases + 'P'

        upp = upp + bases.ljust(8)

        trade = ''

        if world.tradeAg:
            trade = trade + 'Ag '
        if world.tradeAs:
            trade = trade + 'As '
        if world.tradeBa:
            trade = trade + 'Ba '
        if world.tradeDe:
            trade = trade + 'De '
        if world.tradeFl:
            trade = trade + 'Fl '
        if world.tradeGa:
            trade = trade + 'Ga '
        if world.tradeHi:
            trade = trade + 'Hi '
        if world.tradeHt:
            trade = trade + 'Ht '
        if world.tradeIC:
            trade = trade + 'IC '
        if world.tradeIn:
            trade = trade + 'In '
        if world.tradeLo:
            trade = trade + 'Lo '
        if world.tradeLt:
            trade = trade + 'Lt '
        if world.tradeNa:
            trade = trade + 'Na '
        if world.tradeNI:
            trade = trade + 'NI '
        if world.tradePo:
            trade = trade + 'Po '
        if world.tradeRi:
            trade = trade + 'Ri '
        if world.tradeVa:
            trade = trade + 'Va '
        if world.tradeWa:
            trade = trade + 'Wa '

        upp = upp + trade.ljust(22)

        if world.travelCode.code == 'Red':
            upp = upp + 'R'
        elif world.travelCode.code == 'Amber':
            upp = upp + 'A'
        else:
            upp = upp + ' '

        upp = upp + '  '

        if world.hasGasGiant:
            upp = upp + 'G'
        else:
            upp = upp + ' '

        upp = upp + '  ' + world.allegiance.code

        return upp


    def slugify(self, name):
        name = unicode(name)
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        name = unicode(re.sub('[^\w\s-]', '', name).strip().lower())
        return str(re.sub('[-\s]+', '-', name))


    def storeWorldImage(self, world_name, image):
        world_path = os.path.join(self.project_path,
                                  'worlds',
                                  self.slugify(world_name))
        world_path = str(world_path)
        if not os.path.exists(world_path):
            os.makedirs(world_path)
            
        file_name = self.slugify(world_name) + '.png'
        file_path = os.path.join(world_path,  file_name)
        
        with open(file_path, 'w') as f:
            image.save(file_path,  'PNG')
        
        return file_path


    def storeTextData(self, world_name, file_name, text):
        world_path = os.path.join(self.project_path,
                                  'worlds',
                                  self.slugify(world_name))
        world_path = str(world_path)
        if not os.path.exists(world_path):
            os.makedirs(world_path)
        file_path = os.path.join(world_path,  file_name)
        with open(file_path, 'w') as f:
                f.seek(0)
                f.truncate()
                f.write(text)

    def retrieveTextData(self, world_name, file_name):
        path = os.path.join(self.project_path,'worlds',
                            self.slugify(world_name),
                            file_name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                text = f.read()
                return text
        return False

    def cleanupWorldsDirectory(self, world_name):
        path = os.path.join(self.project_path,
                            'worlds',
                            self.slugify(world_name))
        
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                debug_log('Deleted ' + path)
            except Exception, e:
                debug_log('Failed to delete ' + path)
                debug_log(e)
                return False

        return True

    # storeX methods to persist sesion parameters to config file
    def storeZoomLevel(self, zl):
        self.config.set('Display', 'ZoomLevel', str(zl))

    def storeHorizontalScroll(self, value):
        self.config.set('Display', 'HorizontalScroll', str(value))

    def storeVerticalScroll(self, value):
        self.config.set('Display', 'VerticalScroll', str(value))

    def storeAllegianceInfo(self):
        codes = ','.join(Traveller.allegiance_codes)
        names = ','.join(Traveller.allegiance_names)
        colors = ','.join(Traveller.allegiance_colors)
        
        self.config.set('Overrides', 'allegiancecodes', codes)
        self.config.set('Overrides', 'allegiancenames', names)
        #self.config.set('Overrides', 'allegiancecolors', colors)
        

##    def storeDisplayMatrix(self, m11, m12, m21, m22, dx, dy):
##        self.config.set('Display', 'HorizontalScale', str(m11))
##        self.config.set('Display', 'VerticalShear', str(m12))
##        self.config.set('Display', 'HorizontalShear', str(m21))
##        self.config.set('Display', 'VerticalScale', str(m22))
##        self.config.set('Display', 'HorizontalTranslation', str(dx))
##        self.config.set('Display', 'VerticalTranslation', str(dy))
        

    # Provides PMI for column 0 of given row. Used later to map back to the row.
    def getPMI(self, row):
        index = self.index(row,  NAME)
        return QPersistentModelIndex(index)

    def getPmiAt(self, grid_col, grid_row):
        for world in self.worlds:
            if world.col == grid_col and world.row == grid_row:
                model_row = self.worlds.index(world)
                index = self.index(model_row,  NAME)
                return QPersistentModelIndex(index)
        else:
            return None

    def getWorld(self, pmi):
        row = pmi.row()
        return self.worlds[row]

    def getDistance(self, fromColRow, toColRow):
        #Parameters are two-tupples of integers
        x1, y1 = gridToSlant(fromColRow[0], fromColRow[1])
        x2, y2 = gridToSlant(toColRow[0], toColRow[1])

        dx = x2 - x1
        dy = y2 - y1
        dd = dx - dy
##        debug_log("getDistance:")
##        debug_log("from: " + str(fromColRow) + "  to: " + str(toColRow))
##        debug_log("x1: " + str(x1) + "  y1: " + str(y1))
##        debug_log("x2: " + str(x2) + "  y2: " + str(y2))
##        debug_log("dx: " + str(dx) + "  dy: " + str(dy) + " dd: " + str(dd))
        
        return int(max([math.fabs(dx), math.fabs(dy), math.fabs(dd)]))


    def rollToPopulate(self):
        roll = random.randint(1, 6) + self.worldOccurrenceDM
        if roll >= 4:
            debug_log('Model: rollToPopulate True = ' + str(roll))
            return True
        else:
            debug_log('Model: rollToPopulate False = ' + str(roll))
            return False

    def insertRandomWorld(self, row):
        #self.insertRow(row)
        debug_log('Model: Inserting random world at row ' + str(row))
##        world = Traveller.World()
##        world.randomize()
        self.insertRow(row)
        self.regenerateWorld(row)

    def regenerateWorld(self, row):
        debug_log('Model: Randomizing existing world at row ' + str(row))
        ##port, size, atmo, hydro, pop, gov, law, tech, temp = Traveller.getRandomWorldData()
        modelIndex1 = self.index(row, 0)
        modelIndex2 = self.index(row, LAST)
        ##self.setData(modelIndex, int(port.index))

        #self.worlds[row].randomize()
        self.worlds[row].reconfigure(self.worldGenerators[self.currentWorldGeneratorName].generateWorld())

        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      modelIndex1, modelIndex2)


    def toggleAutoName(self, flag):
        if flag:
            debug_log('World Model: Enabling auto-name')
            self.auto_name = True
        else:
            debug_log('World Model: Disabling auto-name')
            self.auto_name = False

    def createWorldName(self, salt):
        if len(self.world_name_list) > 0:
            name_number = random.randint(0, (len(self.world_name_list) - 1))
            name = self.world_name_list.pop(name_number).rstrip()

            if salt and len(name) < 8:
                limit = 15 - len(name)
                d20 = random.randint(1, 20)
                if d20 <= 2:
                    name = 'New ' + name
                elif 2 <= d20 <= limit:
                    suffix = random.choice([' Prime', ' Prime', ' Alpha', ' Alpha',
                                            ' Beta', ' Gamma', ' Delta', ' Minor',
                                            ' Majoris', ' II', ' II', ' III', ' III',
                                            ' IV', ' IV', ' V', ' V', ' VI', ' IX'])
                    name = name + suffix
        else:
            debug_log('World Model: world_name_list empty')
        
        return name


    def hasWorldAtXY(self, x, y):
        answer = False
        self.world_at_xy = None
        for w in self.worlds:
            if w.col == x and w.row == y:
                answer = True
                self.world_at_xy = w
        return answer

    def hasNamedWorld(self, name):
        for world in self.worlds:
            if world.name == name:
                return True
        return False

##    def sortByName(self):
##        self.worlds = sorted(self.worlds)
##        self.reset()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.worlds)):
            return None
        world = self.worlds[index.row()]
        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            
            if column == NAME:
                return world.name
            
            elif column == COL:
                return world.col
            
            elif column == ROW:
                return world.row

            elif column == SECTOR_COORDS:
                x, y = self.gridToSector(world.col, world.row)
                text = str(x).zfill(2) + str(y).zfill(2)
                return text
            
            elif column == STARPORT:
                if role == Qt.EditRole:
                    return world.starport.index
                elif role == Qt.DisplayRole:
                    text = str(world.starport.code + ' - ' + world.starport.quality)
                    return text
                else:
                    return world.starport.code

            elif column == STARPORT_TEXT:
                if world.starport.userText != '':
                    return world.starport.userText
                else:
                    return world.starport.description

            elif column == SIZE:
                if role == Qt.EditRole:
                    return world.size.index
                elif role == Qt.DisplayRole:
                    return world.size.code
                else:
                    return world.size.code

            elif column == SIZE_TEXT:
                if world.size.userText != '':
                    return world.size.userText
                else:
                    return world.size.description

            elif column == ATMOSPHERE:
                if role == Qt.EditRole:
                    return world.atmosphere.index
                elif role == Qt.DisplayRole:
                    return world.atmosphere.code
                else:
                    return world.atmosphere.code

            elif column == ATMOSPHERE_TEXT:
                if world.atmosphere.userText != '':
                    return world.atmosphere.userText
                else:
                    return world.atmosphere.description

            elif column == HYDROGRAPHICS:
                if role == Qt.EditRole:
                    return world.hydrographics.index
                elif role == Qt.DisplayRole:
                    return world.hydrographics.code
                else:
                    return world.hydrographics.code

            elif column == WATER_TEXT:
                if world.hydrographics.userText != '':
                    return world.hydrographics.userText
                else:
                    return world.hydrographics.description
            
            elif column == POPULATION:
                if role == Qt.EditRole:
                    return world.population.index
                elif role == Qt.DisplayRole:
                    return world.population.code
                else:
                    return world.population.code

            elif column == POPULATION_TEXT:
                if world.population.userText != '':
                    return world.population.userText
                else:
                    return world.population.description
            
            elif column == GOVERNMENT:
                if role == Qt.EditRole:
                    return world.government.index
                elif role == Qt.DisplayRole:
                    return world.government.code
                else:
                    return world.government.code

            elif column == GOVERNMENT_TEXT:
                if world.government.userText != '':
                    return world.government.userText
                else:
                    return world.government.description

            elif column == LAW_LEVEL:
                if role == Qt.EditRole:
                    return world.lawLevel.index
                elif role == Qt.DisplayRole:
                    return world.lawLevel.code
                else:
                    return world.lawLevel.code

            elif column == LAW_LEVEL_TEXT:
                if world.lawLevel.userText != '':
                    return world.lawLevel.userText
                else:
                    return world.lawLevel.description

            elif column == TECH_LEVEL:
                if role == Qt.EditRole:
                    return world.techLevel.index
                elif role == Qt.DisplayRole:
                    return world.techLevel.code
                else:
                    return world.techLevel.code

            elif column == TECH_LEVEL_TEXT:
                if world.techLevel.userText != '':
                    return world.techLevel.userText
                else:
                    return world.techLevel.description

            elif column == TEMPERATURE:
                if role == Qt.EditRole:
                    return world.temperature.index
                elif role == Qt.DisplayRole:
                    return world.temperature.code
                else:
                    return world.temperature.code

            elif column == TEMPERATURE_TEXT:
                if world.temperature.userText != '':
                    return world.temperature.userText
                else:
                    return world.temperature.description

            elif column == OWNING_SECTOR:
                return self.owningSector(world.col, world.row)

            elif column == OWNING_SUBSECTOR:
                return self.owningSubsector(world.col, world.row)

            elif column == TRAVEL_CODE:
                if role == Qt.EditRole:
                    return world.travelCode.index
                elif role == Qt.DisplayRole:
                    return world.travelCode.code
                else:
                    return world.travelCode.code

            elif column == GAS_GIANT:
                return world.hasGasGiant

            elif column == ALLEGIANCE_CODE:
                if role == Qt.EditRole:
                    return world.allegiance.index
                elif role == Qt.DisplayRole:
                    return world.allegiance.code
                else:
                    return world.allegiance.code

            elif column == ALLEGIANCE_NAME:
                if role == Qt.EditRole:
                    return world.allegiance.index
                elif role == Qt.DisplayRole:
                    return world.allegiance.name
                else:
                    return world.allegiance.name

            elif column == BERTHING_COST:
                return world.starport.berthingCost

            elif column == REFINED_FUEL:
                return world.starport.hasRefined

            elif column == UNREFINED_FUEL:
                return world.starport.hasUnrefined

            elif column == STARSHIP_YARD:
                return world.starport.hasStarshipYard

            elif column == SPACECRAFT_YARD:
                return world.starport.hasSpacecraftYard

            elif column == SMALL_CRAFT_YARD:
                return world.starport.hasSmallCraftYard

            elif column == FULL_REPAIR:
                return world.starport.hasFullRepair

            elif column == LIMITED_REPAIR:
                return world.starport.hasLimitedRepair

            elif column == NAVY_BASE:
                return world.starport.hasNavyBase

            elif column == SCOUT_BASE:
                return world.starport.hasScoutBase

            elif column == RESEARCH_BASE:
                return world.starport.hasResearchBase

            elif column == TAS:
                return world.starport.hasTas

            elif column == CONSULATE:
                return world.starport.hasConsulate

            elif column == PIRATE_BASE:
                return world.starport.hasPirateBase

            elif column == DIAMETER:
                return world.size.diameter

            elif column == GRAVITY:
                return world.size.gravity

            elif column == PRESSURE:
                return world.atmosphere.pressure

            elif column == REQ_VACC:
                return world.atmosphere.requiresVacc

            elif column == REQ_RESPIRATOR:
                return world.atmosphere.requiresRespirator

            elif column == REQ_FILTER:
                return world.atmosphere.requiresFilter

            elif column == REQ_AIR:
                return world.atmosphere.requiresAir

            elif column == WATER_PERCENT:
                return world.hydrographics.percentage

            elif column == INHABITANTS:
                def splitThousands(s, sep=','):
                    if len(s) <= 3: return s
                    return splitThousands(s[:-3], sep) + sep + s[-3:]
                return splitThousands(str(world.population.inhabitants))

            elif column == AGRICULTURAL:
                return world.tradeAg

            elif column == ASTEROID :
                return world.tradeAs

            elif column == BARREN :
                return world.tradeBa

            elif column == DESERT :
                return world.tradeDe

            elif column == FLUID_OCEAN :
                return world.tradeFl

            elif column == GARDEN :
                return world.tradeGa

            elif column == HIGH_POP :
                return world.tradeHi

            elif column == HIGH_TECH :
                return world.tradeHt

            elif column == ICE_CAPPED :
                return world.tradeIC

            elif column == INDUSTRIAL :
                return world.tradeIn

            elif column == LOW_POP :
                return world.tradeLo

            elif column == LOW_TECH :
                return world.tradeLt

            elif column == NON_AGRICULTURAL :
                return world.tradeNa

            elif column == NON_INDUSTRIAL :
                return world.tradeNI

            elif column == POOR :
                return world.tradePo

            elif column == RICH :
                return world.tradeRi

            elif column == VACUUM :
                return world.tradeVa

            elif column == WATER_WORLD :
                return world.tradeWa

        elif role == Qt.TextAlignmentRole:
            if column == NAME:
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        elif role == Qt.TextColorRole and column == STARPORT:
            return QColor(Qt.darkBlue)
        elif role == Qt.BackgroundColorRole:
            if world.starport.code == "A" or world.starport.code == "B":
                return QColor(250, 230, 250)
            else:
                return QColor(210, 230, 230)
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == NAME:
                return "Name"
            elif section == COL:
                return "Column"
            elif section == ROW:
                return "Row"
            elif section == SECTOR_COORDS:
                return "Sector Hex"
            elif section == STARPORT:
                return "Starport"
            elif section == STARPORT_TEXT:
                return "Starport Description"
            elif section == SIZE :
                return "Size"
            elif section == SIZE_TEXT :
                return "Size Description"
            elif section == ATMOSPHERE :
                return "Atmosphere"
            elif section == ATMOSPHERE_TEXT :
                return "Atmosphere Description"
            elif section == HYDROGRAPHICS :
                return "Hydrographics"
            elif section == WATER_TEXT :
                return "Hydrographics Description"
            elif section == POPULATION :
                return "Population"
            elif section == POPULATION_TEXT :
                return "Population Description"
            elif section == GOVERNMENT :
                return "Government"
            elif section == GOVERNMENT_TEXT :
                return "Government Description"
            elif section == LAW_LEVEL :
                return "Law Level"
            elif section == LAW_LEVEL_TEXT :
                return "Law Level Description"
            elif section == TECH_LEVEL :
                return "Tech Level"
            elif section == TECH_LEVEL_TEXT :
                return "Tech Level Description"
            elif section == TEMPERATURE :
                return "Temperature"
            elif section == TEMPERATURE_TEXT :
                return "Temperature Description"
            elif section == OWNING_SECTOR :
                return "Sector"
            elif section == OWNING_SUBSECTOR :
                return "Subsector"
            elif section == TRAVEL_CODE :
                return "Travel Code"
            elif section == GAS_GIANT :
                return "Gas Giant"
            elif section == ALLEGIANCE_CODE:
                return "Allegiance Code"
            elif section == ALLEGIANCE_NAME:
                return "Allegiance Name"
            elif section == BERTHING_COST :
                return "Berthing cost"
            elif section == REFINED_FUEL :
                return "Refined Fuel"
            elif section == UNREFINED_FUEL :
                return "Unrefined fuel"
            elif section == STARSHIP_YARD :
                return "Starship yard"
            elif section == SPACECRAFT_YARD :
                return "Spacecraft yard"
            elif section == SMALL_CRAFT_YARD :
                return "Small craft yard"
            elif section == FULL_REPAIR :
                return "Full repair"
            elif section == LIMITED_REPAIR :
                return "Limited repair"
            elif section == NAVY_BASE :
                return "Navy base"
            elif section == SCOUT_BASE :
                return "Scout base"
            elif section == RESEARCH_BASE :
                return "Research base"
            elif section == TAS :
                return "TAS lodge"
            elif section == CONSULATE :
                return "Consulate"
            elif section == PIRATE_BASE :
                return "Pirate base"
            elif section == DIAMETER :
                return "Diameter"
            elif section == GRAVITY :
                return "Gravity"
            elif section == PRESSURE :
                return "Pressure"
            elif section == REQ_VACC :
                return "Vacc. Suit"
            elif section == REQ_RESPIRATOR :
                return "Respirator"
            elif section == REQ_FILTER :
                return "Air Filter"
            elif section == REQ_AIR :
                return "Air Supply"
            elif section == WATER_PERCENT :
                return "Water Coverage"
            
            elif section == INHABITANTS :
                return "Inhabitants"

            elif section == AGRICULTURAL  :
                return "Agricultural"
            elif section == ASTEROID  :
                return "Asteroid"
            elif section == BARREN  :
                return "Barren"
            elif section == DESERT  :
                return "Desert"
            elif section == FLUID_OCEAN  :
                return "Fluid Ocean"
            elif section == GARDEN    :
                return "Garden"
            elif section == HIGH_POP  :
                return "High Pop."
            elif section == HIGH_TECH  :
                return "High Tech."
            elif section == ICE_CAPPED  :
                return "Ice Capped"
            elif section == INDUSTRIAL  :
                return "Industrial"
            elif section == LOW_POP   :
                return "Low Pop."
            elif section == LOW_TECH  :
                return "Low Tech."
            elif section == NON_AGRICULTURAL  :
                return "Non-Agricultural"
            elif section == NON_INDUSTRIAL  :
                return "Non-Industrial"
            elif section == POOR  :
                return "Poor"
            elif section == RICH  :
                return "Rich"
            elif section == VACUUM  :
                return "Vacuum"
            elif section == WATER_WORLD  :
                return "Water World"
            
        return int(section + 1)


    def rowCount(self, index=QModelIndex()):
        return len(self.worlds)

    def columnCount(self, index=QModelIndex()):
        return (LAST + 1)

    @logmethod
    def setData(self, index, value, role=Qt.EditRole):
        #debug_log('Model setData called with role: ' + str(role))
        debug_log("Row " + str(index.row()) + " Col " + str(index.column()) +
                  " value " + str(value))
        if index.isValid() and 0 <= index.row() < len(self.worlds):
            world = self.worlds[index.row()]
            column = index.column()
            
            if column == NAME:
                new_name = str(value)
                if new_name != world.name:
                    for w in self.worlds:
                        if new_name == w.name:
                            debug_log('Models:setData duplicate world name ' + new_name)
                            return False
                        
                    old_path = os.path.join(self.project_path, 'worlds', 
                                            self.slugify(world.name))
                    new_path = os.path.join(self.project_path, 'worlds', 
                                            self.slugify(new_name))
                    
                    if os.path.exists(new_path):
                        self.cleanupWorldsDirectory(new_name)
                    
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        debug_log('Model.setData: Renamed world details directory.')

                    debug_log('Model.setData: Changing' + world.name + ' to ' + new_name)


                    world.name = new_name
                    
                
            elif column == COL:
                newCol = int(value)
                newPos = (newCol, world.row)
                if newPos != (world.col, world.row):
                    collided = False
                    for w in self.worlds:
                        if newPos == (w.col, w.row):
                            debug_log('Worlds Collided at ' + str(w.col) + ' ' + str(w.row))
                            collided = True
                    if not collided:
                        world.col = newCol
                
            elif column == ROW:
                newRow = int(value)
                newPos = (world.col, newRow)
                if newPos != (world.col, world.row):
                    collided = False
                    for w in self.worlds:
                        if newPos == (w.col, w.row):
                            debug_log('Worlds Collided at ' + str(w.col) + ' ' + str(w.row))
                            collided = True
                    if not collided:
                        world.row = newRow

            elif column == SECTOR_COORDS:
                pass
            
            elif column == STARPORT:
                new_index = value
                if world.starport.index != int(new_index):
                    world.starport.index = int(new_index)

            elif column == STARPORT_TEXT:
                debug_log('Size text changed!')
                world.starport.userText = str(value)
                world.starport.userTextChanged = True
                world.dirty = True

            elif column == SIZE :
                new_index = value
                if world.size.index != int(new_index):
                    world.size.index =int(new_index)

            elif column == SIZE_TEXT:
                debug_log('Size text changed!')
                world.size.userText = str(value)
                world.size.userTextChanged = True
                world.dirty = True

            elif column == ATMOSPHERE :
                new_index = value
                if world.atmosphere.index != int(new_index):
                    world.atmosphere.index = int(new_index)

            elif column == ATMOSPHERE_TEXT:
                debug_log('Atmosphere text changed!')
                world.atmosphere.userText = str(value)
                world.atmosphere.userTextChanged = True
                world.dirty = True

            elif column == HYDROGRAPHICS :
                new_index = value
                if world.hydrographics.index != int(new_index):
                    world.hydrographics.index = int(new_index)
                    self.storeTextData(world.name,
                                       'Hydrographics.txt',
                                       world.hydrographics.description)

            elif column == WATER_TEXT:
                debug_log('Hydrographics text changed!')
                world.hydrographics.userText = str(value)
                world.hydrographics.userTextChanged = True
                world.dirty = True

            elif column == POPULATION :
                new_index = value
                if world.population.index != int(new_index):
                    world.population.index = int(new_index)
                    self.storeTextData(world.name,
                                       'Population.txt',
                                       world.population.description)

            elif column == POPULATION_TEXT:
                debug_log('Population text changed!')
                world.population.userText = str(value)
                world.population.userTextChanged = True
                world.dirty = True

            elif column == GOVERNMENT :
                new_index = value
                if world.government.index != int(new_index):
                    world.government.index =int(new_index)

            elif column == GOVERNMENT_TEXT:
                debug_log('Government text changed!')
                world.government.userText = str(value)
                world.government.userTextChanged = True
                world.dirty = True

            elif column == LAW_LEVEL :
                new_index = value
                if world.lawLevel.index != int(new_index):
                    world.lawLevel.index = int(new_index)

            elif column == LAW_LEVEL_TEXT:
                debug_log('Law level text changed!')
                world.lawLevel.userText = str(value)
                world.lawLevel.userTextChanged = True
                world.dirty = True

            elif column == TECH_LEVEL :
                new_index = value
                if world.techLevel.index != int(new_index):
                    world.techLevel.index = int(new_index)

            elif column == TECH_LEVEL_TEXT:
                debug_log('Tech level text changed!')
                world.techLevel.userText = str(value)
                world.techLevel.userTextChanged = True
                world.dirty = True

            elif column == TEMPERATURE :
                new_index = value
                if world.temperature.index != int(new_index):
                    world.temperature.index = int(new_index)

            elif column == TEMPERATURE_TEXT:
                debug_log('Temperature text changed!')
                world.temperature.userText = str(value)
                world.temperature.userTextChanged = True
                world.dirty = True

            elif column == OWNING_SECTOR:
                pass

            elif column == OWNING_SUBSECTOR:
                pass

            elif column == TRAVEL_CODE:
                number = value
                world.travelCode.index = int(number)

            elif column == GAS_GIANT:
                world.hasGasGiant = value

            elif column == ALLEGIANCE_CODE:
                new_index = value
                if world.allegiance != int(new_index):
                    world.allegiance.index = int(new_index)

            elif column == ALLEGIANCE_NAME:
                new_index = value
                if world.allegiance != int(new_index):
                    world.allegiance.index = int(new_index)

            elif column == BERTHING_COST:
                cost = value
                world.starport.berthingCost = int(cost)

            elif column == REFINED_FUEL:
                world.starport.hasRefined = value

            elif column == UNREFINED_FUEL:
                world.starport.hasUnrefined = value

            elif column == STARSHIP_YARD:
                world.starport.hasStarshipYard = value

            elif column == SPACECRAFT_YARD:
                world.starport.hasSpacecraftYard = value

            elif column == SMALL_CRAFT_YARD:
                world.starport.hasSmallCraftYard = value

            elif column == FULL_REPAIR:
                world.starport.hasFullRepair = value

            elif column == LIMITED_REPAIR:
                world.starport.hasLimitedRepair = value

            elif column == NAVY_BASE:
                world.starport.hasNavyBase = value

            elif column == SCOUT_BASE:
                world.starport.hasScoutBase = value

            elif column == RESEARCH_BASE:
                world.starport.hasResearchBase = value

            elif column == TAS:
                world.starport.hasTas = value

            elif column == CONSULATE:
                world.starport.hasConsulate = value

            elif column == PIRATE_BASE:
                world.starport.hasPirateBase = value

            elif column == DIAMETER:
                pass

            elif column == GRAVITY:
                pass

            elif column == PRESSURE:
                pass

            elif column == REQ_VACC:
                world.atmosphere.requiresVacc = value

            elif column == REQ_RESPIRATOR:
                world.atmosphere.requiresRespirator = value

            elif column == REQ_FILTER:
                world.atmosphere.requiresFilter = value

            elif column == REQ_AIR:
                world.atmosphere.requiresAir = value

            elif column == WATER_PERCENT:
                pass

            elif column == INHABITANTS:
                pass

            elif column == AGRICULTURAL:
                world.tradeAg = value

            elif column == ASTEROID :
                world.tradeAs = value

            elif column == BARREN :
                world.tradeBa = value

            elif column == DESERT :
                world.tradeDe = value

            elif column == FLUID_OCEAN :
                world.tradeFl = value

            elif column == GARDEN :
                world.tradeGa = value

            elif column == HIGH_POP :
                world.tradeHi = value

            elif column == HIGH_TECH :
                world.tradeHt = value

            elif column == ICE_CAPPED :
                world.tradeIC = value

            elif column == INDUSTRIAL :
                world.tradeIn = value

            elif column == LOW_POP :
                world.tradeLo = value

            elif column == LOW_TECH :
                world.tradeLt = value

            elif column == NON_AGRICULTURAL :
                world.tradeNa = value

            elif column == NON_INDUSTRIAL :
                world.tradeNI = value

            elif column == POOR :
                world.tradePo = value

            elif column == RICH :
                world.tradeRi = value

            elif column == VACUUM :
                world.tradeVa = value

            elif column == WATER_WORLD :
                world.tradeWa = value

            self.dirty = True
            modelIndex1 = self.index(index.row(), 0)
            modelIndex2 = self.index(index.row(), LAST)
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      modelIndex1, modelIndex2)
            
            return True
        return False

    @logmethod
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position)
        #Code supporting multiple row insert removed. Only one at a time.
        current_xy = self.currentCell
        col = current_xy[0]
        row = current_xy[1]
 
        if self.auto_name:
            name = self.createWorldName(True)
        else:
            if len(self.world_name_list) == 0:
                debug_log('Models.insertRows: Run out of world names!')
            name = str(col + 500).zfill(3) + ':' + str(row + 500).zfill(3)

        for world in self.worlds:
            if name == world.name:
                debug_log('Models.insertRows: Name Clash creating world ' + name)
                return False
        self.worlds.insert(position, Traveller.World(name, col, row))
##        self.links.insert(position, [])
        self.endInsertRows()
        self.dirty = True
        return True

    @logmethod
    def removeRows(self, position, rows=1, index=QModelIndex()):
        debug_log("About to remove row(s).")
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        debug_log("Removing row(s).")
        self.deleted_worlds.extend(self.worlds[position:(position + rows)])
        
        self.worlds = self.worlds[:position] + \
                     self.worlds[position + rows:]

        self.endRemoveRows()
        self.dirty = True
        return True


    def loadSectors(self):
        debug_log('Loading Sectors')
        exception = None
        f = open(self.sectors_file, "r")
        self.sectors = []
        try:
            reader = csv.reader(f, dialect='excel')
            for line in reader:
                if line[0] != "Sector Name":
                    name, column, row = line[0], int(line[1]), int(line[2])
                    if  0 <= column <= (self.secsWide - 1) and \
                           0 <= row <= (self.secsHigh - 1):
                        self.sectors.append(Traveller.Sector(name, column, row))
                    else:
                        debug_log('Sector outside grid: ' + str(name))
                        debug_log('secsWide = ' + str(self.secsWide) + \
                                  '    secsHigh = ' + str(self.secsHigh))
                        debug_log('')
                                  
        except IOError, e:
            exception = e
            debug_log(e)
        finally:
            f.close()

            def hasSectorAt(x, y):
                for sector in self.sectors:
                    if sector.sectorCol == x and sector.sectorRow == y:
                        return True
                return False

            for x in range(self.secsWide):
                for y in range(self.secsHigh):
                    if not hasSectorAt(x, y):
                        name = 'Sector ' + str(x + 10) + '/' + str(y + 10)
                        self.sectors.append(Traveller.Sector(name, x, y))
                        
            #self.dirty = False
            #self.reset()
        
    def loadSubsectors(self):
        debug_log('Loading Subsectors')
        exception = None
        f = open(self.subsectors_file, "r")
        self.subsectors = []
        try:
            reader = csv.reader(f, dialect='excel')
            for line in reader:
                if line[0] != "Subsector Name":
                    name, column, row = line[0], int(line[1]), int(line[2])
                    if 0 <= column <= ((self.secsWide * 4) - 1) and \
                            0 <= row <= ((self.secsHigh * 4) - 1):
                        self.subsectors.append(Traveller.Subsector(name, column, row))
                    else:
                        debug_log('Subsector outside grid: ' + str(name))
                        debug_log('secsWide = ' + str(self.secsWide) + \
                                  '    secsHigh = ' + str(self.secsHigh))
                        debug_log('Subsector col= ' + str(column) + '    ' + \
                                  'Subsector row= ' + str(row))
        except IOError, e:
            exception = e
            debug_log(e)
        finally:
            f.close()

            def hasSubsectorAt(x, y):
                for sub in self.subsectors:
                    if sub.subsectorCol == x and sub.subsectorRow == y:
                        return True
                return False

            for x in range(self.secsWide * 4):
                for y in range(self.secsHigh * 4):
                    if not hasSubsectorAt(x, y):
                        sx = x; sy = y
                        while sx >= 4:
                            sx = sx - 4
                        while sy >= 4:
                            sy = sy - 4
                        name = str(self.owningSector((x * 8), (y * 10))) + \
                               ': ' + str(sx) + '/' + str(sy)
                        self.subsectors.append(Traveller.Subsector(name, x, y))
            #self.dirty = False
            #self.reset()

    @logmethod
    def loadWorlds(self):
        
        def checkYesNo(text):
            if text == 'Yes': return True
            else: return False
        
        exception = None
        f = open(self.worlds_file, "r")
        self.worlds = []
        try:
            reader = csv.DictReader(f, dialect='excel')
            for line in reader:
                world = Traveller.World(
                    name=line['World Name'],
                    x=int(line['Column']),
                    y=int(line['Row']),
                    port=line['Starport'],
                    size=line['Size'],
                    atmosphere=line['Atmosphere'],
                    hydrographics=line['Hydrographics'],
                    population=line['Population'],
                    government=line['Government'],
                    law_level=line['Law Level'],
                    tech_level=line['Tech Level'],
                    temperature=line['Temperature'],
                    gas=checkYesNo(line['Gas Giant']),
                    travel_code=line['Travel Code'],
                    berthing_cost=line['Berthing Cost'],
                    navy=checkYesNo(line['Naval Base']),
                    scout=checkYesNo(line['Scout Base']),
                    research=checkYesNo(line['Research Base']),
                    tas=checkYesNo(line['TAS']),
                    consulate=checkYesNo(line['Imperial Consulate']),
                    pirate=checkYesNo(line['Pirate Base']),
                    hydro_pc=line['Hydro. %'],
                    allegiance=line['Allegiance'],
                    Ag=checkYesNo(line['Ag']),
                    As=checkYesNo(line['As']),
                    Ba=checkYesNo(line['Ba']),
                    De=checkYesNo(line['De']),
                    Fl=checkYesNo(line['Fl']),
                    Ga=checkYesNo(line['Ga']),
                    Hi=checkYesNo(line['Hi']),
                    Ht=checkYesNo(line['Ht']),
                    IC=checkYesNo(line['IC']),
                    In=checkYesNo(line['In']),
                    Lo=checkYesNo(line['Lo']),
                    Lt=checkYesNo(line['Lt']),
                    Na=checkYesNo(line['Na']),
                    NI=checkYesNo(line['NI']),
                    Po=checkYesNo(line['Po']),
                    Ri=checkYesNo(line['Ri']),
                    Va=checkYesNo(line['Va']),
                    Wa=checkYesNo(line['Wa'])
                    )
                #world.recalculateTradeCodes()
                self.worlds.append(world)
                #debug_log(self.getUWP(len(self.worlds) - 1))

        except IOError, e:
            exception = e
        finally:
            f.close()
            self.dirty = False
            self.reset()

        # Load custom user text
        for world in self.worlds:
            world_path = os.path.join(self.project_path, 'worlds',  self.slugify(world.name))
            if os.path.exists(world_path):
                
                filepath = os.path.join(world_path,'Starport.txt')
                if os.path.exists(filepath):
                    world.starport.userText = self.retrieveTextData(world.name, 'Starport.txt')
                
                filepath = os.path.join(world_path, 'Size.txt')
                if os.path.exists(filepath):
                    world.size.userText = self.retrieveTextData(world.name, 'Size.txt')
                    
                filepath = os.path.join(world_path,'Atmosphere.txt')
                if os.path.exists(filepath):
                    world.atmosphere.userText = self.retrieveTextData(world.name, 'Atmosphere.txt')
                    
                filepath = os.path.join(world_path,'Hydrographics.txt')
                if os.path.exists(filepath):
                    world.hydrographics.userText = self.retrieveTextData(world.name, 'Hydrographics.txt')
                    
                filepath = os.path.join(world_path, 'Population.txt')
                if os.path.exists(filepath):
                    world.population.userText = self.retrieveTextData(world.name, 'Population.txt')
                    
                filepath = os.path.join(world_path, 'Government.txt')
                if os.path.exists(filepath):
                    world.government.userText = self.retrieveTextData(world.name, 'Government.txt')
                    
                filepath = os.path.join(world_path, 'LawLevel.txt')
                if os.path.exists(filepath):
                    world.lawLevel.userText = self.retrieveTextData(world.name, 'LawLevel.txt')
                    
                filepath = os.path.join(world_path, 'TechLevel.txt')
                if os.path.exists(filepath):
                    world.techLevel.userText = self.retrieveTextData(world.name, 'TechLevel.txt')
                    
                filepath = os.path.join(world_path, 'Temperature.txt')
                if os.path.exists(filepath):
                    world.temperature.userText = self.retrieveTextData(world.name, 'Temperature.txt')

        # Load Cell Group data
        group_filename = os.path.join(self.project_path, 'HexGroupData.dat')
        if os.path.exists(group_filename):
            with open(group_filename, "rb") as group_file:
                self.groupNames = pickle.load(group_file)
                self.groupCells = pickle.load(group_file)


    @logmethod
    def save(self):
        # Save world data
        
        def setYesNo(value):
            if value: return 'Yes'
            else: return 'No'

        # Clean up custom directories for deleted worlds
        for world in self.deleted_worlds:
            self.cleanupWorldsDirectory(world.name)

        # Save worlds csv file
        exception = None
        f = open(self.worlds_file, "wb")
        try:
            writer = csv.DictWriter(f,
                                    dialect='excel',
                                    fieldnames=FIELD_NAMES)
            headers = {}
            for n in FIELD_NAMES:
                headers[n] = n
            writer.writerow(headers)
            for world in self.worlds:
                writer.writerow( {'World Name': world.name,
                                  'Column' : world.col,
                                  'Row' : world.row,
                                  'Starport' : world.starport,
                                  'Size' : world.size,
                                  'Atmosphere' : world.atmosphere,
                                  'Hydrographics' : world.hydrographics,
                                  'Hydro. %' : world.hydrographics.percentage,
                                  'Population' : world.population,
                                  'Government' : world.government,
                                  'Law Level' : world.lawLevel,
                                  'Tech Level' : world.techLevel,
                                  'Temperature' : world.temperature,
                                  'Gas Giant' : setYesNo(world.hasGasGiant),
                                  'Travel Code' : world.travelCode,
                                  'Berthing Cost' : world.starport.berthingCost,
                                  'Naval Base' : setYesNo(world.starport.hasNavyBase),
                                  'Scout Base' : setYesNo(world.starport.hasScoutBase),
                                  'Research Base' : setYesNo(world.starport.hasResearchBase),
                                  'TAS' : setYesNo(world.starport.hasTas),
                                  'Imperial Consulate' : setYesNo(world.starport.hasConsulate),
                                  'Pirate Base' : setYesNo(world.starport.hasPirateBase),
                                  'Allegiance' : world.allegiance,
                                  'Ag' : setYesNo(world.tradeAg),
                                  'As' : setYesNo(world.tradeAs),
                                  'Ba' : setYesNo(world.tradeBa),
                                  'De' : setYesNo(world.tradeDe),
                                  'Fl' : setYesNo(world.tradeFl),
                                  'Ga' : setYesNo(world.tradeGa),
                                  'Hi' : setYesNo(world.tradeHi),
                                  'Ht' : setYesNo(world.tradeHt),
                                  'IC' : setYesNo(world.tradeIC),
                                  'In' : setYesNo(world.tradeIn),
                                  'Lo' : setYesNo(world.tradeLo),
                                  'Lt' : setYesNo(world.tradeLt),
                                  'Na' : setYesNo(world.tradeNa),
                                  'NI' : setYesNo(world.tradeNI),
                                  'Po' : setYesNo(world.tradePo),
                                  'Ri' : setYesNo(world.tradeRi),
                                  'Va' : setYesNo(world.tradeVa),
                                  'Wa' : setYesNo(world.tradeWa)
                                  })
        except IOError,  e:
            exception = e
        finally:
            f.close()

        # Save custom user text
        for world in self.worlds:
            if world.dirty:
                world.dirty = False
                if world.starport.userTextChanged:
                    world.starport.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Starport.txt',
                                       world.starport.userText)
                if world.size.userTextChanged:
                    world.size.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Size.txt',
                                       world.size.userText)
                if world.atmosphere.userTextChanged:
                    world.atmosphere.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Atmosphere.txt',
                                       world.atmosphere.userText)
                if world.hydrographics.userTextChanged:
                    world.hydrographics.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Hydrographics.txt',
                                       world.hydrographics.userText)
                if world.population.userTextChanged:
                    world.population.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Population.txt',
                                       world.population.userText)
                if world.government.userTextChanged:
                    world.government.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Government.txt',
                                       world.government.userText)
                if world.lawLevel.userTextChanged:
                    world.lawLevel.userTextChanged = False
                    self.storeTextData(world.name,
                                       'LawLevel.txt',
                                       world.lawLevel.userText)
                if world.techLevel.userTextChanged:
                    world.techLevel.userTextChanged = False
                    self.storeTextData(world.name,
                                       'TechLevel.txt',
                                       world.techLevel.userText)
                if world.temperature.userTextChanged:
                    world.temperature.userTextChanged = False
                    self.storeTextData(world.name,
                                       'Temperature.txt',
                                       world.temperature.userText)

        # Save Sector Data
        exception = None
        f = open(self.sectors_file, "wb")
        try:
            writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow( ('Sector Name',  'Column',  'Row') )
            for sector in self.sectors:
                writer.writerow( (sector.name,
                                  sector.sectorCol,
                                  sector.sectorRow) )
        except IOError,  e:
            exception = e
        finally:
            f.close()

        # Save Subsector Data
        exception = None
        f = open(self.subsectors_file, "wb")
        try:
            writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow( ('Subsector Name',  'Column',  'Row') )
            for subsector in self.subsectors:
                writer.writerow( (subsector.name,
                                  subsector.subsectorCol,
                                  subsector.subsectorRow) )
        except IOError,  e:
            exception = e
        finally:
            f.close()

        # Save Cell Group data
        group_filename = os.path.join(self.project_path, 'HexGroupData.dat')
        with open(group_filename, "wb") as group_file:
            pickle.dump(self.groupNames, group_file, 2)
            pickle.dump(self.groupCells, group_file, 2)

        # Save Config Data
        self.config.set('Overrides', 'allegiancecodes',
                        ','.join(Traveller.allegiance_codes))
        self.config.set('Overrides', 'allegiancenames',
                        ','.join(Traveller.allegiance_names))
        self.config.set('Overrides', 'allegiancecolors',
                        ','.join(Traveller.allegiance_colors))
        self.config.set('Overrides', 'worldgeneratorname', self.currentWorldGeneratorName)
        self.config.write(open(self.config_file, "w"))
        

# Still under development

    def importSEC(self, import_file, sec_col, sec_row):
        #Assumes the sector has been blanked already

        base_col = sec_col * 32
        base_row = sec_row * 40

        sub_map = {'A' : (0, 0),
                   'B' : (1, 0),
                   'C' : (2, 0),
                   'D' : (3, 0),
                   'E' : (0, 1),
                   'F' : (1, 1),
                   'G' : (2, 1),
                   'H' : (3, 1),
                   'I' : (0, 2),
                   'J' : (1, 2),
                   'K' : (2, 2),
                   'L' : (3, 2),
                   'M' : (0, 3),
                   'N' : (1, 3),
                   'O' : (2, 3),
                   'P' : (3, 3)}

        # 0:Navy, 1:Scout
        base_codes = {'A' : (True, True),
                      'N' : (True, False),
                      'S' : (False, True)}

        travel_zone_lookup = {'A' : 'Amber',
                              'R' : 'Red',
                              ' ' : 'Green'}
        
        with open(import_file, "r") as secfile:
            all_lines = secfile.readlines()
            
            #Discard first two lines of the file
            for line in all_lines[2:]:
                debug_log(line)
                if len(line) < 3:
                    debug_log('Short line')
                
                elif line[0] == '#' and line[2] == ':':
                    #Set subsector name
                    if line[1] in sub_map:
                        col_offset, row_offset = sub_map[line[1]]
                        sub_name = line[4:]
                        sub_col = (sec_col * 4) + col_offset
                        sub_row = (sec_row * 4) + row_offset
                        debug_log('Setting subsector name: ' + sub_name)
                        debug_log(' subsector column: ' + str(sub_col))
                        debug_log(' subsector row:    ' + str(sub_row))
                        self.subsectors.append(Traveller.Subsector(
                            sub_name, sub_col, sub_row))
                    else:
                        debug_log('Sector import error, bad subsector: ' + line)

                elif line[0] == '+' and line[3] == ' ':
                    #Add allegiance config, if not already present
                    new_code = line[1:3]
                    new_name = line[4:]
                    if new_code not in Traveller.allegiance_codes:
                        debug_log('New allegiance: '
                                  + new_code + ' '
                                  + new_name)
                        Traveller.allegiance_codes.append(new_code)
                        Traveller.allegiance_names.append(new_name)
                        Traveller.allegiance_colors.append('#CCCCCC')

                elif line[0] not in ('#', '+'):
                    debug_log('Parsing world data line:')
                    debug_log(line)
                    
                    world_name = line[0:18].rstrip()
                    column = base_col + int(line[19:21]) - 1
                    row = base_row + int(line[21:23]) - 1
                    trade_list = (line[36:38], line[39:41], line[42:44],
                                  line[45:47], line[48:50])
                    hasNavy, hasScout = False, False
                    if line[34] in base_codes:
                        hasNavy, hasScout = base_codes[line[34]]
                    hasResearch = 'Rs' in trade_list
                    travel_zone = travel_zone_lookup[line[52]]
                    pop_multiplier = int(line[54])
                    num_belts = int(line[55])
                    num_gas_giants = int(line[56])
                    if num_gas_giants > 0:
                        hasGasGiant = True
                    else:
                        hasGasGiant = False
                    allegiance_code = line[58:60]

                    world = Traveller.World(
                        name=world_name,
                        x=column,
                        y=row,
                        port=line[24],
                        size=line[25],
                        atmosphere=line[26],
                        hydrographics=line[27],
                        population=line[28],
                        government=line[29],
                        law_level=line[30],
                        tech_level=line[32],
                        gas=hasGasGiant,
                        travel_code=travel_zone,
                        navy=hasNavy,
                        scout=hasScout,
                        research=hasResearch,
                        tas=False,
                        consulate=False,
                        pirate=False,
                        allegiance=allegiance_code,
                        port_txt='',
                        size_txt='',
                        atmo_txt='',
                        hydro_txt='',
                        pop_txt='',
                        gov_txt='',
                        law_txt='',
                        tech_txt='',
                        hydro_pc=None,
                        Ag='Ag' in trade_list,
                        As='As' in trade_list,
                        Ba='Ba' in trade_list,
                        De='De' in trade_list,
                        Fl='Fl' in trade_list,
                        Ga='Ga' in trade_list,
                        Hi='Hi' in trade_list,
                        Ht='Ht' in trade_list,
                        IC='IC' in trade_list,
                        In='In' in trade_list,
                        Lo='Lo' in trade_list,
                        Lt='Lt' in trade_list,
                        Na='Na' in trade_list,
                        NI='NI' in trade_list,
                        Po='Po' in trade_list,
                        Ri='Ri' in trade_list,
                        Va='Va' in trade_list,
                        Wa='Wa' in trade_list)

                    new_row = len(self.worlds)
                    self.beginInsertRows(QModelIndex(), new_row, new_row)
                    self.worlds.append(world)
                    self.endInsertRows()
                    debug_log(self.getUWP(len(self.worlds) - 1))
        self.dirty = True

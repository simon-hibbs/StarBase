import os
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

import sys
import math
from PySide.QtCore import *
from PySide.QtGui import *
from model import Models
#import MapGlyphs
#import MapScene
from reports import WorldReport
from resources import starmap_rc
from log import *
from model import Traveller

# Set up modes

MAPPER_MODE = QDataWidgetMapper.AutoSubmit

SINGLE_WORLD = 0
MULTI_WORLD = 1

RANDOM_ROLL = 0
MANUAL_SELECT = 1

"""
The World Generator can operate in a variety of modes.
- If it is called and no hex is selected, it operates in manual mode only.
  All world detals, including hex co-ordinates, must be entered manualy.
- When called with a single hex selected, it may operate in manual or
  random world generation modes to populate that hex with a world.
- When called with more than one hex selected it will ony operate in
  random generation mode to populate the hexes with worlds. There is a
  selectable die roll target to determine if each hex is populated. Set
  a target of 1+ to populate every hex.
"""


class StarportDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(StarportDetails, self).__init__(parent)
        #self.setTitle('Starport Details')
        self.pmi = pmi

        self.berthingCostSpinBox = Traveller.BerthingCostSpinBox()
        self.hasRefined = QCheckBox('Refined Fuel')
        self.hasUnrefined = QCheckBox('Unrefined fuel')
        self.hasStarshipYard = QCheckBox('Starship yard')
        self.hasSpacecraftYard = QCheckBox('Spacecraft yard')
        self.hasSmallCraftYard = QCheckBox('Small craft yard')
        self.hasFullRepair = QCheckBox('Full repair')
        self.hasLimitedRepair = QCheckBox('Limited repair')
##        self.hasNavyBase = QCheckBox('Navy base')
##        self.hasScoutBase = QCheckBox('Scout base')
##        self.hasResearchBase = QCheckBox('Research base')
##        self.hasTas = QCheckBox('TAS lodge')
##        self.hasConsulate = QCheckBox('Consulate')
##        self.hasPirateBase = QCheckBox('Pirate base')

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.berthingCostSpinBox, Models.BERTHING_COST)
        self.mapper.addMapping(self.hasRefined, Models.REFINED_FUEL)
        self.mapper.addMapping(self.hasUnrefined, Models.UNREFINED_FUEL)
        self.mapper.addMapping(self.hasStarshipYard, Models.STARSHIP_YARD)
        self.mapper.addMapping(self.hasSpacecraftYard, Models.SPACECRAFT_YARD)
        self.mapper.addMapping(self.hasSmallCraftYard, Models.SMALL_CRAFT_YARD)
        self.mapper.addMapping(self.hasFullRepair, Models.FULL_REPAIR)
        self.mapper.addMapping(self.hasLimitedRepair, Models.LIMITED_REPAIR)
##        self.mapper.addMapping(self.hasNavyBase, Models.NAVY_BASE)
##        self.mapper.addMapping(self.hasScoutBase, Models.SCOUT_BASE)
##        self.mapper.addMapping(self.hasResearchBase, Models.RESEARCH_BASE)
##        self.mapper.addMapping(self.hasTas, Models.TAS)
##        self.mapper.addMapping(self.hasConsulate, Models.CONSULATE)
##        self.mapper.addMapping(self.hasPirateBase, Models.PIRATE_BASE)

        self.starportGrid = QGridLayout()
        self.starportGrid.addWidget(QLabel('Berthing Cost Cr:'),0,0, Qt.AlignLeft)
        self.starportGrid.addWidget(self.berthingCostSpinBox,0,1, Qt.AlignLeft)
        
        self.starportGrid.addWidget(self.hasRefined,1,0, Qt.AlignLeft)
        self.starportGrid.addWidget(self.hasUnrefined,1,1, Qt.AlignLeft)

        self.starportGrid.addWidget(self.hasStarshipYard,2,0, Qt.AlignLeft)
        self.starportGrid.addWidget(self.hasSpacecraftYard,2,1, Qt.AlignLeft)

        self.starportGrid.addWidget(self.hasSmallCraftYard,3,0,1,2, Qt.AlignLeft)

        self.starportGrid.addWidget(self.hasFullRepair,4,0, Qt.AlignLeft)
        self.starportGrid.addWidget(self.hasLimitedRepair,4,1, Qt.AlignLeft)

##        self.starportGrid.addWidget(self.hasNavyBase,5,0, Qt.AlignLeft)
##        self.starportGrid.addWidget(self.hasScoutBase,5,1, Qt.AlignLeft)
##
##        self.starportGrid.addWidget(self.hasResearchBase,6,0, Qt.AlignLeft)
##        self.starportGrid.addWidget(self.hasTas,6,1, Qt.AlignLeft)
##
##        self.starportGrid.addWidget(self.hasConsulate,7,0, Qt.AlignLeft)
##        self.starportGrid.addWidget(self.hasPirateBase,7,1, Qt.AlignLeft)
        self.starportGrid.addItem(QSpacerItem(5,5, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.starportGrid)
        self.mapper.setCurrentIndex(self.pmi.row())


class SizeDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(SizeDetails, self).__init__(parent)
        #self.setTitle('Size Details')
        self.pmi = pmi

        self.diameterField = Traveller.DiameterSpinBox()
        self.gravityField = Traveller.GravityLineEdit()
        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)
        
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.diameterField, Models.DIAMETER)
        self.mapper.addMapping(self.gravityField, Models.GRAVITY)
        self.mapper.addMapping(self.descriptionField, Models.SIZE_TEXT)

        self.sizeGrid = QGridLayout()
        self.sizeGrid.addWidget(QLabel('Diameter:'),0,0,Qt.AlignLeft)
        self.sizeGrid.addWidget(self.diameterField,0,1,Qt.AlignLeft)

        self.sizeGrid.addWidget(QLabel('Gravity:'),1,0,1,1, Qt.AlignLeft)
        self.sizeGrid.addWidget(self.gravityField,1,1,1,1, Qt.AlignLeft)

        self.sizeGrid.addWidget(QLabel('Description:'),2,0,1,1,Qt.AlignTop)
        self.sizeGrid.addWidget(self.descriptionField,2,1,2,3)

        self.setLayout(self.sizeGrid)
        self.mapper.setCurrentIndex(self.pmi.row())


class AtmosphereDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(AtmosphereDetails, self).__init__(parent)
        #self.setTitle('Atmosphere Details')
        self.pmi = pmi

        self.pressureField = Traveller.PressureLineEdit()
        self.requiresVaccSuit = QCheckBox('Requires vacc. suit')
        self.requiresRespirator = QCheckBox('Requires respirator')
        self.requiresFilter = QCheckBox('Requires air filter')
        self.requiresAirSupply = QCheckBox('Requires air supply')
        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)
        
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.pressureField, Models.PRESSURE)
        self.mapper.addMapping(self.requiresVaccSuit, Models.REQ_VACC)
        self.mapper.addMapping(self.requiresRespirator, Models.REQ_RESPIRATOR)
        self.mapper.addMapping(self.requiresFilter, Models.REQ_FILTER)
        self.mapper.addMapping(self.requiresAirSupply, Models.REQ_AIR)
        self.mapper.addMapping(self.descriptionField, Models.ATMOSPHERE_TEXT)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(QLabel('Surface Pressure:'),0,0, Qt.AlignLeft)
        self.gridLayout.addWidget(self.pressureField,0,1, Qt.AlignLeft)

        self.gridLayout.addWidget(self.requiresVaccSuit,1,0,1,1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.requiresFilter,1,1,1,1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.requiresRespirator,2,0,1,1, Qt.AlignLeft)
        self.gridLayout.addWidget(self.requiresAirSupply,2,1,1,1, Qt.AlignLeft)
        self.gridLayout.addWidget(QLabel('Atmosphere Type:'),3,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,3,1,2,3)
        #self.gridLayout.addItem(QSpacerItem(5,5, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class HydrographicsDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(HydrographicsDetails, self).__init__(parent)
        #self.setTitle('Hydrographics Details')
        self.pmi = pmi

        self.percentageField = Traveller.NumberText()
        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.percentageField, Models.WATER_PERCENT)
        self.mapper.addMapping(self.descriptionField, Models.WATER_TEXT)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(QLabel('Water Coverage:'),0,0,Qt.AlignLeft)
        self.gridLayout.addWidget(self.percentageField,0,1,1,1,Qt.AlignLeft)

        self.gridLayout.addWidget(QLabel('Geography:'),1,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,1,1,1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class PopulationDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(PopulationDetails, self).__init__(parent)
        #self.setTitle('Population Details')
        self.pmi = pmi

        self.populationField = Traveller.LongNumberText()
        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.populationField, Models.INHABITANTS)
        self.mapper.addMapping(self.descriptionField, Models.POPULATION_TEXT)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(QLabel('Inhabitants:'),0,0,Qt.AlignLeft)
        self.gridLayout.addWidget(self.populationField,0,1,1,1,Qt.AlignLeft)

        self.gridLayout.addWidget(QLabel('Settlements:'),1,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,1,1,1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class GovernmentDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(GovernmentDetails, self).__init__(parent)
        #self.setTitle('Government Details')
        self.pmi = pmi

        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)
        self.addFactionsButton = QPushButton('Add Factions')

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.descriptionField, Models.GOVERNMENT_TEXT)

        self.gridLayout = QGridLayout()

        self.gridLayout.addWidget(QLabel('Government:'),0,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.addFactionsButton,1,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,0,1,-1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())
        self.addFactionsButton.clicked.connect(self.addFactions)

    def addFactions(self):
        self.pmi.model().addFactions(self.pmi)


class LawLevelDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(LawLevelDetails, self).__init__(parent)
        #self.setTitle('Law Level Details')
        self.pmi = pmi

        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.descriptionField, Models.LAW_LEVEL_TEXT)

        self.gridLayout = QGridLayout()

        self.gridLayout.addWidget(QLabel('Restrictions:'),0,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,0,1,1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class TechLevelDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(TechLevelDetails, self).__init__(parent)
        #self.setTitle('Tech. Level Details')
        self.pmi = pmi

        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.descriptionField, Models.TECH_LEVEL_TEXT)

        self.gridLayout = QGridLayout()

        self.gridLayout.addWidget(QLabel('Achievements:'),0,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,0,1,1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class TemperatureDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(TemperatureDetails, self).__init__(parent)
        #self.setTitle('Temperature Details')
        self.pmi = pmi

        self.descriptionField = Traveller.DescriptionText()
        self.descriptionField.setReadOnly(False)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.descriptionField, Models.TEMPERATURE_TEXT)

        self.gridLayout = QGridLayout()

        self.gridLayout.addWidget(QLabel('Description:'),0,0,1,1,Qt.AlignTop)
        self.gridLayout.addWidget(self.descriptionField,0,1,1,3)

        self.setLayout(self.gridLayout)
        self.mapper.setCurrentIndex(self.pmi.row())


class TradeDetails(QGroupBox):
    def __init__(self, pmi, parent=None):
        super(TradeDetails, self).__init__(parent)
        #self.setTitle('Trade Details')
        self.pmi = pmi

        self.tradeAg = QCheckBox('Agricultural')
        self.tradeAs = QCheckBox('Asteroid')
        self.tradeBa = QCheckBox('Barren')
        self.tradeDe = QCheckBox('Desert')
        self.tradeFl = QCheckBox('Fluid Ocean')
        self.tradeGa = QCheckBox('Garden')
        self.tradeHi = QCheckBox('High Pop.')
        self.tradeHt = QCheckBox('High Tech.')
        self.tradeIC = QCheckBox('Ice Capped')
        self.tradeIn = QCheckBox('Industrial')
        self.tradeLo = QCheckBox('Low Pop.')
        self.tradeLt = QCheckBox('Low Tech.')
        self.tradeNa = QCheckBox('Non-Agricultural')
        self.tradeNI = QCheckBox('Non-Industrial')
        self.tradePo = QCheckBox('Poor')
        self.tradeRi = QCheckBox('Rich')
        self.tradeVa = QCheckBox('Vacuum')
        self.tradeWa = QCheckBox('Water World')

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.tradeAg, Models.AGRICULTURAL)
        self.mapper.addMapping(self.tradeAs, Models.ASTEROID)
        self.mapper.addMapping(self.tradeBa, Models.BARREN)
        self.mapper.addMapping(self.tradeDe, Models.DESERT)
        self.mapper.addMapping(self.tradeFl, Models.FLUID_OCEAN)
        self.mapper.addMapping(self.tradeGa, Models.GARDEN)
        self.mapper.addMapping(self.tradeHi, Models.HIGH_POP)
        self.mapper.addMapping(self.tradeHt, Models.HIGH_TECH)
        self.mapper.addMapping(self.tradeIC, Models.ICE_CAPPED)
        self.mapper.addMapping(self.tradeIn, Models.INDUSTRIAL)
        self.mapper.addMapping(self.tradeLo, Models.LOW_POP)
        self.mapper.addMapping(self.tradeLt, Models.LOW_TECH)
        self.mapper.addMapping(self.tradeNa, Models.NON_AGRICULTURAL)
        self.mapper.addMapping(self.tradeNI, Models.NON_INDUSTRIAL)
        self.mapper.addMapping(self.tradePo, Models.POOR)
        self.mapper.addMapping(self.tradeRi, Models.RICH)
        self.mapper.addMapping(self.tradeVa, Models.VACUUM)
        self.mapper.addMapping(self.tradeWa, Models.WATER_WORLD)

        self.tradeGrid = QGridLayout()
        self.tradeGrid.addWidget(self.tradeAg,0,0, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeHi,0,1, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeHt,0,2, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeRi,0,3, Qt.AlignLeft)
        
        self.tradeGrid.addWidget(self.tradeNa,1,0, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeLo,1,1, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeLt,1,2, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradePo,1,3, Qt.AlignLeft)

        self.tradeGrid.addWidget(self.tradeIn,2,0, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeWa,2,1, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeGa,2,2, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeAs,2,3, Qt.AlignLeft)

        self.tradeGrid.addWidget(self.tradeNI,3,0, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeDe,3,1, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeBa,3,2, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeVa,3,3, Qt.AlignLeft)

        self.tradeGrid.addWidget(self.tradeFl,4,0, Qt.AlignLeft)
        self.tradeGrid.addWidget(self.tradeIC,4,1, Qt.AlignLeft)

        self.tradeGrid.addItem(QSpacerItem(5,5,
                                           QSizePolicy.Minimum,
                                           QSizePolicy.Expanding),
                               5,0,4,4)

        self.setLayout(self.tradeGrid)
        self.mapper.setCurrentIndex(self.pmi.row())



class WorldDataFrame(QFrame):
    def __init__(self, pmi, parent=None, moveable=False):
        super(WorldDataFrame, self).__init__(parent)
        self.pmi = pmi
        #self.setFrameShape(QFrame.StyledPanel)

        self.nameLineEdit = Traveller.WorldNameLineEdit()
        #self.nameLineEdit.setReadOnly(True)
        
        if moveable:
            self.columnSpinBox = Traveller.ColumnSpinBox()
            self.rowSpinBox = Traveller.RowSpinBox()

        else:
            self.sectorCoords = Traveller.SectorCoords()
            self.sectorCoords.setDisabled(True)
        
        self.allegianceComboBox = Traveller.AllegianceNameComboBox()
        self.starportComboBox = Traveller.StarportComboBox()
        self.sizeComboBox = Traveller.SizeComboBox()
        self.atmosphereComboBox = Traveller.AtmosphereComboBox()
        self.hydrographicsComboBox = Traveller.HydrographicsComboBox()
        self.populationComboBox = Traveller.PopulationComboBox()
        self.governmentComboBox = Traveller.GovernmentComboBox()
        self.lawLevelComboBox = Traveller.LawLevelComboBox()
        self.techLevelComboBox = Traveller.TechLevelComboBox()
        self.temperatureComboBox = Traveller.TemperatureComboBox()

        self.owningSector = Traveller.OwningSector()
        self.owningSector.setDisabled(True)
        self.owningSubsector = Traveller.OwningSubsector()
        self.owningSubsector.setDisabled(True)
        self.travelCodeComboBox = Traveller.TravelCodeComboBox()
        self.hasGasGiant = QCheckBox('Gas Giant')

        self.hasNavyBase = QCheckBox('Navy base')
        self.hasScoutBase = QCheckBox('Scout base')
        self.hasResearchBase = QCheckBox('Research base')
        self.hasTas = QCheckBox('TAS lodge')
        self.hasConsulate = QCheckBox('Consulate')
        self.hasPirateBase = QCheckBox('Pirate base')

        
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.pmi.model())
        self.mapper.setSubmitPolicy(MAPPER_MODE)
        self.mapper.addMapping(self.nameLineEdit, Models.NAME)

##        self.changeNameButton = QToolButton()
##        self.changeNameButton.setArrowType(Qt.LeftArrow)
##        self.changeNameButton.setCheckable(True)
        
        if moveable:
            self.mapper.addMapping(self.columnSpinBox, Models.COL)
            self.mapper.addMapping(self.rowSpinBox, Models.ROW)
        else:
            self.mapper.addMapping(self.sectorCoords, Models.SECTOR_COORDS)

        self.mapper.addMapping(self.allegianceComboBox, Models.ALLEGIANCE_NAME,
                               "currentIndex")
        
        self.mapper.addMapping(self.starportComboBox, Models.STARPORT,
                               "currentIndex")
        self.mapper.addMapping(self.sizeComboBox, Models.SIZE,
                               "currentIndex")
        self.mapper.addMapping(self.atmosphereComboBox, Models.ATMOSPHERE,
                               "currentIndex")
        self.mapper.addMapping(self.hydrographicsComboBox, Models.HYDROGRAPHICS,
                               "currentIndex")
        self.mapper.addMapping(self.populationComboBox, Models.POPULATION,
                               "currentIndex")
        self.mapper.addMapping(self.governmentComboBox, Models.GOVERNMENT,
                               "currentIndex")
        self.mapper.addMapping(self.lawLevelComboBox, Models.LAW_LEVEL,
                               "currentIndex")
        self.mapper.addMapping(self.techLevelComboBox, Models.TECH_LEVEL,
                               "currentIndex")
        self.mapper.addMapping(self.temperatureComboBox, Models.TEMPERATURE,
                               "currentIndex")

        self.mapper.addMapping(self.owningSector, Models.OWNING_SECTOR)
        self.mapper.addMapping(self.owningSubsector, Models.OWNING_SUBSECTOR)
        self.mapper.addMapping(self.travelCodeComboBox, Models.TRAVEL_CODE,
                               "currentIndex")
        self.mapper.addMapping(self.hasGasGiant, Models.GAS_GIANT)

        self.mapper.addMapping(self.hasNavyBase, Models.NAVY_BASE)
        self.mapper.addMapping(self.hasScoutBase, Models.SCOUT_BASE)
        self.mapper.addMapping(self.hasResearchBase, Models.RESEARCH_BASE)
        self.mapper.addMapping(self.hasTas, Models.TAS)
        self.mapper.addMapping(self.hasConsulate, Models.CONSULATE)
        self.mapper.addMapping(self.hasPirateBase, Models.PIRATE_BASE)

        # Widget Layout
        self.worldGrid = QGridLayout()
        self.worldGrid.addWidget(QLabel('World Name:'),0,0)
        self.worldGrid.addWidget(self.nameLineEdit,0,1)
        self.worldGrid.addWidget(QLabel('Sector:'),0,2)
        self.worldGrid.addWidget(self.owningSector,0,3)
        self.worldGrid.addWidget(self.hasNavyBase,0,4)
        self.worldGrid.addWidget(self.hasScoutBase,0,5)
        
        self.worldGrid.addWidget(QLabel('Sector Hex:'),1,0)
        self.miniHBoxLayout = QHBoxLayout()
        self.miniHBoxLayout.addWidget(self.sectorCoords)
        self.miniHBoxLayout.addWidget(self.hasGasGiant)
        self.worldGrid.addLayout(self.miniHBoxLayout,1,1)
        self.worldGrid.addWidget(QLabel('Subsector:'),1,2)
        self.worldGrid.addWidget(self.owningSubsector,1,3)
        self.worldGrid.addWidget(self.hasResearchBase,1,4)
        self.worldGrid.addWidget(self.hasTas,1,5)
        
        self.worldGrid.addWidget(QLabel('Allegiance:'),2,0)
        self.worldGrid.addWidget(self.allegianceComboBox,2,1)
        self.worldGrid.addWidget(QLabel('Travel Code:'),2,2,Qt.AlignLeft)
        self.worldGrid.addWidget(self.travelCodeComboBox,2,3, Qt.AlignLeft)
        self.worldGrid.addWidget(self.hasConsulate,2,4)
        self.worldGrid.addWidget(self.hasPirateBase,2,5)
        
        self.worldGrid.addWidget(QLabel('Starport Type:'),3,0)
        self.worldGrid.addWidget(self.starportComboBox,3,1)

        self.worldGrid.addWidget(QLabel('Size:'),4,0)
        self.worldGrid.addWidget(self.sizeComboBox,4,1)

        self.worldGrid.addWidget(QLabel('Atmosphere:'),5,0)
        self.worldGrid.addWidget(self.atmosphereComboBox,5,1)

        self.worldGrid.addWidget(QLabel('Hydrographics:'),6,0)
        self.worldGrid.addWidget(self.hydrographicsComboBox,6,1)

        self.worldGrid.addWidget(QLabel('Population:'),7,0)
        self.worldGrid.addWidget(self.populationComboBox,7,1)

        self.worldGrid.addWidget(QLabel('Government:'),8,0)
        self.worldGrid.addWidget(self.governmentComboBox,8,1)

        self.worldGrid.addWidget(QLabel('Law Level:'),9,0)
        self.worldGrid.addWidget(self.lawLevelComboBox,9,1)

        self.worldGrid.addWidget(QLabel('Tech Level:'),10,0)
        self.worldGrid.addWidget(self.techLevelComboBox,10,1)

        self.worldGrid.addWidget(QLabel('Temperature:'),11,0)
        self.worldGrid.addWidget(self.temperatureComboBox,11,1)

        self.worldGrid.setColumnStretch(3,1)
        self.worldGrid.setColumnStretch(4,2)

        self.detailsTabWidget = QTabWidget()
        self.detailsTabWidget.setUsesScrollButtons(False)
        self.detailsTabWidget.addTab(StarportDetails(self.pmi), 'Port')
        self.detailsTabWidget.addTab(SizeDetails(self.pmi), 'Siz')
        self.detailsTabWidget.addTab(AtmosphereDetails(self.pmi), 'Atm')
        self.detailsTabWidget.addTab(HydrographicsDetails(self.pmi), 'Hyd')
        self.detailsTabWidget.addTab(PopulationDetails(self.pmi),'Pop')
        self.detailsTabWidget.addTab(GovernmentDetails(self.pmi),'Gov')
        self.detailsTabWidget.addTab(LawLevelDetails(self.pmi),'Law')
        self.detailsTabWidget.addTab(TechLevelDetails(self.pmi),'Tech')
        self.detailsTabWidget.addTab(TemperatureDetails(self.pmi),'Temp')
        self.detailsTabWidget.addTab(TradeDetails(self.pmi),'Trade')
        self.worldGrid.addWidget(self.detailsTabWidget,3,2,-1,-1, Qt.AlignLeft)

        self.setLayout(self.worldGrid)

        debug_log('WorldDataForm: Row is ' + str(self.pmi.row()))
        self.mapper.setCurrentIndex(self.pmi.row())

##        self.connect(self.changeNameButton, SIGNAL("clicked()"),
##                     self.changeName)


##    def changeName(self):
##        new_name, ok = QInputDialog.getText(self, 'New World Name',
##                                         'World Name:', QLineEdit.Normal)
##        model = self.pmi.model()
##        if model.hasNamedWorld(new_name):
##            msgbx = QMessageBox()
##            msgbx.setText('A world with that name already exists')
##            msgbx.exec_()
##        else:
##            name_index = model.index(self.pmi.row(),  Models.NAME)
##            model.setData(name_index, QVariant(new_name), Qt.EditRole)


    def setStarportDetails(self):
        self.detailsStack.setCurrentIndex(0)

    def setSizeDetails(self):
        self.detailsStack.setCurrentIndex(1)

    def setAtmosphereDetails(self):
        self.detailsStack.setCurrentIndex(2)

    def setHydrographicsDetails(self):
        self.detailsStack.setCurrentIndex(3)

    def setPopulationDetails(self):
        self.detailsStack.setCurrentIndex(4)

    def setGovernmentDetails(self):
        self.detailsStack.setCurrentIndex(5)

    def setLawLevelDetails(self):
        self.detailsStack.setCurrentIndex(6)

    def setTechLevelDetails(self):
        self.detailsStack.setCurrentIndex(7)

    def setTemperatureDetails(self):
        self.detailsStack.setCurrentIndex(8)
    
    def resetMappedRow(self,  new_pmi):
        self.pmi = new_pmi
        self.mapper.setModel(self.pmi.model())
        self.mapper.setCurrentIndex(self.pmi.row())


class EditWorldDialog(QDialog):
    def __init__(self, pmi, parent=None):
        super(EditWorldDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Edit World')
        self.pmi = pmi

        self.worldDataFrame = WorldDataFrame(pmi)
        
        self.okButton = QPushButton("OK")
        self.applyButton = QPushButton("Apply")
        self.randomRollButton = QPushButton("Random Roll")
        self.reportButton = QPushButton("View Report")
        self.deleteWorldButton = QPushButton("Delete World")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.reportButton)
        buttonLayout.addWidget(self.randomRollButton)
        buttonLayout.addWidget(self.deleteWorldButton)
        buttonLayout.addStretch()

        masterLayout = QVBoxLayout()
        masterLayout.addWidget(self.worldDataFrame)
        masterLayout.addLayout(buttonLayout)
        self.setLayout(masterLayout)

##        self.connect(okButton, SIGNAL("clicked()"),
##                     self.okButtonClicked)
##        self.connect(applyButton, SIGNAL("clicked()"),
##                     self.applyButtonClicked)
##        self.connect(reportButton, SIGNAL("clicked()"),
##                     self.reportButtonClicked)
##        self.connect(randomRollButton, SIGNAL("clicked()"),
##                     self.randomRollButtonClicked)
##        self.connect(deleteWorldButton, SIGNAL("clicked()"),
##                     self.deleteWorldButtonClicked)

        self.okButton.clicked.connect(self.okButtonClicked)
        self.applyButton.clicked.connect(self.applyButtonClicked)
        self.reportButton.clicked.connect(self.reportButtonClicked)
        self.randomRollButton.clicked.connect(self.randomRollButtonClicked)
        self.deleteWorldButton.clicked.connect(self.deleteWorldButtonClicked)
        

    def okButtonClicked(self):
        self.close()

    def applyButtonClicked(self):
        self.worldDataFrame.mapper.submit()

    def reportButtonClicked(self):
        self.reportDialog = WorldReport.WorldReportDialog(self.pmi, self)
        self.reportDialog.show()
        self.reportDialog.raise_()
        self.reportDialog.activateWindow()

    def deleteWorldButtonClicked(self):
        self.pmi.model().removeRow(self.pmi.row())
        self.close()

    def randomRollButtonClicked(self):
        self.pmi.model().regenerateWorld(self.pmi.row())


# Deprecated
class AddWorldDialog(QDialog):
    def __init__(self, world_model, x, y, parent=None):
        super(AddWorldDialog, self).__init__(parent)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Add World")
        self.model = world_model

        self.model.currentCell = (x, y)
        self.model.insertRow(self.model.rowCount())
        
##        col_index = self.model.index((self.model.rowCount() - 1), Models.COL)
##        row_index = self.model.index((self.model.rowCount() - 1), Models.ROW)
##
##        #print 'Col ', x, 'Row ', y
##        self.model.setData(col_index, QVariant(x))
##        self.model.setData(row_index, QVariant(y))
        self.ref_index = self.model.index((self.model.rowCount() - 1), Models.NAME)
        self.ref_index = QPersistentModelIndex(self.ref_index)
        
        self.worldDataFrame = WorldDataFrame(self.ref_index)
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        randomRollButton = QPushButton("Random Roll")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(randomRollButton)
        buttonLayout.addStretch()

        masterLayout = QVBoxLayout()
        masterLayout.addWidget(self.worldDataFrame)
        masterLayout.addLayout(buttonLayout)
        self.setLayout(masterLayout)

##        self.connect(okButton, SIGNAL("clicked()"),
##                     self.okButtonClicked)
##        self.connect(cancelButton, SIGNAL("clicked()"),
##                     self.cancelButtonClicked)
##        self.connect(randomRollButton, SIGNAL("clicked()"),
##                     self.randomRollButtonClicked)

        self.okButton.cliecked.connect(self.okButtonClicked)
        self.cancelButton.cliecked.connect(self.cancelButtonClicked)
        self.randomRollButton.cliecked.connect(self.randomRollButtonClicked)

        self.show()
        
    def okButtonClicked(self, result=1):
        QDialog.done(self, result)

    def cancelButtonClicked(self, result=0):
        self.model.removeRow(self.ref_index.row())
        QDialog.done(self, result)

    def randomRollButtonClicked(self):
        self.model.regenerateWorld(self.ref_index.row())
##        old_index = self.ref_index
##        old_col = self.worldDataFrame.columnSpinBox.value()
##        old_row = self.worldDataFrame.rowSpinBox.value()
##        print old_col,  old_row
##        
##        print 'old index row',  self.ref_index.row()
##        self.model.insertRandomWorld(self.ref_index.row())
##        print 'old index new row',  self.ref_index.row()
##        self.ref_index = self.model.index((self.ref_index.row() - 1), Models.NAME)
##        print 'new ref index row',  self.ref_index.row()
##        self.ref_index = QPersistentModelIndex(self.ref_index)
##        self.worldDataFrame.resetMappedRow(self.ref_index)
##        
##        self.model.removeRow(old_index.row())
##        
##        col_index = self.model.index(self.ref_index.row(), Models.COL)
##        row_index = self.model.index(self.ref_index.row(), Models.ROW)
##
##        self.model.setData(col_index, QVariant(old_col))
##        self.model.setData(row_index, QVariant(old_row))        




# Deprecated?

class GenerateWorldsDialog(QDialog):

    def __init__(self, world_model, scene, parent=None):
        super(GenerateWorldsDialog, self).__init__(parent)

        info_log("Initialising AddWorldDialog")
        self.world_model = world_model
        self.scene = scene

        self.target_number_to_populate_hex = 3

        self.selected_items = self.scene.selectedItems()
        # Purge non-hex items?
        # Also, need to support generating subsectors and sectors.
        # Hexes only for now.
        if len(self.selected_items) <= 1:
            self.manual_mode_enabled = True
        elif len(self.selected_items) > 1:
            self.manual_mode_enabled = False

        if len(self.selected_items) > 0:
            self.random_roll_enabled = True
        else:
            self.random_roll_enabled = False

        self.totalSelectedHexes = QLabel("0")
        selectedHexesLabel = QLabel("Selected hexes:")
        selectedHexesLabel.setBudy(self.totalSelectedHexes)

        self.targetNumberSpinBox = QSpinBox()
        self.targetNumberSpinBox.setSuffix("+")
        self.targetNumberSpinBox.setMinimum(0)
        self.targetNumberSpinBox.setMaximum(6)
        self.targetNumberSpinBox.setValue(self.target_number_to_populate_hex)
        targetNumberlabel = QLabel("Each hex &populated on:")
        targetNumberlabel.setBuddy(self.targetNumberSpinBox)





#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide.QtCore import *
from PySide.QtGui import *
import random
from log import *



def d6():
    return random.randint(1, 6)

def target(target):
    if (d6() + d6()) >= target:
        return True
    else:
        return False

allegiance_codes = ['Na', 'Im', 'Zh', 'As', 'Va']
allegiance_names = ['Non-alligned', 'Imperial',
                           'Zhodani', 'Aslan', 'Vargr']
#allegiance_colors = [Qt.darkCyan, Qt.red, Qt.darkGreen, Qt.yellow,
#                     Qt.blue, Qt.darkRed, Qt.green, Qt.darkMagenta,
#                     Qt.darkYellow, Qt.cyan, Qt.lightGray, Qt.darkBlue]
allegiance_colors = ['#FFFF99', '#00FF33', '#FF0099', '#FF6600',
                     '#CCFFCC', '#993399', '#993300', '#663399']


atmosphere_display = {'Breathable' : {'codes' : ['5', '6', '8', 'D', 'E'],
                                      'color' : '#55AAFF'},
                      'Negligible' : {'codes' : ['0', '1'],
                                      'color' : '#3C3C3C'},
                      'Thin' : {'codes' : ['2', '3', '4'],
                                'color' : '#CDCDFA'},
                      'Tainted' : {'codes' : ['7', '9'],
                                   'color' : '#FFAA78'},
                      'Extreme' : {'codes' : ['A', 'B', 'C', 'F'],
                                   'color' : '#A03CFF'}
                      }

starport_types = ['A', 'B', 'C', 'D', 'E', 'X']
starport_labels = ['A - Excellent', 'B - Good', 'C - Routine',
                   'D - Poor', 'E - Frontier', 'X - No starport']

size_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A']
size_labels = ['0 - 800km, 0.0G', '1 - 1,600km, 0.05G',
               '2 - 3,200km, 0.15G', '3 - 4,800km, 0.25G',
               '4 - 6,400km, 0.35G', '5 - 8,000km, 0.45G',
               '6 - 9,600km, 0.7G', '7 - 11,200km, 0.9G',
               '8 - 12,800km, 1.0G', '9 - 14,400km, 1.25G',
               'A - 16,000km, 1.4G']

atmosphere_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
atmosphere_labels = ['0 - None', '1 - Trace', '2 - V. Thin, Tainted',
                     '3 - V. Thin', '4 - Thin, Tainted', '5 - Thin',
                     '6 - Standard', '7 - Standard, Tainted',
                     '8 - Dense', '9 - Dense, Tainted', 'A - Exotic',
                     'B - Corrosive', 'C - Insidious', 'D - Dense, High',
                     'E - Thin, Low', 'F - Unusual']

atmosphere_colors = ['#3C3C3C', '#3C3C3C', '#CDCDFA', '#CDCDFA', '#CDCDFA',
                     '#55AAFF', '#55AAFF', '#FFAA78', '#55AAFF', '#FFAA78',
                     '#A03CFF', '#A03CFF', '#A03CFF', '#55AAFF', '#55AAFF',
                     '#A03CFF']

hydrographics_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A']
hydrographics_labels = ['0 - Desert World', '1 - Dry World',
                        '2 - A few small seas', '3 - Small seas and oceans',
                        '4 - Wet world', '5 - Large Oceans',
                        '6 - Large Oceans', '7 - Earth-like world',
                        '8 - Water world', '9 - Small islands',
                        'A - Almost all water']

population_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A', 'B', 'C']
population_labels = ['0 - None', '1 - Tiny', '2 - Village',
                     '3 - Large village', '4 - Small town',
                     '5 - Average city', '6 - Medium city',
                     '7 - Large city', '8 - Large cities',
                     '9 - Earth-like', 'A - Crowded',
                     'B - Very crowded', 'C - World-city']

government_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A', 'B', 'C', 'D']
government_labels = ['0 - None', '1 - Company/corporaton',
                     '2 - Part. democracy', '3 - Oligarchy',
                     '4 - Repr. democracy', '5 - Feudal technocracy',
                     '6 - Captive government', '7 - Balkanisation',
                     '8 - Civil service bureau.',
                     '9 - Impersonal bureau.', 'A - Charismatic dict.',
                     'B - Non-charismatic leader', 'C - Charismatic oligarchy',
                     'D - Religious dictatorship']

law_level_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
law_level_labels= ['0 - None', '1 - Permissive', '2 - Few restrictions',
                   '3 - Some restrictions', '4 - Some restrictions',
                   '5 - Standard', '6 - Restrictive', '7 - Controlling',
                   '8 - Repressive', '9 - Harsh']

tech_level_types = ['0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
tech_level_labels = ['0 - Primitive', '1 - Primitive', '2 - Primitive',
                     '3 - Primitive', '4 - Industrial', '5 - Industrial',
                     '6 - Industrial', '7 - Pre-Stellar', '8 - Pre-Stellar',
                     '9 - Pre-Stellar', 'A - Early Stellar',
                     'B - Early Stellar', 'C - Average Stellar',
                     'D - Average Stellar', 'E - Average Stellar',
                     'F - High Stellar',  'G - Advanced',  'H - Sublime',
                     'I - Sublime', 'J-Sublime', 'K-Sublime',
                     'L-Sublime', 'M-Sublime', 'N-Sublime',]

temperature_types = ['Frozen', 'Cold', 'Temperate',
                           'Hot', 'Roasting', 'Extreme Swings']

travel_code_types = ['Green', 'Amber', 'Red']


class Starport(object):
    def __init__(self, code):
        self.types_list = starport_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()

    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid starport code ' + value)
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Starport code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid starport index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Starport index property')

    def __repr__(self):
        return self.code

    def initAttributes(self):
        self.userTextChanged = False
        self.userText = self.ref_data[self.index]['User Text']
        self.description = self.ref_data[self.index]['Description']
        self.berthingCost = self.ref_data[self.index]['Berthing Cost']
        self.hasRefined = self.ref_data[self.index]['has_refined']
        self.hasUnrefined = self.ref_data[self.index]['has_unrefined']
        self.hasStarshipYard = self.ref_data[self.index]['has_starship_yard']
        self.hasSpacecraftYard = self.ref_data[self.index]['has_spacecraft_yard']
        self.hasSmallCraftYard = self.ref_data[self.index]['has_small_craft_yard']
        self.hasFullRepair = self.ref_data[self.index]['has_full_repair']
        self.hasLimitedRepair = self.ref_data[self.index]['has_limited_repair']
        self.hasNavyBase = self.ref_data[self.index]['has_naval']
        self.hasScoutBase = self.ref_data[self.index]['has_scout']
        self.hasResearchBase = self.ref_data[self.index]['has_research']
        self.hasTas = self.ref_data[self.index]['has_tas']
        self.hasConsulate = self.ref_data[self.index]['has_consulate']
        self.hasPirateBase = self.ref_data[self.index]['has_pirate']

    def initRefData(self):
        self.ref_data = [ {'Code' : 'A',
                           'User Text' : '',
                           'Description' : 'Excellent',
                           'Berthing Cost' : (d6() * 1000),
                           'Fuel' : 'Refined',
                           'has_refined' : True,
                           'has_unrefined' : True,
                           'has_starship_yard': True,
                           'has_spacecraft_yard' : True,
                           'has_small_craft_yard' : True,
                           'has_full_repair' : True,
                           'has_limited_repair' : False,
                           'has_naval' : target(8),
                           'has_scout' : target(10),
                           'has_research' : target(8),
                           'has_tas' : target(4),
                           'has_consulate' : target(6),
                           'has_pirate' : False},
                          {'Code' : 'B',
                           'User Text' : '',
                           'Description' : 'Good',
                           'Berthing Cost' : (d6() * 500),
                           'Fuel' : 'Refined',
                           'has_refined' : True,
                           'has_unrefined' : True,
                           'has_starship_yard': False,
                           'has_spacecraft_yard' : True,
                           'has_small_craft_yard' : True,
                           'has_full_repair' : True,
                           'has_limited_repair' : False,
                           'has_naval' : target(8),
                           'has_scout' : target(8),
                           'has_research' : target(10),
                           'has_tas' : target(6),
                           'has_consulate' : target(8),
                           'has_pirate' : target(12)},
                          {'Code' : 'C',
                           'User Text' : '',
                           'Description' : 'Routine',
                           'Berthing Cost' : (d6() * 100),
                           'Fuel' : 'Unrefined',
                           'has_refined' : False,
                           'has_unrefined' : True,
                           'has_starship_yard': False,
                           'has_spacecraft_yard' : False,
                           'has_small_craft_yard' : True,
                           'has_full_repair' : True,
                           'has_limited_repair' : False,
                           'has_naval' : False,
                           'has_scout' : target(8),
                           'has_research' : target(10),
                           'has_tas' : target(10),
                           'has_consulate' : target(10),
                           'has_pirate' : target(10)},
                          {'Code' : 'D',
                           'User Text' : '',
                           'Description' : 'Poor',
                           'Berthing Cost' : (d6() * 10),
                           'Fuel' : 'Unrefined',
                           'has_refined' : False,
                           'has_unrefined' : True,
                           'has_starship_yard': False,
                           'has_spacecraft_yard' : False,
                           'has_small_craft_yard' : False,
                           'has_full_repair' : False,
                           'has_limited_repair' : True,
                           'has_naval' : False,
                           'has_scout' : target(7),
                           'has_research' : False,
                           'has_tas' : False,
                           'has_consulate' : False,
                           'has_pirate' : target(12)},
                          {'Code' : 'E',
                           'User Text' : '',
                           'Description' : 'Frontier',
                           'Berthing Cost' : 0,
                           'Fuel' : 'None',
                           'has_refined' : False,
                           'has_unrefined' : False,
                           'has_starship_yard': False,
                           'has_spacecraft_yard' : False,
                           'has_small_craft_yard' : False,
                           'has_full_repair' : False,
                           'has_limited_repair' : False,
                           'has_naval' : False,
                           'has_scout' : False,
                           'has_research' : False,
                           'has_tas' : False,
                           'has_consulate' : False,
                           'has_pirate' : target(12)},
                          {'Code' : 'X',
                           'User Text' : '',
                           'Description' : 'No Starport',
                           'Berthing Cost' : 0,
                           'Fuel' : 'None',
                           'has_refined' : False,
                           'has_unrefined' : False,
                           'has_starship_yard': False,
                           'has_spacecraft_yard' : False,
                           'has_small_craft_yard' : False,
                           'has_full_repair' : False,
                           'has_limited_repair' : False,
                           'has_naval' : False,
                           'has_scout' : False,
                           'has_research' : False,
                           'has_tas' : False,
                           'has_consulate' : False,
                           'has_pirate' : False}
                          ]


class Size(object):
    def __init__(self, code):
        self.types_list = size_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid size code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Size code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid size index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Size index property')

    def __repr__(self):
        return self.code

    def initAttributes(self):
        i = self.index
        self.diameter = self.ref_data[i]['Diameter']
        self.gravity = self.ref_data[i]['Gravity']
        self.description = self.ref_data[i]['Description']
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']

    def initRefData(self):
        self.ref_data = [ {'Code' : '0',
                           'Diameter' : 800,
                           'Gravity' : 0.00,
                           'User Text' : '',
                           'Description' : 'Asteroid or Orbital Complex'},
                          {'Code' : '1',
                           'Diameter' : 1600,
                           'Gravity' : 0.05,
                           'User Text' : '',
                           'Description' : ''},
                          {'Code' : '2',
                           'Diameter' : 3200,
                           'Gravity' : 0.15,
                           'User Text' : '',
                           'Description' : 'Similar to Triton, Luna or Europa'},
                          {'Code' : '3',
                           'Diameter' : 4800,
                           'Gravity' : 0.25,
                           'User Text' : '',
                           'Description' : 'Mercury or Ganymede'},
                          {'Code' : '4',
                           'Diameter' : 6400,
                           'Gravity' : 0.35,
                           'User Text' : '',
                           'Description' : 'Similar to Mars'},
                          {'Code' : '5',
                           'Diameter' : 8000,
                           'Gravity' : 0.45,
                           'User Text' : '',
                           'Description' : 'Small'},
                          {'Code' : '6',
                           'Diameter' : 9600,
                           'Gravity' : 0.7,
                           'User Text' : '',
                           'Description' : 'Small'},
                          {'Code' : '7',
                           'Diameter' : 11200,
                           'Gravity' : 0.9,
                           'User Text' : '',
                           'Description' : 'Venus-size'},
                          {'Code' : '8',
                           'Diameter' : 12800,
                           'Gravity' : 1.0,
                           'User Text' : '',
                           'Description' : 'Earth-sized'},
                          {'Code' : '9',
                           'Diameter' : 14400,
                           'Gravity' : 1.25,
                           'User Text' : '',
                           'Description' : 'Large'},
                          {'Code' : 'A',
                           'Diameter' : 16000,
                           'Gravity' : 1.4,
                           'User Text' : '',
                           'Description' : 'Very large'} ]


class Atmosphere(object):
    def __init__(self, code):
        self.types_list = atmosphere_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid atmosphere code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Atmosphere code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid atmosphere index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Atmosphere index property')

    def __repr__(self):
        return self.code
    
    def initAttributes(self):
        i = self.index
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']
        self.pressure = self.ref_data[i]['Pressure']
        self.requiresVacc = self.ref_data[i]['requires_vacc']
        self.requiresRespirator = self.ref_data[i]['requires_respirator']
        self.requiresFilter = self.ref_data[i]['requires_filter']
        self.requiresAir = self.ref_data[i]['requires_air']
        self.requirementsVary = self.ref_data[i]['requirements_vary']

    def initRefData(self):
        self.ref_data = [ {'Code' : '0',
                           'User Text' : '',
                           'Description' : 'None',
                           'Pressure' : 0.0,
                           'requires_vacc' : True,
                           'requires_respirator' : False,
                           'requires_filter' : False,
                           'requires_air' : False,
                           'requirements_vary' : False},
                          {'Code' : '1',
                           'User Text' : '',
                          'Description' : 'Trace',
                          'Pressure' : round(random.uniform(0.001, 0.09),4),
                          'requires_vacc' : True,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '2',
                          'User Text' : '',
                          'Description' : 'Very Thin, Tainted',
                          'Pressure' : round(random.uniform(0.1, 0.42),3),
                          'requires_vacc' : False,
                          'requires_respirator' : True,
                          'requires_filter' : True,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '3',
                          'User Text' : '',
                          'Description' : 'Very Thin',
                          'Pressure' : round(random.uniform(0.1, 0.42),3),
                          'requires_vacc' : False,
                          'requires_respirator' : True,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '4',
                          'User Text' : '',
                          'Description' : 'Thin, Tainted',
                          'Pressure' : round(random.uniform(0.43, 0.7),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : True,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '5',
                          'User Text' : '',
                          'Description' : 'Thin',
                          'Pressure' : round(random.uniform(0.43, 0.7),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '6',
                          'User Text' : '',
                          'Description' : 'Standard',
                          'Pressure' : round(random.uniform(0.71, 1.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '7',
                          'User Text' : '',
                          'Description' : 'Standard, Tainted',
                          'Pressure' : round(random.uniform(0.71, 1.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : True,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '8',
                          'User Text' : '',
                          'Description' : 'Dense',
                          'Pressure' : round(random.uniform(1.5, 2.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : '9',
                          'User Text' : '',
                          'Description' : 'Dense, Tainted',
                          'Pressure' : round(random.uniform(1.5, 2.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : True,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : 'A',
                          'User Text' : '',
                          'Description' : 'Exotic',
                          'Pressure' : round(random.uniform(0.5, 2.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : True,
                          'requirements_vary' : False},
                         {'Code' : 'B',
                          'User Text' : '',
                          'Description' : 'Corrosive',
                          'Pressure' : round(random.uniform(0.5, 2.49),3),
                          'requires_vacc' : True,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : 'C',
                          'User Text' : '',
                          'Description' : 'Insidious',
                          'Pressure' : round(random.uniform(0.5, 2.49),3),
                          'requires_vacc' : True,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : 'D',
                          'User Text' : '',
                          'Description' : 'Dense, High',
                          'Pressure' : round(random.uniform(2.5, 100),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : 'E',
                          'User Text' : '',
                          'Description' : 'Thin, Low',
                          'Pressure' : round(random.uniform(0.1, 0.42),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : False},
                         {'Code' : 'F',
                          'User Text' : '',
                          'Description' : 'Unusual',
                          'Pressure' : round(random.uniform(0.5, 3.49),3),
                          'requires_vacc' : False,
                          'requires_respirator' : False,
                          'requires_filter' : False,
                          'requires_air' : False,
                          'requirements_vary' : True}]



class Hydrographics(object):
    def __init__(self, code):
        self.types_list = hydrographics_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()

    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid Hydrographics code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Hydrographics code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid Hydrographics index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Hydrographics index property')

    def __repr__(self):
        return self.code

    def initAttributes(self):
        i = self.index
        self.percentage = self.ref_data[i]['Percentage']
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']

    def initRefData(self):
        self.ref_data = [{'Code' : "0",
                          'Percentage' : (str(random.randint(0, 5)) + '%'),
                          'User Text' : '',
                          'Description' : 'Desert World'},
                         {'Code' : "1",
                          'Percentage' : (str(random.randint(6, 15)) + '%'),
                          'User Text' : '',
                          'Description' : 'Dry World'},
                         {'Code' : "2",
                          'Percentage' : (str(random.randint(16, 25)) + '%'),
                          'User Text' : '',
                          'Description' : 'A few small seas'},
                         {'Code' : "3",
                          'Percentage' : (str(random.randint(26, 35)) + '%'),
                          'User Text' : '',
                          'Description' : 'Small seas and oceans'},
                         {'Code' : "4",
                          'Percentage' : (str(random.randint(36, 45)) + '%'),
                          'User Text' : '',
                          'Description' : 'Wet world'},
                         {'Code' : "5",
                          'Percentage' : (str(random.randint(46, 55)) + '%'),
                          'User Text' : '',
                          'Description' : 'Large Oceans'},
                         {'Code' : "6",
                          'Percentage' : (str(random.randint(56, 65)) + '%'),
                          'User Text' : '',
                          'Description' : 'Large Oceans'},
                         {'Code' : "7",
                          'Percentage' : (str(random.randint(66, 75)) + '%'),
                          'User Text' : '',
                          'Description' : 'Earth-like world'},
                         {'Code' : "8",
                          'Percentage' : (str(random.randint(76, 85)) + '%'),
                          'User Text' : '',
                          'Description' : 'Water world'},
                         {'Code' : "9",
                          'Percentage' : (str(random.randint(86, 95)) + '%'),
                          'User Text' : '',
                          'Description' : ('Only a few small islands ' +
                                           'and archipelagos')},
                         {'Code' : "A",
                          'Percentage' : (str(random.randint(96, 100)) + '%'),
                          'User Text' : '',
                          'Description' : 'Almost entirely water'}]


class Population(object):
    def __init__(self, code):
        self.types_list = population_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid Population code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Population code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid Population index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Population index property')

    def __repr__(self):
        return self.code
    

    def initAttributes(self):
        i = self.index
        self.inhabitants = self.ref_data[i]['Population']
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']

    def initRefData(self):
        self.ref_data = [{'Code' : '0',
                          'Population' : 0,
                          'User Text' : '',
                          'Description' : 'None'},
                         {'Code' : '1',
                          'Population' : random.randint(1, 99),
                          'User Text' : '',
                          'Description' : 'Tiny farmstead or a single family'},
                         {'Code' : '2',
                          'Population' : (random.randint(10, 99) * 10),
                          'User Text' : '',
                          'Description' : 'A vilage'},
                         {'Code' : '3',
                          'Population' : (random.randint(10, 99) * 100),
                          'User Text' : '',
                          'Description' : 'Large village'},
                         {'Code' : '4',
                          'Population' : (random.randint(10, 99) * 1000),
                          'User Text' : '',
                          'Description' : 'Small town'},
                         {'Code' : '5',
                          'Population' : (random.randint(10, 99) * 10000),
                          'User Text' : '',
                          'Description' : 'Average city'},
                         {'Code' : '6',
                          'Population' : (random.randint(10, 99) * 100000),
                          'User Text' : '',
                          'Description' : 'Medium city'},
                         {'Code' : '7',
                          'Population' : (random.randint(10, 99) * 1000000),
                          'User Text' : '',
                          'Description' : 'Large city'},
                         {'Code' : '8',
                          'Population' : (random.randint(10, 99) * 10000000),
                          'User Text' : '',
                          'Description' : 'Several large cities'},
                         {'Code' : '9',
                          'Population' : (random.randint(10, 99) * 100000000),
                          'User Text' : '',
                          'Description' : 'Present day earth'},
                         {'Code' : 'A',
                          'Population' : (random.randint(10, 99) * 1000000000),
                          'User Text' : '',
                          'Description' : 'Crowded world'},
                         {'Code' : 'B',
                          'Population' : (random.randint(10, 99) * 10000000000),
                          'User Text' : '',
                          'Description' : 'Incredibly crowded world'},
                          {'Code' : 'C',
                          'Population' : (random.randint(10, 99) * 100000000000),
                          'User Text' : '',
                          'Description' : 'World-city'}]


class Government(object):
    def __init__(self, code):
        self.types_list = government_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)
        self.initAttributes()

    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid Government code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Government code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid Government index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Government index property')

    def __repr__(self):
        return self.code
    
    def initAttributes(self):
        i = self.index
        self.type = self.ref_data[i]['Type']
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']
        self.factionModifier = self.ref_data[i]['Faction Modifier']

    def initRefData(self):
        self.ref_data = [{'Code' : '0',
                          'Type' : 'None',
                          'User Text' : '',
                          'Description' : 'No government structure. ' +
                          'In many cases, family bonds predominate.\n' +
                          'Example: Family, Clan, Anarchy.\n' +
                          'Contraband: None',
                          'Faction Modifier' : 1},
                         {'Code' : '1',
                          'Type' : 'Company/corporation',
                          'User Text' : '',
                          'Description' : 'Ruling functions are assumed by ' +
                          'a company managerial elite, and most citizenry ' +
                          'are company employees or dependents.\n' +
                          'Example: Corporate outpost, asteroid mine, ' +
                          'feudal domain.\n' +
                          'Contraband: Weapons, Drugs, Travellers.',
                          'Faction Modifier' : 0},
                         {'Code' : '2',
                          'Type' : 'Participating democracy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are reached ' +
                          'by the advice and consent of the citizenry ' +
                          'directly.\n' +
                          'Example: Collective, tribal council, ' +
                          'comm-linked consensus.\n' +
                          'Contraband: Drugs',
                          'Faction Modifier' : 0},
                         {'Code' : '3',
                          'Type' : 'Self-perpetuating oligarchy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by a restricted minority, with little or no ' +
                          'input from the mass of citizenry.\n' +
                          'Example: Plutocracy, hereditary ruling caste.\n' +
                          'Contraband: Technology, Weapons, Travellers.',
                          'Faction Modifier' : 0},
                         {'Code' : '4',
                          'Type' : 'Representative democracy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by elected representatives.\n' +
                          'Example: Republic, democracy.\n' +
                          'Contraband: Dugs, Weapons, Psionics.',
                          'Faction Modifier' : 0},
                         {'Code' : '5',
                          'Type' : 'Feudal technocracy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by specific individuals for persons who agree ' +
                          'to be ruled by them. Relationships are based ' +
                          'on the performance of technical activities ' +
                          'which are mutualy beneficial.\n' +
                          'Example: \n' +
                          'Contraband: Technology, Weapons, Computers',
                          'Faction Modifier' : 0},
                         {'Code' : '6',
                          'Type' : 'Captive government',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by an imposed leadership answerable to an ' +
                          'outside group.\n' +
                          'Example: A colony or conquered area.\n' +
                          'Contraband: Weapons, Technology, Travellers',
                          'Faction Modifier' : 0},
                         {'Code' : '7',
                          'Type' : 'Balkanisation',
                          'User Text' : '',
                          'Description' : 'No central authority exists; ' +
                          'rival governments compete for control. Law ' +
                          'level refers to the government nearest the ' +
                          'starport.\n' +
                          'Example: Multiple governments, civil war.\n' +
                          'Contraband: Varies',
                          'Faction Modifier' : 1},
                         {'Code' : '8',
                          'Type' : 'Civil service bureaucracy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by government agencies employing individuals ' +
                          'selected for their expertise.\n' +
                          'Example: Entrenched castes of bureaucrats, ' +
                          'decaying empire.\n' +
                          'Contraband: Technology, Weapons, Drugs, ' +
                          'Travellers, Psionics.',
                          'Faction Modifier' : 0},
                         {'Code' : '9',
                          'Type' : 'Impersonal Bureaucracy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by agencies which have become insulated from the ' +
                          'governed citizens.\n' +
                          'Example: Entrenched castes of bureaucrats, ' +
                          'decaying empire.\n' +
                          'Contraband: Technology, Weapons, Drugs, ' +
                          'Travellers, Psionics.',
                          'Faction Modifier' : 0},
                         {'Code' : 'A',
                          'Type' : 'Charismatic Dictatorship',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by agencies directed by a single leader who ' +
                          'enjoys the overwhelming confidence ' +
                          'of the citizens.\n' +
                          'Example: Revolutionary leader, messiah, ' +
                          'emperor.\n' +
                          'Contraband: None',
                          'Faction Modifier' : -1},
                         {'Code' : 'B',
                          'Type' : 'Non-charismatic leader',
                          'User Text' : '',
                          'Description' : 'A previous charismatic leader has ' +
                          'been replaced by a leader through normal ' +
                          'channels.\n' +
                          'Example: Military dictatorship, hereditary ' +
                          'kingship.\n' +
                          'Contraband: Weapons, Technology, Computers.',
                          'Faction Modifier' : -1},
                         {'Code' : 'C',
                          'Type' : 'Charismatic oligarchy',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by a select group of members of an organisation ' +
                          'or class which enjoys the overwhelming ' +
                          'confidence of the citizenry.\n' +
                          'Example: Junta, revolutionary council.\n' +
                          'Contraband: Weapons',
                          'Faction Modifier' : -1},
                         {'Code' : 'D',
                          'Type' : 'Religious dictatorship',
                          'User Text' : '',
                          'Description' : 'Ruling functions are performed ' +
                          'by a religious organisation without regard to ' +
                          'the specific individual needs of the ' +
                          'citizenry.\n' +
                          'Example: Cult, transcendent philosophy, ' +
                          'psionic group mind.\n' +
                          'Contraband: Varies.',
                          'Faction Modifier' : -1}]


class LawLevel(object):
    def __init__(self, code):
        self.types_list = law_level_types
        self.initRefData()
        if code in law_level_types:
            self._code = code
            self._index = self.types_list.index(code)
        else:
            code = law_level_types[-1]
            self._code = code
            self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid LawLevel code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'LawLevel code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid LawLevel index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'LawLevel index property')

    def __repr__(self):
        return self.code

    def initAttributes(self):
        i = self.index
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']


    def initRefData(self):
        self.ref_data = [{'Code' : '0',
                          'User Text' : '',
                          'Description' : 'No restrictions.'},
                         {'Code' : '1',
                          'User Text' : '',
                          'Description' : 'Weapons: Poison gas, explosives, ' + \
                          'undetectable weapons, WMD.\n' + \
                          'Drugs: Highly addictive and dangerous ' + \
                          'narcotics.\n' + \
                          'Information: Intellect programs.\n' + \
                          'Technology: Dangerous technologies such as ' + \
                          'nanotechnology.\n' + \
                          'Travellers: Visitors must contact planetary ' + \
                          'authorities by radio, landing is permited ' + \
                          'anywhere.\n' + \
                          'Psionics: Dangerous talents must be registered.'},
                         {'Code' : '2',
                          'User Text' : '',
                          'Description' : 'Weapons: Portable energy weapons (except ' +
                          'ship-mounted weapons.\n' + 
                          'Drugs: Highly addictive narcotics.\n' +
                          'Information: Agent programs.\n' +
                          'Technology: Alien technology.\n' +
                          'Travellers: Visitors must report passenger ' +
                          'manifests, landing is permitted anywhere.\n' +
                          'Psionics: All psionic powers must be ' +
                          'registered; use of dangerous powers forbidden.'},
                         {'Code' : '3',
                          'User Text' : '',
                          'Description' : 'Weapons: Heavy weapons.\n' +
                          'Drugs: Combat drugs.\n' +
                          'Information: Intrusion programs.\n' +
                          'Technology: TL 15 items.\n' +
                          'Travellers: Landing only at starports or ' +
                          'other authorized sites.\n' +
                          'Psionics: Use of telepathy restricted to ' +
                          'government-approved telepaths.'},
                         {'Code' : '4',
                          'User Text' : '',
                          'Description' : 'Weapons: Light assault weapons ' +
                          'and submachine guns.\n' +
                          'Drugs: Addictive narcotics.\n' +
                          'Information: Security programs.\n' +
                          'Technology: TL 13 items.\n' +
                          'Travellers: Landing only at starport.\n' +
                          'Psionics: Use of teleportation and ' +
                          'clairvoyance restricted.'},
                         {'Code' : '5',
                          'User Text' : '',
                          'Description' : 'Weapons: Personal concealable ' +
                          'weapons.\n' +
                          'Drugs: Anagathics.\n' +
                          'Information: Expert programs.\n' +
                          'Technology: TL 11 items.\n' +
                          'Travellers: Citizens must register offworld ' +
                          'travel, visitors must register all business.\n' +
                          'Psionics: Use of all psionic powers restricted ' +
                          'to government psionicists.'},
                         {'Code' : '6',
                          'User Text' : '',
                          'Description' : '' +
                          'Weapons: All firearms except shotguns and ' +
                          'stunners; carrying weapons discouraged.\n' +
                          'Drugs: Fast and Slow drugs.\n' +
                          'Information: Recent news from offworld.\n' +
                          'Technology: TL 9 items.\n' +
                          'Travellers: Visits discouraged; excessive ' +
                          'contact with citizens forbidden.\n' +
                          'Psionics: Possession of psionic drugs banned.'},
                         {'Code' : '7',
                          'User Text' : '',
                          'Description' : 'Weapons: Shotguns.\n' +
                          'Drugs: All narcotics.\n' +
                          'Information: Library programs, unfiltered data ' +
                          'about other worlds. Free speech curtailed.\n' +
                          'Technology: TL 7 items.\n' +
                          'Travellers: Citizens may not leave planet; ' +
                          'visitors may not leave starport.\n' +
                          'Psionics: Use of psionics forbidden.'},
                          {'Code' : '8',
                           'User Text' : '',
                           'Description' : '' +
                           'Weapons: All bladed weapons, stunners.\n' +
                           'Drugs: Medicinal drugs.\n' +
                           'Information: Information technology, ' +
                           'any non-critical data from offworld personal ' +
                           'media.\n' +
                           'Technology: TL 5 items.\n' +
                           'Travellers: Landing permitted only to ' +
                           'imperial agents.\n' +
                           'Psionics: Psionic-related technology banned.'},
                          {'Code' : '9',
                           'User Text' : '',
                           'Description' : 'Weapons: Any weapons.\n' +
                           'Drugs: All drugs.\n' +
                           'Information: Any data from offworld. ' +
                           'No free press.\n' +
                           'Technology: TL 3 items.\n' +
                           'Travellers: No offworlders permitted.\n' +
                           'Psionics: All psionics.'}]
                         

class TechnologyLevel(object):
    def __init__(self, code):
        self.types_list = tech_level_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid Technology Level code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Technology Level code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid Technology Level index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Technology Level index property')

    def __repr__(self):
        return self.code

    def initAttributes(self):
        self.category = self.ref_data[self.index]['Category']
        self.userTextChanged = False
        self.userText = self.ref_data[self.index]['User Text']
        self.description = self.ref_data[self.index]['Description']
        
    def initRefData(self):
        self.ref_data = [ {'Code' : '0',
                           'Category' : 'Primitive',
                           'User Text' : '',
                           'Description' : 'No technnology. TL 0 species ' +
                           'have only discovered the simplest tools and ' +
                           "principles, and are on a par with Earth's " +
                           'stone age'},
                          {'Code' : '1',
                           'Category' : 'Primitive',
                           'User Text' : '',
                           'Description' : 'Bronze or Iron Age. Most ' +
                           'science is supersition, but they can ' +
                           'manufacture weapons and work metal.'},
                          {'Code' : '2',
                           'Category' : 'Primitive',
                           'User Text' : '',
                           'Description' : 'Renaisance technology. Some ' +
                           'understanding of chemistry, physics, biology ' +
                           'and astronomy as well as the scientific method'},
                          {'Code' : '3',
                           'Category' : 'Primitive',
                           'User Text' : '',
                           'Description' : 'Beginnings of the industrial ' +
                           'revolution and steam power. Primitive firearms ' +
                           'now dominate the battlefield.'},
                          {'Code' : '4',
                           'Category' : 'Industrial',
                           'User Text' : '',
                           'Description' : 'Industrialisation is complete ' +
                           'bringing plastics, radio, etc.'},
                          {'Code' : '5',
                           'Category' : 'Industrial',
                           'User Text' : '',
                           'Description' : 'Widespread electrification, ' +
                           'telecommunications and internal combustion. ' +
                           'Atomics and primitive computing may appear.'},
                          {'Code' : '6',
                           'Category' : 'Industrial',
                           'User Text' : '',
                           'Description' : 'Fission power and computing. ' +
                           'Early space age.'},
                          {'Code' : '7',
                           'Category' : 'Pre-Stellar',
                           'User Text' : '',
                           'Description' : 'Can rach orbit reliably and ' +
                           'has telecommunications satelites. Computers ' +
                           'become common.'},
                          {'Code' : '8',
                           'Category' : 'Pre-Stellar',
                           'User Text' : '',
                           'Description' : 'It is possible to reach other ' +
                           'worlds in the solar system. Permanent ' +
                           'space habitats become possible. Fusion power ' +
                           'becomes commercialy viable.'},
                          {'Code' : '9',
                           'Category' : 'Pre-Stellar',
                           'User Text' : '',
                           'Description' : 'Capable of Gravity manipulation. ' +
                           'Experimental jump drives.'},
                          {'Code' : 'A',
                           'Category' : 'Early Stellar',
                           'User Text' : '',
                           'Description' : 'Orbital habitats and factories ' +
                           'are common. Capable of regular interstellar ' +
                           'trade.'},
                          {'Code' : 'B',
                           'Category' : 'Early Stellar',
                           'User Text' : '',
                           'Description' : 'True AI. Grav-supported ' +
                           'structures. Jump-2. '},
                          {'Code' : 'C',
                           'Category' : 'Average Stellar',
                           'User Text' : '',
                           'Description' : 'Weather control. man-portable ' +
                           'plasma guns, mounted fusion guns. Jump-3.'},
                          {'Code' : 'D',
                           'Category' : 'Average Stellar',
                           'User Text' : '',
                           'Description' : 'Battle dress, Cloning of ' +
                           'body parts. Advanced hull design & thruster ' +
                           'plates. Jump-4.'},
                          {'Code' : 'E',
                           'Category' : 'Average Stellar',
                           'User Text' : '',
                           'Description' : 'Man-portable fusion weapons. ' +
                           'Flying cities. Jump-5.'},
                          {'Code' : 'F',
                           'Category' : 'High Stellar',
                           'User Text' : '',
                           'Description' : 'Black globe generators. ' +
                           'Anagathics. Jump-6.'}, 
                          {'Code' : 'G',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'}, 
                          {'Code' : 'H',
                           'Category' : 'Super-advanced',
                           'User Text' : '',
                           'Description' : 'Super-advanced stuff.'},
                          {'Code' : 'I',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'},
                          {'Code' : 'J',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'},
                          {'Code' : 'K',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'},
                          {'Code' : 'L',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'},
                          {'Code' : 'M',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'},
                          {'Code' : 'N',
                           'Category' : 'Advanced',
                           'User Text' : '',
                           'Description' : 'Advanced stuff.'} ]


class Temperature(object):
    def __init__(self, code):
        self.types_list = temperature_types
        self.initRefData()
        self._code = code
        self._index = self.types_list.index(code)

        self.initAttributes()


    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
            self.initAttributes()
        else:
            debug_log('Invalid Temperature code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Temperature code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
            self.initAttributes()
        else:
            debug_log('Invalid Temperature index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Temperature index property')

    def __repr__(self):
        return self.code
    

    def initAttributes(self):
        i = self.index
        self.category = self.ref_data[i]['Category']
        self.avg_temp = self.ref_data[i]['Avg. Temp']
        self.userTextChanged = False
        self.userText = self.ref_data[i]['User Text']
        self.description = self.ref_data[i]['Description']


    def initRefData(self):
        self.ref_data = [{'Category' : "Frozen",
                          'Avg. Temp' : random.randint(-100, -51),
                          'User Text' : '',
                          'Description' : ('Frozen World. No liquid water, ' +
                                           'very dry atmosphere.')},
                         {'Category' : "Cold",
                          'Avg. Temp' : random.randint(-50, 0),
                          'User Text' : '',
                          'Description' : ('Icy world. Little liquid water, ' +
                                           'extensive ice caps, few clouds.')},
                          {'Category' : "Temperate",
                           'Avg. Temp' : random.randint(0, 30),
                          'User Text' : '',
                          'Description' : ('Temperate world. Earthlike. ' +
                                           'Liquid and vaporised water are ' +
                                           'common, moderate ice caps')},
                         {'Category' : "Hot",
                          'Avg. Temp' : random.randint(31, 80),
                          'User Text' : '',
                          'Description' : ('Hot world. Small or no ice ' +
                                           'caps,little liquid water. Most ' +
                                           'water in the form of clouds.')},
                         {'Category' : "Roasting",
                          'Avg. Temp' : random.randint(81, 150),
                          'User Text' : '',
                          'Description' : ('Boiling world. No ice caps, ' +
                                           'little liquid water.')},
                         {'Category' : "Extreme Swings",
                          'Avg. Temp' : random.randint(-50, 50),
                          'User Text' : '',
                          'Description' : ('Temperature swings from ' +
                                           'roasting during the day to ' +
                                           'frozen at night.')}]

class TravelCode(object):
    def __init__(self, code):
        self.types_list = travel_code_types
        self._code = code
        self._index = self.types_list.index(code)

    def getCode(self):
        return self._code
    def setCode(self, value):
        if value in self.types_list and value != self._code:
            self._code = value
            self._index = self.types_list.index(self._code)
        else:
            debug_log('Invalid Travel code ' + str(value))
    def delCode(self):
        del self._code
    code = property(getCode, setCode, delCode, 'Travel code property.')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(self.types_list):
            self._index = int(value)
            self._code = self.types_list[self._index]
        else:
            debug_log('Invalid Travel index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Travel index property')

    def __repr__(self):
        return self.code


class Allegiance(object):
    def __init__(self, code):
        self._index = 0
        if code in allegiance_codes:
            self.code = code

    def getCode(self):
        return allegiance_codes[self._index]
    def setCode(self, value):
        if value in allegiance_codes:
            self._index = allegiance_codes.index(value)
        else:
            debug_log('Invalid Allegiance code ' + str(value))
            debug_log('Allegiances are ' + str(allegiance_codes))

    def delCode(self):
        pass
    code = property(getCode, setCode, delCode, 'Allegiance code property.')

    def getName(self):
        return allegiance_names[self._index]
    def setName(self, value):
        if value in allegiance_names and value != allegiance_names[self._index]:
            #Make sure both index and code are updated
            self.index = allegiance_names.index(value)
        else:
            debug_log('Invalid Allegiance name ' + str(value))
    def delName(self):
        pass
    name = property(getName, setName, delName, 'Allegiance name property')

    def getIndex(self):
        return self._index
    def setIndex(self, value):
        if 0 <= value < len(allegiance_codes):
            self._index = value
        else:
            debug_log('Invalid Allegiance index ' + str(value))
    def delIndex(self):
        del self._index
    index = property(getIndex, setIndex, delIndex, 'Allegiance index property')

    def __repr__(self):
        return self.code



class NumberText(QLineEdit):
    def __init__(self, parent=None):
        super(NumberText, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("888888") + 8), (metrics.height() + 8))

class LongNumberText(QLineEdit):
    def __init__(self, parent=None):
        super(LongNumberText, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("888888888888888888") + 8), (metrics.height() + 8))

    def setText(self, text):
        locale.setlocale(locale.LC_ALL, "")
        newText = locale.format('%d', int(text), True)
        print newText
        QLineEdit.setText(newText)


class DescriptionText(QPlainTextEdit):
    def __init__(self, parent=None):
        super(DescriptionText, self).__init__(parent)
        self.setReadOnly(True)
        
class DiameterSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(DiameterSpinBox, self).__init__(parent)
        self.setReadOnly(True)
        self.setSuffix(' km')
        self.setMaximum(1000000)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("888888888888") + 8), (metrics.height() + 8))


class WorldNameLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(WorldNameLineEdit, self).__init__(parent)
        #self.setPlaceholderText('world name')
        self.setMaxLength(20)
        #metrics = QFontMetrics(QApplication.font())
        #self.setFixedSize((metrics.width('8' * 20) + 8), (metrics.height() + 8))

class ColumnSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(ColumnSpinBox, self).__init__(parent)
        pass

class RowSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(RowSpinBox, self).__init__(parent)
        pass

class SectorCoords(QLineEdit):
    def __init__(self, parent=None):
        super(SectorCoords, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("8888") + 8), (metrics.height() + 8))

class StarportComboBox(QComboBox):
    def __init__(self, parent=None):
        super(StarportComboBox, self).__init__(parent)
        self.setModel(QStringListModel(starport_labels))

class SizeComboBox(QComboBox):
    def __init__(self, parent=None):
        super(SizeComboBox, self).__init__(parent)
        self.setModel(QStringListModel(size_labels))

class AtmosphereComboBox(QComboBox):
    def __init__(self, parent=None):
        super(AtmosphereComboBox, self).__init__(parent)
        self.setModel(QStringListModel(atmosphere_labels))

class HydrographicsComboBox(QComboBox):
    def __init__(self, parent=None):
        super(HydrographicsComboBox, self).__init__(parent)
        self.setModel(QStringListModel(hydrographics_labels))

class PopulationComboBox(QComboBox):
    def __init__(self, parent=None):
        super(PopulationComboBox, self).__init__(parent)
        self.setModel(QStringListModel(population_labels))

class GovernmentComboBox(QComboBox):
    def __init__(self, parent=None):
        super(GovernmentComboBox, self).__init__(parent)
        self.setModel(QStringListModel(government_labels))

class LawLevelComboBox(QComboBox):
    def __init__(self, parent=None):
        super(LawLevelComboBox, self).__init__(parent)
        self.setModel(QStringListModel(law_level_labels))

class TechLevelComboBox(QComboBox):
    def __init__(self, parent=None):
        super(TechLevelComboBox, self).__init__(parent)
        self.setModel(QStringListModel(tech_level_labels))

class TemperatureComboBox(QComboBox):
    def __init__(self, parent=None):
        super(TemperatureComboBox, self).__init__(parent)
        self.setModel(QStringListModel(temperature_types))

class AllegianceNameComboBox(QComboBox):
    def __init__(self, parent=None):
        super(AllegianceNameComboBox, self).__init__(parent)
        self.setModel(QStringListModel(allegiance_names))

class OwningSector(QLineEdit):
    def __init__(self, parent=None):
        super(OwningSector, self).__init__(parent)
        self.setReadOnly(True)

class OwningSubsector(QLineEdit):
    def __init__(self, parent=None):
        super(OwningSubsector, self).__init__(parent)
        self.setReadOnly(True)

class TravelCodeComboBox(QComboBox):
    def __init__(self, parent=None):
        super(TravelCodeComboBox, self).__init__(parent)
        self.setModel(QStringListModel(travel_code_types))

class BerthingCostSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(BerthingCostSpinBox, self).__init__(parent)
        self.setMaximum(10000)
        self.setSingleStep(100)

class ShortLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(ShortLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("8888") + 8), (metrics.height() + 8))

class LongLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LongLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("88888888") + 8), (metrics.height() + 8))

# Specific line edits to be deprecated
class DiameterLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(DiameterLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("8888") + 8), (metrics.height() + 8))

class GravityLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(GravityLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("8888") + 8), (metrics.height() + 8))

class PressureLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(PressureLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        metrics = QFontMetrics(QApplication.font())
        self.setFixedSize((metrics.width("88888888") + 8), (metrics.height() + 8))




#Traveller Classes
def getRandomWorldData():
    dm = 0

    def numberToCode(number):
        string_list = ['0', '1', '2', '3', '4', '5', '6', '7',
                       '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
                       'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
        return string_list[number]

    if (d6() + d6()) >= 10:
        gas_giant = False
    else:
        gas_giant = True

    #Starport
    port_roll = d6() + d6()
    if port_roll <= 2:
        starport = 'X'
    elif port_roll in [3, 4]:
        starport = 'E'
    elif port_roll in [5, 6]:
        starport = 'D'
    elif port_roll in [7, 8]:
        starport = 'C'
    elif port_roll in [9, 10]:
        starport = 'B'
    elif port_roll >= 11:
        starport = 'A'

    # Size
    size_roll = d6() + d6() - 2
    size = numberToCode(size_roll)

    # Atmosphere
    atmo_roll = d6() + d6() - 7 + size_roll
    if atmo_roll <= 0: atmo_roll = 0
    atmosphere = numberToCode(atmo_roll)

    # Temperature
    if atmo_roll <= 1: temperature = 'Extreme Swings'
    else:
        if atmo_roll <= 3: dm = -2
        elif atmo_roll <= 5 or atmosphere == 'E': dm = -1
        elif atmo_roll <= 7: dm = 0
        elif atmo_roll <= 9: dm = 1
        elif atmosphere in ['A', 'D', 'F']: dm = 2
        elif atmosphere in ['B', 'C']: dm = 6
        temp_roll = d6() + d6() + dm
        if temp_roll <= 2: temperature = 'Frozen'
        elif temp_roll <= 4: temperature = 'Cold'
        elif temp_roll <= 9: temperature = 'Temperate'
        elif temp_roll <= 11: temperature = 'Hot'
        elif temp_roll >= 12: temperature = 'Roasting'

    #Hydrographics
    if size in ['0', '1']:
        hydrographics = '0'
    else:
        if atmosphere in ['0', '1', 'A', 'B', 'C']:
            dm = -4
        if temperature == 'Hot' : dm = dm - 2
        elif temperature == 'Roasting': dm = dm - 6

        hydro_roll = d6() + d6() - 7 + size_roll + dm
        if hydro_roll <= 0: hydro_roll = 0
        elif hydro_roll >= 10 : hydro_roll = 10

        hydrographics = numberToCode(hydro_roll)

    #Population
    pop_roll = d6() + d6() - 2
    population = numberToCode(pop_roll)

    #Government
    gov_roll = d6() + d6() - 7 + pop_roll
    if gov_roll <= 0 : gov_roll = 0
    elif gov_roll >= 13: gov_roll = 13
    government = numberToCode(gov_roll)

    #Law Level
    law_roll = d6() + d6() - 7 + gov_roll
    if law_roll <= 0 : law_roll = 0
    elif law_roll >= 9: law_roll = 9
    law_level = numberToCode(law_roll)

    #Technology Level
    tldm = 0
    if starport == 'A' : tldm = tldm + 6
    elif starport == 'B': tldm = tldm + 4
    elif starport == 'C': tldm = tldm + 2
    elif starport == 'X': tldm = tldm - 4
    if size in ['0', '1'] : tldm = tldm + 2
    elif size in ['2', '3', '4']: tldm = tldm + 1
    if atmosphere in ['0', '1', '2', '3', 'A', 'B', 'C', 'D', 'E', 'F']:
        tldm = tldm + 1
    if hydrographics in ['0', '9']: tldm = tldm + 1
    elif hydrographics == 'A' : tldm = tldm + 2
    if population in ['1', '2', '3', '4', '5', '9']: tldm = tldm + 1
    elif population == 'A': tldm = tldm + 2
    elif population == 'B': tldm = tldm + 3
    elif population == 'C': tldm = tldm + 4
    if government in ['0', '5'] : tldm = tldm + 1
    elif government == '7': tldm = tldm + 2
    elif government in ['D', 'E'] : tldm = tldm - 2
    tl_roll = d6() + tldm
    if tl_roll <= 0: tl_roll = 0
    tech_level = numberToCode(tl_roll)

    debug_log(starport + size + atmosphere + hydrographics + population + \
           government + law_level + tech_level + temperature)
    return starport, size, atmosphere, hydrographics, population, \
           government, law_level, tech_level, temperature, gas_giant


class Sector(object):
    def __init__(self, name='Unknown', x=0, y=0):
        self.name = name
        self.sectorCol = int(x)
        self.sectorRow = int(y)

class Subsector(object):
    def __init__(self, name='Unknown', x=0, y=0):
        self.name = name
        self.subsectorCol = int(x)
        self.subsectorRow = int(y)

class World(object):
    def __init__(self, name='Unknown', x=-1, y=-1, port='X', size='0',
                 atmosphere='0', hydrographics='0', population='0',
                 government='0', law_level='0', tech_level='0',
                 temperature='Frozen', gas=True, travel_code='Green',
                 berthing_cost=False, navy=False, scout=False, research=False,
                 tas=False, consulate=False, pirate=False, allegiance='Na',
                 port_txt='', size_txt='', atmo_txt='', hydro_txt='',
                 pop_txt='', gov_txt='', law_txt='', tech_txt='',
                 hydro_pc=None,
                 Ag=False, As=False, Ba=False, De=False, Fl=False,
                 Ga=False, Hi=False, Ht=False, IC=False, In=False,
                 Lo=False, Lt=False, Na=False, NI=False, Po=False,
                 Ri=False, Va=False, Wa=False):

        # Indicates if custom user text has changed
        self.dirty = False
        
        self.name = name
        self.col = int(x)
        self.row = int(y)
        #self._starport = Starport(str(port))
        self.starport = Starport(str(port))
        self.starport.userText = port_txt
        self.size = Size(str(size))
        self.size.userText = size_txt
        self.atmosphere = Atmosphere(str(atmosphere))
        self.atmosphere.userText = atmo_txt
        self.hydrographics = Hydrographics(str(hydrographics))
        if hydro_pc is not None:
            self.hydrographics.percentage = hydro_pc
        self.hydrographics.userText = hydro_txt
        self.population = Population(str(population))
        self.population.userText = pop_txt
        self.government = Government(str(government))
        self.government.userText = gov_txt
        self.lawLevel = LawLevel(str(law_level))
        self.lawLevel.userText = law_txt
        self.techLevel = TechnologyLevel(str(tech_level))
        self.techLevel.userText = tech_txt
        self.temperature = Temperature(str(temperature))
        self.hasGasGiant = gas
        self.travelCode = TravelCode(travel_code)
        if berthing_cost:
            self.starport.berthingCost = berthing_cost
        self.starport.hasNavyBase = navy
        self.starport.hasScoutBase = scout
        self.starport.hasResearchBase = research
        self.starport.hasTas = tas
        self.starport.hasConsulate = consulate
        self.starport.hasPirateBase = pirate
        self.allegiance = Allegiance(str(allegiance))

        self.tradeAg = Ag
        self.tradeAs = As
        self.tradeBa = Ba
        self.tradeDe = De
        self.tradeFl = Fl
        self.tradeGa = Ga
        self.tradeHi = Hi
        self.tradeHt = Ht
        self.tradeIC = IC
        self.tradeIn = In
        self.tradeLo = Lo
        self.tradeLt = Lt
        self.tradeNa = Na
        self.tradeNI = NI
        self.tradePo = Po
        self.tradeRi = Ri
        self.tradeVa = Va
        self.tradeWa = Wa

    def addFactions(self):
        KEY,SIZE,LABEL = range(3)
        factions = []
        for f in range(random.randint(1, 3) + self.government.factionModifier):
            roll = d6() + d6()
            if roll <= 3:
                factions.append([0, 'Obscure - few have heard of them, no popular support.'])
            elif 4 <= roll <= 5:
                factions.append([1, 'Fringe group - few supporters.'])
            elif 6 <= roll <= 7:
                factions.append([2, 'Minor group - some supportters.'])
            elif 8 <= roll <= 9:
                factions.append([3, 'Notable - Significant support, well known.'])
            elif 10 <= roll <= 11:
                factions.append([4, 'Significant - nearly as powerful as the government.'])
            elif 12 <= roll:
                factions.append([5, 'Overwhelming popular support.'])
        for faction in factions:
            fact_roll = d6() + d6() - 7 + self.population.index
            if fact_roll <= 0 : fact_roll = 0
            elif fact_roll >= 13: fact_roll = 13
            faction.append(government_labels[fact_roll])
        factions = sorted(factions, key=lambda gov: gov[0], reverse=True)
        debug_log('Traveller:World:addFactions ' + str(factions))

        text = '\n'
        for f in factions:
            text += '\n' + 'Faction type: ' + f[LABEL] + '\n'
            text += 'Faction Size: ' + f[SIZE] + '\n'
        if self.government.userTextChanged:
            self.government.userText += text
        else:
            self.government.userText = self.government.description + text
            self.government.userTextChanged = True

    def recalculateTradeCodes(self):
        if self.atmosphere.code in ['4', '5', '6', '7', '8', '9'] \
           and self.hydrographics.code in ['4', '5', '6', '7', '8'] \
           and self.population.code in ['5', '6', '7']:
            self.tradeAg = True
        else:
            self.tradeAg = False

        if self.size.code == '0' \
           and self.atmosphere.code == '0' \
           and self.hydrographics.code == '0':
            self.tradeAs = True
        else:
            self.tradeAs = False

        if self.population.code == '0' \
           and self.government.code == '0' \
           and self.lawLevel.code == '0':
            self.tradeBa = True
        else:
            self.tradeBa = False

        if self.atmosphere.index >= 2 \
           and self.hydrographics.code == '0':
            self.tradeDe = True
        else:
            self.tradeDe = False

        if self.atmosphere.index >= 10 \
           and self.hydrographics.index >= 1:
            self.tradeFl = True
        else:
            self.tradeFl = False

        if self.atmosphere.code in ['4', '5', '6', '7', '8', '9'] \
           and self.hydrographics.code in  ['4', '5', '6', '7', '8']:
            self.tradeGa = True
        else:
            self.tradeGa = False

        if self.population.index >= 9:
            self.tradeHi = True
        else:
            self.tradeHi = False

        if self.techLevel.index >= 12:
            self.tradeHt = True
        else:
            self.tradeHt = False

        if self.atmosphere.code in ['0', '1'] \
           and self.hydrographics.index >= 1:
            self.tradeIC = True
        else:
            self.tradeIC = False

        if self.atmosphere.code in ['0', '1', '2', '4', '7', '9'] \
           and self.population.index >= 9:
            self.tradeIn = True
        else:
            self.tradeIn = False

        if self.techLevel.index <= 5:
            self.tradeLt = True
        else:
            self.tradeLt = False

        if self.atmosphere.code in ['0', '1', '2', '3'] \
           and self.hydrographics.code in ['0', '1', '2', '3'] \
           and self.population.index >= 6:
            self.tradeNa = True
        else:
            self.tradeNa = False

        if self.population.code in ['4', '5', '6']:
            self.tradeNI = True
        else:
            self.tradeNI = False

        if self.atmosphere.code in ['2', '3', '4', '5'] \
           and self.hydrographics.code in ['0', '1', '2', '3']:
            self.tradePo = True
        else:
            self.tradePo = False

        if self.atmosphere.code in ['6', '8'] \
           and self.population.code in ['6', '7', '8']:
            self.tradeRi = True
        else:
            self.tradeRi = False

        if self.atmosphere.code == '0':
            self.tradeVa = True
        else:
            self.tradeVa = False

        if self.hydrographics.code == 'A':
            self.tradeWa = True
        else:
            self.tradeWa = False


##    def getStarport(self):
##        return self._starport
##    def setStarport(self, i):
##        self._starport = Starport(index=i)
##    def delStarport(self):
##        del self._starport
##    starport = property(getStarport, setStarport, delStarport, 'Starport.')
        

    def reconfigure(self, params):
        (port, size, atmo, hydro, pop, gov, law, tech, temp, gas) = params
        self.starport = Starport(port)
        self.size = Size(size)
        self.atmosphere = Atmosphere(atmo)
        self.hydrographics = Hydrographics(hydro)
        self.population = Population(pop)
        self.government = Government(gov)
        self.lawLevel = LawLevel(law)
        self.techLevel = TechnologyLevel(tech)
        self.temperature = Temperature(temp)
        self.hasGasGiant = gas
        self.travelCode = TravelCode('Green')
        self.recalculateTradeCodes()

    def randomize(self):
        port, size, atmo, hydro, pop, gov, law, tech, temp, \
              gas = getRandomWorldData()
        self.starport = Starport(port)
        self.size = Size(size)
        self.atmosphere = Atmosphere(atmo)
        self.hydrographics = Hydrographics(hydro)
        self.population = Population(pop)
        self.government = Government(gov)
        self.lawLevel = LawLevel(law)
        self.techLevel = TechnologyLevel(tech)
        self.temperature = Temperature(temp)
        self.hasGasGiant = gas
        self.travelCode = TravelCode('Green')
        self.recalculateTradeCodes()


    

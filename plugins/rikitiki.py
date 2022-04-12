import random
from categories import WorldGenerator
from log import *

def d6():
    return random.randint(1, 6)

class Rikitiki(WorldGenerator):
    name = "Rikitiki"

    def generateWorld(self):
        
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

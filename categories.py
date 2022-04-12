class WorldGenerator(object):
    """Plugins of this class geenrate world data"""

    name = "Blank World"

    def generateWorld(self):
        """Generates a barren, uninhabited world"""

        temperature_list = ['Frozen', 'Cold', 'Temperate',
                             'Hot', 'Roasting', 'Extreme Swings']

        starport = 'X'
        size = '0'
        atmosphere = '0'
        hydrographics = '0'
        population = '0'
        government = '0'
        law_level = '0'
        tech_level = '0'
        temperature = temperature_list[0]
        gas_giant = False

        return starport, size, atmosphere, hydrographics, population, \
           government, law_level, tech_level, temperature, gas_giant

import numpy as np


ZONE_SUBURBAN_COMMERCIAL = 0    #
ZONE_URBAN_COMMERCIAL = 1       #
ZONE_SUBURBAN_RESIDENTIAL = 2   #
ZONE_URBAN_RESIDENTIAL = 3      #
ZONE_INDUSTRIAL = 4             #
ZONE_AIRPORT = 5                #
ZONE_AGRICULTURAL = 6           # farmland
ZONE_RURAL = 7                  # houses with farms or lots of land
ZONE_MILITARY = 8
ZONE_HISTORIC_SUBURBAN_COMMERCIAL = 9
ZONE_HISTORIC_URBAN_COMMERCIAL = 10
ZONE_HISTORIC_SUBURBAN_RESIDENTIAL = 11
ZONE_HISTORIC_URBAN_RESIDENTIAL = 12
ZONE_PARK = 13                  # designated non-construction zone
ZONE_AESTHETIC = 14             # wealthy housing
ZONE_HISTORIC_AESTHETIC = 15

HIGHEST_ALTITUDE = 8850
LOWEST_ALTITUDE = -11000

CLIMATE_TROPICAL_RAINFOREST = 0         # tropical wet
CLIMATE_SAVANNA = 1                     # subtropical wet and dry
CLIMATE_ARID = 2                        # dryest and warm
CLIMATE_SEMIARID = 3                    # dry and cold or warm
CLIMATE_TEMPERATE_RAINFOREST = 4        # temperate wet
CLIMATE_TEMPERATE_SEASONAL_FOREST = 5   # temperate wet and dry
CLIMATE_TEMPERATE_GRASSLAND = 6         # temperate dry
CLIMATE_BOREAL_FOREST = 7               # taiga
CLIMATE_BOREAL_TUNDRA = 8               # ice covered year round
CLIMATE_BOREAL_STEPPE = 9               # taiga
CLIMATE_BOREAL_ICECAP = 10              # taiga
FLORA_

# 32 bit int
# zone          4
# development   4
# climate       4
# flora         3
# altitude      11      -> 10m increments
# highway       1
# wildfire      2
#
# 2 remaining bits
def _genCell(zone, development, climate, flora, altitude, highway):
    pass

class World:
    
    def __init__(self):
        self.width = 25431
        self.height = 20015
        self.grid = np.array([[0 for _ in range(self.height)] for _ in range(self.width)], dtype=np.int32)

world = World()
world.grid[2][2] = 2
print(world.grid[2][2])

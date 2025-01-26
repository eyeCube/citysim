import math
        
def sign(val):
    return 1 if val >= 0 else -1
def ssign(val):
    return "+" if val >= 0 else "-"

def get_ugpm3(val, land):
    return val * 0.1 / GMULT / land

def get_col_intensity(value, min_value=0, max_value=100, reverse=False):
    if reverse:
        value = max_value - value
    v = max(0, value - min_value) / (max_value - min_value)
    r = g = b = 255
    if (v < 1):
        r = 255
        g = max(0, round(255*math.sin(math.pi*0.5*v)))
        b = max(0, round(255*math.sin(math.pi*0.5*v))) if v > 0 else 255
    return (r, g, b,)


PRIORITY_LOW = False
PRIORITY_HIGH = True

MAX_ALLOCATION = 1000
GMULT = 100

MONTHS=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

RED = (255, 64, 64,)
YELLOW = (255, 200, 0)
GREEN = (0, 255, 0,)
WHITE = (255, 255, 255,)
BLACK = (0, 0, 0,)
GRAY = (150,150,150,)
LTGRAY = (200, 200, 200,)
OFFWHITE = (255, 230, 210,)
COL_UI_BG = (4, 8, 0,)
COL_UI_HIGHLIGHT = (255, 190, 120,)
COL_UI_INTERACTABLE = (255, 215, 150,)
COL_UI_DARK = (128, 107, 75,)
COL_UI_DEEP = (32, 27, 18,)
COL_CONSTRUCTION = (165, 165, 165,)
COL_AGRICULTURE = (255, 96, 64,)
COL_INDUSTRY = (255, 127, 0,)
COL_INNOVATION = (255, 255, 0,)
COL_ENVIRONMENTAL = (0, 255, 0,)
COL_HEALTHCARE = (215, 255, 255,)
COL_LAWENFORCEMENT = (127, 127, 255,)
COL_DEFENSE = (255, 0, 127,)
COL_INFRASTRUCTURE = (196, 160, 196,)
COL_UNUSEDINFRASTRUCTURE = (128, 96, 128,)
COL_POPULATION = (255, 255, 64,)
COL_FOOD = (255, 128, 64,)
COL_OIL = (64, 64, 255,)
COL_WEAPONS = (255, 64, 255,)
COL_RESEARCH = (128, 255, 255,)
COL_PRODUCTIVITY = (64, 255, 64,)
COL_FERTILITY = (255, 128, 255,)
COL_HAPPINESS = (255, 180, 128,)
COL_SANITY = (96, 255, 128,)
COL_HEALTH = (255, 128, 128,)
COL_CRIME = (128, 128, 255,)
COL_POLLUTION = (255, 128, 0,)
COL_POWER = (255, 255, 210,)
COL_WARMACHINES = (255, 64, 127,)
COL_TRUST = (255, 255, 192,)
COL_WEALTH = (255, 215, 128,)
COL_INFLUENCE = (160, 32, 255,)
COL_BUSINESS = (64, 255, 64,)
COL_INCOME_INEQUALITY = (255, 215, 0,)
COL_TERRITORY = (64, 215, 128,)
COL_UNEMPLOYMENT = (160, 96, 0,)
COL_ZUA = (0, 215, 215,)
COL_FMA = (255, 128, 0,)
COL_EA = (255, 255, 0,)
COL_CA = (128, 128, 255,)
COL_RA = (255, 160, 64,)
COL_LLA = (64, 196, 255,)
COL_GEA = (0, 255, 0,)
COL_SSA = (255, 64, 128,)

HARV        = 0
INFR        = 1
AGRI        = 2
DEFE        = 3
SCIE        = 4
POLI        = 5
ENVI        = 6
HEAL        = 7
UNEMPLOYED  = 8
HOMELESS    = 9
DISABLED    = 10
SOLDIERS    = 11
VETERANS    = 12
RETIREES    = 13
CASUALTIES  = 14
ILLEGALS    = 15
PRIVATE     = 16
GENERAL     = 99


ICON_BUTTON_ARROW_LEFT = 174
ICON_BUTTON_ARROW_RIGHT = 175
ICON_BUTTON_ARROW_DOWN = 158
ICON_BUTTON_PLUS = 132
ICON_BUTTON_MINUS = 133
ICON_BUTTON_RADIO = 160
ICON_BUTTON_RADIO_ON = 161
ICON_PER_MILLE = 251

ICON_AM = 157
ICON_PM = 156
ICON_CONSTRUCTION = 165
ICON_AGRICULTURE = 166
ICON_INDUSTRY = 167
ICON_INNOVATION = 168
ICON_ENVIRONMENTAL = 169
ICON_HEALTHCARE = 170
ICON_LAWENFORCEMENT = 171
ICON_DEFENSE = 6
ICON_FOOD = 1
ICON_OIL = 2
ICON_POPULATION = 3
ICON_INFRASTRUCTURE = 4
ICON_RESEARCH = 5
ICON_WEAPONS = 6
ICON_PRODUCTIVITY = 7
ICON_POLLUTION = 13
ICON_WARMACHINES = 14
ICON_TRUST = 15
ICON_WEALTH = 16
ICON_INFLUENCE = 17
ICON_BUSINESS = 18
ICON_INCOME_INEQUALITY = 19
ICON_TERRITORY = 27
ICON_UNEMPLOYMENT = 31
ICON_FERTILITY_100 = 8
ICON_HEALTH_100 = 9
ICON_SANITY_100 = 10
ICON_HAPPINESS_100 = 11
ICON_CRIME_100 = 12
ICON_FERTILITY_75 = 134
ICON_HEALTH_75 = 135
ICON_SANITY_75 = 136
ICON_HAPPINESS_75 = 137
ICON_CRIME_75 = 138
ICON_FERTILITY_50 = 139
ICON_HEALTH_50 = 140
ICON_SANITY_50 = 141
ICON_HAPPINESS_50 = 142
ICON_CRIME_50 = 143
ICON_FERTILITY_25 = 144
ICON_HEALTH_25 = 145
ICON_SANITY_25 = 146
ICON_HAPPINESS_25 = 147
ICON_CRIME_25 = 148
ICON_LOCKED = 163

GROUP_ALLIES = 0
GROUP_AXIS = 1
GROUP_NEUTRAL = 2
GROUP_UNAFFILIATED = 3
GROUP_BORGS = 4
GROUP_XURGS = 5

TAB_GAME = 0
TAB_SECTORS = 1
TAB_AGENCIES = 2
TAB_AGENCIES2 = 3
TAB_AGENCIES3 = 4
TAB_AGENCIES4 = 5
TAB_AGENCIES5 = 6
TAB_TECHS = 10
TAB_HISTORY = 11
TAB_SETTINGS = 12
TAB_TECH_TREE = 13
TAB_ADVISORY = 14
TAB_PRIVATE_SECTORS = 15
TAB_STATS = 97
TAB_WORLDMAP = 98
TAB_DASHBOARD = 99

# TECHS # TECHNOLOGIES # TECHNOLOGY #TECHS #TECHNOLOGIES #TECHNOLOGY

i = 0
TECH_BASIC_INFRASTRUCTURE                   = i; i+= 1;
TECH_HOT_TURBINES                           = i; i+= 1;
TECH_CITY_PLANNING                          = i; i+= 1;
TECH_CROP_DIVERSIFICATION                   = i; i+= 1;
TECH_PRESERVATIVES                          = i; i+= 1;
TECH_HEAT_RECOVERY                          = i; i+= 1;
TECH_PUBLIC_SCHOOLS                         = i; i+= 1;
TECH_PRIVATE_SCHOOLS                        = i; i+= 1;
TECH_SANITATION                             = i; i+= 1;
TECH_LOBOTOMY                               = i; i+= 1;
TECH_AUTOMOBILE_INDUSTRY                    = i; i+= 1;
TECH_PUBLIC_TRANSPORT                       = i; i+= 1;
TECH_PUBLIC_PARKS                           = i; i+= 1;
TECH_MECHANIZED_FARMING                     = i; i+= 1;
TECH_FRACKING                               = i; i+= 1;
TECH_FRACKING_REGULATIONS                   = i; i+= 1;
TECH_AIRPORT                                = i; i+= 1;
TECH_URBANIZATION_I                         = i; i+= 1;
TECH_URBANIZATION_II                        = i; i+= 1;
TECH_URBANIZATION_III                       = i; i+= 1;
TECH_ANTIDEPRESSANTS                        = i; i+= 1;
TECH_DSM                                    = i; i+= 1;
TECH_POWER_GRID                             = i; i+= 1;
TECH_POWER_GRID_II                          = i; i+= 1;
TECH_CONVENIENCE_MACHINES                   = i; i+= 1;
TECH_MASSIVE_HYDRAULIC_FRACKING             = i; i+= 1;
TECH_REGULATED_MASSIVE_HYDRAULIC_FRACKING   = i; i+= 1;
TECH_AUTOCRACY                              = i; i+= 1;
TECH_DEMOCRACY                              = i; i+= 1;
TECH_TRANSISTOR                             = i; i+= 1;
TECH_NEWS_BROADCAST                         = i; i+= 1;
TECH_INTEGRATED_CIRCUIT                     = i; i+= 1;
TECH_CHEMICAL_PESTICIDES                    = i; i+= 1;
TECH_COMBINED_CYCLE                         = i; i+= 1;
TECH_CONTRACEPTIVES                         = i; i+= 1;
TECH_BIKE_LANES                             = i; i+= 1;
TECH_CAR_ORIENTED_PLANNING                  = i; i+= 1;
TECH_WALKABLE_CITIES                        = i; i+= 1;
TECH_GATED_COMMUNITIES                      = i; i+= 1;
TECH_RESEARCH_COMPUTERS                     = i; i+= 1;
TECH_SUBLIMINAL_MESSAGING                   = i; i+= 1;
TECH_SUBWAY                                 = i; i+= 1;
TECH_STROADS                                = i; i+= 1;
TECH_LARGE_SCALE_INTEGRATION                = i; i+= 1;
TECH_PROPAGANDA_MACHINE                     = i; i+= 1;
TECH_CIVIL_RIGHTS                           = i; i+= 1;
TECH_PERSONAL_COMPUTER                      = i; i+= 1;
TECH_SOCIALISM                              = i; i+= 1;
TECH_CAPITALISM                             = i; i+= 1;
TECH_TOTALITARIANISM                        = i; i+= 1;
TECH_ANOCRACY                               = i; i+= 1;
TECH_BALLISTIC_MISSILES                     = i; i+= 1; # +1 influence
TECH_V2_ROCKET                              = i; i+= 1; # +1 influence
TECH_NUCLEAR_BOMBS                          = i; i+= 1; # +2 influence
TECH_NUCLEAR_MISSILES                       = i; i+= 1; # +2 influence

TECH_FRACKING_KEY                           = i; i+= 1;
TECH_TRANSPORT_KEY                          = i; i+= 1;
'''    TECH_CHEMICAL_PESTICIDES : {
    TECH_COMBINED_CYCLE : {
    TECH_CONTRACEPTIVES : {
    TECH_BIKE_LANES : {
    TECH_CAR_ORIENTED_PLANNING : {
    TECH_WALKABLE_CITIES : {
    TECH_TRANSISTOR : {'''

# AGES #AGES # EPOCHS #EPOCHS

AGE_UNDARK                  = 0
AGE_SURVIVAL                = 1
AGE_FOUNDRY                 = 2
AGE_TRUST                   = 3
AGE_RECONSTRUCTION          = 4
AGE_2NDINDUSTRIAL           = 5
AGE_AUTOMATION              = 6
AGE_INVENTION               = 7
AGE_PROSPEROUS              = 8
AGE_SECURITY                = 9
AGE_WAR                     = 10
AGE_EXPANSION               = 11
AGE_INTEGRATION             = 12
AGE_GLOBALIZATION           = 13
AGE_INFORMATION             = 14
AGE_CYBER                   = 15
AGE_INTELLIGENCE            = 16
AGE_ROBOTICS                = 17
AGE_SPACE                   = 18
AGE_1STENERGY               = 19
AGE_WORLDWAR3               = 20
AGE_WORLDDOMINATION         = 21
AGE_SOLAR                   = 22

AGES = {
    AGE_UNDARK                : {
        'Name'              : '      Undark Epoch      ', # Access to builders, agriculture, import/export food 1910
        'Upgrade'           : {'$': GMULT*500,},
        'Infrastructure'    : 50,},
    AGE_SURVIVAL  : {
        'Name'              : '     Survival Epoch     ', # Ability to upgrade job categories. Reveal productivity. 1915
        'Upgrade'    : {'$': GMULT*5000,},
        'Infrastructure' : 200,},
    AGE_FOUNDRY  : {
        'Name'              : '     Foundry Epoch      ', # Introduces miners, oil import / energy production 1920
        'Upgrade'    : {'$': GMULT*15000,},
        'Infrastructure' : 200,},
    AGE_TRUST               : {
        'Name'              : '     Epoch of Trust     ', #  +10 fertility. Reveals Happiness, agencies. Happiness bonus to fertility. 1925
        'Upgrade'    : {'$': GMULT*40000,},
        'Infrastructure' : 800,},
    AGE_RECONSTRUCTION                : {
        'Name'              : '     Reconstruction     ', # Reveals science, research, and tech tree 1930
        'Upgrade'    : {'$': GMULT*150000,},
        'Infrastructure' : 1600,},
    AGE_2NDINDUSTRIAL                   : {
        'Name'              : '2nd Industry Revolution ', # Reveals custodials and pollution. Reveals sanity. 1935
        'Upgrade'    : {'$': GMULT*750000,},
        'Infrastructure' : 3200,},
    AGE_AUTOMATION                : {
        'Name'              : '     Automation Age     ', # Reveals hospitals. Reveals health. Immigration increases. 1940
        'Upgrade'    : {'$': GMULT*8500000,},
        'Infrastructure' : 6400,},
    AGE_INVENTION                 : {
        'Name'              : '   Epoch of Invention   ', # Immigration increases. 1945
        'Upgrade'    : {'$': GMULT*35000000,},
        'Infrastructure' : 12500,},
    AGE_PROSPEROUS                    : {
        'Name'              : '    Prosperous Epoch    ', # political style (autocrat or democrat) 1950
        'Upgrade'    : {'$': GMULT*250000000,},
        'Infrastructure' : 25000,},
    AGE_SECURITY                    : {
        'Name'              : '   Epoch of Security    ', # Reveals crime. Introduces riots, elections, and mutiny. 1955
        'Upgrade'    : {'$': GMULT*4000000000,},
        'Infrastructure' : 50000,},
    AGE_WAR                   : {
        'Name'              : '      Epoch of War      ', # Reveals defense. 1960
        'Upgrade'    : {'$': GMULT*75000000000,},
        'Infrastructure' : 100000,},
    AGE_EXPANSION                    : {
        'Name'              : '   Epoch of Expansion   ', # Expansion to War system: strategy, conquest 1965
        'Upgrade'    : {'$': GMULT*3200000000000,},
        'Infrastructure' : 80000,},
    AGE_INTEGRATION                      : {
        'Name'              : '  Epoch of Integration  ', # 2nd political style. 1975
        'Upgrade'    : {'$': GMULT*88000000000000,},
        'Infrastructure' : 200000,},
    AGE_GLOBALIZATION                     : {
        'Name'              : '  Age of Globalization  ', # 1985 
        'Upgrade'    : {'$': GMULT*270000000000000,},
        'Infrastructure' : 400000,},
    AGE_INFORMATION                      : {
        'Name'              : '     Information Age    ', # 1995
        'Upgrade'    : {'$': GMULT*270000000000000,},
        'Infrastructure' : 400000,},
    AGE_CYBER                     : {
        'Name'              : '      Cyber Epoch       ', # 2005
        'Upgrade'    : {'$': GMULT*5500000000000000,},
        'Infrastructure' : 800000,},
    AGE_INTELLIGENCE                      : {
        'Name'              : '  Age of Intelligence   ', # 2015
        'Upgrade'    : {'$': GMULT*5500000000000000,},
        'Infrastructure' : 800000,},
    AGE_ROBOTICS                     : {
        'Name'              : '     Age of Robotics    ', # 2025
        'Upgrade'    : {'$': GMULT*5500000000000000,},
        'Infrastructure' : 800000,},
    AGE_SPACE              : {
        'Name'              : '        Space Age       ', # 2035
        'Upgrade'    : {'$': GMULT*95000000000000000,},
        'Infrastructure' : 2500000,},
    AGE_1STENERGY                : {
        'Name'              : ' 1st Energy Revolution  ', # Type 1 civ
        'Upgrade'    : {'$': GMULT*2500000000000000000,},
        'Infrastructure' : 7500000,},
    AGE_WORLDWAR3               : {
        'Name'              : '      World War III     ',
        'Upgrade'    : {'$': GMULT*800000000000000000000,},
        'Infrastructure' : 30000000,},
    AGE_WORLDDOMINATION                : {
        'Name'              : '    World Domination    ',
        'Upgrade'    : {'$': GMULT*1000000000000000000000000,},
        'Infrastructure' : 80000000,},
    AGE_SOLAR       : {
        'Name'              : '       Solar Epoch      ',
        'Upgrade'    : {'$': GMULT*80000000000000000000000000000,},
        'Infrastructure' : 1000000000,},
    }



TECHNOLOGIES = {
    TECH_BASIC_INFRASTRUCTURE : {
        'name': 'Basic Infrastructure',
        'age': 4,
        'cost': GMULT*40000,
        'research': GMULT*500,
        'upkeep': {INFR : 1, SCIE : 1,},
        'pop': 100000,
        'description': ['+75% infrastructure from Construction', '+3 business growth', '+1 wealth'],
        'trust': 1,
        'stats': {
            'construction_infrastructure_mult' : 1.75,
            'business_growth_add' : 3,
            'wealth_add' : 1,
            }
        },
    TECH_HOT_TURBINES : {
        'name': 'Hot Turbines',
        'age': 4,
        'cost': GMULT*25000,
        'research': GMULT*2500,
        'upkeep': {},
        'description': ['+33% power production from oil', '+1 wealth'],
        'trust': 1,
        'stats': {
            'oil_export_mult' : 1.33,
            'wealth_add' : 1,
            }
        },
    TECH_CROP_DIVERSIFICATION : {
        'name': 'Crop Diversification',
        'age': 4,
        'cost': GMULT*15000,
        'research': GMULT*1000,
        'upkeep': {AGRI : 1, SCIE : 1,},
        'trust': 2,
        'description': ['+33% food production from Agriculture'],
        'stats': {
            'agriculture_food_mult' : 1.33,
            }
        },
    TECH_CITY_PLANNING : {
        'name': 'City Planning',
        'age': 5,
        'requires': [TECH_BASIC_INFRASTRUCTURE],
        'cost': GMULT*250000,
        'research': GMULT*2500,
        'upkeep': {INFR : 1,},
        'infrastructure_upkeep': 1,
        'pop': 200000,
        'description': ['+50% infrastructure from Construction', 'Double production from Environmental', '+1 wealth'],
        'trust': 1,
        'stats': {
            'infrastructure_per_population_add': 0.25,
            'construction_infrastructure_mult' : 1.5,
            'environmental_happiness_mult' : 2,
            'environmental_pollution_mult' : 2,
            'environmental_sanity_mult' : 2,
            'wealth_add' : 1,
            }
        },
    TECH_HEAT_RECOVERY : {
        'name': 'Heat Recovery Steam Generator',
        'age': 5,
        'requires': [TECH_HOT_TURBINES],
        'cost': GMULT*300000,
        'research': GMULT*20000,
        'upkeep': {HARV : 1, INFR : 1, DEFE : 1, SCIE : 1, HEAL : 1,},
        'description': ['+33% power production from oil', '+1 wealth'],
        'trust': 1,
        'stats': {
            'oil_export_mult' : 1.33,
            'wealth_add' : 1,
            }
        },
    TECH_PRESERVATIVES : {
        'name': 'Chemical Preservatives',
        'age': 5,
        'requires': [TECH_CROP_DIVERSIFICATION],
        'cost': GMULT*150000,
        'research': GMULT*1000,
        'upkeep': {SCIE : 1,},
        'description': ['+10% food production from Agriculture', 'Food decay reduced from 5% to 1%', '+1 pollution from agriculture'],
        'trust': 1,
        'stats': {
            'agriculture_food_mult' : 1.10,
            'food_decay_set' : 1,
            'agriculture_pollution_add': 1,
            }
        },
    TECH_PUBLIC_SCHOOLS : {
        'name': 'Public Schools',
        'requires': [TECH_CITY_PLANNING],
        'age': 5,
        'cost': GMULT*250000,
        'research': GMULT*9000,
        'upkeep': {SCIE : 1,},
        'pop': 50000,
        'description': ['+100% info from Innovation', 'Cheaper allocation rate upgrades'],
        'trust': 1,
        'stats': {
            'researchers_research_mult' : 2,
            'public_schools_researched': True,
            }
        },
    TECH_PUBLIC_TRANSPORT : {
        'name': 'Public Transport',
        'exclusive': [TECH_AUTOMOBILE_INDUSTRY],
        'requires': [TECH_CITY_PLANNING],
        'age': 5,
        'cost': GMULT*500000,
        'research': GMULT*20000,
        'upkeep': {INFR : 1,},
        'infrastructure_upkeep': 1,
        'pop': 250000,
        'trust': 1,
        'description': ['+10% power production from oil', '+3 business growth', '+1 wealth'],
        'key': TECH_TRANSPORT_KEY,
        'stats': {
            'oil_export_mult' : 1.1,
            'business_growth_add' : 3,
            'wealth_add' : 1,
            }
        },
    TECH_AUTOMOBILE_INDUSTRY : {
        'name': 'Subsidize Automotive Industry',
        'exclusive': [TECH_PUBLIC_TRANSPORT],
        'requires': [TECH_CITY_PLANNING, TECH_HEAT_RECOVERY],
        'age': 5,
        'cost': GMULT*500000,
        'research': GMULT*30000,
        'upkeep': {},
        'infrastructure_upkeep': 1,
        'pop': 180000,
        'trust': 3,
        'description': ['+3 wealth; +12 business growth', '+3 pollution per capita', 'increased infrastructure requirements'],
        'key': TECH_TRANSPORT_KEY,
        'stats': {
            'infrastructure_per_population_add': 0.5,
            'pollution_per_capita_add' : 3,
            'business_growth_add' : 12,
            'wealth_add' : 3,
            'health_per_capita_add': -5,
            }
        },
    TECH_AIRPORT : {
        'name': 'Airport',
        'age': 6,
        'requires': [TECH_TRANSPORT_KEY],
        'cost': GMULT*950000,
        'research': GMULT*35000,
        'upkeep': {GENERAL: 1, INFR : 1,},
        'infrastructure_upkeep': 1,
        'pop': 250000,
        'description': ['+20% power from exports', '+2 pollution per capita', '+2 wealth'],
        'stats': {
            'oil_export_mult' : 1.2,
            'food_export_mult' : 1.2,
            'pollution_per_capita_add' : 2,
            'wealth_add' : 2,
            }
        },
    TECH_URBANIZATION_I : {
        'name': 'Urbanization I',
        'age': 6,
        'requires': [TECH_AIRPORT],
        'cost': GMULT*1000000,
        'research': GMULT*8000,
        'upkeep': {UNEMPLOYED: 1, INFR : 1, GENERAL : 1,},
        'infrastructure_upkeep': 1,
        'pop': 500000,
        'description': ['+20% infrastructure from construction', '+1 pollution per capita', '+1 wealth'],
        'stats': {
            'construction_infrastructure_mult' : 1.2,
            'pollution_per_capita_add' : 1,
            'wealth_add' : 1,
            }
        },
    TECH_SANITATION : {
        'name': 'Sanitary Facilities',
        'age': 6,
        'cost': GMULT*250000,
        'research': GMULT*3500,
        'upkeep': {HEAL: 2, SCIE : 1,},
        'description': ['+100% health from Healthcare'],
        'trust': 2,
        'stats': {
            'healthcare_health_mult' : 2,
            }
        },
    TECH_MECHANIZED_FARMING : {
        'name': 'Mechanized Farming',
        'age': 6,
        'requires': [TECH_CITY_PLANNING, TECH_HEAT_RECOVERY, TECH_PRESERVATIVES],
        'cost': GMULT*2000000,
        'research': GMULT*15000,
        'upkeep': {AGRI: 2, INFR : 1,},
        'description': ['+75% food from agriculture', '+3 pollution from agriculture', '+1 wealth'],
        'trust': 1,
        'stats': {
            'agriculture_food_mult' : 1.75,
            'wealth_add' : 1,
            'agriculture_pollution_add' : 3,
            }
        },
    TECH_LOBOTOMY : {
        'name': 'Lobotomy',
        'age': 6,
        'requires': [TECH_SANITATION],
        'cost': GMULT*500000,
        'research': GMULT*48000,
        'upkeep': {HEAL: 2, SCIE : 2,},
        'description': ['Increased sanity from Healthcare',], #  'Decreased happiness from healthcare'
        'trust': -2,
        'stats': {
            'healthcare_sanity_mult' : 2,
            'healthcare_happiness_set' : -8,
            }
        },
    TECH_PUBLIC_PARKS : {
        'name': 'Public Parks',
        'age': 6,
        'requires': [TECH_CITY_PLANNING],
        'cost': GMULT*500000,
        'research': GMULT*5000,
        'upkeep': {ENVI : 1,},
        'infrastructure_upkeep': 1,
        'pop': 100000,
        'description': ['+50% happiness from Environmental', '+50% sanity from Environmental', '+1 wealth'],
        'trust': 2,
        'stats': {
            'environmental_happiness_mult' : 1.5,
            'environmental_sanity_mult' : 1.5,
            'wealth_add' : 1,
            }
        },
    TECH_FRACKING : {
        'name': 'Unrestricted Fracking',
        'exclusive': [TECH_FRACKING_REGULATIONS],
        'age': 6,
        'cost': GMULT*3000000,
        'research': GMULT*27500,
        'upkeep': {HARV : 1,},
        'description': ['+33% oil from Industry', '+50% pollution from Industry', '+50% health loss from Industry', '+2 wealth'],
        'trust': 2,
        'key': TECH_FRACKING_KEY,
        'stats': {
            'industry_oil_mult' : 1.33,
            'industry_pollution_mult' : 1.5,
            'industry_health_mult' : 1.5,
            'industry_happiness_mult' : 1.5,
            'wealth_add' : 2,
            }
        },
    TECH_FRACKING_REGULATIONS : {
        'name': 'Fracking Regulations',
        'exclusive': [TECH_FRACKING],
        'age': 6,
        'cost': GMULT*3800000,
        'research': GMULT*39000,
        'upkeep': {HARV : 1, SCIE : 1, ENVI : 1,},
        'description': ['+15% oil from Industry', '+10% health loss from Industry', '+1 wealth'],
        'key': TECH_FRACKING_KEY,
        'trust': 1,
        'stats': {
            'industry_oil_mult' : 1.15,
            'industry_pollution_mult' : 1.05,  # invisible +5% pollution from Industry 
            'industry_health_mult' : 1.1,
            'wealth_add' : 1,
            }
        },
    TECH_PRIVATE_SCHOOLS : {
        'name': 'Private Schooling',
        'requires': [TECH_CITY_PLANNING],
        'age': 6,
        'cost': GMULT*50000,
        'research': GMULT*2000,
        'upkeep': {},
        'description': ['+80% info from Private sector', '+3 business growth', '+1 wealth', 'Private sector raises allocation rate'],
        'trust': 1,
        'stats': {
            'business_growth_add' : 3,
            'wealth_add' : 1,
            'private_sector_research_mult': 1.8,
            'private_schools_researched': True,
            }
        },
    TECH_CHEMICAL_PESTICIDES : {
        'name': 'Chemical Pesticides',
        'age': 7,
        'requires': [TECH_SANITATION],
        'cost': GMULT*1000000,
        'research': GMULT*15000,
        'upkeep': {AGRI : 1, SCIE : 1,},
        'description': ['+25% food from Agriculture', '+2 pollution from Agriculture'],
        'trust': 1,
        'stats': {
            'agriculture_food_mult' : 1.25,
            'agriculture_pollution_add' : 2,
            }
        },
    TECH_COMBINED_CYCLE : {
        'name': 'Combined Cycle Power Plants',
        'age': 7,
        'requires': [TECH_HEAT_RECOVERY],
        'cost': GMULT*5000000,
        'research': GMULT*45000,
        'upkeep': {HARV : 2, INFR : 1, AGRI : 1, DEFE : 2, SCIE : 3,},
        'description': ['+50% power production from oil',],
        'trust': 1,
        'stats': {
            'oil_export_mult' : 1.5,
            }
        },
    TECH_CONTRACEPTIVES : {
        'name': 'Contraceptives',
        'age': 7,
        'requires': [TECH_SANITATION, TECH_CITY_PLANNING, TECH_PUBLIC_SCHOOLS],
        'cost': GMULT*1300000,
        'research': GMULT*40000,
        'upkeep': {SCIE : 1, HEAL : 1,},
        'pop': 25000,
        'description': ['Introduces Fertility controls to', '    Food & Medical Agency (FMA)', '+5% fertility', '+1 wealth'],
        'trust': 1,
        'stats': {
            'contraceptives' : True,
            'wealth_add': 1,
            }
        },
    TECH_BIKE_LANES : {
        'name': 'Dedicated Bike Lanes',
        'age': 7,
        'exclusive': [TECH_CAR_ORIENTED_PLANNING],
        'requires': [TECH_PUBLIC_PARKS],
        'cost': GMULT*750000,
        'research': GMULT*12000,
        'upkeep': {ENVI: 1,},
        'pop': 150000,
        'description': ['+25% happiness from Environmental', '+25% sanity from Environmental'],
        'trust': 1,
        'stats': {
            'environmental_happiness_mult': 1.25,
            'environmental_sanity_mult': 1.25,
            }
        },
    TECH_CAR_ORIENTED_PLANNING : {
        'name': 'Car-Oriented City Planning',
        'age': 7,
        'exclusive': [TECH_WALKABLE_CITIES, TECH_BIKE_LANES],
        'requires': [TECH_AUTOMOBILE_INDUSTRY],
        'cost': GMULT*2500000,
        'research': GMULT*25000,
        'upkeep': {SCIE : 2, INFR: 2, POLI : 2,},
        'infrastructure_upkeep': 1,
        'pop': 1000000,
        'description': ['+25% power production from oil', '+3 pollution per capita', '+1 wealth, +3 business growth'],
        'trust': 1,
        'stats': {
            'oil_export_mult': 1.25,
            'pollution_per_capita_add': 3,
            'wealth_add': 1,
            'business_growth_add': 3,
            }
        },
    TECH_WALKABLE_CITIES : {
        'name': 'Walkable Cities',
        'age': 7,
        'requires': [TECH_PUBLIC_TRANSPORT],
        'cost': GMULT*2200000,
        'research': GMULT*13000,
        'upkeep': {SCIE : 1, INFR: 1,},
        'infrastructure_upkeep': 1,
        'pop': 500000,
        'description': ['+15% happiness from Environmental', '+3 business growth', '+2 wealth'],
        'trust': 1,
        'stats': {
            'environmental_happiness_mult': 1.15,
            'wealth_add': 2,
            'business_growth_add': 3,
            }
        },
    TECH_POWER_GRID : {
        'name': 'Power Grid I',
        'age': 7,
        'requires': [TECH_CITY_PLANNING],
        'cost': GMULT*4500000,
        'research': GMULT*45000,
        'upkeep': {HARV : 1, INFR : 1, SCIE : 1, HEAL : 1, GENERAL: 1,},
        'infrastructure_upkeep': 1,
        'description': ['+15% production from agriculture,', '    construction, health & industry', '+2 wealth', 'increased infrastructure requirements'],
        'trust': 1,
        'stats': {
            'infrastructure_per_population_add': 1,
            'agriculture_food_mult': 1.15,
            'construction_infrastructure_mult': 1.15,
            'industry_oil_mult': 1.15,
            'healthcare_health_mult': 1.15,
            'wealth_add': 2,
            }
        },
    TECH_CONVENIENCE_MACHINES : {
        'name': 'Mass Produced Appliances',
        'requires': [TECH_POWER_GRID],
        'age': 7,
        'cost': GMULT*2000000,
        'research': GMULT*85000,
        'upkeep': {},
        'description': ['+10% power production from oil', '+2 pollution per capita', '+1 wealth', '+5 business growth'],
        'trust': 1,
        'stats': {
            'oil_export_mult': 1.1,
            'pollution_per_capita_add': 2,
            'wealth_add': 1,
            'business_growth_add': 5,
            }
        },
    TECH_URBANIZATION_II : {
        'name': 'Urbanization II',
        'age': 8,
        'requires': [TECH_URBANIZATION_I],
        'cost': GMULT*40000000,
        'research': GMULT*20000,
        'upkeep': {UNEMPLOYED: 1, INFR : 1, POLI: 1, DEFE: 1, GENERAL : 1,},
        'infrastructure_upkeep': 1,
        'pop': 1000000,
        'description': ['+20% infrastructure from construction', '+2 pollution per capita', '+2 wealth'],
        'stats': {
            'construction_infrastructure_mult' : 1.2,
            'pollution_per_capita_add': 2,
            'wealth_add': 2,
            }
        },
    TECH_DEMOCRACY : {
        'name': 'Democracy',
        'exclusive': [TECH_AUTOCRACY],
        'age': 8,
        'cost': GMULT*40000000,
        'research': GMULT*190000,
        'upkeep': {DEFE : 1, SCIE : 1, HEAL : 1},
        'description': ['+2 wealth', '+10 business growth', '+ trust'],
        'trust': 5,
        'stats': {
            'democracy': True,
            'business_growth_add': 10,
            'wealth_add': 2,
            }
        },
    TECH_AUTOCRACY : {
        'name': 'Autocracy',
        'exclusive': [TECH_DEMOCRACY],
        'age': 8,
        'cost': GMULT*60000000,
        'research': GMULT*70000,
        'upkeep': {HARV : 1, INFR : 1, AGRI : 1, ENVI : 1,},
        'description': ['+5 influence', '-10 business growth', '- trust'],
        'trust': -5,
        'stats': {
            'autocracy': True,
            'business_growth_add': -10,
            'influence_add': 5,
            }
        },
    TECH_ANTIDEPRESSANTS : {
        'name': 'Antidepressants',
        'requires': [TECH_SANITATION],
        'age': 8,
        'cost': GMULT*350000,
        'research': GMULT*45000,
        'upkeep': {HEAL: 1,},
        'description': ['+50% sanity from Healthcare',],
        'trust': 1,
        'stats': {
            'healthcare_sanity_mult' : 1.5,
            }
        },
    TECH_DSM : {
        'name': 'DSM Psychology Manual',
        'age': 8,
        'cost': GMULT*250000,
        'research': GMULT*75000,
        'upkeep': {HEAL: 1,},
        'description': ['+50% sanity from Healthcare',],
        'trust': 1,
        'stats': {
            'healthcare_sanity_mult' : 1.5,
            }
        },
    TECH_GATED_COMMUNITIES : {
        'name': 'Gated Communities',
        'age': 8,
        'requires': [TECH_PUBLIC_PARKS, TECH_PRIVATE_SCHOOLS],
        'cost': GMULT*5000000,
        'research': GMULT*25000,
        'upkeep': {INFR: 1, ENVI: 1, GENERAL: 1,},
        'infrastructure_upkeep': 1,
        'description': ['+2 wealth', '+3 business growth'],
        'trust': 2,
        'stats': {
            'business_growth_add': 3,
            'wealth_add': 2,
            }
        },
    TECH_TRANSISTOR : {
        'name': 'Transistor',
        'age': 8,
        'cost': GMULT*1500000,
        'research': GMULT*95000,
        'upkeep': {SCIE : 1,},
        'trust': 1,
        'description': ['Required precursor technology'],
        },
    TECH_POWER_GRID_II : {
        'name': 'Power Grid II',
        'age': 8,
        'requires': [TECH_POWER_GRID],
        'cost': GMULT*25000000,
        'research': GMULT*120000,
        'upkeep': {HARV : 1, INFR : 1, SCIE : 1, HEAL : 1, GENERAL: 1,},
        'infrastructure_upkeep': 2,
        'description': ['+25% production from agriculture,', '    construction, health & industry', '+2 wealth', 'increased infrastructure requirements'],
        'trust': 2,
        'stats': {
            'infrastructure_per_population_add': 1,
            'agriculture_food_mult': 1.25,
            'construction_infrastructure_mult': 1.25,
            'industry_oil_mult': 1.25,
            'healthcare_health_mult': 1.25,
            'wealth_add': 2,
            }
        },
    TECH_RESEARCH_COMPUTERS : {
        'name': 'Research Computers',
        'age': 9,
        'requires': [TECH_INTEGRATED_CIRCUIT, TECH_POWER_GRID_II],
        'cost': GMULT*75000000,
        'research': GMULT*240000,
        'upkeep': {SCIE : 2,},
        'description': ['+100% info from Innovation', '+1 wealth'],
        'trust': 2,
        'stats': {
            'researchers_research_mult': 2,
            'wealth_add': 1,
            }
        },
    TECH_SUBLIMINAL_MESSAGING : {
        'name': 'Subliminal Messaging',
        'age': 9,
        'requires': [TECH_NEWS_BROADCAST],
        'cost': GMULT*5000000,
        'research': GMULT*80000,
        'upkeep': {SCIE : 1,},
        'description': ['+5% happiness per capita'],
        'trust': -2,
        'stats': {
            'researchers_research_mult': 1.5,
            'business_growth_add': 5,
            'wealth_add': 1,
            }
        },
    TECH_NEWS_BROADCAST : {
        'name': 'Public Broadcast System',
        'age': 9,
        'requires': [TECH_TRANSISTOR, TECH_POWER_GRID_II],
        'cost': GMULT*2000000,
        'research': GMULT*125000,
        'upkeep': {SCIE : 1,},
        'description': ['+50% info from Innovation', '+5 business growth', '+1 wealth'],
        'trust': 1,
        'stats': {
            'researchers_research_mult': 1.5,
            'business_growth_add': 5,
            'wealth_add': 1,
            }
        },
    TECH_INTEGRATED_CIRCUIT : {
        'name': 'Integrated Circuit',
        'age': 9,
        'requires': [TECH_TRANSISTOR],
        'cost': GMULT*3000000,
        'research': GMULT*175000,
        'upkeep': {SCIE : 1,},
        'description': ['Required precursor technology'],
        'trust': 1,
        },
    TECH_MASSIVE_HYDRAULIC_FRACKING : {
        'name': 'Massive Hydraulic Fracking',
        'exclusive': [TECH_REGULATED_MASSIVE_HYDRAULIC_FRACKING],
        'requires': [TECH_FRACKING_KEY],
        'age': 9,
        'cost': GMULT*25000000,
        'research': GMULT*275000,
        'upkeep': {HARV : 3, ENVI: 2, HEAL: 3, DEFE: 2, POLI: 1,},
        'trust': -1,
        'description': ['+50% oil from Industry', '+25% pollution from Industry', '+2 wealth'], 
        'stats': {
            'industry_oil_mult': 1.6,
            'industry_pollution_mult': 1.25,
            'wealth_add': 2,
            }
        },
    TECH_REGULATED_MASSIVE_HYDRAULIC_FRACKING : {
        'name': 'Regulated Massive Hydraulic Fracking',
        'exclusive': [TECH_MASSIVE_HYDRAULIC_FRACKING],
        'requires': [TECH_FRACKING_KEY],
        'age': 9,
        'cost': GMULT*30000000,
        'research': GMULT*385000,
        'upkeep': {HARV : 2, INFR : 1, HEAL : 2, ENVI: 2, POLI: 1,},
        'description': ['+40% oil from Industry', '+1 wealth'], # invisible +10% pollution from Industry 
        'stats': {
            'industry_oil_mult': 1.4,
            'wealth_add': 1,
            }
        },
    TECH_SUBWAY : {
        'name': 'Subway System',
        'age': 9,
        'requires': [TECH_PUBLIC_TRANSPORT, TECH_POWER_GRID_II],
        'cost': GMULT*500000000,
        'research': GMULT*350000,
        'upkeep': {INFR : 2,},
        'infrastructure_upkeep': 2,
        'pop': 2000000,
        'trust': 1,
        'description': ['+15% power production from oil', '+1 wealth', 'increased infrastructure requirements'],
        'stats': {
            'infrastructure_per_population_add': 0.33,
            'oil_export_mult': 1.15,
            'pollution_per_capita_add': 1,
            'wealth_add': 1,
            }
        },
    TECH_STROADS : {
        'name': 'Stroads',
        'age': 9,
        'requires': [TECH_AUTOMOBILE_INDUSTRY],
        'cost': GMULT*300000000,
        'research': GMULT*180000,
        'upkeep': {INFR : 2, POLI : 1, ENVI : 1, HEAL : 1,},
        'infrastructure_upkeep': 2,
        'pop': 1500000,
        'trust': -1,
        'description': ['+25% power production from oil', '+3 business growth', 'increased infrastructure requirements'],
        'stats': {
            'infrastructure_per_population_add': 0.15,
            'oil_export_mult': 1.25,
            'business_growth_add': 3,
            'pollution_per_capita_add': 2,
            }
        },
    TECH_LARGE_SCALE_INTEGRATION : {
        'name': 'Large Scale Integrated Chips',
        'age': 10,
        'requires': [TECH_RESEARCH_COMPUTERS],
        'cost': GMULT*75000000,
        'research': GMULT*550000,
        'upkeep': {SCIE : 1,},
        'trust': 1,
        'description': ['Required precursor technology'],
        },
    TECH_URBANIZATION_III : {
        'name': 'Urbanization III',
        'age': 10,
        'requires': [TECH_URBANIZATION_II, TECH_POWER_GRID_II],
        'cost': GMULT*120000000,
        'research': GMULT*250000,
        'upkeep': {UNEMPLOYED: 1, INFR : 1, POLI: 1, DEFE: 1, HEAL: 1, SCIE: 1, GENERAL : 1,},
        'infrastructure_upkeep': 1,
        'pop': 2000000,
        'trust': -1,
        'description': ['+20% infrastructure from construction', '+3 pollution per capita', '+3 wealth'],
        'stats': {
            'construction_infrastructure_mult' : 1.2,
            'pollution_per_capita_add': 3,
            'wealth_add': 3,
            }
        },
    TECH_CIVIL_RIGHTS : {
        'name': 'Civil Rights',
        'age': 11,
        'requires': [TECH_DEMOCRACY],
        'exclusive': [TECH_PROPAGANDA_MACHINE],
        'cost': GMULT*55000000,
        'research': GMULT*200000,
        'upkeep': {UNEMPLOYED: 2, GENERAL: 1,},
        'infrastructure_upkeep': 1,
        'trust': 5,
        'description': ['While happiness is >= 75%,', '    productivity improves by 5%', '+5 business growth'], # also while happiness <= 25, rioting increases 400%
        'stats': {
            'civil_rights': True,
            'business_growth_add': 5,
            }
        },
    TECH_PROPAGANDA_MACHINE : {
        'name': 'Propaganda Machine',
        'age': 11,
        'requires': [TECH_NEWS_BROADCAST, TECH_RESEARCH_COMPUTERS],
        'exclusive': [TECH_CIVIL_RIGHTS],
        'cost': GMULT*35000000,
        'research': GMULT*300000,
        'upkeep': {GENERAL: 1, DEFE : 1, SCIE : 2, POLI : 1,},
        'infrastructure_upkeep': 1,
        'trust': -5,
        'description': ['+5% total happiness', 'Harvesting, Military, and Police', '    no longer lower happiness', '- trust'],
        'stats': {
            'happiness_per_capita_add': 5,
            'industry_happiness_mult': 0,
            'police_happiness_mult': 0,
            'military_happiness_mult': 0,
            }
        },
    TECH_PERSONAL_COMPUTER : {
        'name': 'Personal Computer',
        'age': 12,
        'requires': [TECH_LARGE_SCALE_INTEGRATION],
        'cost': GMULT*1000000000,
        'research': GMULT*750000,
        'upkeep': {INFR : 1, DEFE : 1, SCIE : 1, HEAL : 1,},
        'infrastructure_upkeep': 1,
        'trust': 2,
        'description': ['+25% power production from', '    oil, solar, and nuclear', '+5 business growth', '+2 wealth'],
        'stats': {
            'oil_export_mult': 1.25,
            'solar_export_mult': 1.25,
            'nuclear_export_mult': 1.25,
            'wealth_add': 2,
            'business_growth_add': 5,
            }
        },
    TECH_CAPITALISM : {
        'name': 'Capitalism',
        'requires': [TECH_DEMOCRACY],
        'exclusive': [TECH_SOCIALISM],
        'age': 12,
        'cost': GMULT*1000000000,
        'research': GMULT*1500000,
        'upkeep': {DEFE : 2, SCIE : 2, HEAL : 2, HARV: 1, INFR: 1, GENERAL: 1,},
        'trust': 1,
        'description': ['+3 wealth, +1 influence', '+10 business growth', '+15% power from exports & trade'],
        'stats': {
            'capitalism': True,
            'business_growth_add': 10,
            'wealth_add': 3,
            'influence_add': 1,
            'oil_export_mult': 1.15,
            'food_export_mult': 1.15,
            'warmachines_export_mult': 1.15,
            'trade_mult': 1.15,
            }
        },
    TECH_SOCIALISM : {
        'name': 'Socialism',
        'requires': [TECH_DEMOCRACY],
        'exclusive': [TECH_CAPITALISM],
        'age': 12,
        'cost': GMULT*2500000000,
        'research': GMULT*750000,
        'upkeep': {GENERAL: 2,},
        'trust': 2,
        'description': ['+1 wealth, +2 influence', '+10% productivity'],
        'stats': {
            'socialism': True,
            'productivity_add': 10,
            'wealth_add': 1,
            'influence_add': 2,
            }
        },
    TECH_ANOCRACY : {
        'name': 'Anocracy',
        'requires': [TECH_AUTOCRACY],
        'exclusive': [TECH_TOTALITARIANISM],
        'age': 12,
        'cost': GMULT*1000000000,
        'research': GMULT*1800000,
        'upkeep': {GENERAL: 2,},
        'trust': 1,
        'description': ['+2 wealth, +1 influence', '+20 business growth', '+5% productivity'],
        'stats': {
            'anocracy': True,
            'business_growth_add': 20,
            'wealth_add': 2,
            'influence_add': 1,
            'productivity_add': 5,
            }
        },
    TECH_TOTALITARIANISM : {
        'name': 'Totalitarianism',
        'requires': [TECH_AUTOCRACY],
        'exclusive': [TECH_ANOCRACY],
        'age': 12,
        'cost': GMULT*3200000000,
        'research': GMULT*1200000,
        'upkeep': {GENERAL: 2,},
        'trust': -5,
        'description': ['+5 influence', 'full control over private sector', '- trust'], # 0 private sector, all is public now. Public is taxed at private sector rate.
        'stats': {
            'totalitarianism': True,
            'influence_add': 5,
            'business_growth_set': 0,
            }
        },
    }


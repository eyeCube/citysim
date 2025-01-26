from const import *
import ui
import advice

import tcod
from tcod import libtcodpy
import time
import math
import random
import textwrap
#from input_handlers import handle_keys

'''

ideas:

crime can be solved by prison
    "solved"

health causes deaths
    the lower the health per capita is, the higher the population decay.

events:
    cold front for a 2+ month period
        -30% food production
        -10% oil production
        homeless (unemployed people with no infrastructure) die
    drought for a 2+ month period
        -50% food production
    pathogen for a 3+ month period
        -10 health per capita
    plague for a 4+ month period
        -50 health per capita
    


starts with just builders, then adds farmers, then miners
    (have to start with more $)
tutorial tooltips whenever a new mechanic appears
    explain aging up, upgrading, play/pause, every mechanic
    also have dedicated help page
pause game when stock is low, alert player (setting, default ON)
slow game down slightly
people don't all die when food is out, you just lose a lot of people (pop decay is up to 25%?)


human modification OR machine intelligence
human science > chimera people OR undead soldiers OR gene splicing
undead soldiers >
    +$10 upkeep per soldier
    soldier strength x1.5
    mutually exclusive:
        artificial life
        
chimera people >
    +$10 upkeep per citizen
    +10% fertility maximum
    mutually exclusive:
        mole people
            underground habitation:
                require half as much infrastructure (for all jobs and citizens)
            auto repair:
                running out of infrastructure results in loss of power instead of loss of employment.
        rabbit people
            rapid reproduction:
                fertility +50%
                fertility maximum +50%
        cat people
            healing vibrations:
                health maximum +100%
        insect people
            chitin armor:
                soldier strength +100%
        lizard people
            sun basking:
                require 0 energy to employ lizard people


TODO board

implement:
    contraceptives_researched

Agencies
    all mechanics implemented, tested
weapons / combat
World map
Disabled / veterans / homeless / etc. categories
more bills / techs
    through all ages
events
weather / climate
    drought
    flooding
    tsunami
    earthquake
    volcano
    thunder storm (infrastructure damage)
    wildfire
    building fire
    car fire
warning / alert dialogue box when food is low, etc.
advisory
    gives tips on gameplay
techs have other requirements
    new techs can appear after any month passes (add to month pass func)
    population requirement
    health requirement (low health resulting in a new healthcare tech being developed out of necessity, etc.)
simulation speed runs at 1 sec/sec, 1 min/sec, etc. instead of just x1, x2, etc.

play test!

'''

class Game:

    TIME_INTERVALS = [86400, 1800, 30, 1, 0.11666, 0.05832, 0.03333]
    TIME_INTERVALS_TEXT = ["1 s/s", "1 m/s", "1 hr/s", "1 day/s", "1 wk./s", "2 wk./s", "1 mo./s"]
    speed = 3
    time_interval_value = 1 # set by code
    values_dirty = True
    tile_w = 12
    tile_h = 16
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "tileset_12x16.png", 16, 16, [i for i in range(256)]
    )

    KEY_COMMANDS = {
        tcod.event.KeySym.UP: "move N",
        tcod.event.KeySym.DOWN: "move S",
        tcod.event.KeySym.LEFT: "move W",
        tcod.event.KeySym.RIGHT: "move E",
    }
    
                        #       0                   1                   2                   3                   4                   5                       6                   7           
    FOOD_DISTRIBUTION       = ["None / Starving", "Critical / Famished","Poor / Hungry","Fair / Rationing", "Good / Sated", "Excellent / Well-fed", "Excessive / Over-fed", "Superfluous / Over-fed",]
    FOOD_DISTRIBUTION2      = ["Starving", "Famished", "Hungry", "Rationing", "Sated", "Well-fed", "Over-fed", "Over-fed",]
    FOOD_QUALITY            = ["Abysmal", "Paltry", "Poor", "Deficient", "Modest", "Fair", "Good", "Great", "Excellent", "Extraordinary", "Perfect"]
    AGENCY_COMMERCE_FEES    = ["Minimal", "Discounted", "Acceptable", "High", "Prohibitive", "Extortionate"]
    HOUSING_COSTS           = ["Minimal", "Low", "Discounted", "Standard", "High", "Prohibitive", "Extortionate", "Outrageous"]
    AGENCY_TRAVEL_POLICIES  = ["Welcoming", "Relaxed", "Controlled", "Strict", "Quarantine", "Shut-down"]
    AGENCY_BORDER_CONTROL   = ["Open to all", "Open to most", "Open to some", "Locked down", "Militarized"]
    SECTOR_FUNDING          = ["Poor", "Sub-par", "Meeting goals", "Exceeding goals", "Bonus funding"]
    TAXES                   = ["Negligible", "Inconsequential", "Nominal", "Low", "Standard", "Fair", "Admissible", "Steep", "Excessive", "Unreasonable", "Exorbitant", "Extortionate", "Outrageous", "Heinous", "Criminal"]
    PUNISHMENT              = ["Slap on wrist", "Minimal force", "Sublethal force", "Lethal force", "Militarized", "Kill on sight"] # for felons
    CORRECTIONS             = ["No rehab", "Minimal", "Re-education", "Robust programs", "Exceptional", "Propagandized"]
    ENVIRONMENTAL_POLICY    = ["Under the rug", "Some recycling", "Moderate", "Superior", "Extensive", "Comprehensive"]
    GROWTH_INFRASTRUCTURE   = ["Methodical", "Moderate", "Agile", "Rapid", "Extreme", "Unbridled"]
    BIRTH_CONTROL           = ["1 / family max.", "2 / family max.", "3 / family max.", "4 / family max.", "None"]
    PENSIONS_DICT           = {0:"None", 1:"Negligible", 3:"Minimal", 5:"Poor", 7:"Fair", 9:"Good", 12:"Generous", 15:"Ample", 18:"Munificent"}
    HEALTH_INSURANCE_DICT   = {0:"None", 1:"Negligible", 25:"Minimal", 60:"Poor", 80:"Fair", 88:"Good", 95:"Ample", 100:"Munificent"}
    INCOME_ASSISTANCE_DICT  = {0:"None", 1:"Negligible", 4:"Minimal", 7:"Poor", 11:"Fair", 15:"Good", 20:"Generous", 25:"Ample", 30:"Munificent"}
    AGENCY_COMMERCE_FEES_TRUST = [2, 0, -1, -4, -9, -16]
    GROWTH_INFRASTRUCTURE_RATES = [.75, .88, 1, 1.13, 1.25, 1.38]
    INFRASTRUCTURE_DECAY_RATES = [0.8, 0.9, 1, 1.1605, 1.3, 1.45]
    FOOD_DISTRIBUTION_WASTE_RATE = [0, 1, 4, 9, 16, 25, 36, 49] # added percent
    FUNDING_EDUCATION_RESEARCH = [-50, -40, -30, -20, -10, 0]
    WAGES = [0.34, 0.5, 0.67, 0.78, 0.89, 1, 1.11, 1.23, 1.35, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10]
    FULLTIME_HOURS = [16, 24, 32, 40, 50, 60, 80, 100]
    
    mouse_clicking = False
    mouse_released = False
    mouse_held = False
    shift_held = False
    ctrl_held = False
    alt_held = False
    
    paused = True
    show_gdp = False
    
    contraceptives_researched = False
    democracy_researched = False
    autocracy_researched = False
    civil_rights_researched = False
    private_schools_researched = False
    public_schools_researched = False

    tab_groups = [TAB_SECTORS, TAB_ADVISORY, TAB_DASHBOARD, TAB_GAME]
    
    # sector allocation

    harvesting_power = 0 # power generated -- separate from upkeep costs (power may not always be generated, values fluctuate)
    harvesting_resources = 4
    harvesting_required_infrastructure = 2
    harvesting_workforce = -1
    harvesting_physical = -40
    harvesting_mental = 0
    harvesting_happiness = -8
    harvesting_pollution = 10

    infrastructure_infrastructure = 2.334
    infrastructure_resources = -1
    infrastructure_workforce = -1
    infrastructure_pollution = 2
    infrastructure_physical = -16

    agriculture_required_infrastructure = 1
    agriculture_food = 24
    agriculture_workforce = -1
    agriculture_physical = -8
    agriculture_pollution = 1

    defense_required_infrastructure = 2
    defense_weapons = 1 # war machines, per mille (1000 points here == 1 war machine)
    defense_workforce = -1
    defense_physical = 0
    defense_mental = -48
    defense_pollution = 3
    defense_resources = -1
    defense_happiness = -16

    police_required_infrastructure = 1
    police_workforce = -1
    police_mental = -16
    police_happiness = -32
    police_crime = -64

    science_required_infrastructure = 2
    science_research = 3
    science_workforce = -1
    science_resources = -1
    
    qol_mental = 16
    qol_pollution = -8
    qol_happiness = 24
    qol_workforce = -1

    hospitals_required_infrastructure = 1
    hospitals_physical = 64
    hospitals_mental = 32
    hospitals_happiness = -4
    hospitals_workforce = -1

    

    # special stats
    land                    = round(9950 + random.random()*100) # sq km
    water                   = round(150 + random.random()*100)
    income_inequality       = 1
    income_inequality_actual= 1
    diplomacy               = {GROUP_ALLIES:0, GROUP_AXIS:0, GROUP_NEUTRAL:0,} # UNUSED
    tourism                 = 0     
    wealth                  = 1     # affects tourism, wages, and business productivity. 1 wealth == $1 bil spent on improvements. Cannot be negative.
    trust                   = 5     # affected by choices in technology. Affects diplomatic tension and civilian happiness.
    trust_actual            = 0
    influence               = 0     # affects soldier strength  and age up cost. Cannot be negative.
    business_growth         = 6     # percentage of total incoming workforce that will be in private sector (businesses, making $ by investor taxes)
    riot_chance             = 0     # percentage chance of a riot breaking out this coming month, provided the conditions are right (low enough happiness or sanity; age requirement is met, etc.)
    conscription_rate       = 0     # per mille of people set to become soldiers this coming month, provided the conditions are right (good happiness, age req. met).
                                    # IDEA: Prioritize unemployed, then private sector, then public sector workers (customizable ?)


    # market

    market_value_food = 200
    market_value_oil = 100
    market_value_bombs = 100
    market_value_goods = 100

    food_boxes_to_kg = 15
    oil_barrels_to_gallons = 42
    buying_resources = 1 # resources bought per point
    buying_resources_economy = -48 # $ lost per point
    buying_food = 1
    buying_food_economy = -4
    selling_resources = -1 # resources sold per point
    selling_resources_economy = 24 # $ gained per point
    selling_food = -1
    selling_food_economy = 2
    buying_warmachines = 1
    buying_warmachines_economy = -1600000
    selling_warmachines = -1
    selling_warmachines_economy = 400000
    power_production_solar = 32 # starts lower but eventually is more effective
    power_production_nuclear = 48
    
    buying_resources_points = 0
    buying_food_points = 0
    selling_resources_points = 0
    selling_food_points = 0

    # agencies

    market_resources_set            = False
    market_food_set                 = False
    spending_agency_food            = 0
    spending_agency_zoning          = 0
    spending_agency_education       = 0
    spending_agency_commerce        = 0
    spending_agency_revenue         = 0
    spending_agency_justice         = 0
    spending_agency_homeland        = 0
    spending_agency_environmental   = 0
    spending_agency_labor           = 0
    spending_agency_social_services = 0
    agency_commerce_fees            = 0 #1
    trade                           = 1     # multiplier for Commerce Agency
    travel_policy                   = 0
    border_control                  = 1
    birth_control                   = 4
    food_distribution               = 3 # boxes per capita distributed monthly
    food_distribution_efficiency    = 4 # change in health/happiness per ton per capita distributed
    #taxes                           = 7
    civilian_taxing                 = 8
    investor_taxing                 = 8
    sales_taxing                    = 8
    punishment                      = 1
    corrections                     = 0
    environmental_policy            = 0
    growth_infrastructure_rate      = 1
    funding_education               = 0
    wages                           = 5
    safety_law                      = 4
    housing_subsidies               = 4
    fulltime_hours                  = 3
    health_insurance_policy         = 0
    veteran_pension_policy          = 7
    income_assistance_policy        = 6
    import_pollution                = False
    export_pollution                = False
    power_income_pollution_trade    = 0

    # output parameters

    turn = 0
    year = 1920
    month = 1
    day = 1

    popratio = 0
    population_gross_growth = 0
    population_gross_loss = 0
    population_growth = 0
    population_decay = 0 # percent
    population_deaths_poor_health_percent = 0
    population = (98+4*random.random())*GMULT
    allocation_speed = 250
    allocation_speed_actual = 0
    allocation_speed_maximum = allocation_speed
    allocation_speed_income = 0
    number_allocation_upgrades = 0
    
    civilians = 0
    population_max = 300*GMULT
    population_max_actual = 0
    prisoners = 0
    disabled = 0    # number of people who cannot work or fight. Combat can result in disabled people (casualties could be separate but that's a lot of categories..)
    private_sector = (business_growth*random.random()*0.1 + business_growth*0.95)*0.01*population # number of people working in the private sector; business owners, and employees.
    private_sector_research = 1
    #casualties = 0
    veterans = 0
    retirees = 0
    workforce = 0
    illegals = 0
    homeless = 0
    soldiers = 0    # active duty army personnel
    reserves = 0    # reserve duty / militia (still work in public or private sector as well)
    soldier_strength = 0
    births_per_month = 0
    deaths_per_month = 0
    natural_deaths_per_month = 0
    starve_per_month = 0
    murders_per_month = 0 # gun violence from police and crime and domestic violence etc.
    deaths_per_month_from_terrorists = 0
    cloning_per_month = 0
    
    #militia                             = 0             # percentage of civilian force that can be drafted on moment's notice

    age_max                             = 22
    age                                 = 0
    existing_infrastructure             = 220*GMULT
    unused_infrastructure               = 0
    unused_infrastructure_prev          = unused_infrastructure
    unused_infrastructure_delta         = 0
    infrastructure_growth               = 1
    existing_infrastructure_decay       = 12.5  # percent
    infrastructure_income_decay         = 0
    infrastructure_delta                = 0
    infrastructure_usage_population     = 0
    infrastructure_usage_private        = 0
    infrastructure_usage_harvesting     = 0
    infrastructure_usage_agriculture    = 0
    infrastructure_usage_defense        = 0
    infrastructure_usage_science        = 0
    infrastructure_usage_hospitals      = 0
    infrastructure_usage_police         = 0
    infrastructure_usage_public_sector  = 0
    
    __starting_power                    = 0
    __testing_power                     = 1000000000000000000000000000
    
    research                            = 0 #13371337133713371337
    research_income                     = 0
    research_decay                      = 0

    power                               = __testing_power
    power_income                        = 0             # economy
    power_income_previous               = 0
    power_income_delta                  = 0
    power_income_export                 = 0
    power_income_import                 = 0
    power_income_upkeep_costs           = 0
    power_income_agency_gross           = 0
    power_income_agency_loss            = 0
    power_income_ha_agency_gross        = 0
    power_income_ha_agency_loss         = 0
    power_income_fma_agency_loss        = 0
    power_income_ca_agency_gross        = 0
    power_income_gea_agency_loss        = 0
    power_income_ra_agency_gross        = 0
    power_income_ja_agency_loss         = 0
    power_income_infrastructure_upkeep  = 0
    power_income_public_sector_upkeep   = 0
    power_income_social_programs_upkeep = 0
    infrastructure_upkeep_value         = 1 # cost per infrastructure
    infrastructure_per_population       = 1 # extra infra. required per population member
    private_tax_income                  = 0
    public_tax_income                   = 0
    property_tax_income                 = 0
    
    food                                = 2500*GMULT
    food_income                         = 0
    food_decay                          = 5            # percent
    food_waste                          = 0             # percent
    food_income_decay                   = 0
    food_income_agriculture             = 0
    food_income_commerce                = 0
    food_income_distribution            = 0
    
    resources                           = 300*GMULT           # oil
    resources_income                    = 0
    resources_income_industry           = 0
    resources_income_commerce           = 0
    resources_income_public             = 0
    
    warmachines                         = 0
    warmachines_income                  = 0
    warmachines_decay                   = 0
    pollution                           = 2000000*GMULT
    pollution_income                    = 0
    pollution_per_capita                = 1 # extra pollution per population member
    pollution_ugpm3                     = 10
    happiness                           = 0
    happiness_bonus                     = 50
    physical                            = 0
    physical_bonus                      = 30
    mental                              = 0
    mental_bonus                        = 45
    crime                               = 0
    fertility                           = 1
    fertility_y                         = 0
    immigration                         = 3*GMULT*0.1
    immigration_actual                  = 0
    emigration                          = 0
    emigration_actual                   = 0
    productivity                        = 100
    productivity_bonus                  = 0
    private_sector_productivity         = 100
    intelligence                        = 0     # affects gullibility. Resistance to propaganda; + info gathering; + riots & mutiny
    intelligence_bonus                  = 75

    threat_level                        = 0

    time_since_last_turn                = 0
    last_time                           = time.time()

    mouse_x = 0
    mouse_y = 0

    advice = []
    techs = {}
    for k,v in TECHNOLOGIES.items():
        techs.update({k:v})
    list_available_techs = []
    list_purchased_techs = []
    list_disabled_techs = []
    
    population_upkeeps = {
        GENERAL: -2, # general cost across the board, applies to all populus
        UNEMPLOYED : -2,
        ILLEGALS : 0,
        RETIREES : 0,
        VETERANS : 0,
        SOLDIERS : -7,
        DISABLED : 0,
        HOMELESS : 0,
        PRIVATE : 0,
        HARV : -3,
        INFR : -4,
        AGRI : -2,
        DEFE : -10,
        SCIE : -4,
        POLI : -4,
        ENVI : -1,
        HEAL : -3,
        }

    # workforce / employment points put into each category

    points_allocated = {
        HARV : 0,
        INFR : 0,
        AGRI : 0,
        DEFE : 0,
        SCIE : 0,
        POLI : 0,
        ENVI : 0,
        HEAL : 0,
        }
    employees = {
        HARV : 0,
        INFR : population*0.2,
        AGRI : population*0.5,
        DEFE : 0,
        SCIE : 0,
        POLI : 0,
        ENVI : 0,
        HEAL : 0,
        }
    levels = {
        HARV : 0,
        INFR : 0,
        AGRI : 0,
        DEFE : 0,
        SCIE : 0,
        POLI : 0,
        ENVI : 0,
        HEAL : 0,
        }

    @classmethod
    def get_food_decay_rate(cls):
        return cls.food_waste + cls.food_decay
    @classmethod
    def get_infrastructure_decay_rate(cls):
        return cls.existing_infrastructure_decay * cls.INFRASTRUCTURE_DECAY_RATES[cls.growth_infrastructure_rate]

    @classmethod
    def get_sell_value_oil(cls):
        return Game.selling_resources_economy*(Game.market_value_oil * 0.01)
    @classmethod
    def get_purchase_value_oil(cls):
        return Game.buying_resources_economy*(Game.market_value_oil * 0.01)
    @classmethod
    def get_sell_value_food(cls):
        return Game.selling_food_economy*(Game.market_value_food * 0.01)
    @classmethod
    def get_purchase_value_food(cls):
        return Game.buying_food_economy*(Game.market_value_food * 0.01)
    
    @classmethod
    def get_favor(cls, side=GROUP_ALLIES):
        favor_loss = cls.agency_commerce_fees
        diplo = cls.diplomacy.get(side, 0) - favor_loss
        return diplo
    
    @classmethod
    def get_productivity(cls):
        return cls.productivity
    
    @classmethod
    def get_cost_per(cls, job):
        return (0.25 + 0.75 * cls.WAGES[Game.wages]) * (-cls.wealth + cls.population_upkeeps[job] + cls.population_upkeeps[GENERAL])
    @classmethod
    def get_cost_total(cls, job):
        return cls.get_cost_per(job) * cls.employees[job]
    
    @classmethod
    def get_infrastructure_infrastructure_per(cls):
        return cls.infrastructure_infrastructure * (1 + 0.01 * cls.levels[INFR]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_infrastructure_infrastructure_total(cls):
        return round(cls.infrastructure_infrastructure * (1 + 0.01 * cls.levels[INFR]) * cls.employees[INFR] * 0.01 * cls.get_productivity())
    @classmethod
    def get_infrastructure_physical_per(cls):
        return cls.infrastructure_physical
    @classmethod
    def get_infrastructure_physical_total(cls):
        return round(cls.infrastructure_physical * cls.employees[INFR])
    @classmethod
    def get_infrastructure_pollution_per(cls):
        return cls.infrastructure_pollution
    @classmethod
    def get_infrastructure_pollution_total(cls):
        return round(cls.infrastructure_pollution * cls.employees[INFR])
    @classmethod
    def get_infrastructure_resources_per(cls):
        return cls.infrastructure_resources
    @classmethod
    def get_infrastructure_resources_total(cls):
        return round(cls.infrastructure_resources * cls.employees[INFR])
    
    @classmethod
    def get_agriculture_food_per(cls):
        return cls.agriculture_food * (1 + 0.01 * cls.levels[AGRI]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_agriculture_food_total(cls):
        return round(cls.agriculture_food * (1 + 0.01 * cls.levels[AGRI]) * cls.employees[AGRI] * 0.01 * cls.get_productivity())
    @classmethod
    def get_agriculture_physical_per(cls):
        return cls.agriculture_physical
    @classmethod
    def get_agriculture_physical_total(cls):
        return round(cls.agriculture_physical * cls.employees[AGRI])
    @classmethod
    def get_agriculture_pollution_per(cls):
        return cls.agriculture_pollution
    @classmethod
    def get_agriculture_pollution_total(cls):
        return round(cls.agriculture_pollution * cls.employees[AGRI])
    @classmethod
    def get_agriculture_required_infrastructure_per(cls):
        return cls.agriculture_required_infrastructure
    @classmethod
    def get_agriculture_required_infrastructure_total(cls):
        return round(cls.agriculture_required_infrastructure * cls.employees[AGRI])
    
    @classmethod
    def get_harvesting_resources_per(cls):
        return cls.harvesting_resources * (1 + 0.01 * cls.levels[HARV]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_harvesting_resources_total(cls):
        return round(cls.harvesting_resources * (1 + 0.01 * cls.levels[HARV]) * cls.employees[HARV] * 0.01 * cls.get_productivity())
    @classmethod
    def get_harvesting_power_per(cls):
        return cls.harvesting_power
    @classmethod
    def get_harvesting_power_total(cls):
        return round(cls.harvesting_power * cls.employees[HARV])
    @classmethod
    def get_harvesting_happiness_per(cls):
        return cls.harvesting_happiness
    @classmethod
    def get_harvesting_happiness_total(cls):
        return round(cls.harvesting_happiness * cls.employees[HARV])
    @classmethod
    def get_harvesting_mental_per(cls):
        return cls.harvesting_mental
    @classmethod
    def get_harvesting_mental_total(cls):
        return round(cls.harvesting_mental * cls.employees[HARV])
    @classmethod
    def get_harvesting_physical_per(cls):
        return cls.harvesting_physical
    @classmethod
    def get_harvesting_physical_total(cls):
        return round(cls.harvesting_physical * cls.employees[HARV])
    @classmethod
    def get_harvesting_pollution_per(cls):
        return cls.harvesting_pollution
    @classmethod
    def get_harvesting_pollution_total(cls):
        return round(cls.harvesting_pollution * cls.employees[HARV])
    @classmethod
    def get_harvesting_required_infrastructure_per(cls):
        return cls.harvesting_required_infrastructure
    @classmethod
    def get_harvesting_required_infrastructure_total(cls):
        return round(cls.harvesting_required_infrastructure * cls.employees[HARV])

    @classmethod
    def get_science_research_per(cls):
        return cls.science_research * (1 + 0.01 * cls.levels[SCIE]) * 0.01 * cls.get_productivity() * (1 + 0.01 * Game.FUNDING_EDUCATION_RESEARCH[Game.funding_education])
    @classmethod
    def get_science_research_total(cls):
        return round(cls.get_science_research_per() * cls.employees[SCIE])
    @classmethod
    def get_science_resources_per(cls):
        return cls.science_resources
    @classmethod
    def get_science_resources_total(cls):
        return round(cls.science_resources * cls.employees[DEFE])
    @classmethod
    def get_science_required_infrastructure_per(cls):
        return cls.science_required_infrastructure
    @classmethod
    def get_science_required_infrastructure_total(cls):
        return round(cls.science_required_infrastructure * cls.employees[DEFE])
    
    @classmethod
    def get_qol_happiness_per(cls):
        return cls.qol_happiness * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_qol_happiness_total(cls):
        return round(cls.qol_happiness * cls.employees[ENVI] * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity())
    @classmethod
    def get_qol_mental_per(cls):
        return cls.qol_mental * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_qol_mental_total(cls):
        return round(cls.qol_mental * cls.employees[ENVI] * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity())
    @classmethod
    def get_qol_pollution_per(cls):
        return cls.qol_pollution * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_qol_pollution_total(cls):
        return round(cls.qol_pollution * cls.employees[ENVI] * (1 + 0.01 * cls.levels[ENVI]) * 0.01 * cls.get_productivity())

    @classmethod
    def get_hospitals_mental_per(cls):
        return cls.hospitals_mental * (1 + 0.01 * cls.levels[HEAL]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_hospitals_mental_total(cls):
        return round(cls.hospitals_mental * (1 + 0.01 * cls.levels[HEAL]) * cls.employees[HEAL] * 0.01 * cls.get_productivity())
    @classmethod
    def get_hospitals_physical_per(cls):
        return cls.hospitals_physical * (1 + 0.01 * cls.levels[HEAL]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_hospitals_physical_total(cls):
        return round(cls.hospitals_physical * (1 + 0.01 * cls.levels[HEAL]) * cls.employees[HEAL] * 0.01 * cls.get_productivity())
    @classmethod
    def get_hospitals_happiness_per(cls):
        return cls.hospitals_happiness
    @classmethod
    def get_hospitals_happiness_total(cls):
        return round(cls.hospitals_happiness * cls.employees[HEAL])
    @classmethod
    def get_hospitals_required_infrastructure_per(cls):
        return cls.hospitals_required_infrastructure
    @classmethod
    def get_hospitals_required_infrastructure_total(cls):
        return round(cls.hospitals_required_infrastructure * cls.employees[HEAL])
    
    @classmethod
    def get_police_crime_per(cls):
        return cls.police_crime * (1 + 0.01 * cls.levels[POLI]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_police_crime_total(cls):
        return round(cls.police_crime * (1 + 0.01 * cls.levels[POLI]) * cls.employees[POLI] * 0.01 * cls.get_productivity())
    @classmethod
    def get_police_happiness_per(cls):
        return cls.police_happiness
    @classmethod
    def get_police_happiness_total(cls):
        return round(cls.police_happiness * cls.employees[POLI])
    @classmethod
    def get_police_mental_per(cls):
        return cls.police_mental
    @classmethod
    def get_police_mental_total(cls):
        return round(cls.police_mental * cls.employees[POLI])
    @classmethod
    def get_police_required_infrastructure_per(cls):
        return cls.police_required_infrastructure
    @classmethod
    def get_police_required_infrastructure_total(cls):
        return round(cls.police_required_infrastructure * cls.employees[POLI])

    @classmethod
    def get_defense_warmachines_per(cls):
        return cls.defense_weapons * (1 + 0.01 * cls.levels[DEFE]) * 0.01 * cls.get_productivity()
    @classmethod
    def get_defense_warmachines_total(cls):
        return round(cls.defense_weapons * (1 + 0.01 * cls.levels[DEFE]) * cls.employees[DEFE] * 0.01 * cls.get_productivity())
    @classmethod
    def get_defense_resources_per(cls):
        return cls.defense_resources
    @classmethod
    def get_defense_resources_total(cls):
        return round(cls.defense_resources * cls.employees[DEFE])
    @classmethod
    def get_defense_happiness_per(cls):
        return cls.defense_happiness
    @classmethod
    def get_defense_happiness_total(cls):
        return round(cls.defense_happiness * cls.employees[DEFE])
    @classmethod
    def get_defense_mental_per(cls):
        return cls.defense_mental
    @classmethod
    def get_defense_mental_total(cls):
        return round(cls.defense_mental * cls.employees[DEFE])
    @classmethod
    def get_defense_physical_per(cls):
        return cls.defense_physical
    @classmethod
    def get_defense_physical_total(cls):
        return round(cls.defense_physical * cls.employees[DEFE])
    @classmethod
    def get_defense_pollution_per(cls):
        return cls.defense_pollution
    @classmethod
    def get_defense_pollution_total(cls):
        return round(cls.defense_pollution * cls.employees[DEFE])
    @classmethod
    def get_defense_required_infrastructure_per(cls):
        return cls.defense_required_infrastructure
    @classmethod
    def get_defense_required_infrastructure_total(cls):
        return round(cls.defense_required_infrastructure * cls.employees[DEFE])
        
    @classmethod
    def sim_food_loss(cls, food_amount, sim_income=False):
        if food_amount <= 0:
            return 0
        f = food_amount
        n = -1
        if sim_income:
            while f >= 0:
                n += 1
                fig = (1+cls.levels[AGRI]*0.01) * cls.agriculture_food * cls.employees[AGRI]
                fig = max(0, f * 0.01 * cls.get_productivity())
                fig += cls.buying_food_points * cls.buying_food
                fi = cls.food_income_gross - cls.food_distribution * cls.population + cls.selling_food_points * cls.selling_food - round(0.01 * cls.get_food_decay_rate() * f)
                if fi > 0:
                    n = "'"
                    break
                f += fi
        else:
            while f >= 0:
                n += 1
                f = f - cls.population * cls.food_distribution - round(0.01 * cls.get_food_decay_rate() * f)
        return n

    @classmethod
    def advise(cls, priority: bool, string: str, full_message: list):
        ls = []
        for item in full_message:
            ls.extend(textwrap.wrap(item, width=39))
        cls.advice.insert(0, advice.Advice(string, priority, ls))

    @classmethod
    def queue_tech(cls, tech_id, tech_data):
        cls.complete_tech(tech_id, tech_data)

    @classmethod
    def complete_tech(cls, tech_id, tech_data):
        population_max_delta = tech_data.get('pop', 0)
        exclusive_list = tech_data.get('exclusive', [])
        infrastructure_upkeep = tech_data.get('infrastructure_upkeep', 0)
        trustd = tech_data.get('trust', 0)
        
        cls.infrastructure_upkeep_value += infrastructure_upkeep
        cls.population_max += population_max_delta
        cls.trust += trustd
        
        # apply upgrades
        for k,v in tech_data['upkeep'].items():
            cls.population_upkeeps[k] -= v

        for k,v in tech_data.get('stats', {}).items():
            # mult
            if k=='construction_infrastructure_mult':
                print('construction_infrastructure_mult')
                cls.infrastructure_infrastructure *= v
            elif k=='warmachines_export_mult':
                print('warmachines_export_mult')
                cls.selling_warmachines_economy *= v
            elif k=='food_export_mult':
                print('food_export_mult')
                cls.selling_food_economy *= v
            elif k=='oil_export_mult':
                print('oil_export_mult')
                cls.selling_resources_economy *= v
            elif k=='solar_export_mult':
                print('solar_export_mult')
                cls.power_production_solar *= v
            elif k=='nuclear_export_mult':
                print('nuclear_export_mult')
                cls.power_production_nuclear *= v
            elif k=='agriculture_food_mult':
                print('agriculture_food_mult')
                cls.agriculture_food *= v
            elif k=='environmental_happiness_mult':
                print('environmental_happiness_mult')
                cls.qol_happiness *= v
            elif k=='environmental_sanity_mult':
                print('environmental_sanity_mult')
                cls.qol_mental *= v
            elif k=='environmental_pollution_mult':
                print('environmental_pollution_mult')
                cls.qol_pollution *= v
            elif k=='researchers_research_mult':
                print('researchers_research_mult')
                cls.science_research *= v
            elif k=='healthcare_health_mult':
                print('healthcare_health_mult')
                cls.hospitals_physical *= v
            elif k=='healthcare_sanity_mult':
                print('healthcare_sanity_mult')
                cls.hospitals_mental *= v
            elif k=='industry_oil_mult':
                print('industry_oil_mult')
                cls.harvesting_resources *= v
            elif k=='industry_health_mult':
                print('industry_health_mult')
                cls.harvesting_physical *= v
            elif k=='industry_pollution_mult':
                print('industry_pollution_mult')
                cls.harvesting_pollution *= v
            elif k=='industry_happiness_mult':
                print('industry_happiness_mult')
                cls.harvesting_happiness *= v
            elif k=='police_happiness_mult':
                print('police_happiness_mult')
                cls.police_happiness *= v
            elif k=='military_happiness_mult':
                print('military_happiness_mult')
                cls.defense_happiness *= v
            elif k=='trade_mult':
                print('trade_mult')
                cls.trade *= v
            # set
            elif k=='healthcare_happiness_set':
                print('healthcare_happiness_set')
                cls.hospitals_happiness = v
            elif k=='food_decay_set':
                print('food_decay_set')
                cls.food_decay = v
            elif k=='business_growth_set':
                print('business_growth_set')
                cls.business_growth = v
            # add
            elif k=='agriculture_pollution_add':
                print('agriculture_pollution_add')
                cls.agriculture_pollution += v
            elif k=='business_growth_add':
                print('business_growth_add')
                cls.business_growth = max(0, cls.business_growth + v)
            elif k=='wealth_add':
                print('wealth_add')
                cls.wealth += v
            elif k=='pollution_per_capita_add':
                print('pollution_per_capita_add')
                cls.pollution_per_capita += v
            elif k=='happiness_per_capita_add':
                print('happiness_per_capita_add')
                cls.happiness_bonus += v
            elif k=='health_per_capita_add':
                print('health_per_capita_add')
                cls.physical_bonus += v
            elif k=='private_sector_productivity_add':
                print('private_sector_productivity_add')
                cls.private_sector_productivity += v
            elif k=='productivity_add':
                print('productivity_add')
                cls.productivity_bonus += v
            elif k=='influence_add':
                print('influence_add')
                cls.influence += v
            # special
            elif k=='infrastructure_per_population_add':
                print('infrastructure_per_population_add')
                cls.infrastructure_per_population += v
            elif k=='private_schools_researched':
                print('private_schools_researched')
                cls.private_schools_researched = v
            elif k=='public_schools_researched':
                print('public_schools_researched')
                cls.public_schools_researched = v
            elif k=='contraceptives':
                print('contraceptives')
                cls.contraceptives_researched = v
            elif k=='anocracy':
                print('anocracy')
                cls.anocracy_researched = v
            elif k=='totalitarianism':
                print('totalitarianism')
                cls.totalitarianism_researched = v
            elif k=='autocracy':
                print('autocracy')
                cls.autocracy_researched = v
            elif k=='democracy':
                print('democracy')
                cls.democracy_researched = v
            elif k=='socialism':
                print('socialism')
                cls.socialism_researched = v
            elif k=='capitalism':
                print('capitalism')
                cls.capitalism_researched = v
            elif k=='civil_rights':
                print('civil_rights')
                cls.civil_rights_researched = v
            elif k=='diplomacy':
                print('diplomacy')
                if v > 0:
                    cls.diplomacy[GROUP_ALLIES] += v
                    cls.diplomacy[GROUP_AXIS] -= v
                else:
                    cls.diplomacy[GROUP_AXIS] += v
                    cls.diplomacy[GROUP_ALLIES] -= v
            # we need to have found SOMETHING else we've missed an upgrade
            else:
                print("ERRORRRRR not found: < {} : {} >".format(k, v))
        
        if tech_id == TECH_PUBLIC_TRANSPORT:
            cls.techs[TECH_PUBLIC_SCHOOLS]['cost'] *= 2
            cls.techs[TECH_PUBLIC_SCHOOLS]['pop'] *= 4
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        elif tech_id == TECH_PUBLIC_SCHOOLS:
            cls.techs[TECH_PUBLIC_TRANSPORT]['cost'] *= 2
            cls.techs[TECH_PUBLIC_TRANSPORT]['pop'] *= 4
            cls.techs[TECH_AUTOMOBILE_INDUSTRY]['cost'] *= 2
            cls.techs[TECH_AUTOMOBILE_INDUSTRY]['pop'] *= 4
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        elif tech_id == TECH_AUTOMOBILE_INDUSTRY:
            cls.techs[TECH_PUBLIC_SCHOOLS]['cost'] *= 4
            cls.techs[TECH_PUBLIC_SCHOOLS]['pop'] *= 4
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        elif tech_id == TECH_PUBLIC_PARKS:
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        elif tech_id == TECH_CIVIL_RIGHTS:
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        elif tech_id == TECH_DEMOCRACY:
            cls.techs[TECH_CONTRACEPTIVES]['pop'] *= 2
        # exclusive techs
        for t in exclusive_list:
            del_if_found(cls.list_available_techs, t)
            cls.list_disabled_techs.append(t)
        # add new techs into the list, if applicable;
        #  preclude this tech from being bought again
        cls.list_disabled_techs.append(tech_id)
        cls.list_purchased_techs.append(tech_id)
        key = tech_data.get('key', -1)
        if key not in cls.list_purchased_techs:
            cls.list_purchased_techs.append(key)
        cls.add_new_available_techs()
    
    @classmethod
    def add_new_available_techs(cls):
        for i in range(len(cls.techs)):
            tech = i
            if tech in cls.list_available_techs:
                continue
            if tech in cls.list_disabled_techs:
                continue
            if not cls.techs.get(tech, None):
                continue
            if cls.techs[tech]['age'] > cls.age:
                continue
            requires = cls.techs[tech].get('requires', [])
            if requires:
                will_continue = False
                for required in requires:
                    if required not in cls.list_purchased_techs:
                        will_continue = True
                        break
                if will_continue:
                    continue
            cls.list_available_techs.append(tech)


def update_values():
    if Game.population <= 0:
        return

    _update_begin()
    _update_unemployment()
    _update_wealth()
    _update_influence()
    _update_business_growth()
    _update_income_inequality()
    _update_infrastructure()
    _update_weapons()
    _update_oil()
    _update_food()
    _update_market()
    _update_civilian_count()
    _update_trust()
    _update_pollution()
    _update_information()
    _update_happiness()
    _update_health()
    _update_sanity()
    _update_crime()
    _update_productivity()
    _update_fertility()
    _update_population()
    _update_impose_maximums()
    _update_allocation_speed()
    _update_power()
        
def _update_begin():
    Game.population_density = Game.population / max(1, Game.land)

    Game.points_remaining = MAX_ALLOCATION - (Game.points_allocated[INFR] + Game.points_allocated[HARV] + Game.points_allocated[AGRI] + Game.points_allocated[SCIE] + Game.points_allocated[DEFE] + Game.points_allocated[HEAL] + Game.points_allocated[POLI] + Game.points_allocated[ENVI])
    
    Game.lv_bonuses = {
        INFR : (100 + Game.levels[INFR]) * 0.01,
        HARV : (100 + Game.levels[HARV]) * 0.01,
        ENVI : (100 + Game.levels[ENVI]) * 0.01,
        AGRI : (100 + Game.levels[AGRI]) * 0.01,
        SCIE : (100 + Game.levels[SCIE]) * 0.01,
        POLI : (100 + Game.levels[POLI]) * 0.01,
        DEFE : (100 + Game.levels[DEFE]) * 0.01,
        HEAL : (100 + Game.levels[HEAL]) * 0.01,
        }
    
def _update_unemployment():
# workforce
    Game.workforce_employed = Game.employees[HARV] * Game.harvesting_workforce + Game.employees[POLI] * Game.police_workforce
    Game.workforce_employed += Game.employees[INFR] * Game.infrastructure_workforce + Game.employees[AGRI] * Game.agriculture_workforce
    Game.workforce_employed += Game.employees[DEFE] * Game.defense_workforce + Game.employees[SCIE] * Game.science_workforce
    Game.workforce_employed += Game.employees[HEAL] * Game.hospitals_workforce + Game.employees[ENVI] * Game.qol_workforce
    actively_working = abs(Game.workforce_employed) + Game.private_sector + Game.soldiers
    Game.workforce = Game.workforce_employed + Game.population - Game.prisoners - Game.disabled - Game.illegals - Game.retirees - Game.private_sector

    # todo allocation speed isn't working properly
    # This isn't working properly, can go over 100%
    # todo: when infra. runs out, don't unemploy everyone...!
    Game.unemployment_rate = 100 * Game.workforce / actively_working

def _update_wealth():
    Game.wealth_actual = Game.wealth

def _update_influence():
    Game.influence_actual = Game.influence

def _update_business_growth():
    Game.business_growth_from_taxing = 25 - round(pow(Game.investor_taxing, 1.15)) - Game.housing_subsidies
    Game.business_growth_from_unemployment = max(0, 6 - 2*abs(3 - Game.unemployment_rate))
    Game.business_growth_from_wages = -3 + 0.5*Game.wages
    Game.business_growth_actual = min(95, Game.business_growth + Game.business_growth_from_taxing + Game.business_growth_from_unemployment + Game.business_growth_from_wages)

def _update_income_inequality():
    it = Game.investor_taxing
    ct = 2*Game.civilian_taxing
    Game.income_inequality_from_ssa_policy = 1 - 0.005555 * (Game.health_insurance_policy + 2*Game.income_assistance_policy)
    Game.income_inequality_from_taxing_mod = 0.5 + 0.5*(ct / it + 0.1 * Game.sales_taxing)
    Game.income_inequality_from_influence = 0.25*Game.influence_actual
    Game.income_inequality_from_wages = 12 / (6 + Game.wages)
    Game.income_inequality_from_business_mod = 0.2 * (10 + Game.wealth_actual) * (100+Game.business_growth_actual)
    Game.income_inequality_from_housing_mod = 0.334*(7 - Game.housing_subsidies)
    Game.income_inequality_actual = 1 + 0.013 * Game.income_inequality * Game.income_inequality_from_taxing_mod * Game.income_inequality_from_business_mod * Game.income_inequality_from_housing_mod * Game.income_inequality_from_wages * Game.income_inequality_from_ssa_policy
    Game.income_inequality_actual += Game.income_inequality_from_influence
           
def _update_infrastructure():
    Game.housing_density = round(Game.unused_infrastructure / Game.existing_infrastructure * 100) # just unused infrastructure 
    Game.infrastructure_growth = Game.lv_bonuses[INFR] * Game.infrastructure_infrastructure * Game.employees[INFR] * 0.01 * Game.get_productivity()
    Game.infrastructure_growth *= Game.GROWTH_INFRASTRUCTURE_RATES[Game.growth_infrastructure_rate]
    Game.infrastructure_income_decay = -Game.existing_infrastructure * 0.01 * Game.get_infrastructure_decay_rate()
    Game.infrastructure_delta = Game.infrastructure_growth + Game.infrastructure_income_decay
    Game.infrastructure_usage_population = -Game.population * Game.infrastructure_per_population * (1 + 0.1*Game.wealth)
    Game.infrastructure_usage_private = -Game.private_sector * (1 + 0.2*Game.wealth)
    Game.infrastructure_usage_harvesting = -Game.harvesting_required_infrastructure * Game.employees[HARV]
    Game.infrastructure_usage_agriculture = -Game.agriculture_required_infrastructure * Game.employees[AGRI]
    Game.infrastructure_usage_defense = -Game.defense_required_infrastructure * Game.employees[DEFE]
    Game.infrastructure_usage_science = -Game.science_required_infrastructure * Game.employees[SCIE]
    Game.infrastructure_usage_hospitals = -Game.hospitals_required_infrastructure * Game.employees[HEAL]
    Game.infrastructure_usage_police = -Game.police_required_infrastructure * Game.employees[POLI]
    Game.infrastructure_usage_public_sector = (Game.infrastructure_usage_harvesting + Game.infrastructure_usage_agriculture + Game.infrastructure_usage_defense + Game.infrastructure_usage_science + Game.infrastructure_usage_hospitals + Game.infrastructure_usage_police)
    Game.unused_infrastructure = Game.existing_infrastructure + Game.infrastructure_usage_population + Game.infrastructure_usage_private + Game.infrastructure_usage_public_sector
    
def _update_weapons():
    Game.warmachines_income_gross = Game.lv_bonuses[DEFE] * Game.defense_weapons * Game.employees[DEFE]
    Game.warmachines_income_gross = max(0, Game.warmachines_income_gross * 0.01 * Game.get_productivity())
    Game.warmachines_income = Game.warmachines_income_gross - Game.warmachines_decay

def _update_oil():
    Game.resources_income_industry = Game.lv_bonuses[HARV] * Game.employees[HARV] * Game.harvesting_resources * 0.01 * Game.get_productivity()
    Game.resources_income_gross = Game.resources_income_industry
    Game.resources_income_commerce = Game.buying_resources_points * Game.buying_resources + Game.selling_resources_points * Game.selling_resources
    Game.resources_income_public = Game.employees[INFR] * Game.infrastructure_resources + Game.employees[SCIE] * Game.science_resources + Game.employees[DEFE] * Game.defense_resources
    Game.resources_income = Game.resources_income_gross + Game.resources_income_commerce + Game.resources_income_public

def _update_food():
    if Game.food <= 0:
        Game.food_distribution = 0
    Game.food_income_agriculture = Game.lv_bonuses[AGRI] * Game.agriculture_food * Game.employees[AGRI] * 0.01 * Game.get_productivity()
    Game.food_income_commerce = Game.buying_food_points * Game.buying_food + Game.selling_food_points * Game.selling_food
    Game.food_income_gross = Game.food_income_agriculture
    Game.food_income_distribution = -Game.food_distribution * Game.population
    Game.food_waste = Game.FOOD_DISTRIBUTION_WASTE_RATE[Game.food_distribution]
    Game.food_income_decay = -0.01 * (Game.food_decay) * Game.food
    Game.food_income_waste = -0.01 * (Game.food_waste) * Game.food
    Game.food_income = Game.food_income_gross + Game.food_income_commerce + Game.food_income_distribution + Game.food_income_decay + Game.food_income_waste

def _update_market():
    # market value updates
    y = (Game.year-1900)
    Game.market_value_food = round(Game.wealth_actual + 2*Game.influence_actual + 200 * (1 + math.sin(y * 0.1)*0.2 - min(0.5, y*0.05))) #round(97 + 8 * -math.cos(0.002777778 * Game.turn) + random.random()*6)
    Game.market_value_oil = round(Game.wealth_actual + 2*Game.influence_actual + 100 * (1 + math.sin(y * 0.3)*0.333)) #round(97 + 8 * math.sin(0.001341823 * Game.turn) + random.random()*6)
    # auto commerce
    if Game.market_resources_set:
        if Game.resources_income >= 1:
            if Game.buying_resources_points > 0:
                Game.buying_resources_points = max(0, Game.buying_resources_points - math.floor(abs(Game.resources_income)))
            else:
                Game.selling_resources_points += math.floor(Game.resources_income) - 1
        elif Game.resources_income <= -1:
            if Game.selling_resources_points <= 0:
                Game.buying_resources_points += math.floor(abs(Game.resources_income)) - 1
            else:
                Game.selling_resources_points = max(0, Game.selling_resources_points - math.floor(abs(Game.resources_income)))
    if Game.market_food_set:
        if Game.food_income >= 1:
            if Game.buying_food_points > 0:
                Game.buying_food_points = max(0, Game.buying_food_points - math.floor(abs(Game.food_income)))
            else:
                Game.selling_food_points += math.floor(Game.food_income) - 1
        elif Game.food_income <= -1:
            if Game.selling_food_points <= 0:
                Game.buying_food_points += math.floor(abs(Game.food_income)) - 1
            else:
                Game.selling_food_points = max(0, Game.selling_food_points - math.floor(abs(Game.food_income)))

def _update_civilian_count():
    Game.civilians = Game.population - Game.soldiers - Game.prisoners - Game.illegals - Game.employees[INFR] + Game.employees[SCIE] + Game.employees[AGRI] + Game.employees[HARV] + Game.employees[ENVI] + Game.employees[HEAL] + Game.employees[POLI] + Game.employees[DEFE]

def _update_trust():
    Game.trust_from_food = -6 + math.floor(Game.food_distribution + Game.food_distribution_efficiency)
    Game.trust_from_education_agency = Game.funding_education
    Game.trust_from_zoning_agency = 2 + Game.growth_infrastructure_rate - Game.housing_subsidies
    Game.trust_from_labor_agency = 0.5 * (Game.safety_law - 3) + Game.fulltime_hours
    Game.trust_from_tariffs = Game.AGENCY_COMMERCE_FEES_TRUST[Game.agency_commerce_fees]
    Game.trust_from_taxing = 0.5 * (4 - Game.investor_taxing) + 0.25 * (4 - Game.sales_taxing)
    Game.trust_from_environmental_policy = Game.environmental_policy - 2
    Game.trust_actual = round(Game.trust + Game.trust_from_labor_agency + Game.trust_from_food + Game.trust_from_education_agency + Game.trust_from_zoning_agency + Game.trust_from_tariffs + Game.trust_from_taxing + Game.trust_from_environmental_policy)

def _update_pollution():
    if Game.age >= 5:
        Game.pollution_income_density = (0.1*Game.wealth + Game.pollution_per_capita) * Game.population * (1 + Game.population_density * 0.01)
        Game.pollution_income_industry = Game.employees[HARV] * Game.harvesting_pollution
        Game.pollution_income_public = Game.employees[INFR] * Game.infrastructure_pollution + Game.employees[AGRI] * Game.agriculture_pollution + Game.employees[DEFE] * Game.defense_pollution
        Game.pollution_income_gross = Game.pollution_income_industry + Game.pollution_income_public + Game.pollution_income_density
        Game.gea_agency_modifier = (1 + 0.2 * Game.environmental_policy)
        Game.pollution_income_environmental = -Game.gea_agency_modifier * Game.lv_bonuses[ENVI] * Game.employees[ENVI] * Game.qol_pollution
        Game.pollution_income = Game.pollution_income_gross + Game.pollution_income_environmental
        Game.pollution_ugpm3 = get_ugpm3(Game.pollution, Game.land)
        # trade through gea
        Game.power_income_pollution_trade = 0
        Game.pollution_income_trade = 0
        if (Game.import_pollution):
            Game.pollution_income_trade = Game.land * (100 + Game.trust_actual)
            Game.power_income_pollution_trade = Game.pollution_income_trade * min(150, max(1, (100 + Game.trust_actual))) * 0.01
        elif (Game.export_pollution):
            Game.pollution_income_trade = -Game.land * max(25, 100 - Game.trust_actual)
            Game.power_income_pollution_trade = Game.pollution_income_trade * max(150, (200 - Game.trust_actual)) * 0.01
        Game.pollution_income += Game.pollution_income_trade
        Game.pollution_ugpm3 = get_ugpm3(Game.pollution, Game.land)
  
def _update_information():
    #Game.research_max = 100 * Game.science_research * Game.employees[SCIE]
    funding_mod = 1 + 0.01 * Game.FUNDING_EDUCATION_RESEARCH[Game.funding_education]
    Game.research_income_science = Game.lv_bonuses[SCIE] * Game.employees[SCIE] * Game.science_research * 0.01 * Game.get_productivity() * funding_mod
    Game.research_income_private = (0.1 + Game.wealth_actual * 0.3334) * 0.005 * Game.get_productivity() * Game.private_sector * Game.private_sector_research
    Game.research_income_gross = Game.research_income_private + Game.research_income_science
    Game.research_income_decay = -Game.research * (0.01 * Game.research_decay)
    Game.research_income = Game.research_income_gross + Game.research_income_decay
    
def _update_happiness():
    # job satisfaction
    Game.happiness_from_environmental = 0.5 * ((Game.lv_bonuses[ENVI] * Game.qol_happiness * Game.employees[ENVI]) / Game.population)
    Game.happiness_from_private_sector = 0.5 * (-0.334*max(0, (Game.income_inequality_actual - 5)) * Game.private_sector / Game.population)
    Game.happiness_from_jobs = -5 + 5*Game.WAGES[Game.wages] + (Game.happiness_from_private_sector + (Game.employees[DEFE] * Game.defense_happiness + Game.employees[HARV] * Game.harvesting_happiness + Game.employees[POLI] * Game.police_happiness + Game.employees[HEAL] * Game.hospitals_happiness) / Game.population)
    if Game.happiness_from_jobs > 0:
        Game.happiness_from_jobs *= 0.25*(40 / Game.FULLTIME_HOURS[Game.fulltime_hours])
    else:
        Game.happiness_from_jobs *= Game.FULLTIME_HOURS[Game.fulltime_hours] / 40
    Game.happiness_from_jobs += 0.5*(40 -Game.FULLTIME_HOURS[Game.fulltime_hours])

    Game.happiness = Game.happiness_from_environmental + Game.happiness_from_jobs
    # flat modifiers
    Game.happiness_from_pensions = -6 + 0.5*Game.veteran_pension_policy + math.log(max(1, Game.veteran_pension_policy), 2)
    Game.happiness_from_birth_policy = -6 + 2*Game.birth_control
    Game.happiness_from_income_distribution = 0.5 * (-0.334*max(0, (Game.income_inequality_actual - 5)))
    Game.happiness_from_pollution = 0.5 * (-math.log(max(1, Game.pollution_ugpm3), 2) - 0.1*Game.pollution_ugpm3)
    Game.happiness_from_density = 0.5 * (-6*Game.population_density * 0.001)
    Game.happiness_from_taxes = 0.5 * (12 - pow(1*Game.civilian_taxing, 1.25) - 0.2*Game.investor_taxing - 0.75*pow(Game.sales_taxing, 1.25) + pow(Game.housing_subsidies, 1.25))
    Game.happiness_from_food = 0.5 * (Game.food_distribution_efficiency * math.log(1 + Game.food_distribution, 2))
    Game.happiness += (Game.happiness_from_food + Game.happiness_from_pollution + Game.happiness_from_density) + Game.happiness_bonus
    Game.happiness += (Game.happiness_from_taxes + Game.happiness_from_income_distribution + Game.happiness_from_birth_policy + Game.happiness_from_pensions)
    
def _update_health():
    # per pop
    construction_ratio = Game.employees[INFR] / Game.population
    Game.physical_from_lla_policy = 5 / (1 + Game.safety_law)
    Game.physical_from_zua_policy = construction_ratio * (-3*Game.growth_infrastructure_rate if Game.growth_infrastructure_rate >= 3 else -2*Game.growth_infrastructure_rate)
    Game.physical_from_pandemic = 0 # temporary
    Game.physical_from_drug_abuse = -0.25 * (10 - Game.food_distribution_efficiency) * (1 + Game.crime) * max(0, 100 - Game.happiness) * 0.01

    # calculating who can afford health insurance...
    Game.percent_cant_afford_health_care = max(0, Game.income_inequality_actual - 0.5*Game.wealth_actual - 2*Game.health_insurance_policy)
    Game.hc_policy_mult = max(1, min(100, 100 - Game.percent_cant_afford_health_care)) * 0.01
    
    Game.physical_from_healthcare = Game.hc_policy_mult * (Game.lv_bonuses[HEAL] * Game.hospitals_physical * Game.employees[HEAL]) / Game.population # TEST this with hc_policy_mult
    Game.physical_from_private_sector = -0.2 * (Game.crime + max(0, (Game.income_inequality_actual - 5))) * Game.private_sector / Game.population
    Game.physical_from_public = Game.physical_from_zua_policy + (Game.infrastructure_physical * Game.employees[INFR] + Game.harvesting_physical * Game.employees[HARV] + Game.defense_physical * Game.employees[DEFE]) / Game.population
    Game.physical_from_public *= Game.physical_from_lla_policy
    Game.physical = Game.physical_from_healthcare + Game.physical_from_public + Game.physical_from_drug_abuse + Game.physical_from_private_sector
    # flat
    Game.physical_from_food_drugs = Game.food_distribution_efficiency + Game.food_distribution_efficiency * (Game.food_distribution if Game.food_distribution <= 5 else (10 - Game.food_distribution))
    Game.physical_from_pollution = -(0.1*Game.pollution_ugpm3)
    Game.physical += Game.physical_from_food_drugs + Game.physical_from_pollution + Game.physical_bonus
# threat level ("natural" threats like weather, bad pollution, etc.)
    Game.threat_level = Game.population * max(0, 100 - Game.physical) * 0.00005
    
def _update_sanity():
    # per pop
    Game.mental_from_environmental = (Game.lv_bonuses[ENVI] * Game.qol_mental * Game.employees[ENVI]) / Game.population
    Game.mental_from_healthcare = Game.hc_policy_mult * (Game.lv_bonuses[HEAL] * Game.hospitals_mental * Game.employees[HEAL]) / Game.population # TEST this with hc_policy_mult
    Game.mental_from_private_sector = -0.1*max(0, (Game.income_inequality_actual - 5)) * Game.private_sector / Game.population
    Game.mental_from_jobs_loss = Game.mental_from_private_sector + (Game.harvesting_mental * Game.employees[HARV] + Game.police_mental * Game.employees[POLI]) / Game.population
    Game.mental = Game.mental_from_environmental + Game.mental_from_healthcare + Game.mental_from_jobs_loss
    # flat
    Game.mental_from_income_insurance = Game.income_assistance_policy - 0.25*Game.income_inequality
    #Game.mental_from_population_density = -10*Game.population_density * 0.001
    Game.mental_from_pollution = -(0.2*Game.pollution_ugpm3)
    Game.mental_from_dread = -Game.age
    Game.mental_from_grief = -200 * Game.deaths_per_month / max(1, Game.population)
    Game.mental_from_war = -0.1 # temporary
    Game.mental += Game.mental_from_war + Game.mental_from_dread + Game.mental_from_grief + Game.mental_from_pollution + Game.mental_bonus + Game.mental_from_income_insurance
    
def _update_crime():
    # TODO: curve that makes it so you have to find the right amount, you can't just pump tons of resources into police to "solve crime"
    Game.crime = (Game.lv_bonuses[POLI] * Game.police_crime * Game.employees[POLI]) / (Game.population)
    # up to 5% from pop ratio
    Game.crime += 5*Game.population_density * 0.001
    # up to 10% + 2.5% from mental / happiness = 12.5% total
    Game.crime += 0.09*max(0, 100 - Game.mental) + 0.01*max(0, 100 - Game.happiness)
    # up to 6% from food distribution
    Game.crime += max(0, 6 - Game.food_distribution)
    # maximum crime = 23.5%
    
def _update_productivity():
    # is AFFECTED BY crime, physical, happiness, and mental, so those should not be dependent upon productivity.
    # physical health only affects productivity when it's below 50%
    # physical health should also affect your soldier's effectiness in battle
    Game.soldier_strength = round(3*Game.physical + 2*Game.mental + Game.happiness)
    Game.productivity_from_health = max(0, min(20, 0.4*Game.physical))
    Game.productivity_from_happiness = max(0, 0.3*Game.happiness)
    Game.productivity_from_sanity = max(0, min(20, 0.4*Game.mental))
    Game.productivity_from_hours = -20 + 0.12*Game.FULLTIME_HOURS[Game.fulltime_hours] + 6 * math.log(Game.FULLTIME_HOURS[Game.fulltime_hours], 1.5)
    Game.productivity_from_trust = 0.05*Game.trust_actual
    Game.productivity_from_crime = -Game.crime
    Game.productivity_from_housing_density = -5 + 5*max(0, Game.unused_infrastructure / Game.existing_infrastructure)
    Game.productivity = Game.productivity_bonus + Game.productivity_from_crime + Game.productivity_from_housing_density + Game.productivity_from_trust
    Game.productivity += Game.productivity_from_health + Game.productivity_from_happiness + Game.productivity_from_sanity + Game.productivity_from_hours
    Game.productivity = min(100, max(0, Game.productivity))
    
def _update_fertility():
    # (not mortality!)
    ebfh = 3 if Game.age >= 2 else 2 # epoch bonus fertility happiness multiplier
    ebf = 1 if Game.age >= 2 else 0.5 # epoch bonus fertility flat bonus
    contrab = 0.5 if Game.contraceptives_researched else 0
    Game.max_fertility                  = min(3 + 1.4*Game.food_distribution, 3 + 2*Game.birth_control)
    Game.min_fertility                  = 3
    Game.fertility_from_technology      = ebf
    Game.fertility_from_sanity          = 0.075 * Game.mental
    Game.fertility_from_health          = 0.075 * Game.physical
    Game.fertility_from_happiness       = 0.0334 * ebfh*Game.happiness
    if Game.fertility_from_sanity + Game.fertility_from_health > Game.fertility_from_happiness:
        Game.fertility_from_happiness = 0
    else: # happiness > sanity and health happiness
        Game.fertility_from_sanity = 0
        Game.fertility_from_health = 0
    Game.fertility = min(Game.max_fertility, max(Game.min_fertility, contrab + Game.fertility_from_technology + Game.fertility_from_sanity + Game.fertility_from_health + Game.fertility_from_happiness))
    
def _update_population():
    Game.population_max_from_land_mult = Game.land * 0.0001
    Game.population_max_actual = Game.population_max * Game.population_max_from_land_mult
    Game.homeless = max(0, -math.floor(Game.unused_infrastructure))
    Game.emigration_actual = Game.emigration + (0.00001 * max(0, 95 - Game.happiness)) * Game.population
    # pop decay = deaths, emigration = leaving from unhappiness
    Game.immigration_actual = Game.trust + Game.immigration * max(0, 30 - (Game.civilian_taxing + Game.investor_taxing - 8)) * 0.00333 * min(100, max(0, Game.happiness))
    Game.population_decay = 0.005
    Game.population_deaths_poor_health_percent = 0.005 * max(0, 100 - Game.physical) + 0.003 * max(0, 15 - Game.mental) + 0.003 * max(0, 15 - Game.happiness)
    Game.births_per_month = Game.fertility * 0.002 * Game.population
    Game.natural_deaths_per_month = (Game.population * Game.population_decay)
    Game.health_deaths_per_month = (Game.population * 0.01 * (Game.population_deaths_poor_health_percent) + Game.threat_level)
    Game.deaths_per_month = Game.natural_deaths_per_month + Game.health_deaths_per_month + Game.murders_per_month + Game.deaths_per_month_from_terrorists
    Game.population_gross_growth = Game.immigration_actual + Game.births_per_month + 0.333*Game.wealth_actual
    Game.population_gross_loss = -Game.emigration_actual - Game.deaths_per_month
    Game.population_growth = Game.population_gross_growth
    Game.population_delta = Game.population_growth + Game.population_gross_loss
    if (Game.population >= Game.population_max_actual and Game.population_growth > 0):
        Game.population_growth = 0

def _update_impose_maximums():
    Game.soldier_strength = max(0, Game.soldier_strength)
    Game.productivity = max(1, Game.productivity)
    Game.population = max(0, Game.population)
    Game.warmachines = max(0, Game.warmachines)
    Game.resources = max(0, Game.resources)
    Game.existing_infrastructure = max(0, Game.existing_infrastructure)
    Game.pollution = max(0, Game.pollution)
    Game.happiness = max(0, Game.happiness)
    Game.physical = max(0, Game.physical)
    Game.mental = max(0, Game.mental)
    Game.crime = max(0, Game.crime)

def _update_allocation_speed():
    if (Game.allocation_speed < Game.population_growth + 50):
        Game.allocation_speed_income = 0.0005 * Game.private_sector
    # income assistance can reduce, but cannot increase, allocation rate
    Game.allocation_rate_from_income_assistance = min(1, 2.5 * (2 + Game.income_assistance_policy) / (3 + Game.income_inequality_actual))
    Game.allocation_speed_actual = min(Game.allocation_speed, Game.allocation_speed * Game.allocation_rate_from_income_assistance)

def _update_power():
    Game.power_income_delta = Game.power_income - Game.power_income_previous
    # exports / imports
    Game.power_income_export = Game.selling_resources_economy * Game.selling_resources_points * (Game.market_value_oil * 0.01) + Game.selling_food_economy * Game.selling_food_points * (Game.market_value_food * 0.01)
    Game.power_income_import = Game.buying_resources_economy * Game.buying_resources_points * (Game.market_value_oil * 0.01) + Game.buying_food_economy * Game.buying_food_points * (Game.market_value_food * 0.01)

    '''# testing
    Game.population = 80000
    Game.private_sector = .9 * Game.population
    Game.wealth_actual = 40
    Game.existing_infrastructure = 22000*8
    Game.unused_infrastructure = 5
    Game.power = 50000000000000
    Game.happiness = 100'''
    
    # taxes make up majority of revenue in a capitalist society, exports and trade (commerce agency fees) make up majority of revenue in autocratic society
    investor_ratio = Game.private_sector / Game.civilians
    civilian_ratio = 1 - investor_ratio
# public property tax: dependent on infrastructure usage, wealth, and proportion of public sector
    Game.property_tax_income = 0.03 * abs(Game.infrastructure_usage_population) * max(0, 14 + Game.civilian_taxing - 4*Game.housing_subsidies) * (civilian_ratio) * (1 + 2.8*Game.wealth_actual)
# private property tax: dependent on infrastructure usage, income inequality, wealth, and proportion of private sector
    Game.property_tax_income += 0.05 * max(0, Game.existing_infrastructure - max(0, Game.unused_infrastructure)) * max(0, Game.investor_taxing - Game.housing_subsidies) * (investor_ratio) * (Game.income_inequality_actual + 2 * Game.wealth_actual)
    assert(Game.property_tax_income >= 0)
# public / civilian tax: dependent on wealth, doesn't earn very much
    Game.public_tax_income = 0.012 * (5 + 2.4*Game.wealth_actual) * Game.civilians * Game.civilian_taxing
# private / business / investor tax: dependent on productivity, high income inequality, high wealth, and a high proportion of private sector
    Game.private_tax_income = 0.0012 * Game.get_productivity() * (-5 + 3.2*Game.income_inequality_actual + 2*Game.wealth_actual) * Game.private_sector * Game.investor_taxing
# sales tax: dependent on high wealth, low income inequality (or high influence). High income inequality results in sales tax dropping to near 0 unless influence picks up slack.
    Game.consumers = Game.population * 0.01 * (100 - Game.unemployment_rate) + Game.private_sector
    Game.sales_tax_income = 0.18 * max(0, 2.5 + 2.5*Game.wealth_actual - 0.03*pow(max(0, Game.income_inequality_actual - 0.5*Game.influence_actual), 2)) * Game.consumers * Game.sales_taxing

# agencies
    # zua / za
    Game.power_income_za_agency_housing = 0.03 * pow(Game.housing_subsidies, 2) * Game.infrastructure_usage_population
    Game.power_income_za_agency_growth = -0.04 * pow(Game.growth_infrastructure_rate, 2) * Game.existing_infrastructure
    Game.power_income_za_agency_loss = Game.power_income_za_agency_growth + Game.power_income_za_agency_housing
    # fma
    Game.power_income_fma_agency_loss = (-Game.population * pow(Game.food_distribution, 1.5) * 0.003 * pow(1 + Game.food_distribution_efficiency, 3))
    # ea
    Game.power_income_ea_agency_higher_ed = -(0.1 * pow(Game.funding_education, 2) * Game.employees[SCIE] * Game.population_upkeeps[SCIE])
    Game.power_income_ea_agency_lower_ed = -(0.001 * Game.allocation_speed_actual * Game.population * (1+Game.wealth))
    Game.power_income_ea_agency_loss = Game.power_income_ea_agency_lower_ed + Game.power_income_ea_agency_higher_ed
    # ca
    if Game.trust_actual >= 0:
        Game.power_income_ca_agency_trade = (0.2 * Game.wealth_actual * Game.population) + (0.01 * Game.wealth_actual * Game.private_sector * Game.income_inequality * Game.trust_actual)
        Game.power_income_ca_agency_trade += abs(0.01 * Game.population * (pow(1 + Game.wealth_actual*0.5 + 2*Game.influence_actual + 0.5*Game.trust_actual, 2)))
        Game.power_income_ca_agency_trade *= (1 + Game.trade * Game.agency_commerce_fees)
        Game.power_income_ca_agency_fees_tariffs = abs(0.125 * Game.agency_commerce_fees * Game.power_income_import) + abs(0.125 * Game.agency_commerce_fees * Game.power_income_export)
        Game.power_income_ca_agency_gross = Game.power_income_ca_agency_trade + Game.power_income_ca_agency_fees_tariffs
    else:
        Game.power_income_ca_agency_gross = 0
    # ra
    Game.power_income_ra_agency_gross = Game.public_tax_income + Game.private_tax_income + Game.property_tax_income + Game.sales_tax_income
    # lla
    Game.power_income_lla_agency_loss = 0.15 * pow(Game.safety_law, 2) * Game.workforce_employed
    # gea
    Game.power_income_gea_agency_loss = -(pow(Game.environmental_policy, 1.5)) * Game.population * 0.03 * max(1, (1 + Game.wealth_actual + Game.pollution_ugpm3 - 0.5*Game.trust_actual))
    # ja
    Game.power_income_ja_agency_loss = -(Game.punishment + 2*Game.corrections) * Game.population * Game.crime * 0.01
    # ha
    Game.power_income_ha_agency_gross = (5 - Game.travel_policy) * (0.5*Game.wealth_actual) * Game.private_sector
    Game.power_income_ha_agency_loss = -Game.border_control * Game.population

    # combine numbers into power_income_agency_gross / _loss
# ra
    Game.spending_agency_revenue = Game.power_income_ra_agency_gross # display value
    Game.power_income_agency_gross = Game.power_income_ra_agency_gross
# fma
    Game.spending_agency_food = Game.power_income_fma_agency_loss
    Game.power_income_agency_loss = Game.power_income_fma_agency_loss
# za
    Game.spending_agency_zoning = Game.power_income_za_agency_loss
    Game.power_income_agency_loss += Game.power_income_za_agency_loss
# lla
    Game.spending_agency_labor = Game.power_income_lla_agency_loss
    Game.power_income_agency_loss += Game.power_income_lla_agency_loss
# ea
    if Game.age >= AGE_TRUST:
        Game.spending_agency_education = Game.power_income_ea_agency_loss
        Game.power_income_agency_loss += Game.power_income_ea_agency_loss
# ha
    if Game.age >= AGE_EXPANSION:
        Game.spending_agency_homeland = Game.power_income_ha_agency_gross + Game.power_income_ha_agency_loss
        Game.power_income_agency_loss += Game.power_income_ha_agency_loss
        Game.power_income_agency_gross += Game.power_income_ha_agency_gross
# ca
    if Game.age >= AGE_RECONSTRUCTION:
        Game.spending_agency_commerce = Game.power_income_ca_agency_gross
        Game.power_income_agency_gross += Game.power_income_ca_agency_gross
# ja
    if Game.age >= AGE_SECURITY:
        Game.spending_agency_justice = Game.power_income_ja_agency_loss
        Game.power_income_agency_loss += Game.power_income_ja_agency_loss
# gea
    if Game.age >= AGE_2NDINDUSTRIAL:
        Game.spending_agency_environmental = Game.power_income_gea_agency_loss + Game.power_income_pollution_trade
        Game.power_income_agency_loss += Game.power_income_gea_agency_loss + Game.power_income_pollution_trade
    #print("{}, {}".format(Game.power_income_ha_agency_gross, Game.power_income_ha_agency_loss))
# upkeeps
    Game.power_income_infrastructure_upkeep = -Game.infrastructure_upkeep_value * Game.existing_infrastructure
    Game.power_income_social_programs_upkeep = -0.25 * Game.wealth_actual * Game.population + (Game.population_upkeeps[UNEMPLOYED] * Game.workforce)
    Game.power_income_public_sector_upkeep = (0.25 + 0.75*Game.WAGES[Game.wages]) * (Game.population_upkeeps[GENERAL] * abs(Game.workforce_employed) + Game.population_upkeeps[INFR] * Game.employees[INFR] + Game.population_upkeeps[AGRI] * Game.employees[AGRI] + Game.population_upkeeps[DEFE] * Game.employees[DEFE] + Game.population_upkeeps[SCIE] * Game.employees[SCIE] + Game.population_upkeeps[HEAL] * Game.employees[HEAL] + Game.population_upkeeps[ENVI] * Game.employees[ENVI] + Game.employees[POLI] * Game.population_upkeeps[POLI] + Game.population_upkeeps[HARV] * Game.employees[HARV])
    Game.power_income_upkeep_costs = Game.power_income_infrastructure_upkeep + Game.power_income_public_sector_upkeep + Game.power_income_social_programs_upkeep
# total gross
    Game.power_income_gross = Game.power_income_export + Game.power_income_agency_gross
# spending allocated portions of GDP
# ssa
    Game.power_income_ssa_agency_loss = -Game.power_income_gross * 0.01 * (Game.health_insurance_policy + Game.veteran_pension_policy + Game.income_assistance_policy)
    Game.spending_agency_social_services = Game.power_income_ssa_agency_loss
    Game.power_income_agency_loss += Game.power_income_ssa_agency_loss
# net / mo
    Game.power_income = Game.power_income_gross + Game.power_income_upkeep_costs + Game.power_income_import + Game.power_income_agency_loss + Game.power_income_ssa_agency_loss


def day_elapse():
    
    Game.turn += 1
    Game.day += 1
    if Game.day > 30:
        Game.day = 1
        Game.month += 1
        month_elapse()
        if Game.month > 12:
            Game.month = 1
            Game.year += 1

def month_elapse():
    Game.power_income_previous = Game.power_income
    Game.power_income_delta = Game.power_income - Game.power_income_previous
    killpop(max(0, Game.population_gross_loss), reduce_points=False)
    addpop()
    Game.unused_infrastructure_delta = Game.unused_infrastructure - Game.unused_infrastructure_prev
    Game.unused_infrastructure_prev = Game.unused_infrastructure
    
    # kill population from depravity and pop. decay
    '''if Game.power < 0:
        print("Unemployed {} from lack of power".format(-Game.power))
        killpop(-Game.power)
        Game.population += (-Game.power)
        Game.power = 0'''
    '''if Game.unused_infrastructure < 0:
        print("Unemployed {} from lack of infrastructure".format(-Game.unused_infrastructure))
        killpop(-Game.unused_infrastructure, types="infra")
        Game.population += (-Game.unused_infrastructure)'''
    if Game.resources <= 0:
        print("Unemployed {} from lack of oil".format(-Game.resources))
        killpop(-Game.resources, types="oil")
        if not Game.market_resources_set:
            Game.selling_resources_points = 0
            Game.buying_resources_points = 0
        Game.population += (-Game.resources)
        Game.resources = 0
    if Game.food <= 0:
        print("OUT OF FOOD!")
        if not Game.market_food_set:
            Game.selling_food_points = 0
            Game.buying_food_points = 0
    if Game.population_growth < 0:
        print("Killed {} from decay".format(-Game.population_growth))
        killpop(-Game.population_growth)
    
def time_elapse(months):
    
    Game.values_dirty = True
    # income updates
    Game.existing_infrastructure += months * Game.infrastructure_delta
    Game.power += months * Game.power_income
    Game.food += months * Game.food_income
    Game.pollution += months * Game.pollution_income
    Game.allocation_speed += months * Game.allocation_speed_income

    if Game.age >= 2:
        Game.resources += months * Game.resources_income
    
    if Game.age >= 4:
        Game.research += months * Game.research_income
    
    if Game.age >= 10:
        Game.warmachines += months * Game.warmachines_income
    
    # limits
    Game.existing_infrastructure = max(0, Game.existing_infrastructure)
    Game.resources = max(0, Game.resources)
    Game.warmachines = max(0, Game.warmachines)
    Game.food = max(0, Game.food)
    Game.population = max(0, Game.population)
    Game.research = max(0, Game.research)
    Game.pollution = max(0, Game.pollution)

def addpop():
    # population delta
    amt = max(0, min(Game.population_growth, Game.population_max_actual - Game.population))
    Game.population = max(0, Game.population + amt)
    Game.workforce = math.floor(max(0, Game.workforce + amt))
    
    allocate_workers()

def allocate_workers(): # add employees from our workforce

    wf = math.floor(Game.workforce)
    maxtimes = math.floor(Game.allocation_speed_actual)
    for pop in range(min(maxtimes, wf)):
        
        if (Game.age >= AGE_WAR and random.random()*1000 <= Game.conscription_rate):
            Game.soldiers += 1
            continue
        elif (random.random()*100 <= Game.business_growth_actual):
            Game.private_sector += 1
            continue

        # do not add employees that require infrastructure unless it's available
        need_infra = (Game.unused_infrastructure <= 0)
        
        dice = random.random()*MAX_ALLOCATION
        compareroll = Game.points_allocated[INFR]
        if (need_infra or dice < compareroll):
            Game.employees[INFR] += 1
            continue
        compareroll += Game.points_allocated[ENVI]
        if dice < compareroll:
            Game.employees[ENVI] += 1
            continue
        compareroll += Game.points_allocated[HARV]
        if dice < compareroll:
            Game.employees[HARV] += 1
            continue
        compareroll += Game.points_allocated[AGRI]
        if dice < compareroll:
            Game.employees[AGRI] += 1
            continue
        compareroll += Game.points_allocated[DEFE]
        if dice < compareroll:
            Game.employees[DEFE] += 1
            continue
        compareroll += Game.points_allocated[SCIE]
        if dice < compareroll:
            Game.employees[SCIE] += 1
            continue
        compareroll += Game.points_allocated[POLI]
        if dice < compareroll:
            Game.employees[POLI] += 1
            continue
        compareroll += Game.points_allocated[HEAL]
        if dice < compareroll:
            Game.employees[HEAL] += 1
            continue
        
'''     if not need_infra:
            proportion_inf      = Game.employees[INFR]
            proportion_inf_exp  = Game.points_allocated[INFR] * Game.population * 0.01
            proportion_inf_diff = {'name':'inf', 'value':proportion_inf_exp - proportion_inf}
            proportion_qol      = Game.employees[ENVI]
            proportion_qol_exp  = Game.points_allocated[ENVI] * Game.population * 0.01
            proportion_qol_diff = {'name':'qol', 'value':proportion_qol_exp - proportion_qol}
            proportion_har      = Game.employees[HARV]
            proportion_har_exp  = Game.points_allocated[HARV] * Game.population * 0.01
            proportion_har_diff = {'name':'har', 'value':proportion_har_exp - proportion_har}
            proportion_agr      = Game.employees[AGRI]
            proportion_agr_exp  = Game.points_allocated[AGRI] * Game.population * 0.01
            proportion_agr_diff = {'name':'agr', 'value':proportion_agr_exp - proportion_agr}
            proportion_def      = Game.employees[DEFE]
            proportion_def_exp  = Game.points_allocated[DEFE] * Game.population * 0.01
            proportion_def_diff = {'name':'def', 'value':proportion_def_exp - proportion_def}
            proportion_sci      = Game.employees[SCIE]
            proportion_sci_exp  = Game.points_allocated[SCIE] * Game.population * 0.01
            proportion_sci_diff = {'name':'sci', 'value':proportion_sci_exp - proportion_sci}
            proportion_pol      = Game.employees[POLI]
            proportion_pol_exp  = Game.points_allocated[POLI] * Game.population * 0.01
            proportion_pol_diff = {'name':'pol', 'value':proportion_pol_exp - proportion_pol}
            proportion_hos      = Game.employees[HEAL]
            proportion_hos_exp  = Game.points_allocated[HEAL] * Game.population * 0.01
            proportion_hos_diff = {'name':'hos', 'value':proportion_hos_exp - proportion_hos}
        
            lst = [proportion_inf_diff, proportion_har_diff, proportion_agr_diff, proportion_def_diff, proportion_sci_diff, proportion_pol_diff, proportion_qol_diff, proportion_hos_diff]
            sort = max(lst, key=lambda x:x['value'])
            if sort['value'] == 0:
                continue
        if (need_infra or sort['name'] == 'inf'):   Game.employees[INFR] += 1
        elif sort['name'] == 'har': Game.employees[HARV] += 1
        elif sort['name'] == 'agr': Game.employees[AGRI] += 1
        elif sort['name'] == 'def': Game.employees[DEFE] += 1
        elif sort['name'] == 'sci': Game.employees[SCIE] += 1
        elif sort['name'] == 'pol': Game.employees[POLI] += 1
        elif sort['name'] == 'qol': Game.employees[ENVI] += 1
        elif sort['name'] == 'hos': Game.employees[HEAL] += 1'''

def killpop(amount, types="all", reduce_points=True):
    for _ in range(round(amount)):
        if Game.population <= 0:
            break
        dice = 0
        tobeat = 0
        
        if types=="oil": # all jobs that require oil
            mm = Game.employees[SCIE] + Game.employees[DEFE] + Game.employees[INFR]
            if mm == 0:
                break
            dice = random.random()*(mm)
            tobeat += Game.employees[DEFE]
            if dice < tobeat:
                #print("kill_soldier. tobeat: ", tobeat)
                kill_job(DEFE, 1, reduce_points)
                continue
            tobeat += Game.employees[SCIE]
            if dice < tobeat:
                #print("kill_scientist. tobeat: ", tobeat)
                kill_job(SCIE, 1, reduce_points)
                continue
            tobeat += Game.employees[INFR]
            if dice < tobeat:
                #print("kill_scientist. tobeat: ", tobeat)
                kill_job(INFR, 1, reduce_points)
                continue
            
        if types=="all": # all people (homeless is a status that is temporary so it's not counted here)
            dice = random.random()*Game.population
            tobeat += Game.soldiers
            if dice < tobeat:
                kill(SOLDIERS, 1)
                continue
            tobeat += Game.disabled
            if dice < tobeat:
                kill(DISABLED, 1)
                continue
            tobeat += Game.retirees
            if dice < tobeat:
                kill(RETIREES, 1)
                continue
            tobeat += Game.private_sector
            if dice < tobeat:
                kill(PRIVATE, 1)
                continue
            tobeat += Game.veterans
            if dice < tobeat:
                kill(VETERANS, 1)
                continue
            tobeat += Game.illegals
            if dice < tobeat:
                kill(ILLEGALS, 1)
                continue
            tobeat += Game.employees[INFR]
            if dice < tobeat:
                kill_job(INFR, 1, reduce_points)
                continue
            tobeat += Game.employees[ENVI]
            if dice < tobeat:
                kill_job(ENVI, 1, reduce_points)
                continue
            
        if types=="infra": # all jobs that require infrastructure
            dice = random.random()*(Game.population - Game.employees[INFR] - Game.employees[ENVI])
            
        tobeat += Game.employees[HARV]
        if dice < tobeat:
            kill_job(HARV, 1, reduce_points)
            continue
        tobeat += Game.employees[AGRI]
        if dice < tobeat:
            kill_job(AGRI, 1, reduce_points)
            continue
        tobeat += Game.employees[DEFE]
        if dice < tobeat:
            kill_job(DEFE, 1, reduce_points)
            continue
        tobeat += Game.employees[SCIE]
        if dice < tobeat:
            kill_job(SCIE, 1, reduce_points)
            continue
        tobeat += Game.employees[POLI]
        if dice < tobeat:
            kill_job(POLI, 1, reduce_points)
            continue
        tobeat += Game.employees[HEAL]
        if dice < tobeat:
            kill_job(HEAL, 1, reduce_points)
            continue
        tobeat += Game.disabled
        if dice < tobeat:
            kill(DISABLED, 1)
            continue
        tobeat += Game.veterans
        if dice < tobeat:
            kill(VETERANS, 1)
            continue
        tobeat += Game.retirees
        if dice < tobeat:
            kill(RETIREES, 1)
            continue
        # none other was chosen; kill unemployed citizen
        kill_unemployed(1)
    
    if Game.population <= 0:
        Game.population = 0
        game_over()


def kill(_type, number):
    Game.population -= 1
    if _type==HOMELESS:
        Game.homeless -= 1
    if _type==DISABLED:
        Game.disabled -= 1
    if _type==SOLDIERS:
        Game.soldiers -= 1
    if _type==VETERANS:
        Game.veterans -= 1
    if _type==RETIREES:
        Game.retirees -= 1
    if _type==PRIVATE:
        Game.private_sector -= 1
    if _type==ILLEGALS:
        Game.illegals -= 1
def kill_job(job, number, reduce_points=True):
    if reduce_points:
        Game.points_allocated[job] = max(0, Game.points_allocated[job] - number)
    Game.employees[job] = max(0, Game.employees[job] - number)
    Game.population -= number
def kill_unemployed(number):
    Game.population -= number

def game_over():
    # TEMPORARY!!!
    print("Game Over")
    Game.paused = True
    #raise SystemExit()


def del_if_found(lis, item):
    thisindex = 0
    found = False
    for avail in lis:
        if avail==item:
            found = True
            break
        thisindex += 1
    if found:
        del lis[thisindex]

def run():
    if Game.values_dirty:
        update_values()
        update_values()
        Game.values_dirty = False
    ui.display(Game, context, root_console)
    
    #tcod.sys_set_fps(60)
    #time_interval = 0.15 / Game.speed
    
    ui.check_inputs(Game)

    if not Game.paused:
        Game.time_interval_value = Game.TIME_INTERVALS[Game.speed]
        delta = time.time() - Game.last_time
        Game.time_since_last_turn += delta
        time_elapse(delta / Game.time_interval_value / 30) # months
        while Game.time_since_last_turn > Game.time_interval_value:
            Game.time_since_last_turn -= Game.time_interval_value
            day_elapse()
        Game.last_time = time.time()
    else:
        Game.last_time = time.time()

if __name__=="__main__":

    Game.advise(PRIORITY_LOW, "How to gain $ power", ["How to gain $ power:", " - For now, your primary means of gaining $ will be through exports.", " - Export food you don't need to gain $", " - (Use Ctrl & click to add 100, or Alt & click to add 1000)"])
    Game.advise(PRIORITY_LOW, "Tips to start", ["Set allocations of Public sector workers.", "Recommended starter values:", " - Construction 300", " - Agriculture 700", " - (Use Shift & click the '+' to add 10, or Ctrl & click to add 100 allocation points)", "Press the Play button or press Space to begin"])

    with tcod.context.new_terminal(
        Game.screen_width,
        Game.screen_height,
        tileset=Game.tileset,
        title="Mayor",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(Game.screen_width, Game.screen_height, order="F")
        update_values()
        while True:
            run()

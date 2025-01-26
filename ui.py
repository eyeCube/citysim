from const import *

import tcod
from tcod import libtcodpy
import math

INFOY = 8
SIDEBARX = 40
AGEX = 28

class ButtonList:
    def __init__(self):
        self.buttonList = {}
    def add(self, button, name):
        self.buttonList.update({name : button})
    def attempt_clicks(self, Game, mousex, mousey):
        for button in self.buttonList.values():
            if not button.on_release:
                button.attempt_click(Game, mousex, mousey)
    def attempt_click_release(self, Game, mousex, mousey):
        for button in self.buttonList.values():
            if button.on_release:
                button.attempt_click(Game, mousex, mousey)
    def attempt_hold_clicks(self, Game, mousex, mousey):
        for button in self.buttonList.values():
            button.attempt_hold_click(Game, mousex, mousey)
    def draw_all(self, Game, root_console, mousex, mousey):
        for button in self.buttonList.values():
            button.draw(Game, root_console, mousex, mousey)
    def reset_hold_times(self):
        for button in self.buttonList.values():
            button.holdtime = 0


class Button:
    def __init__(self, x, y, char, function, mult, age,
                 caption="", caption2="", caption_x=0, caption_y=0, caption_col=(255,255,255),
                 tab_group=0, tab_id=0, char2=0, func_check_param=0, xsize=0,
                 func_check_enable=None, func_check=None, all_right=False, mult_allowed = True, hold_allowed=True, on_release=False
                 ):
        self.x = x
        self.y = y
        self.char = char
        self.function = function
        self.mult = mult
        self.disabled = False
        self.age = age
        self.caption = caption
        self.caption2 = caption2
        self.caption_x = caption_x
        self.caption_y = caption_y
        self.caption_col = caption_col
        self.all_right = all_right
        self.tab_group = tab_group
        self.tab_id = tab_id
        self.func_check = func_check # to change the char under condition
        self.func_check_enable = func_check_enable # to enable the button under condition
        self.char2 = char2
        self.holdtime = 0
        self.mult_allowed = mult_allowed
        self.func_check_param = func_check_param
        self.hold_allowed = hold_allowed
        self.on_release = on_release
        self.xsize = xsize
    def attempt_click(self, Game, mousex, mousey, extramultiplier=1):
        if Game.age < self.age:
            return
        if self.disabled:
            return
        if (mousey!=self.y):
            return
        if (self.all_right and self.x>mousex):
            return
        if (not self.all_right and (mousex < self.x or mousex > self.x+self.xsize)):
            return
        if (self.tab_group > 0 and Game.tab_groups[self.tab_group - 1] != self.tab_id):
            return
        if (self.tab_group < 4 and Game.tab_groups[2] != TAB_DASHBOARD):
            return
        if (self.func_check_enable and self.func_check_enable(Game)==False):
            return
        multiplier = self.mult * extramultiplier if self.mult_allowed else self.mult
        if Game.shift_held:
            multiplier *= 10
        if Game.ctrl_held:
            multiplier *= 100
        if Game.alt_held:
            multiplier *= 1000
        self.function(Game, multiplier)
        Game.values_dirty = True
    def attempt_hold_click(self, Game, mousex, mousey):
        if not self.hold_allowed:
            return
        if Game.age < self.age:
            self.holdtime = 0
            return
        if self.disabled:
            self.holdtime = 0
            return
        if (mousey!=self.y):
            self.holdtime = 0
            return
        if (self.all_right and self.x>mousex):
            self.holdtime = 0
            return
        if (not self.all_right and (mousex < self.x or mousex > self.x+self.xsize)):
            self.holdtime = 0
            return
        if (self.tab_group > 0 and Game.tab_groups[self.tab_group - 1] != self.tab_id):
            self.holdtime = 0
            return
        if (self.tab_group < 4 and Game.tab_groups[2] != TAB_DASHBOARD):
            self.holdtime = 0
            return
        if (self.func_check_enable and self.func_check_enable(Game)==False):
            return
        self.holdtime += 1
        if self.holdtime >= 15:
            multiplier = 1
            if self.holdtime >= 240:
                multiplier = 1000
            elif self.holdtime >= 180:
                multiplier = 100
            elif self.holdtime >= 120:
                multiplier = 10
            if (self.holdtime >= 60 or self.holdtime % 4 == 0):
                self.attempt_click(Game, mousex, mousey, extramultiplier=multiplier)
        
    def draw(self, Game, root_console, mousex, mousey):
        if Game.age < self.age:
            return
        if (self.tab_group > 0 and Game.tab_groups[self.tab_group - 1] != self.tab_id):
            return
        if (self.tab_group < 4 and Game.tab_groups[2] != TAB_DASHBOARD):
            return
        xmet = False
        ymet = False
        if (self.func_check_enable and self.func_check_enable(Game)==False):
            lightcol = COL_UI_DARK
            interactable = False
        else:
            lightcol = COL_UI_INTERACTABLE
            interactable = True
        if (mousey==self.y):
            ymet = True
        if (self.all_right and self.x<=mousex):
            xmet = True
        if (not self.all_right and (mousex >= self.x and mousex <= self.x+self.xsize)):
            xmet = True
        ch = self.char
        if (self.func_check and self.func_check(Game, self.func_check_param)):
            ch = self.char2
        if (interactable and xmet and ymet):
            libtcodpy.console_put_char_ex(root_console, self.x, self.y, ch, (0,0,0,), lightcol)
        else:
            libtcodpy.console_put_char_ex(root_console, self.x, self.y, ch, lightcol, COL_UI_BG)
        if (self.caption2 != "" and self.func_check(Game, self.func_check_param)):
            root_console.print(x=self.caption_x,y=self.caption_y, string=self.caption2, fg=self.caption_col)
        elif self.caption != "":
            root_console.print(x=self.caption_x,y=self.caption_y, string=self.caption, fg=self.caption_col)

class Tab:
    def __init__(self, x, y, name, function, func_check, age, caption="", caption_x=0, caption_y=0, tab_group=3, tab_id=TAB_DASHBOARD):
        self.x = x
        self.y = y
        self.name = name
        self.function = function
        self.func_check = func_check
        self.disabled = False
        self.age = age
        self.caption = caption
        self.caption_x = caption_x
        self.caption_y = caption_y
        self.size = len(name)
        self.tab_group=tab_group
        self.tab_id=tab_id
        self.on_release = True
        
    def attempt_click(self, Game, mousex, mousey):
        if (self.tab_group > 0 and Game.tab_groups[self.tab_group - 1] != self.tab_id):
            return
        if Game.age < self.age:
            return
        if self.disabled:
            return
        if (mousey != self.y):
            return
        if (mousex > self.x+self.size):
            return
        if (mousex < self.x):
            return
        self.function(Game)
        Game.values_dirty = True
    def attempt_hold_click(self, Game, mousex, mousey):
        pass
        
    def draw(self, Game, root_console, mousex, mousey):
        if (self.tab_group > 0 and Game.tab_groups[self.tab_group - 1] != self.tab_id):
            return
        if Game.age < self.age:
            return
        xmet = False
        ymet = False
        if (mousey==self.y):
            ymet = True
        if (mousex >= self.x and mousex <= self.x + self.size):
            xmet = True
        on = self.func_check(Game)
        lightcol = COL_UI_HIGHLIGHT if on else COL_UI_INTERACTABLE
        fg=lightcol
        bg=BLACK
        if (xmet and ymet):
            fg=BLACK
            bg=lightcol
            i = 0
            for ch in self.name:
                c = ch.upper() if on else ch
                libtcodpy.console_put_char_ex(root_console, self.x + 1 + i, self.y, c, fg, bg)
                i += 1
            if self.caption != "":
                root_console.print(x=self.caption_x,y=self.caption_y, string=caption, fg=lightcol)
        else:
            s = self.name.upper() if on else self.name
            root_console.print(x=self.x + 1,y=self.y, string=s, fg=lightcol)
        if on:
            libtcodpy.console_put_char_ex(root_console, self.x, self.y, 219, lightcol, bg)
        else:
            libtcodpy.console_put_char_ex(root_console, self.x, self.y, 228, fg, bg)


def _lvcost(clv): # clv == current level
    v = pow(2, clv)
    if clv <= 5:
        return GMULT * v
    w = pow(10, max(1, round(math.log10(v)) - 2))
    return GMULT * round(v / w) * w

buttonList = ButtonList()
fxpx = 2 # 8

def tab_sectors(Game): Game.tab_groups[0] = TAB_SECTORS
def tab_sectors_check(Game): return True if Game.tab_groups[0] == TAB_SECTORS else False
def tab_private_sector(Game): Game.tab_groups[0] = TAB_PRIVATE_SECTORS
def tab_private_sector_check(Game): return True if Game.tab_groups[0] == TAB_PRIVATE_SECTORS else False
def tab_agencies(Game): Game.tab_groups[0] = TAB_AGENCIES
def tab_agencies_check(Game): return True if Game.tab_groups[0] == TAB_AGENCIES else False
def tab_agencies2(Game): Game.tab_groups[0] = TAB_AGENCIES2
def tab_agencies2_check(Game): return True if Game.tab_groups[0] == TAB_AGENCIES2 else False
def tab_agencies3(Game): Game.tab_groups[0] = TAB_AGENCIES3
def tab_agencies3_check(Game): return True if Game.tab_groups[0] == TAB_AGENCIES3 else False
def tab_agencies4(Game): Game.tab_groups[0] = TAB_AGENCIES4
def tab_agencies4_check(Game): return True if Game.tab_groups[0] == TAB_AGENCIES4 else False
def tab_agencies5(Game): Game.tab_groups[0] = TAB_AGENCIES5
def tab_agencies5_check(Game): return True if Game.tab_groups[0] == TAB_AGENCIES5 else False
def tab_techs(Game): Game.tab_groups[1] = TAB_TECHS
def tab_techs_check(Game): return True if Game.tab_groups[1] == TAB_TECHS else False
def tab_tech_tree(Game): Game.tab_groups[1] = TAB_TECH_TREE
def tab_tech_tree_check(Game): return True if Game.tab_groups[1] == TAB_TECH_TREE else False
def tab_history(Game): Game.tab_groups[1] = TAB_HISTORY
def tab_history_check(Game): return True if Game.tab_groups[1] == TAB_HISTORY else False
def tab_settings(Game): Game.tab_groups[1] = TAB_SETTINGS
def tab_settings_check(Game): return True if Game.tab_groups[1] == TAB_SETTINGS else False
def tab_advisors(Game): Game.tab_groups[1] = TAB_ADVISORY
def tab_advisors_check(Game): return True if Game.tab_groups[1] == TAB_ADVISORY else False
def tab_info(Game): pass
def tab_info_check(Game): return True
def tab_dashboard(Game): Game.tab_groups[2] = TAB_DASHBOARD
def tab_dashboard_check(Game): return True if Game.tab_groups[2] == TAB_DASHBOARD else False
def tab_world_map(Game): Game.tab_groups[2] = TAB_WORLDMAP
def tab_world_map_check(Game): return True if Game.tab_groups[2] == TAB_WORLDMAP else False
def tab_stats(Game): Game.tab_groups[2] = TAB_STATS
def tab_stats_check(Game): return True if Game.tab_groups[2] == TAB_STATS else False
buttonList.add(Tab(2, 7, "public", tab_sectors, tab_sectors_check, 0), "sectors_tab")
buttonList.add(Tab(13, 7, "agencies a", tab_agencies, tab_agencies_check, AGE_FOUNDRY), "agencies_tab")
buttonList.add(Tab(26, 7, "b", tab_agencies2, tab_agencies2_check, AGE_FOUNDRY), "agencies2_tab")
buttonList.add(Tab(30, 7, "c", tab_agencies3, tab_agencies3_check, AGE_FOUNDRY), "agencies3_tab")
buttonList.add(Tab(34, 7, "d", tab_agencies4, tab_agencies4_check, AGE_FOUNDRY), "agencies4_tab")
#buttonList.add(Tab(34, 7, "e", tab_agencies5, tab_agencies5_check, AGE_INTEGRATION), "agencies5_tab")
buttonList.add(Tab(42, 18, "desk", tab_techs, tab_techs_check, AGE_RECONSTRUCTION), "techs_tab")
buttonList.add(Tab(54, 18, "tree", tab_tech_tree, tab_tech_tree_check, AGE_RECONSTRUCTION), "tech_tree_tab")
#buttonList.add(Tab(60, 18, "History", tab_history, tab_history_check, AGE_RECONSTRUCTION), "history_tab")
buttonList.add(Tab(68, 18, "advisory", tab_advisors, tab_advisors_check, 0), "advisors_tab")
buttonList.add(Tab(73, 7, "info", tab_info, tab_info_check, 0), "info_tab")
#buttonList.add(Tab(73, 7, "selected", tab_info, tab_info_check, 0), "info_tab")
buttonList.add(Tab(72, 2, "dash", tab_dashboard, tab_dashboard_check, 0, tab_group=4, tab_id=TAB_GAME), "dashboard_tab")
buttonList.add(Tab(52, 2, "world", tab_world_map, tab_world_map_check, 0, tab_group=4, tab_id=TAB_GAME), "map_tab")
buttonList.add(Tab(62, 2, "law", tab_stats, tab_stats_check, 0, tab_group=4, tab_id=TAB_GAME), "stats_tab")

def market_food_set(Game, value): Game.market_food_set = not Game.market_food_set # auto commerce
def market_oil_set(Game, value): Game.market_resources_set = not Game.market_resources_set
def market_food_check(Game, value): return Game.market_food_set
def market_oil_check(Game, value): return Game.market_resources_set
def import_oil_change(Game, value):
    Game.market_resources_set = False
    if value > 0:
        if Game.buying_resources_points >= 0:
            Game.buying_resources_points = max(0, Game.buying_resources_points + value)
            Game.selling_resources_points = 0
        else:
            Game.selling_resources_points = max(0, Game.selling_resources_points - value)
            Game.buying_resources_points = 0
    else:
        if Game.selling_resources_points >= 0:
            Game.selling_resources_points = max(0, Game.selling_resources_points - value)
            Game.buying_resources_points = 0
        else:
            Game.buying_resources_points = max(0, Game.buying_resources_points + value)
            Game.selling_resources_points = 0
def import_oil_delta(Game, value):
    if Game.selling_resources_points > 0:
        Game.selling_resources_points = max(0, Game.selling_resources_points + value)
        Game.buying_resources_points = 0
    else:
        Game.buying_resources_points = max(0, Game.buying_resources_points + value)
        Game.selling_resources_points = 0
def import_food_change(Game, value): 
    Game.market_food_set = False
    if value > 0:
        if Game.buying_food_points >= 0:
            Game.buying_food_points = max(0, Game.buying_food_points + value)
            Game.selling_food_points = 0
        else:
            Game.selling_food_points = max(0, Game.selling_food_points - value)
            Game.buying_food_points = 0
    else:
        if Game.selling_food_points >= 0:
            Game.selling_food_points = max(0, Game.selling_food_points - value)
            Game.buying_food_points = 0
        else:
            Game.buying_food_points = max(0, Game.buying_food_points + value)
            Game.selling_food_points = 0
def import_food_delta(Game, value):
    if Game.selling_food_points > 0:
        Game.selling_food_points = max(0, Game.selling_food_points + value)
        Game.buying_food_points = 0
    else:
        Game.buying_food_points = max(0, Game.buying_food_points + value)
        Game.selling_food_points = 0
buttonList.add(Button(41,     4, ICON_BUTTON_ARROW_DOWN, import_oil_change, 1, AGE_FOUNDRY, tab_group=3, tab_id=TAB_DASHBOARD, caption="Im", caption_x=42, caption_y=4), "import_oil_up")
buttonList.add(Button(45,     4, ICON_BUTTON_ARROW_RIGHT, import_oil_change, -1, AGE_FOUNDRY, tab_group=3, tab_id=TAB_DASHBOARD, caption="Ex", caption_x=46, caption_y=4), "import_oil_down")
buttonList.add(Button(47,     5, ICON_BUTTON_MINUS, import_oil_delta, -1, AGE_FOUNDRY, tab_group=3, tab_id=TAB_DASHBOARD), "import_oil_delta_down")
buttonList.add(Button(fxpx,   4, ICON_BUTTON_ARROW_DOWN, import_food_change, 1, 0, tab_group=3, tab_id=TAB_DASHBOARD, caption="Im", caption_x=fxpx+1, caption_y=4), "import_food_up")
buttonList.add(Button(fxpx+4, 4, ICON_BUTTON_ARROW_RIGHT, import_food_change, -1, 0, tab_group=3, tab_id=TAB_DASHBOARD, caption="Ex", caption_x=fxpx+5, caption_y=4), "import_food_down")
buttonList.add(Button(fxpx+6, 5, ICON_BUTTON_MINUS, import_food_delta, -1, 0, tab_group=3, tab_id=TAB_DASHBOARD), "import_food_delta_down")


LEVELUPX = 25
def _level_up(Game, job):
    cost = _lvcost(Game.levels[job])
    if Game.power < cost:
        print("Not enough $$$. You have {}".format(number(Game.power)))
        return
    Game.power -= cost
    Game.levels[job] += 1
def builders_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[INFR] = min(MAX_ALLOCATION, max(0, Game.points_allocated[INFR] + value))
buttonList.add(Button(2, 10, 133, builders_change, -1, 0, tab_group=1,tab_id=TAB_SECTORS), "builders_down")
buttonList.add(Button(4, 10, 132, builders_change, 1, 0, tab_group=1,tab_id=TAB_SECTORS), "builders_up")
def builders_level_up(Game, value): _level_up(Game, INFR)
buttonList.add(Button(LEVELUPX, 9, 22, builders_level_up, -1, 1, tab_group=1,tab_id=TAB_SECTORS), "builders_level")
def farmers_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[AGRI] = min(MAX_ALLOCATION, max(0, Game.points_allocated[AGRI] + value))
buttonList.add(Button(2, 12, 133, farmers_change, -1, 0, tab_group=1,tab_id=TAB_SECTORS), "farmers_down")
buttonList.add(Button(4, 12, 132, farmers_change, 1, 0, tab_group=1,tab_id=TAB_SECTORS), "farmers_up")
def farmers_level_up(Game, value): _level_up(Game, AGRI)
buttonList.add(Button(LEVELUPX, 11, 22, farmers_level_up, -1, 1, tab_group=1,tab_id=TAB_SECTORS), "farmers_level")
def miners_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[HARV] = min(MAX_ALLOCATION, max(0, Game.points_allocated[HARV] + value))
buttonList.add(Button(2, 14, 133, miners_change, -1, 2, tab_group=1,tab_id=TAB_SECTORS), "miners_down")
buttonList.add(Button(4, 14, 132, miners_change, 1, 2, tab_group=1,tab_id=TAB_SECTORS), "miners_up")
def miners_level_up(Game, value): _level_up(Game, HARV)
buttonList.add(Button(LEVELUPX, 13, 22, miners_level_up, -1, 2, tab_group=1,tab_id=TAB_SECTORS), "miners_level")
def scientists_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[SCIE] = min(MAX_ALLOCATION, max(0, Game.points_allocated[SCIE] + value))
buttonList.add(Button(2, 16, 133, scientists_change, -1, 4, tab_group=1,tab_id=TAB_SECTORS), "scientists_down")
buttonList.add(Button(4, 16, 132, scientists_change, 1, 4, tab_group=1,tab_id=TAB_SECTORS), "scientists_up")
def scientists_level_up(Game, value): _level_up(Game, SCIE)
buttonList.add(Button(LEVELUPX, 15, 22, scientists_level_up, -1, 4, tab_group=1,tab_id=TAB_SECTORS), "scientists_level")
def custodial_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[ENVI] = min(MAX_ALLOCATION, max(0, Game.points_allocated[ENVI] + value))
buttonList.add(Button(2, 18, 133, custodial_change, -1, 5, tab_group=1,tab_id=TAB_SECTORS), "custodial_down")
buttonList.add(Button(4, 18, 132, custodial_change, 1, 5, tab_group=1,tab_id=TAB_SECTORS), "custodial_up")
def custodial_level_up(Game, value): _level_up(Game, ENVI)
buttonList.add(Button(LEVELUPX, 17, 22, custodial_level_up, -1, 5, tab_group=1,tab_id=TAB_SECTORS), "custodial_level")
def medics_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[HEAL] = min(MAX_ALLOCATION, max(0, Game.points_allocated[HEAL] + value))
buttonList.add(Button(2, 20, 133, medics_change, -1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_SECTORS), "medics_down")
buttonList.add(Button(4, 20, 132, medics_change, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_SECTORS), "medics_up")
def medics_level_up(Game, value): _level_up(Game, HEAL)
buttonList.add(Button(LEVELUPX, 19, 22, medics_level_up, -1, 6, tab_group=1,tab_id=TAB_SECTORS), "medics_level")
def police_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[POLI] = min(MAX_ALLOCATION, max(0, Game.points_allocated[POLI] + value))
buttonList.add(Button(2, 22, 133, police_change, -1, AGE_SECURITY, tab_group=1,tab_id=TAB_SECTORS), "police_down")
buttonList.add(Button(4, 22, 132, police_change, 1, AGE_SECURITY, tab_group=1,tab_id=TAB_SECTORS), "police_up")
def police_level_up(Game, value): _level_up(Game, POLI)
buttonList.add(Button(LEVELUPX, 21, 22, police_level_up, -1, 9, tab_group=1,tab_id=TAB_SECTORS), "police_level")
def soldiers_change(Game, value): 
    if (value > 0 and Game.points_remaining < value):
        value = Game.points_remaining
    Game.points_allocated[DEFE] = min(MAX_ALLOCATION, max(0, Game.points_allocated[DEFE] + value))
buttonList.add(Button(2, 24, 133, soldiers_change, -1, AGE_WAR, tab_group=1,tab_id=TAB_SECTORS), "soldiers_down")
buttonList.add(Button(4, 24, 132, soldiers_change, 1, AGE_WAR, tab_group=1,tab_id=TAB_SECTORS), "soldiers_up")
def soldiers_level_up(Game, value): _level_up(Game, DEFE)
buttonList.add(Button(LEVELUPX, 23, 22, soldiers_level_up, -1, 10, tab_group=1,tab_id=TAB_SECTORS), "soldiers_level")

def pause_button(Game, value): Game.paused = not Game.paused
def check_pause(Game, value): return Game.paused
def fast_forward_button(Game, value):
    Game.speed = min(6, Game.speed + 1)
    ratio = Game.time_since_last_turn / Game.time_interval_value
    Game.time_interval_value = Game.TIME_INTERVALS[Game.speed]
    Game.time_since_last_turn = ratio * Game.time_interval_value
def slow_button(Game, value):
    Game.speed = max(0, Game.speed - 1)
    ratio = Game.time_since_last_turn / Game.time_interval_value
    Game.time_interval_value = Game.TIME_INTERVALS[Game.speed]
    Game.time_since_last_turn = ratio * Game.time_interval_value
#buttonList.add(Button(4, 1, 255, play_button, 1, 0), "button_play")
buttonList.add(Button(3, 1, 254, pause_button, 1, 0, func_check=check_pause, char2=255, caption=" ", caption2="paused", caption_x=5, caption_y=1, caption_col=YELLOW, tab_group=4,tab_id=TAB_GAME), "button_pause")
buttonList.add(Button(1, 0, 30, slow_button, 1, 0, tab_group=4,tab_id=TAB_GAME), "button_slow")
buttonList.add(Button(3, 0, 29, fast_forward_button, 1, 0, tab_group=4,tab_id=TAB_GAME), "button_fast_forward")

# agencies

def food_distribution_change(Game, value): 
    Game.food_distribution = min(7, max(0, Game.food_distribution + value))
def food_quality_change(Game, value): 
    Game.food_distribution_efficiency = min(9, max(0, Game.food_distribution_efficiency + value))

def commerce_fees_change(Game, value): 
    Game.agency_commerce_fees = min(5, max(0, Game.agency_commerce_fees + value))

def travel_policy_change(Game, value): 
    Game.travel_policy = min(5, max(0, Game.travel_policy + value))
def border_control_change(Game, value): 
    Game.border_control = min(5, max(0, Game.border_control + value))

def wages_change(Game, value): 
    Game.wages = min(21, max(0, Game.wages + value))
def safety_law_change(Game, value):
    Game.safety_law = min(10, max(0, Game.safety_law + value)) # 10 * X = percent coverage

def civilian_taxing_change(Game, value): 
    Game.civilian_taxing = min(18, max(4, Game.civilian_taxing + value))
def investor_taxing_change(Game, value): 
    Game.investor_taxing = min(18, max(4, Game.investor_taxing + value))
def sales_taxing_change(Game, value): 
    Game.sales_taxing = min(18, max(4, Game.sales_taxing + value))
'''def weapons_funding_change(Game, value): 
    Game.weapons_funding = min(4, max(0, Game.weapons_funding + value))
#buttonList.add(Button(2, 18, 174, weapons_funding_change, -1, 3, tab_group=1,tab_id=TAB_AGENCIES), "weapons_funding_down")
#buttonList.add(Button(6, 18, 175, weapons_funding_change, 1, 3, tab_group=1,tab_id=TAB_AGENCIES), "weapons_funding_up")
def civilian_weapons_funding_change(Game, value): 
    Game.civilian_funding = min(4, max(0, Game.civilian_funding + value))
    Game.weapons_funding = 4 - Game.civilian_funding
buttonList.add(Button(2, 18, 174, civilian_weapons_funding_change, -1, 10, tab_group=1,tab_id=TAB_AGENCIES), "civilian_funding_down")
buttonList.add(Button(6, 18, 175, civilian_weapons_funding_change, 1, 10, tab_group=1,tab_id=TAB_AGENCIES), "civilian_funding_up")
'''

def corrections_change(Game, value): 
    Game.corrections = min(5, max(0, Game.corrections + value))
def punishment_change(Game, value): 
    Game.punishment = min(5, max(0, Game.punishment + value))

def environmental_policy_change(Game, value):
    Game.environmental_policy = min(5, max(0, Game.environmental_policy + value))
def environmental_policy_set(Game, value):
    Game.environmental_policy = value
def environmental_policy_check(Game, value):
    return Game.environmental_policy == value

def __cost_to_upgrade_allocation(Game):
    powerm = 1.5 if Game.public_schools_researched else 2
    return GMULT * 100 * pow(1 + Game.number_allocation_upgrades, powerm)
def upgrade_allocation(Game, value):
    for i in range(value):
        cost = __cost_to_upgrade_allocation(Game)
        if Game.power >= cost:
            Game.number_allocation_upgrades += 1
            Game.allocation_speed += 100
            Game.allocation_speed_maximum += 100
            Game.power -= cost
        else:
            break
def allocation_change(Game, value):
    Game.allocation_speed = min(Game.allocation_speed_maximum, max(0, Game.allocation_speed + value))
def __cost_to_purchase_research(Game):
    return 0.025*(max(1000, Game.population + Game.research - Game.trust*1000)) + GMULT * 20
def research_purchase(Game, value): #purchase_info
    cost = value * __cost_to_purchase_research(Game)
    if Game.power >= cost:
        Game.research += 10 * GMULT * value
        Game.power -= cost
    
def housing_subsidies_change(Game, value):  Game.housing_subsidies = min(7, max(0, Game.housing_subsidies + value))
def growth_rate_change(Game, value):  Game.growth_infrastructure_rate = min(5, max(0, Game.growth_infrastructure_rate + value))

def fulltime_hours_change(Game, value):  Game.fulltime_hours = min(7, max(0, Game.fulltime_hours + value))

def birth_control_change(Game, value):  Game.birth_control = min(4, max(0, Game.birth_control + value))
def check_birth_control(Game): return Game.contraceptives_researched

def export_pollution_set(Game, value):
    Game.export_pollution = not Game.export_pollution
    Game.import_pollution = False
def export_pollution_check(Game, value): return Game.export_pollution
def import_pollution_set(Game, value):
    Game.import_pollution = not Game.import_pollution
    Game.export_pollution = False
def import_pollution_check(Game, value): return Game.import_pollution
    
def funding_education_change(Game, value): Game.funding_education   = min(5, max(0, Game.funding_education + value))

def income_assistance_change(Game, value): Game.income_assistance_policy    = min(30, max(0, Game.income_assistance_policy + value))
def veteran_pension_change(Game, value): Game.veteran_pension_policy    = min(30, max(0, Game.veteran_pension_policy + value))
def health_insurance_change(Game, value): Game.health_insurance_policy  = min(30, max(0, Game.health_insurance_policy + value))


yy = -1

# zua
buttonList.add(Button(2, 10+yy, 174, growth_rate_change, -1, AGE_FOUNDRY, tab_group=1,tab_id=TAB_AGENCIES), "growth_rate_down")
buttonList.add(Button(6, 10+yy, 175, growth_rate_change, 1, AGE_FOUNDRY, tab_group=1,tab_id=TAB_AGENCIES), "growth_rate_up")
buttonList.add(Button(2, 11+yy, 174, housing_subsidies_change, -1, AGE_FOUNDRY, tab_group=1,tab_id=TAB_AGENCIES), "housing_subsidies_down")
buttonList.add(Button(6, 11+yy, 175, housing_subsidies_change, 1, AGE_FOUNDRY, tab_group=1,tab_id=TAB_AGENCIES), "housing_subsidies_up")

# fma
buttonList.add(Button(2, 14+yy, 174, food_distribution_change, -1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "food_distribution_down")
buttonList.add(Button(6, 14+yy, 175, food_distribution_change, 1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "food_distribution_up")
buttonList.add(Button(2, 15+yy, 174, food_quality_change, -1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "food_quality_down")
buttonList.add(Button(6, 15+yy, 175, food_quality_change, 1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "food_quality_up")
buttonList.add(Button(2, 16+yy, 174, birth_control_change, -1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES, func_check_enable=check_birth_control), "birth_control_down")
buttonList.add(Button(6, 16+yy, 175, birth_control_change, 1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES, func_check_enable=check_birth_control), "birth_control_up")

yy = 0

# ea
buttonList.add(Button(2, 8, 22, upgrade_allocation, 1, AGE_TRUST, tab_group=1,tab_id=TAB_SECTORS), "upgrade_allocation")
buttonList.add(Button(4, 18+yy, 22, upgrade_allocation, 1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "upgrade_allocation2")
buttonList.add(Button(2, 18+yy, 174, allocation_change, -1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "lower_allocation")
buttonList.add(Button(6, 18+yy, 175, allocation_change, 1, AGE_TRUST, tab_group=1,tab_id=TAB_AGENCIES), "raise_allocation")
buttonList.add(Button(4, 19+yy, 21, research_purchase, 1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES), "research_purchase")
buttonList.add(Button(2, 20+yy, 174, funding_education_change, -1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES), "funding_education_down")
buttonList.add(Button(6, 20+yy, 175, funding_education_change, 1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES), "funding_education_up")

# ca
buttonList.add(Button(3, 23+yy, 220, market_food_set, 1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES, func_check=market_food_check, char2=221), "market_food_set")
buttonList.add(Button(9, 23+yy, 220, market_oil_set, 1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES, func_check=market_oil_check, char2=221), "market_oil_set")
buttonList.add(Button(2, 24+yy, 174, commerce_fees_change, -1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES), "commerce_fees_down")
buttonList.add(Button(6, 24+yy, 175, commerce_fees_change, 1, AGE_RECONSTRUCTION, tab_group=1,tab_id=TAB_AGENCIES), "commerce_fees_up")

yy = -1

# ra
buttonList.add(Button(2, 10+yy, 174, civilian_taxing_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "civilian_taxes_down")
buttonList.add(Button(6, 10+yy, 175, civilian_taxing_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "civilian_taxes_up")
buttonList.add(Button(2, 11+yy, 174, investor_taxing_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "investor_taxes_down")
buttonList.add(Button(6, 11+yy, 175, investor_taxing_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "investor_taxes_up")
buttonList.add(Button(2, 12+yy, 174, sales_taxing_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "sales_taxes_down")
buttonList.add(Button(6, 12+yy, 175, sales_taxing_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "sales_taxes_up")

# lla
buttonList.add(Button(2, 15+yy, 174, wages_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "wages_down")
buttonList.add(Button(6, 15+yy, 175, wages_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "wages_up")
buttonList.add(Button(2, 16+yy, 174, safety_law_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "safety_law_down")
buttonList.add(Button(6, 16+yy, 175, safety_law_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "safety_law_up")
buttonList.add(Button(2, 17+yy, 174, fulltime_hours_change, -1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "fulltime_hours_down")
buttonList.add(Button(6, 17+yy, 175, fulltime_hours_change, 1, AGE_2NDINDUSTRIAL, tab_group=1,tab_id=TAB_AGENCIES2), "fulltime_hours_up")

yy = -1

# gea
#buttonList.add(Button(2, 20+yy, 174, environmental_policy_change, -1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "environmental_policy_down")
#buttonList.add(Button(6, 20+yy, 175, environmental_policy_change, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "environmental_policy_up")
buttonList.add(Button(3, 20+yy, ICON_BUTTON_RADIO, import_pollution_set, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2, func_check=import_pollution_check, char2=ICON_BUTTON_RADIO_ON, hold_allowed=False), "import_pollution")
buttonList.add(Button(7, 20+yy, ICON_BUTTON_RADIO, export_pollution_set, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2, func_check=export_pollution_check, char2=ICON_BUTTON_RADIO_ON, hold_allowed=False), "export_pollution")
for h in range(6):
    buttonList.add(Button(4+17+h, 20+yy, 196, environmental_policy_set, h, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2, mult_allowed=False, func_check=environmental_policy_check, func_check_param=h, char2=92, on_release=True), "environmental_policy_set{}".format(h))

# ssa
buttonList.add(Button(2, 23+yy, ICON_BUTTON_MINUS, health_insurance_change, -1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "health_insurance_down")
buttonList.add(Button(8, 23+yy, ICON_BUTTON_PLUS, health_insurance_change, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "health_insurance_up")
buttonList.add(Button(2, 24+yy, ICON_BUTTON_MINUS, veteran_pension_change, -1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "veteran_pension_down")
buttonList.add(Button(8, 24+yy, ICON_BUTTON_PLUS, veteran_pension_change, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "veteran_pension_up")
buttonList.add(Button(2, 25+yy, ICON_BUTTON_MINUS, income_assistance_change, -1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "income_assistance_down")
buttonList.add(Button(8, 25+yy, ICON_BUTTON_PLUS, income_assistance_change, 1, AGE_AUTOMATION, tab_group=1,tab_id=TAB_AGENCIES2), "income_assistance_up")

'''


buttonList.add(Button(2, 24, 174, travel_policy_change, -1, AGE_EXPANSION, tab_group=1,tab_id=TAB_AGENCIES), "travel_policy_down")
buttonList.add(Button(6, 24, 175, travel_policy_change, 1, AGE_EXPANSION, tab_group=1,tab_id=TAB_AGENCIES), "travel_policy_up")
buttonList.add(Button(2, 23, 174, border_control_change, -1, AGE_EXPANSION, tab_group=1,tab_id=TAB_AGENCIES), "border_control_down")
buttonList.add(Button(6, 23, 175, border_control_change, 1, AGE_EXPANSION, tab_group=1,tab_id=TAB_AGENCIES), "border_control_up")
buttonList.add(Button(2, 21, 174, corrections_change, -1, AGE_SECURITY, tab_group=1,tab_id=TAB_AGENCIES), "corrections_down")
buttonList.add(Button(6, 21, 175, corrections_change, 1, AGE_SECURITY, tab_group=1,tab_id=TAB_AGENCIES), "corrections_up")
buttonList.add(Button(2, 20, 174, punishment_change, -1, AGE_SECURITY, tab_group=1,tab_id=TAB_AGENCIES), "punishment_down")
buttonList.add(Button(6, 20, 175, punishment_change, 1, AGE_SECURITY, tab_group=1,tab_id=TAB_AGENCIES), "punishment_up")
'''

def age_change(Game, value):
    if Game.age >= Game.age_max:
        return
    required_power = AGES[Game.age]['Upgrade']['$']
    if Game.power < required_power:
        print("Not enough $$$")
        return
    Game.power -= required_power
    Game.age += 1
    Game.research_decay += 0.15
    #Game.paused = True
    Game.add_new_available_techs()

    Game.population_max += Game.age*100*GMULT
    Game.allocation_speed += 50
    Game.allocation_speed_maximum += 50

    pmult = 1
    if Game.age == AGE_SURVIVAL: # at age 1, set levels to 1, all get +0.01% efficiency bonus for free.
        Game.levels[HARV] = 1
        Game.levels[INFR] = 1
        Game.levels[AGRI] = 1
        Game.levels[SCIE] = 5
        Game.levels[ENVI] = 5
        Game.levels[HEAL] = 10
        Game.levels[POLI] = 10
        Game.levels[DEFE] = 15
    elif (Game.age == AGE_FOUNDRY):
        Game.advise(PRIORITY_LOW, "Foundry Epoch", ["You have gained access to:", " - Industry sector", " - Oil resource", " - Oil export / import", " - Agencies tab & the Zoning agency", "Industry collects Oil for you, which is needed for almost everything in this age.", "Allocate to the Industry sector!"])
        Game.employees[HARV] = 1000
        Game.population += 1000
    elif (Game.age == AGE_TRUST):
        Game.immigration += 1
        Game.trust += 5
        pmult = 2
    elif Game.age == AGE_2NDINDUSTRIAL:
        Game.environmental_policy = 1
    elif Game.age == AGE_PROSPEROUS:
        pmult = 4
    elif Game.age == AGE_SECURITY:
        Game.punishment = 1
        Game.corrections = 1
    elif Game.age == AGE_EXPANSION:
        Game.travel_policy = 1
        Game.border_control = 1
    if (Game.age >= AGE_RECONSTRUCTION):
        Game.immigration += 1 + 0.5*Game.age*Game.wealth
    # increase threat
    #if Game.age >= 4:
    #    Game.threat_level += 1
    #if Game.age >= 10:
        #Game.deaths_per_month_from_terrorists += 1
    if pmult > 1:
        Game.land *= pmult
        Game.population *= pmult
        Game.pollution *= pmult
        Game.employees[AGRI] *= pmult
        Game.employees[INFR] *= pmult
        Game.employees[SCIE] *= pmult
        Game.employees[ENVI] *= pmult
        Game.employees[HEAL] *= pmult
        Game.employees[HARV] *= pmult
        Game.private_sector *= pmult
        Game.existing_infrastructure *= pmult
buttonList.add(Button(AGEX-1, 1, 26, age_change, 1, 0, xsize=25, tab_group=4,tab_id=TAB_GAME), "age_up")

LISTPOS_Y = 19
def purchase_technology(Game, value):
    if Game.mouse_x >= 79: # make room for the dismiss button which is placed at 79 ...
        return
    index = Game.mouse_y - LISTPOS_Y
    if (index + 1 > len(Game.list_available_techs)):
        return
    tech_id = Game.list_available_techs[index]
    tech_data = Game.techs[tech_id]
    
    required_power = tech_data['cost']
    if Game.power < required_power:
        print("Not enough $$$")
        return
    
    required_research = tech_data['research']
    if Game.research < required_research:
        print("Not enough Information")
        return

    # remove from list
    del Game.list_available_techs[index]

    # spend resources
    Game.power -= required_power
    Game.research -= required_research

    # queue the technology for engineering / development
    Game.queue_tech(tech_id, tech_data)
def dismiss_tech(Game, value):
    index = Game.mouse_y - LISTPOS_Y
    if (index + 1 > 6 or index + 1 > len(Game.list_available_techs)):
        return

    del Game.list_available_techs[index]
    print("Deleted index {}".format(index))
    
    
    
buttonList.add(Button(40, LISTPOS_Y,   127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_1")
buttonList.add(Button(40, LISTPOS_Y+1, 127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_2")
buttonList.add(Button(40, LISTPOS_Y+2, 127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_3")
buttonList.add(Button(40, LISTPOS_Y+3, 127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_4")
buttonList.add(Button(40, LISTPOS_Y+4, 127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_5")
buttonList.add(Button(40, LISTPOS_Y+5, 127, purchase_technology, 1, AGE_RECONSTRUCTION, all_right = True, tab_group=2,tab_id=TAB_TECHS), "buy_tech_6")
buttonList.add(Button(79, LISTPOS_Y,   252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_1")
buttonList.add(Button(79, LISTPOS_Y+1, 252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_2")
buttonList.add(Button(79, LISTPOS_Y+2, 252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_3")
buttonList.add(Button(79, LISTPOS_Y+3, 252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_4")
buttonList.add(Button(79, LISTPOS_Y+4, 252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_5")
buttonList.add(Button(79, LISTPOS_Y+5, 252, dismiss_tech, 1, 0, tab_group=2,tab_id=TAB_TECHS), "buy_tech_x_6")

def select_advice(Game, value):
    if Game.mouse_x >= 79: # make room for the dismiss button which is placed at 79 ...
        return
    index = Game.mouse_y - LISTPOS_Y
    if (index + 1 > 6 or index + 1 > len(Game.advice)):
        return

    full_message = Game.advice[index].full_message
    print(full_message)
def dismiss_advice(Game, value):
    index = Game.mouse_y - LISTPOS_Y
    if (index + 1 > 6 or index + 1 > len(Game.advice)):
        return

    del Game.advice[index]
    print("Deleted index {}".format(index))
    

buttonList.add(Button(40, LISTPOS_Y,   127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_1")
buttonList.add(Button(40, LISTPOS_Y+1, 127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_2")
buttonList.add(Button(40, LISTPOS_Y+2, 127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_3")
buttonList.add(Button(40, LISTPOS_Y+3, 127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_4")
buttonList.add(Button(40, LISTPOS_Y+4, 127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_5")
buttonList.add(Button(40, LISTPOS_Y+5, 127, select_advice, 1, 0, all_right = True, tab_group=2,tab_id=TAB_ADVISORY), "advice_6")
buttonList.add(Button(79, LISTPOS_Y,   252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_1")
buttonList.add(Button(79, LISTPOS_Y+1, 252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_2")
buttonList.add(Button(79, LISTPOS_Y+2, 252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_3")
buttonList.add(Button(79, LISTPOS_Y+3, 252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_4")
buttonList.add(Button(79, LISTPOS_Y+4, 252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_5")
buttonList.add(Button(79, LISTPOS_Y+5, 252, dismiss_advice, 1, 0, tab_group=2,tab_id=TAB_ADVISORY), "advice_x_6")

def stringf(string, width=40):
    s = string
    if len(s) > width:
        s = string[:(width-3)]
        s += "..."
    return s
def number(val, dec=0, forcedec=False, signspace=True, showpos=False, leadingspace=True):
    aval = abs(val)
    if aval >= 1000000000000000000000000000:
        n = val / 1000000000000000000000000000
        m = ' oct.'
    elif aval >= 1000000000000000000000000:
        n = val / 1000000000000000000000000
        m = ' sept.'
    elif aval >= 1000000000000000000000:
        n = val / 1000000000000000000000
        m = ' sext.'
    elif aval >= 1000000000000000000:
        n = val / 1000000000000000000
        m = ' quint.'
    elif aval >= 1000000000000000:
        n = val / 1000000000000000
        m = ' quad.'
    elif aval >= 1000000000000:
        n = val / 1000000000000
        m = ' tril.'
    elif aval >= 1000000000:
        n = val / 1000000000
        m = ' bil.'
    elif aval >= 1000000:
        n = val / 1000000
        m = ' mil.'
    else:
        if not forcedec:
            dec = 0
        n = val
        m = ''
    fn = math.floor(n) if n > 0 else math.ceil(n)
    if leadingspace:
        fill = "+" if showpos else " "
    else:
        fill = ""
    if dec:
        dd = pow(10, dec)
        r = abs(math.floor(dd * (n - fn)))
        if r==dd:
            n += sign(n)
            r = 0
        if signspace:
            return "{}{:,}.{}{}".format(fill if n >= 0 else "-", abs(fn), str(r).zfill(dec), m) #"{:,.2f}".format(n) #
        else:
            return "{:,}.{}{}".format(fn, str(r).zfill(dec), m)
    else:
        if signspace:
            return "{}{:,}{}".format(fill if n >= 0 else "-", abs(fn), m)
        else:
            return "{:,}{}".format(fn, m)


def _draw_header(Game, context, root_console, age_x):
    sidebar_x = SIDEBARX
    j = INFOY
    i=0

    age_i = 1
    root_console.print(x=age_x + 9,y=0, string="Age")
    root_console.print(x=age_x + 12,y=0, string=str(Game.age + 1).zfill(2))
    root_console.print(x=age_x,y=age_i, string="{}".format(AGES[Game.age]['Name']), fg=COL_UI_HIGHLIGHT)
    if (Game.mouse_y == age_i and Game.mouse_x >= age_x - 2 and Game.mouse_x <= age_x + 24):
        root_console.print(x=age_x,y=age_i, string=" ${}            ".format(number(AGES[Game.age]['Upgrade']['$'], dec=2)))
        root_console.print(x=sidebar_x,y=j+0, string="Current epoch no. {} of {}".format(Game.age + 1, Game.age_max + 1))
        root_console.print(x=sidebar_x,y=j+1, string="       <{}>".format(AGES[Game.age]['Name']))
        root_console.print(x=sidebar_x,y=j+3, string=" upgrade cost: ${}".format(number(AGES[Game.age]['Upgrade']['$'], dec=2)))
        root_console.print(x=sidebar_x,y=j+5, string=" Age up to")
        root_console.print(x=sidebar_x,y=j+6, string=" - increase population maximum")
        root_console.print(x=sidebar_x,y=j+7, string=" - unlock new technologies, agencies,")
        root_console.print(x=sidebar_x,y=j+8, string="    and features")

    # fast forward speed indicator
    root_console.print(x=5,y=0, string="{}".format(Game.TIME_INTERVALS_TEXT[Game.speed]))
    # date
    date_x = 13
    #root_console.print(x=5,y=1+i, string="Date")
    # if Game.date_format==Game.MMDDYYYY:
    root_console.print(x=date_x,y=0, string="{}".format(MONTHS[Game.month - 1]))
    root_console.print(x=date_x + 4,y=0, string="{}{}".format(" " if Game.day < 10 else "", Game.day))
    root_console.print(x=date_x + 6,y=0, string=",{}".format(Game.year))
    if (Game.paused or Game.speed < 4):
        ampm = "pm"
        tt = Game.time_since_last_turn / Game.time_interval_value
        hr = math.floor(tt * 24)
        if hr >= 12:
            hr -= 12
        if (math.floor(tt * 24) <=11):
            ampm = "am"
        m = math.floor(tt * 1440) % 60
        s = math.floor(tt * 86400) % 60
        root_console.print(x=date_x,y=1, string="{}".format(str(hr if hr > 0 else 12).zfill(2)))
        root_console.print(x=date_x+2,y=1, string=":{}".format(str(m).zfill(2)))
        root_console.print(x=date_x+5,y=1, string=":{} {}".format(str(s).zfill(2), ampm))
    else:
        root_console.print(x=date_x,y=1, string="--:--:-- --")

def _draw_advisory_tab(Game, context, root_console):
    ii = 0
    length = len(Game.advice)
    for ii in range(6):
        if ii >= length:
            break
        a = Game.advice[ii]
        col = WHITE if (Game.mouse_x >= 42 and Game.mouse_y == 19 + ii) else LTGRAY
        root_console.print(x = 42,y = 19 + ii, string = a.string, fg=col)
        if (Game.mouse_x >= 40 and Game.mouse_y == LISTPOS_Y + ii):
            index = Game.mouse_y - LISTPOS_Y
            k = 0
            for line in a.full_message:
                root_console.print(x = 40,y = 8 + k, string = line)
                k += 1

def _draw_technologies_tab(Game, context, root_console):
    k = -1
    for item in Game.list_available_techs:
        if k < 5:
            col = WHITE if (Game.mouse_x >= 42 and Game.mouse_y == 20 + k) else LTGRAY
            root_console.print(x = 42,y = 20 + k, string = Game.techs[item]['name'], fg=col)
        k += 1
        if (Game.mouse_x >= 40 and Game.mouse_y == LISTPOS_Y + k and k < 6):
            index = Game.mouse_y - LISTPOS_Y
            tech_data = Game.techs[Game.list_available_techs[index]]
            root_console.print(x = 40,y = 8, string = tech_data['name'])
            root_console.print(x = 42,y = 9, string =  "Cost:       ${}".format(number(tech_data['cost'], dec=1, leadingspace=False)))
            root_console.print(x = 42,y = 10, string = "Information: {}".format(number(tech_data['research'], dec=1, leadingspace=False)))

            ki = 0
            
            exclusive = tech_data.get('exclusive', [])
            if exclusive:
                ki += 1
                root_console.print(x = 42,y = 10+ki, string = "Exclusive bill precludes:")
                for item in exclusive:
                    ki += 1
                    root_console.print(x = 42,y = 10+ki, string = "    {}".format(stringf(Game.techs[item]['name'], width=34)))
            
            pop = tech_data.get('pop', 0)
            if pop:
                ki += 1
                root_console.print(x = 42,y = 11+ki, string = "+{} max. population".format(number(pop, dec=1,leadingspace=False)))

            for ss in tech_data['description']:
                root_console.print(x = 42,y = 12 + ki, string = ss)
                ki += 1
        if k == 6: break

def _draw_market(Game, context, root_console):
    j = INFOY
    sidebar_x = SIDEBARX
    i=0
    xx = 41
    
    if Game.age >= 2:
        i=3
        if Game.selling_resources_points > Game.buying_resources_points:
            v = Game.selling_resources_points
            if (Game.mouse_x >= xx and Game.mouse_y >= 1+i and Game.mouse_y <= 2+i):
                root_console.print(x=sidebar_x,y=j+0, string="Oil export")
                root_console.print(x=sidebar_x,y=j+1, string=" price        ${} / barrel".format(number(Game.get_sell_value_oil(), dec=2, forcedec=True, leadingspace=False)))
                root_console.print(x=sidebar_x,y=j+2, string=" market value {}%".format(number(Game.market_value_oil)))
                root_console.print(x=sidebar_x,y=j+4, string=" currently earning")
                root_console.print(x=sidebar_x,y=j+5, string="    +${} / mo.".format(number(v*Game.get_sell_value_oil(), dec=1, forcedec=True)))
                root_console.print(x=sidebar_x,y=j+6, string=" currently exporting")
                root_console.print(x=sidebar_x,y=j+7, string="    -{} barrels / mo.".format(number(v, dec=1)))
            root_console.print(x=xx+10,y=1+i, string=" -{} Oil export".format(number(v, dec=1, leadingspace=False)))
            root_console.print(x=xx+10,y=2+i, string="+${} / mo.".format(number(v*Game.get_sell_value_oil(), dec=1, leadingspace=False)))
        else:
            v = Game.buying_resources_points
            if (Game.mouse_x >= xx and Game.mouse_y >= 1+i and Game.mouse_y <= 2+i):
                root_console.print(x=sidebar_x,y=j+0, string="Oil import")
                root_console.print(x=sidebar_x,y=j+1, string=" price        ${} / barrel".format(number(-Game.get_purchase_value_oil(), dec=2, forcedec=True, leadingspace=False)))
                root_console.print(x=sidebar_x,y=j+2, string=" market value {}%".format(number(Game.market_value_oil)))
                root_console.print(x=sidebar_x,y=j+4, string=" currently spending")
                root_console.print(x=sidebar_x,y=j+5, string="    -${} / mo.".format(number(-v*Game.get_purchase_value_oil(), dec=1, forcedec=True)))
                root_console.print(x=sidebar_x,y=j+6, string=" currently importing")
                root_console.print(x=sidebar_x,y=j+7, string="    +{} barrels / mo.".format(number(v, dec=1)))
            root_console.print(x=xx+10,y=1+i, string=" +{} Oil import".format(number(v, dec=1, leadingspace=False)))
            root_console.print(x=xx+10,y=2+i, string="-${} / mo.".format(number(-v*Game.get_purchase_value_oil(), dec=1, leadingspace=False)))
        libtcodpy.console_put_char_ex(root_console, xx+8, 1+i, ICON_OIL, COL_OIL, COL_UI_BG)
    
    i=3
    if Game.selling_food_points > Game.buying_food_points:
        v = Game.selling_food_points
        if (Game.mouse_x < xx-1 and Game.mouse_y >= 1+i and Game.mouse_y <= 2+i):
            root_console.print(x=sidebar_x,y=j+0, string="Food export")
            root_console.print(x=sidebar_x,y=j+1, string=" price        ${} / crate".format(number(Game.get_sell_value_food(), dec=2, forcedec=True, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+2, string=" market value {}%".format(number(Game.market_value_food)))
            root_console.print(x=sidebar_x,y=j+4, string=" currently earning")
            root_console.print(x=sidebar_x,y=j+5, string="    +${} / mo.".format(number(v*Game.get_sell_value_food(), dec=1, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+6, string=" currently exporting")
            root_console.print(x=sidebar_x,y=j+7, string="    -{} crates / mo.".format(number(v, dec=1)))
        root_console.print(x=12,y=1+i, string=" -{} Food export".format(number(v, dec=1, leadingspace=False)))
        root_console.print(x=12,y=2+i, string="+${} / mo.".format(number(v*Game.get_sell_value_food(), dec=1, leadingspace=False)))
    else:
        v = Game.buying_food_points
        if (Game.mouse_x < xx-1 and Game.mouse_y >= 1+i and Game.mouse_y <= 2+i):
            root_console.print(x=sidebar_x,y=j+0, string="Food import")
            root_console.print(x=sidebar_x,y=j+1, string=" price        ${} / crate".format(number(-Game.get_purchase_value_food(), dec=2, forcedec=True, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+2, string=" market value {}%".format(number(Game.market_value_food)))
            root_console.print(x=sidebar_x,y=j+4, string=" currently spending")
            root_console.print(x=sidebar_x,y=j+5, string="    -${} / mo.".format(number(-v*Game.get_purchase_value_food(), dec=1, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+6, string=" currently importing")
            root_console.print(x=sidebar_x,y=j+7, string="    +{} crates / mo.".format(number(v, dec=1)))
        root_console.print(x=12,y=1+i, string=" +{} Food import".format(number(v, dec=1, leadingspace=False)))
        root_console.print(x=12,y=2+i, string="-${} / mo.".format(number(-v*Game.get_purchase_value_food(), dec=1, leadingspace=False)))
    libtcodpy.console_put_char_ex(root_console, 10, 1+i, ICON_FOOD, COL_FOOD, COL_UI_BG)


def _draw_lock(Game, root_console, x, y, caption="", age=1):
    if Game.age < age:
        root_console.print(x=x,y=y, string="{}".format(caption), fg=COL_UI_DARK)
        libtcodpy.console_put_char_ex(root_console, x, y+1, ICON_LOCKED, COL_UI_DARK, COL_UI_BG)
        root_console.print(x=x+2,y=y+1, string="Age {} / {}".format(1 + Game.age, 1 + age), fg=COL_UI_DARK)
def __draw_fma(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_TRUST:
        s ="FMA"
        acol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            s ="Food & Medical Agency"
            acol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_FMA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_food), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+3, string="  - Food distribution affects", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     maximum fertility & food waste", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="  - Food subsidies and distribution")
            root_console.print(x=sidebar_x,y=j+6, string="     affect trust, happiness & health")
            root_console.print(x=sidebar_x,y=j+7, string="  - Child mandate requires bill signed:", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+8, string="     'Contraceptives' in Epoch no. 8", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+9, string="     Affects fertility rate & happiness", fg=OFFWHITE)
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_FMA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_food), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+2, string=" Fertility cap ={} %".format(number(10 * Game.max_fertility, leadingspace=False)), fg=(RED if Game.max_fertility <= 5 else WHITE))
            root_console.print(x=sidebar_x,y=j+3, string=" Health        {} %".format(number(Game.physical_from_food_drugs, showpos=True, dec=2, forcedec=True)), fg=(RED if Game.physical_from_food_drugs <= 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+4, string=" Happiness     {} %".format(number(Game.happiness_from_food, showpos=True, dec=2, forcedec=True)), fg=(RED if Game.happiness_from_food <= 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+5, string=" Trust         {}".format(number(Game.trust_from_food, showpos=True)), fg=(RED if Game.trust_from_food <= 0 else GREEN))
            col = RED if Game.food_distribution <= 2 else (GREEN if Game.food_distribution == 5 else WHITE)
            root_console.print(x=sidebar_x,y=j+6, string=" Population is {} @ {} crates".format(Game.FOOD_DISTRIBUTION2[Game.food_distribution], Game.food_distribution), fg=col)
            root_console.print(x=sidebar_x,y=j+7, string="    distributed per mo. per capita", fg=col)
            col = RED if Game.food_distribution_efficiency <= 3 else (GREEN if Game.food_distribution_efficiency >= 8 else WHITE)
            root_console.print(x=sidebar_x,y=j+8, string=" Food & drug quality is {}".format(Game.FOOD_QUALITY[Game.food_distribution_efficiency]), fg=col)
            col = (RED if Game.food_distribution >= 4 else WHITE)
            root_console.print(x=sidebar_x,y=j+9, string=" {}% food wasted / mo.".format(Game.food_waste), fg=col)
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_FMA)
        root_console.print(x=xx1 + 2,y=1+i, string="{}   Distribution   {} crates / mo.".format(1 + Game.food_distribution, Game.food_distribution), fg=acol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}".format(1 + Game.food_distribution_efficiency), fg=acol)
        root_console.print(x=xx1 + 6,y=2+i, string="Subsidies      {}".format(10 + 10*Game.food_distribution_efficiency), fg=acol)
        root_console.print(x=xx1 + 25,y=2+i, string="%", fg=acol)
        bccol = acol if Game.contraceptives_researched else COL_UI_DARK
        root_console.print(x=xx1 + 2,y=3+i, string="{}".format(1 + Game.birth_control), fg=bccol)
        root_console.print(x=xx1 + 6,y=3+i, string="Child mandate  {}".format(Game.BIRTH_CONTROL[Game.birth_control]), fg=bccol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    FMA", age=AGE_TRUST)
    return 5
def __draw_zua(Game, context, root_console, i, xx1, sidebar_x, j):
    s ="ZUA"
    acol = LTGRAY
    if (Game.mouse_y >= 0+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
        s ="Zoning & Utility Agency"
        acol = WHITE
    if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
        root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_ZUA)
        root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_zoning), dec=1, leadingspace=False)), fg=RED)
        root_console.print(x=sidebar_x,y=j+3, string="  - Funding for the ZUA affects trust,", fg=OFFWHITE)
        root_console.print(x=sidebar_x,y=j+4, string="     rate of growth of infrastructure", fg=OFFWHITE)
        root_console.print(x=sidebar_x,y=j+5, string="  - Low funds causes increased decay")
        root_console.print(x=sidebar_x,y=j+6, string="  - Housing subsidies affect business", fg=OFFWHITE)
        root_console.print(x=sidebar_x,y=j+7, string="     growth, trust, income inequality,", fg=OFFWHITE)
        root_console.print(x=sidebar_x,y=j+8, string="     happiness, property tax income, &", fg=OFFWHITE)
        root_console.print(x=sidebar_x,y=j+9, string="     homelessness rates", fg=OFFWHITE)
    if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
        root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_ZUA)
        root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_zoning), dec=1, leadingspace=False)), fg=RED)
        root_console.print(x=sidebar_x,y=j+2, string="    (does not count property tax:)", fg=COL_UI_DARK)
        root_console.print(x=sidebar_x,y=j+3, string=" Properties earning: +${} / mo.".format(number(abs(Game.property_tax_income), dec=1, leadingspace=False)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+4, string=" Housing prices are {}".format(Game.HOUSING_COSTS[7 - Game.housing_subsidies]))
        root_console.print(x=sidebar_x,y=j+5, string="{} % Growth rate ({})".format(number(100 * Game.GROWTH_INFRASTRUCTURE_RATES[Game.growth_infrastructure_rate]), Game.GROWTH_INFRASTRUCTURE[Game.growth_infrastructure_rate]), fg=(RED if Game.growth_infrastructure_rate == 5 else WHITE))
        root_console.print(x=sidebar_x,y=j+6, string="{} Infrastructure built / mo.".format(number(Game.infrastructure_growth, dec=2)))
        root_console.print(x=sidebar_x,y=j+7, string="{} % Infrastructure decays per mo.".format(number(Game.get_infrastructure_decay_rate(), dec=2, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+9, string=" Trust: {}".format(number(Game.trust_from_zoning_agency, showpos=True)), fg=(GREEN if Game.trust_from_zoning_agency > 0 else WHITE))
        
    root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_ZUA)
    root_console.print(x=xx1 + 2,y=1+i, string="{}   Zoning         {}".format(1 + Game.growth_infrastructure_rate, Game.GROWTH_INFRASTRUCTURE[Game.growth_infrastructure_rate]), fg=acol)
    root_console.print(x=xx1 + 2,y=2+i, string="{}   Housing costs  {}".format(1 + Game.housing_subsidies, Game.HOUSING_COSTS[7 - Game.housing_subsidies]), fg=acol)
    return 4
def __draw_lla(Game, context, root_console, i, xx1, sidebar_x, j):
    ysize = 3
    if Game.age >= AGE_2NDINDUSTRIAL:
        s ="LLA"
        acol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= ysize+i and Game.mouse_x < sidebar_x-1):
            s ="Labor Law Agency"
            acol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_LLA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_labor), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+3, string="  - Employee wages affect happiness,", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     income inequality, business growth", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="     & upkeep costs for public sector", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+6, string="  - Safety law strictness affects")
            root_console.print(x=sidebar_x,y=j+7, string="     trust & employee health")
            root_console.print(x=sidebar_x,y=j+8, string="  - Working hours value affects", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+9, string="     happiness, trust & productivity", fg=OFFWHITE)
        if (Game.mouse_y >= 1+i and Game.mouse_y <= ysize+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_LLA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_labor), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+3, string=" Employee wages:  {} % vs. inflation".format(number(100 * Game.WAGES[Game.wages], leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" Safety law is    {}".format(Game.FOOD_QUALITY[Game.safety_law]))
            root_console.print(x=sidebar_x,y=j+5, string=" Fulltime work is {} hours / wk".format(Game.FULLTIME_HOURS[Game.fulltime_hours]))
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_LLA)
        root_console.print(x=xx1 + 2,y=1+i, string="{}".format(1 + Game.wages), fg=acol)
        root_console.print(x=xx1 + 6,y=1+i, string="Wages          {} %".format(number(100 * Game.WAGES[Game.wages], leadingspace=False)), fg=acol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}".format(1 + Game.safety_law), fg=acol)
        root_console.print(x=xx1 + 6,y=2+i, string="Safety law     {}".format(Game.FOOD_QUALITY[Game.safety_law]), fg=acol)
        root_console.print(x=xx1 + 2,y=3+i, string="{}".format(1 + Game.fulltime_hours), fg=acol)
        root_console.print(x=xx1 + 6,y=3+i, string="Fulltime hours {} / wk".format(Game.FULLTIME_HOURS[Game.fulltime_hours]), fg=acol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    LLA", age=AGE_2NDINDUSTRIAL)
    return ysize+2
def __draw_ea(Game, context, root_console, i, xx1, sidebar_x, j):
    ysize = 3 if Game.age >= AGE_RECONSTRUCTION else 1
    if Game.age >= AGE_TRUST:
        s ="EA"
        acol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= ysize+i and Game.mouse_x < sidebar_x-1):
            s ="Education Agency"
            acol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_EA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_education), dec=1, leadingspace=False)), fg=(RED if Game.spending_agency_education < 0 else WHITE))
            root_console.print(x=sidebar_x,y=j+3, string="  - Upgrade allocation speed to", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     improve lower education and", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="     combat unemployment", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+6, string="  - Higher ed. subsidies affect rate")
            root_console.print(x=sidebar_x,y=j+7, string="     information is procured from")
            root_console.print(x=sidebar_x,y=j+8, string="     Innovation sector")
        if (Game.mouse_y >= 1+i and Game.mouse_y <= ysize+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_EA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_education), dec=1, leadingspace=False)), fg=(RED if Game.spending_agency_education < 0 else WHITE))
            root_console.print(x=sidebar_x,y=j+3, string=" Currently training / mo.:   {}".format(number(Game.allocation_speed_actual, dec=1)), fg=(RED if Game.allocation_speed_actual < Game.population_growth else WHITE))
            root_console.print(x=sidebar_x,y=j+4, string=" New workforce / mo.:        {}".format(number(Game.population_growth, dec=1)), fg=(RED if Game.allocation_speed_actual < Game.population_growth else WHITE))
            root_console.print(x=sidebar_x,y=j+5, string=" Max employees trained / mo.:{}".format(number(Game.allocation_speed_maximum, dec=1)), fg=(RED if Game.allocation_speed_maximum < Game.population_growth else WHITE))
            root_console.print(x=sidebar_x,y=j+7, string=" Innovation capacity:         {} %".format(100 + Game.FUNDING_EDUCATION_RESEARCH[Game.funding_education]), fg=(GREEN if Game.funding_education >= 5 else WHITE))
            root_console.print(x=sidebar_x,y=j+8, string=" Info gained / researcher:   {}".format(number(Game.get_science_research_per(), dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+9, string=" Trust: {}".format(number(Game.trust_from_education_agency, showpos=True)), fg=(GREEN if Game.trust_from_education_agency > 0 else WHITE))
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_EA)
        root_console.print(x=xx1 + 6,y=1+i, string="+ Allocation rate  ${}".format(number(__cost_to_upgrade_allocation(Game), dec=2, leadingspace=False)), fg=(RED if Game.allocation_speed_actual <= Game.population_growth else acol))
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    EA", age=AGE_TRUST)
    if Game.age >= AGE_RECONSTRUCTION:
        root_console.print(x=xx1 + 6,y=2+i, string="Purchase 1k info   ${}".format(number(__cost_to_purchase_research(Game), dec=2, leadingspace=False)), fg=acol)
        root_console.print(x=xx1 + 2,y=3+i, string="{}   Higher ed.     {}".format(1 + Game.funding_education, 100 + Game.FUNDING_EDUCATION_RESEARCH[Game.funding_education]), fg=acol)
        root_console.print(x=xx1 + 25,y=3+i, string="%", fg=acol)
    return 5
def __draw_ca(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_RECONSTRUCTION:
        s ="CA"
        acol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            s ="Commerce Agency"
            acol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_CA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net {}${} / mo.".format(ssign(Game.spending_agency_commerce), number(abs(Game.spending_agency_commerce), dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string="  - Automation makes imports and", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string="     exports of food and oil", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     automatically adjust to net/mo.", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="  - Generate revenue from trade by")
            root_console.print(x=sidebar_x,y=j+6, string="     adding fees & tariffs")
            root_console.print(x=sidebar_x,y=j+7, string="  - Revenue relies on having high", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+8, string="     wealth, trust, & influence", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+9, string="  - Affects trust")
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_CA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net {}${} / mo.".format(ssign(Game.spending_agency_commerce), number(abs(Game.spending_agency_commerce), dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Automate: Food? {}".format("Yes" if Game.market_food_set else "No"))
            root_console.print(x=sidebar_x+22,y=j+3, string=" Oil? {}".format("Yes" if Game.market_resources_set else "No"))
            col = RED if (Game.agency_commerce_fees == 0 or Game.agency_commerce_fees >= 4) else WHITE
            root_console.print(x=sidebar_x,y=j+4, string="  {}/5".format(1 + Game.agency_commerce_fees), fg=col)
            root_console.print(x=sidebar_x + 12,y=j+4, string="Fees are {}".format(Game.AGENCY_COMMERCE_FEES[Game.agency_commerce_fees]), fg=col)
            root_console.print(x=sidebar_x,y=j+6, string=" Trust: {}".format(number(Game.trust_from_tariffs, showpos=True)), fg=(RED if Game.trust_from_tariffs <= -4 else (GREEN if Game.trust_from_tariffs > 0 else WHITE)))
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_CA)
        root_console.print(x=xx1 + 21,y=1+i, string="Auto commerce".format(), fg=acol)
        root_console.print(x=xx1 + 2,y=1+i, string="Food  Oil", fg=acol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}   Fees & tariffs {}".format(1 + Game.agency_commerce_fees, Game.AGENCY_COMMERCE_FEES[Game.agency_commerce_fees]), fg=acol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    CA", age=AGE_RECONSTRUCTION)
    return 4
def __draw_gea(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_AUTOMATION:
        s ="GEA"
        eacol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 1+i and Game.mouse_x < sidebar_x-1):
            s ="Green Earth Agency"
            eacol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_GEA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net {}${} / mo.".format("+" if Game.spending_agency_environmental > 0 else "-", number(abs(Game.spending_agency_environmental), dec=1, leadingspace=False)), fg=(GREEN if Game.spending_agency_environmental > 0 else RED))
            root_console.print(x=sidebar_x,y=j+3, string="  - Affects Environmental sector", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     pollution reduction, & trust", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="  - Landfill results in higher levels")
            root_console.print(x=sidebar_x,y=j+6, string="     of pollution, but is cheaper")
            root_console.print(x=sidebar_x,y=j+7, string="  - Exporting garbage offshore costs", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+8, string="     less $ with higher trust values", fg=OFFWHITE)
        if (Game.mouse_y == 1+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_GEA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net {}${} / mo.".format("+" if Game.spending_agency_environmental > 0 else "-", number(abs(Game.spending_agency_environmental), dec=1, leadingspace=False)), fg=(GREEN if Game.spending_agency_environmental > 0 else RED))
            col = RED if (Game.environmental_policy == 0) else WHITE
            root_console.print(x=sidebar_x,y=j+3, string=" Garbage policy: {}/6   {}".format(1+Game.environmental_policy, Game.ENVIRONMENTAL_POLICY[Game.environmental_policy]), fg=col)
            root_console.print(x=sidebar_x,y=j+4, string=" Pollution reduction:  {} %".format(number(100 * Game.gea_agency_modifier, leadingspace=False)), fg=WHITE)
            root_console.print(x=sidebar_x,y=j+5, string=" Trust:                {}".format(number(Game.trust_from_environmental_policy, showpos=True)), fg=(GREEN if Game.trust_from_environmental_policy >= 0 else RED))
            if (Game.export_pollution or Game.import_pollution):
                root_console.print(x=sidebar_x,y=j+7, string=" Currently {} garbage".format("exporting" if Game.export_pollution else "importing"), fg=WHITE)
                root_console.print(x=sidebar_x,y=j+8, string="    {} [gpm`".format(number(get_ugpm3(Game.pollution_income_trade, Game.land), dec=3, forcedec=True, leadingspace=False)), fg=WHITE)
                root_console.print(x=sidebar_x,y=j+9, string="   {}${}".format("+" if Game.power_income_pollution_trade >= 0 else "-", number(abs(Game.power_income_pollution_trade), dec=2, leadingspace=False)), fg=WHITE)
                root_console.print(x=sidebar_x+18,y=j+8, string="/ mo.", fg=WHITE)
                root_console.print(x=sidebar_x+18,y=j+9, string="/ mo.", fg=WHITE)
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_GEA)
        #root_console.print(x=xx1 + 2,y=1+i, string="{}".format(1 + Game.environmental_policy), fg=eacol)
        root_console.print(x=xx1 + 2,y=1+i, string="Im", fg=eacol)
        root_console.print(x=xx1 + 6,y=1+i, string="Ex", fg=eacol)
        root_console.print(x=xx1 + 10,y=1+i, string="Landfill ______ Recycle", fg=eacol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    GEA", age=AGE_AUTOMATION)
    return 3
def _get_welfare_text(Game, dic, val):
    final = ""
    for k,v in dic.items():
        if val >= k:
            final = v
    return final
def __draw_ssa(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_AUTOMATION:
        s ="SSA"
        eacol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            s ="Social Services Agency"
            eacol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_SSA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_social_services), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+2, string="  - Health insurance is based on income", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string="     inequality, & affects Healthcare", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     sector & death upkeep costs", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="  - Pensions for veterans & retirees")
            root_console.print(x=sidebar_x,y=j+6, string="     affect happiness & longevity")
            root_console.print(x=sidebar_x,y=j+7, string="  - Income assistance affects sanity,", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+8, string="     allocation speed, & income", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+9, string="     inequality", fg=OFFWHITE)
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_SSA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_social_services), dec=1, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+2, string=" Health Insurance using  {}".format(number(Game.health_insurance_policy)), fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string=" Pensions using          {}".format(number(Game.veteran_pension_policy)), fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string=" Income assistance using {}".format(number(Game.income_assistance_policy)), fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string=" % who can afford care   {}".format(number(100 - Game.percent_cant_afford_health_care)), fg=(GREEN if Game.percent_cant_afford_health_care <= 0 else WHITE))
            root_console.print(x=sidebar_x,y=j+6, string=" Income Inequality       {}".format(number(100 * Game.income_inequality_from_ssa_policy, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+7, string=" Allocation speed        {}".format(number(100 * Game.allocation_rate_from_income_assistance, dec=2, forcedec=True)), fg=(RED if Game.allocation_rate_from_income_assistance < 1 else WHITE))
            root_console.print(x=sidebar_x,y=j+8, string=" Happiness               {}".format(number(Game.happiness_from_pensions, dec=2, forcedec=True, showpos=True)), fg=(RED if Game.happiness_from_pensions < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+9, string=" Sanity                  {}".format(number(Game.mental_from_income_insurance, dec=2, forcedec=True, showpos=True)), fg=(RED if Game.mental_from_income_insurance < 0 else GREEN))
            for k in range(3):
                root_console.print(x=sidebar_x+33,y=j+2+k, string="% GDP", fg=OFFWHITE)
                root_console.print(x=sidebar_x+33,y=j+5+k, string="%")
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_SSA)
        root_console.print(x=xx1 + 2,y=1+i, string="{}%".format(str(Game.health_insurance_policy).rjust(2)), fg=eacol)
        root_console.print(x=xx1 + 8,y=1+i, string="Health insurance  {}".format(_get_welfare_text(Game, Game.HEALTH_INSURANCE_DICT, 100 - Game.percent_cant_afford_health_care)), fg=eacol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}%".format(str(Game.veteran_pension_policy).rjust(2)), fg=eacol)
        root_console.print(x=xx1 + 8,y=2+i, string="Veteran & retiree {}".format(_get_welfare_text(Game, Game.PENSIONS_DICT, Game.veteran_pension_policy)), fg=eacol)
        root_console.print(x=xx1 + 2,y=3+i, string="{}%".format(str(Game.income_assistance_policy).rjust(2)), fg=eacol)
        root_console.print(x=xx1 + 8,y=3+i, string="Income assistance {}".format(_get_welfare_text(Game, Game.INCOME_ASSISTANCE_DICT, Game.income_assistance_policy)), fg=eacol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    SSA", age=AGE_AUTOMATION)
    return 5
def __draw_ra(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_2NDINDUSTRIAL:
        s ="RA"
        racol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            s ="Revenue Agency"
            racol = WHITE
        if (Game.mouse_y == 0+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_RA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net ${} / mo.".format(number(Game.spending_agency_revenue, dec=1)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string="  - Use taxes to generate revenue", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string="  - Civilian taxes impact happiness")
            root_console.print(x=sidebar_x,y=j+4, string="  - Investor / Business taxes impact", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="     business growth and trust", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+6, string="  - Sales tax impacts happiness and")
            root_console.print(x=sidebar_x,y=j+7, string="     trust")
            root_console.print(x=sidebar_x,y=j+8, string="  - Property tax impacts immigration", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+9, string="     and is dependent on other taxes", fg=OFFWHITE)
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 3+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=sidebar_x,y=j+0, string=s, fg=COL_RA)
            root_console.print(x=sidebar_x,y=j+1, string=" Net ${} / mo.".format(number(Game.spending_agency_revenue, dec=1)), fg=GREEN)
            # civilian
            col = RED if (Game.civilian_taxing <= 5 or Game.civilian_taxing >= 12) else WHITE
            root_console.print(x=sidebar_x,y=j+2, string=" Civilian tax {}%".format(Game.civilian_taxing), fg=col)
            root_console.print(x=sidebar_x+28,y=j+2, string="${}".format(number(Game.public_tax_income, dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x+20,y=j+3, string="{}".format(Game.TAXES[Game.civilian_taxing-4]), fg=col)
            # property
            col = RED if (Game.civilian_taxing+Game.investor_taxing*2 <= 15 or Game.civilian_taxing+Game.investor_taxing*2 >= 36) else WHITE
            root_console.print(x=sidebar_x,y=j+4, string=" Property tax {0:.2f}%".format(0.04*(Game.civilian_taxing + Game.investor_taxing*2)), fg=col)
            root_console.print(x=sidebar_x+28,y=j+4, string="${}".format(number(Game.property_tax_income, dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x+20,y=j+5, string="{}".format(Game.TAXES[round(0.33 * ((Game.civilian_taxing-4)*2 + (Game.investor_taxing-4)))]), fg=col)
            # investor
            col = RED if (Game.investor_taxing <= 5 or Game.investor_taxing >= 12) else WHITE
            root_console.print(x=sidebar_x,y=j+6, string=" Business tax {}%".format(2*Game.investor_taxing), fg=col)
            root_console.print(x=sidebar_x+28,y=j+6, string="${}".format(number(Game.private_tax_income, dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x+20,y=j+7, string="{}".format(Game.TAXES[Game.investor_taxing-4]), fg=col)
            # sales
            col = RED if (Game.sales_taxing <= 5 or Game.sales_taxing >= 12) else WHITE
            root_console.print(x=sidebar_x,y=j+8, string=" Sales tax    {}%".format(0.5 + 0.5*Game.sales_taxing), fg=col)
            root_console.print(x=sidebar_x+28,y=j+8, string="${}".format(number(Game.sales_tax_income, dec=1, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x+20,y=j+9, string="{}".format(Game.TAXES[Game.sales_taxing-4]), fg=col)
            
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=COL_RA)
        root_console.print(x=xx1 + 2,y=1+i, string="{}".format(Game.civilian_taxing - 3), fg=racol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}".format(Game.investor_taxing - 3), fg=racol)
        root_console.print(x=xx1 + 2,y=3+i, string="{}".format(Game.sales_taxing - 3), fg=racol)
        root_console.print(x=xx1 + 6,y=1+i, string="Civilian taxes {}%".format(Game.civilian_taxing), fg=racol)
        root_console.print(x=xx1 + 6,y=2+i, string="Business taxes {}%".format(2*Game.investor_taxing), fg=racol)
        root_console.print(x=xx1 + 6,y=3+i, string="Sales taxes    {}%".format(0.5 + 0.5*Game.sales_taxing), fg=racol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    RA", age=AGE_2NDINDUSTRIAL)
    return 5
def __draw_ja(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_SECURITY:
        s ="JA"
        jacol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            s ="Justice Agency"
            jacol = WHITE
            root_console.print(x=sidebar_x,y=j+0, string=s)
            root_console.print(x=sidebar_x,y=j+1, string=" Net -${} / mo.".format(number(abs(Game.spending_agency_justice), dec=1)), fg=RED)
            root_console.print(x=sidebar_x,y=j+2, string="  - Punishment reduces crime, creates", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string="     prisoners; affects riot response", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="     High values raise death rates", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+5, string="  - Corrections spends $ to attempt")
            root_console.print(x=sidebar_x,y=j+6, string="     to reintegrate prisoners & felons")
            col = RED if (Game.punishment <= 0 or Game.punishment >= 4) else WHITE
            root_console.print(x=sidebar_x,y=j+8, string=" Punishment:        {}/6 {}".format(1 + Game.punishment, Game.PUNISHMENT[Game.punishment]), fg=col)
            col = RED if (Game.corrections <= 0 or Game.corrections >= 4) else WHITE
            root_console.print(x=sidebar_x,y=j+9, string=" Felon corrections: {}/6 {}".format(1 + Game.corrections, Game.CORRECTIONS[Game.corrections]), fg=col)
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=jacol)
        root_console.print(x=xx1 + 2,y=1+i, string="{}   Punishment     {}".format(1 + Game.punishment, Game.PUNISHMENT[Game.punishment]), fg=jacol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}   Corrections    {}".format(1 + Game.corrections, Game.CORRECTIONS[Game.corrections]), fg=jacol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    JA", age=AGE_SECURITY)
    return 3
def __draw_ha(Game, context, root_console, i, xx1, sidebar_x, j):
    if Game.age >= AGE_EXPANSION:
        s ="HA"
        hacol = LTGRAY
        if (Game.mouse_y >= 0+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            s ="Homeland Agency"
            hacol = WHITE
            root_console.print(x=sidebar_x,y=j+0, string="Homeland Agency")
            root_console.print(x=sidebar_x,y=j+1, string=" Net {}${} / mo.".format("+" if Game.spending_agency_homeland > 0 else "-", number(abs(Game.spending_agency_homeland), dec=1)), fg=(RED if Game.spending_agency_homeland < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+2, string="  - Border Control affects legal and ", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+3, string="     illegal immigration rates", fg=OFFWHITE)
            root_console.print(x=sidebar_x,y=j+4, string="  - Travel affects diplomacy levels,")
            root_console.print(x=sidebar_x,y=j+5, string="     tourism revenue, and chances of")
            root_console.print(x=sidebar_x,y=j+6, string="     pandemic breakout")
            col = RED if (Game.border_control == 0 or Game.border_control == 4) else WHITE
            root_console.print(x=sidebar_x,y=j+8, string=" Border control: {}/5   {}".format(1+Game.border_control, Game.AGENCY_BORDER_CONTROL[Game.border_control]), fg=col)
            col = RED if (Game.travel_policy == 0 or Game.travel_policy == 4) else WHITE
            root_console.print(x=sidebar_x,y=j+9, string=" Travel policy:  {}/5   {}".format(1+Game.travel_policy, Game.AGENCY_TRAVEL_POLICIES[Game.travel_policy]), fg=col)
        root_console.print(x=xx1,    y=0+i, string="{}".format(s), fg=hacol)
        root_console.print(x=xx1 + 2,y=1+i, string="{}   Border control {}".format(1 + Game.border_control, Game.AGENCY_BORDER_CONTROL[Game.border_control]), fg=hacol)
        root_console.print(x=xx1 + 2,y=2+i, string="{}   Travel law     {}".format(1 + Game.travel_policy, Game.AGENCY_TRAVEL_POLICIES[Game.travel_policy]), fg=hacol)
    else:
        _draw_lock(Game, root_console,xx1+13, 1+i, caption="    HA", age=AGE_EXPANSION)
    return 3

def _draw_agencies_tab(Game, context, root_console):
    sidebar_x = SIDEBARX
    j=INFOY
    xx1 = 2
    i=8
    
    i+=__draw_zua(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_fma(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_ea(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_ca(Game, context, root_console, i, xx1, sidebar_x, j)
    
def _draw_agencies2_tab(Game, context, root_console):
    sidebar_x = SIDEBARX
    j=INFOY
    xx1 = 2
    i=8
    
    i+=__draw_ra(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_lla(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_gea(Game, context, root_console, i, xx1, sidebar_x, j)
    i+=__draw_ssa(Game, context, root_console, i, xx1, sidebar_x, j)

def _draw_sector(Game, context, root_console, xx1, symbol, i, s, employed, v, col, jobid):
    libtcodpy.console_put_char_ex(root_console, xx1, 1+i, symbol, col, COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, xx1, 2+i, 28, col, COL_UI_BG)
    root_console.print(x=xx1+1,y=2+i, string="{}".format(Game.points_allocated[jobid]))
    libtcodpy.console_put_char_ex(root_console, xx1+5, 2+i, ICON_PER_MILLE, WHITE, COL_UI_BG)
    root_console.print(x=xx1+10,y=2+i, string="{}{}".format(number(v, dec=1), employed))

def _draw_sectors_tab(Game, context, root_console):
    sidebar_x = SIDEBARX
    i=6
    j=INFOY
    xx1 = 6
    lvx = LEVELUPX + 2
    arrowsidex = 18

    if Game.points_remaining > 0:
        root_console.print(x=7,y=2+i, string="{}".format(Game.points_remaining), fg=RED)
        root_console.print(x=12,y=2+i, string="employment pts unallocated!", fg=RED)
    else:
        col = (RED if Game.allocation_speed_actual <= Game.population_growth else WHITE)
        if (Game.mouse_y == 2+i and Game.mouse_x < sidebar_x-1):
            root_console.print(x=2,y=2+i, string="{} new employees / mo. (max.)".format(number(Game.allocation_speed_actual, dec=2)), fg=col)
        else:
            root_console.print(x=2,y=2+i, string="{}".format(number(Game.allocation_speed_actual, dec=2)), fg=col)
    if (Game.mouse_y == 2+i and Game.mouse_x < sidebar_x-1):
        ii = 0
        if Game.age >= AGE_TRUST:
            root_console.print(x=sidebar_x,y=j+0, string="Allocation rate, AKA lower education,")
            root_console.print(x=sidebar_x,y=j+1, string="    raises rate employees are trained")
            root_console.print(x=sidebar_x,y=j+2, string="Upgrade allocation to curb unemployment!")
            ii += 4
        if Game.points_remaining > 0:
            root_console.print(x=sidebar_x,y=j+ii+0, string="Allocation points {}".format("+{} / mo.".format(number(Game.allocation_speed_income, dec=2, forcedec=True)) if Game.allocation_speed_income > 0 else ""), fg=(RED if Game.points_remaining > 0 else WHITE))
            root_console.print(x=sidebar_x,y=j+ii+1, string="    {} / 1000 {}".format(Game.points_remaining, "remaining!" if Game.points_remaining > 0 else ""), fg=(RED if Game.points_remaining > 0 else WHITE))
            ii += 2
        root_console.print(x=sidebar_x,y=j+ii+0, string="Training capacity : new workforce / mo.", fg=(RED if Game.allocation_speed_actual < Game.population_growth else WHITE))
        root_console.print(x=sidebar_x,y=j+ii+1, string="    {} : {}".format(number(Game.allocation_speed_actual, dec=2), number(Game.population_growth, dec=2)), fg=(RED if Game.allocation_speed_actual < Game.population_growth else WHITE))
        if Game.age >= AGE_TRUST:
            root_console.print(x=sidebar_x,y=j+ii+2, string="Cost to upgrade allocation + 100 / mo.")
            root_console.print(x=sidebar_x,y=j+ii+3, string="    ${}".format(number(__cost_to_upgrade_allocation(Game), dec=2, leadingspace=False)))
        
    
    v = Game.employees[INFR]
    i+=2
    s ="Construction"
    employed = ""
    if Game.age >= 1:
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[INFR]))
    if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
        employed = " employees"
        cost = Game.get_cost_per(INFR)
        root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
        root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[INFR]), fg=COL_CONSTRUCTION)
        root_console.print(x=sidebar_x,y=j+1, string=" builds infrastructure", fg=COL_CONSTRUCTION)
        if Game.age >= 1:
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[INFR]), dec=2, leadingspace=False)))
        root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
        root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
        root_console.print(x=sidebar_x,y=j+4, string=" infrastr.  {}".format(number(Game.get_infrastructure_infrastructure_per(), dec=1, forcedec=True, showpos=True)), fg=GREEN)
        root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {}".format(number(Game.get_infrastructure_infrastructure_total(), dec=1, showpos=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+5, string=" oil        {}".format(number(Game.get_infrastructure_resources_per(), showpos=True)), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {} barrels".format(number(Game.get_infrastructure_resources_total(), dec=1, showpos=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+6, string=" health     {}".format(number(Game.get_infrastructure_physical_per(), showpos=True)), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_infrastructure_physical_total(), dec=1, showpos=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" pollution  {}".format(number(Game.get_infrastructure_pollution_per(), showpos=True)), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {}".format(number(Game.get_infrastructure_pollution_total(), dec=1, showpos=True)), fg=RED)
    _draw_sector(Game, context, root_console, xx1, ICON_CONSTRUCTION, i, s, employed, v, COL_CONSTRUCTION, INFR)
    
    v = Game.employees[AGRI]
    i+=2
    s ="Agriculture"
    employed = ""
    if Game.age >= 1:
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[AGRI]))
    if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
        employed = " employees"
        cost = Game.get_cost_per(AGRI)
        root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
        root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[AGRI]), fg=COL_AGRICULTURE)
        root_console.print(x=sidebar_x,y=j+1, string=" produces food", fg=COL_AGRICULTURE)
        if Game.age >= 1:
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[AGRI]), dec=2, leadingspace=False)))
        root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
        root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
        root_console.print(x=sidebar_x,y=j+4, string=" food       {}".format(number(round(Game.get_agriculture_food_per()), showpos=True)), fg=GREEN)
        root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {} crates".format(number(Game.get_agriculture_food_total(), dec=1, showpos=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+5, string=" health     {}".format(number(Game.get_agriculture_physical_per(), showpos=True)), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {}".format(number(Game.get_agriculture_physical_total(), dec=1, showpos=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+6, string=" pollution  {}".format(number(Game.get_agriculture_pollution_per(), showpos=True)), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_agriculture_pollution_total(), dec=1, showpos=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" req.       {}".format(number(Game.get_agriculture_required_infrastructure_per())), fg=RED)
        root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {} infra.".format(number(Game.get_agriculture_required_infrastructure_total(), dec=1)), fg=RED)
    _draw_sector(Game, context, root_console, xx1, ICON_AGRICULTURE, i, s, employed, v, COL_AGRICULTURE, AGRI)
    
    if Game.age >= 2:
        v = Game.employees[HARV]
        i+=2
        s ="Industry"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[HARV]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(HARV)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[HARV]), fg=COL_INDUSTRY)
            root_console.print(x=sidebar_x,y=j+1, string=" harvests oil & solar / nuclear power", fg=COL_INDUSTRY)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[HARV]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" oil        {}".format(number(Game.get_harvesting_resources_per(), dec=1, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {} barrels".format(number(Game.get_harvesting_resources_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" happiness  {}".format(number(Game.get_harvesting_happiness_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {}".format(number(Game.get_harvesting_happiness_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" health     {}".format(number(Game.get_harvesting_physical_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_harvesting_physical_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" pollution  {}".format(number(Game.get_harvesting_pollution_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {}".format(number(Game.get_harvesting_pollution_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+8, string=" req.       {}".format(number(Game.get_harvesting_required_infrastructure_per())), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+8, string="]   {} infra.".format(number(Game.get_harvesting_required_infrastructure_total(), dec=1)), fg=RED)
        _draw_sector(Game, context, root_console, xx1, ICON_INDUSTRY, i, s, employed, v, COL_INDUSTRY, HARV)
    
    if Game.age >= 4:
        v = Game.employees[SCIE]
        i+=2
        s ="Innovation"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[SCIE]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(SCIE)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[SCIE]), fg=COL_INNOVATION)
            root_console.print(x=sidebar_x,y=j+1, string=" procures information", fg=COL_INNOVATION)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[SCIE]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" info.      {}".format(number(Game.get_science_research_per(), dec=1, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {}".format(number(Game.get_science_research_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" oil        {}".format(number(Game.get_science_resources_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {} barrels".format(number(Game.get_science_resources_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" req.       {}".format(number(Game.get_science_required_infrastructure_per())), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {} infra.".format(number(Game.get_science_required_infrastructure_total(), dec=1)), fg=RED)
        _draw_sector(Game, context, root_console, xx1, ICON_INNOVATION, i, s, employed, v, COL_INNOVATION, SCIE)
            
    if Game.age >= 5:
        v = Game.employees[ENVI]
        i+=2
        s ="Environmental"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[ENVI]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(ENVI)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[ENVI]), fg=COL_ENVIRONMENTAL)
            root_console.print(x=sidebar_x,y=j+1, string=" reduces pollution & raises happiness", fg=COL_ENVIRONMENTAL)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[ENVI]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" pollution  {}".format(number(Game.get_qol_pollution_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {}".format(number(Game.get_qol_pollution_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" happiness  {}".format(number(Game.get_qol_happiness_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {}".format(number(Game.get_qol_happiness_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+6, string=" sanity     {}".format(number(Game.get_qol_mental_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_qol_mental_total(), dec=1, showpos=True)), fg=GREEN)
        _draw_sector(Game, context, root_console, xx1, ICON_ENVIRONMENTAL, i, s, employed, v, COL_ENVIRONMENTAL, ENVI)

    if Game.age >= 6:
        v = Game.employees[HEAL]
        i+=2
        s ="Healthcare"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[HEAL]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(HEAL)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[HEAL]), fg=COL_HEALTHCARE)
            root_console.print(x=sidebar_x,y=j+1, string=" improves health & sanity", fg=COL_HEALTHCARE)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[HEAL]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" sanity     {}".format(number(Game.get_hospitals_mental_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {}".format(number(Game.get_hospitals_mental_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" health     {}".format(number(Game.get_hospitals_physical_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {}".format(number(Game.get_hospitals_physical_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+6, string=" happiness  {}".format(number(Game.get_hospitals_happiness_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_hospitals_happiness_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" req.       {}".format(number(Game.get_hospitals_required_infrastructure_per())), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {} infra.".format(number(Game.get_hospitals_required_infrastructure_total(), dec=1)), fg=RED)
        _draw_sector(Game, context, root_console, xx1, ICON_HEALTHCARE, i, s, employed, v, COL_HEALTHCARE, HEAL)

    if Game.age >= 9:
        v = Game.employees[POLI]
        i+=2
        s ="Law Enforcement"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[POLI]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(POLI)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[POLI]), fg=COL_LAWENFORCEMENT)
            root_console.print(x=sidebar_x,y=j+1, string=" mitigates crime", fg=COL_LAWENFORCEMENT)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[POLI]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" crime      {}".format(number(Game.get_police_crime_per(), showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x + arrowsidex,y=j+4, string="]   {}".format(number(Game.get_police_crime_total(), dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" happiness  {}".format(number(Game.get_police_happiness_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {}".format(number(Game.get_police_happiness_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" sanity     {}".format(number(Game.get_police_mental_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_police_mental_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" req.       {}".format(number(Game.get_police_required_infrastructure_per())), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {} infra.".format(number(Game.get_police_required_infrastructure_total(), dec=1)), fg=RED)
        _draw_sector(Game, context, root_console, xx1, ICON_LAWENFORCEMENT, i, s, employed, v, COL_LAWENFORCEMENT, POLI)
        
    if Game.age >= 10:
        v = Game.employees[DEFE]
        i+=2
        s ="Defense"
        employed = ""
        root_console.print(x=lvx,y=1+i, string="x{0:.2f}".format(1 + 0.01*Game.levels[DEFE]))
        if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < sidebar_x-1):
            employed = " employees"
            cost = Game.get_cost_per(DEFE)
            root_console.print(x=xx1 + 2,y=1+i, string="{}".format(s))
            root_console.print(x=sidebar_x,y=j+0, string="{} Sector Lv {}".format(s, Game.levels[DEFE]), fg=COL_DEFENSE)
            root_console.print(x=sidebar_x,y=j+1, string=" manufactures war machines", fg=COL_DEFENSE)
            root_console.print(x=sidebar_x,y=j+2, string=" upgrade cost: ${}".format(number(_lvcost(Game.levels[DEFE]), dec=2, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string=" power     {}${}".format("-" if cost < 0 else "+", number(abs(cost), leadingspace=False)))
            root_console.print(x=sidebar_x + arrowsidex,y=j+3, string="]  {}${}".format("-" if cost < 0 else "+", number(abs(v*cost), dec=1, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+4, string=" war mach.  {}".format(number(round(Game.get_defense_warmachines_per()), showpos=True)), fg=GREEN)
            if Game.get_defense_warmachines_total() < 1000:
                root_console.print(x=sidebar_x + arrowsidex-2,y=j+4, string="* ]   {}*".format(number(Game.get_defense_warmachines_total(), dec=1, showpos=True)), fg=GREEN)
            else:
                root_console.print(x=sidebar_x + arrowsidex-2,y=j+4, string="* ]   {}".format(number(Game.get_defense_warmachines_total() * 0.001, dec=1, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" oil        {}".format(number(Game.get_defense_resources_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+5, string="]   {} barrels".format(number(Game.get_defense_resources_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" happiness  {}".format(number(Game.get_defense_happiness_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+6, string="]   {}".format(number(Game.get_defense_happiness_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" sanity     {}".format(number(Game.get_defense_mental_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+7, string="]   {}".format(number(Game.get_defense_mental_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+8, string=" pollution  {}".format(number(Game.get_defense_pollution_per(), showpos=True)), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+8, string="]   {}".format(number(Game.get_defense_pollution_total(), dec=1, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+9, string=" req.       {}".format(number(Game.get_defense_required_infrastructure_per())), fg=RED)
            root_console.print(x=sidebar_x + arrowsidex,y=j+9, string="]   {} infra.".format(number(Game.get_defense_required_infrastructure_total(), dec=1)), fg=RED)
        _draw_sector(Game, context, root_console, xx1, ICON_DEFENSE, i, s, employed, v, COL_DEFENSE, DEFE)

def _draw_arrow(Game, context, root_console, x,y, delta):
    col = RED if delta < 0 else (GREEN if delta > 0 else WHITE)
    ch = 25 if delta < 0 else (24 if delta > 0 else 61)
    libtcodpy.console_put_char_ex(root_console, x,y, ch, col, COL_UI_BG)

def _draw_attributes(Game, context, root_console):
    # HEADER
    sidebar_x = SIDEBARX
    j = INFOY
    stockpile_x = 20
    netmo_x = 40
    max_x = 58
    i = 25
    root_console.print(x=2,y=1+i, string="Attribute", fg=WHITE)
    root_console.print(x=netmo_x,y=1+i, string="Net / mo.", fg=WHITE)
    root_console.print(x=stockpile_x,y=1+i, string="Stock", fg=WHITE)
    #root_console.print(x=max_x,y=1+i, string="Limit")
    i+=2

    # POWER
    col = RED if Game.power <= 0 else WHITE
    if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ord('$'), COL_POWER, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Power: {}".format(number(Game.power, dec=2)), fg=col)
        root_console.print(x=sidebar_x,y=j+2, string=" Abstracts available funds $ and", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+3, string="    Kardashev scale energy advancement", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+5, string=" A negative value indicates debt;", fg=col)
        root_console.print(x=sidebar_x,y=j+6, string="    escape debt to avoid game over", fg=col)
    if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 1):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ord('$'), COL_POWER, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Power: {}".format(number(Game.power, dec=2)), fg=col)
        root_console.print(x=sidebar_x,y=j+4, string="Gross Domestic Product (GDP) / mo.", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+5, string="    ${}".format(number(Game.power_income_gross, dec=1)), fg=WHITE)
        root_console.print(x=sidebar_x,y=j+6, string="Depreciation / mo.", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+7, string="    ${}".format(number(Game.power_income_gross - Game.power_income, dec=1)), fg=WHITE)
    if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x):
        root_console.print(x=sidebar_x,y=j+0, string="Income net / mo          {}${}".format("-" if Game.power_income < 0 else " ", number(abs(Game.power_income), dec=2, forcedec=True)), fg=col)
        otheragenciesnet = Game.power_income_agency_gross + Game.power_income_agency_loss
        otheragenciesnet += -Game.private_tax_income - Game.property_tax_income - Game.public_tax_income - Game.sales_tax_income - Game.power_income_ca_agency_trade - Game.power_income_ca_agency_fees_tariffs
        acol = RED if (otheragenciesnet) <= 0 else GREEN
        exportstrade = Game.power_income_export + Game.power_income_ca_agency_trade + Game.power_income_ca_agency_fees_tariffs
        root_console.print(x=sidebar_x,y=j+1, string=" Exports & Trade         {}${}".format("-" if exportstrade < 0 else " ", number(abs(exportstrade), dec=2, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+2, string=" RA: Property & civ. tax {}${}".format("-" if (Game.property_tax_income + Game.public_tax_income) < 0 else " ", number(abs(Game.property_tax_income + Game.public_tax_income), dec=2, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+3, string=" RA: Business taxes      {}${}".format("-" if Game.private_tax_income < 0 else " ", number(abs(Game.private_tax_income), dec=2, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+4, string=" RA: Sales taxes         {}${}".format("-" if Game.sales_tax_income < 0 else " ", number(abs(Game.sales_tax_income), dec=2, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+5, string=" Other agencies net      {}${}".format("-" if otheragenciesnet < 0 else " ", number(abs(otheragenciesnet), dec=2, forcedec=True)), fg=acol)
        root_console.print(x=sidebar_x,y=j+6, string=" Imports                 {}${}".format("-" if Game.power_income_import < 0 else " ", number(abs(Game.power_income_import), dec=2, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" Social program          {}${}".format("-" if Game.power_income_social_programs_upkeep < 0 else " ", number(abs(Game.power_income_social_programs_upkeep), dec=2, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+8, string=" Gov't salaries & upkeep {}${}".format("-" if Game.power_income_public_sector_upkeep < 0 else " ", number(abs(Game.power_income_public_sector_upkeep), dec=2, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+9, string=" Infrastructure upkeep   {}${}".format("-" if Game.power_income_infrastructure_upkeep < 0 else " ", number(abs(Game.power_income_infrastructure_upkeep), dec=2, forcedec=True)), fg=RED)
    root_console.print(x=2,y=1+i, string="Power")
    col = RED if Game.power <= 0 else WHITE
    libtcodpy.console_put_char_ex(root_console, stockpile_x-1, 1+i, ord('$'), COL_POWER, COL_UI_BG)
    root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.power, dec=1)), fg=col)
    _draw_arrow(Game, context, root_console, netmo_x-1,1+i, Game.power_income_delta)
    col = RED if Game.power_income < 0 else WHITE
    root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.power_income, dec=1, showpos=True)), fg=col)
    
    if Game.show_gdp:
        i += 1
        root_console.print(x=2,y=1+i, string="GDP")
        col = RED if Game.power_income_gross < 0 else WHITE
        root_console.print(x=stockpile_x-1,y=1+i, string="${}".format(number(Game.power_income_gross, dec=1)), fg=col)
        col = RED if Game.power_income_delta <= 0 else WHITE
        root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.power_income_delta, dec=1, showpos=True)), fg=col)
    
    # OIL
    if Game.age >= 2:
        i+=1
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_OIL, COL_OIL, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Oil: {} barrels".format(number(Game.resources, dec=2)))
            root_console.print(x=sidebar_x,y=j+2, string=" Harvested from Industry sector")
            root_console.print(x=sidebar_x,y=j+4, string=" Used to build infrastructure,")
            root_console.print(x=sidebar_x,y=j+5, string="    collect information, and more")
            root_console.print(x=sidebar_x,y=j+7, string=" Export excess oil to make $")
            root_console.print(x=sidebar_x,y=j+8, string="    or import oil to meet demands")
        if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 1): # and Game.mouse_x < stockpile_x - 1):
            root_console.print(x=sidebar_x,y=j+0, string="Oil net income / mo. {}".format(number(Game.resources_income, dec=2)), fg=(RED if Game.resources_income < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+1, string=" Industry            {}".format(number(Game.resources_income_industry, dec=2)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Imports / Exports   {}".format(number(Game.resources_income_commerce, dec=2)), fg=(RED if Game.resources_income_commerce < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+3, string=" Public sector       {}".format(number(Game.resources_income_public, dec=2)), fg=RED)
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Oil:    {} barrels".format(number(Game.resources, dec=2)))
            root_console.print(x=sidebar_x,y=j+1, string=" Gross: {} gallons".format(number(Game.resources * Game.oil_barrels_to_gallons, dec=1)))
            root_console.print(x=sidebar_x,y=j+2, string=" Value:  ${}".format(number(Game.resources * Game.selling_resources_economy * Game.market_value_oil * 0.01, dec=2, forcedec=True, leadingspace=False)))
            root_console.print(x=sidebar_x,y=j+3, string="       @ ${} / barrel".format(number(Game.selling_resources_economy * Game.market_value_oil * 0.01, dec=2, forcedec=True, leadingspace=False)))
        root_console.print(x=2,y=1+i, string="Oil, barrels")
        col = RED if Game.resources <= 0 else WHITE
        root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.resources, dec=1)), fg=col)
        if not Game.market_resources_set:
            col = RED if Game.resources_income < 0 else WHITE
            root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.resources_income, dec=1, showpos=True)), fg=col)
        else:
            root_console.print(x=netmo_x,y=1+i, string="(--)", fg=WHITE)
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_OIL, COL_OIL, COL_UI_BG)

    # FOOD
    i+=1
    if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_FOOD, COL_FOOD, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Food: {} crates".format(number(Game.food, dec=2)))
        root_console.print(x=sidebar_x,y=j+2, string=" Harvested from Agriculture sector")
        root_console.print(x=sidebar_x,y=j+3, string=" Used to support your population")
        root_console.print(x=sidebar_x,y=j+5, string=" Export excess food to make $")
        root_console.print(x=sidebar_x,y=j+6, string="    or import food to meet demands")
        root_console.print(x=sidebar_x,y=j+9, string="Food waste: {} % / mo.".format(Game.get_food_decay_rate()), fg=RED)
    if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Food income net / mo. {}".format(number(Game.food_income, dec=2)), fg=(RED if Game.food_income < 0 else GREEN))
        root_console.print(x=sidebar_x,y=j+1, string=" Agriculture          {}".format(number(Game.food_income_agriculture, dec=2)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+2, string=" Imports / Exports    {}".format(number(Game.food_income_commerce, dec=2)), fg=(RED if Game.food_income_commerce < 0 else GREEN))
        root_console.print(x=sidebar_x,y=j+3, string=" Feeding population   {}".format(number(Game.food_income_distribution, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+4, string=" Storage rot (decay)  {}".format(number(Game.food_income_decay, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+5, string=" Food waste           {}".format(number(Game.food_income_waste, dec=2)), fg=RED)
    if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Food:    {} crates".format(number(Game.food, dec=2)))
        root_console.print(x=sidebar_x,y=j+1, string=" Gross:  {} metric tons".format(number(Game.food * Game.food_boxes_to_kg * 0.001, dec=1, forcedec=True)))
        root_console.print(x=sidebar_x,y=j+2, string=" Value:  ${}".format(number(Game.food * Game.selling_food_economy * Game.market_value_food * 0.01, dec=2, forcedec=True, leadingspace=False)))
        root_console.print(x=sidebar_x,y=j+3, string="       @ ${} / crate".format(number(Game.selling_food_economy * Game.market_value_food * 0.01, dec=2, forcedec=True, leadingspace=False)))
        months = Game.sim_food_loss(Game.food, sim_income=True)
        root_console.print(x=sidebar_x,y=j+5, string=" Supply projected to last")
        col = (YELLOW if type(months) is not str and months <= 0 else (RED if type(months) is not str and months <= 3 else WHITE))
        root_console.print(x=sidebar_x+10,y=j+6, string="{} months".format("infinite" if months=="'" else months), fg=col)
        root_console.print(x=sidebar_x,y=j+7, string=" with current parameters")
        root_console.print(x=sidebar_x,y=j+9, string="Food decay: {} % / mo.".format(Game.get_food_decay_rate()), fg=RED)
    root_console.print(x=2,y=1+i, string="Food, crates")
    col = RED if Game.food <= 0 else WHITE
    root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.food, dec=1)), fg=col)
    if not Game.market_food_set:
        col = RED if Game.food_income < 0 else WHITE
        root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.food_income, dec=1, showpos=True)), fg=col)
    else:
        root_console.print(x=netmo_x,y=1+i, string="(--)", fg=WHITE)
    libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_FOOD, COL_FOOD, COL_UI_BG)
    if Game.age >= AGE_TRUST:
        root_console.print(x=max_x,y=1+i, string="{}".format(Game.FOOD_DISTRIBUTION2[Game.food_distribution]), fg=(RED if Game.food_distribution <= 2 else WHITE))
    
    # WEAPONS
    if Game.age >= 10:
        i+=1
        root_console.print(x=2,y=1+i, string="War Machines")
        root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.warmachines * 0.001, dec=3, forcedec=True)))
        root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.warmachines_income * 0.001, dec=3, showpos=True, forcedec=True)))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_WARMACHINES, COL_WARMACHINES, COL_UI_BG)

    # POPULATION
    i+=2
    if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_POPULATION, COL_POPULATION, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Population: {}".format(number(Game.population, dec=1)), fg=WHITE)
        root_console.print(x=sidebar_x,y=j+2, string=" Represents your city / nation's census", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+3, string=" Does not count:", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+4, string="    prisoners of war, tourists, or", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+5, string="    invading armies; nor foreign", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+6, string="    investors, merchants,", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+7, string="    ambassadors or diplomats.", fg=WHITE)
        root_console.print(x=sidebar_x,y=j+9, string="Population density: {}".format(round(Game.population_density)), fg=(RED if round(Game.population_density) >= 80 else (GREEN if round(Game.population_density) <= 20 else WHITE)))
        root_console.print(x=sidebar_x+28,y=j+9, string="/ km", fg=WHITE)
        libtcodpy.console_put_char_ex(root_console, sidebar_x+32, j+9, ord('}'), WHITE, COL_UI_BG)
    if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string=" Gov't workers  ~{}".format(number(Game.employees[INFR] + Game.employees[AGRI] + Game.employees[SCIE] + Game.employees[HARV] + Game.employees[HEAL] + Game.employees[ENVI] + Game.employees[POLI] + Game.employees[DEFE], dec=1)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+1, string=" Private sector ~{}".format(number(Game.private_sector, dec=1)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+2, string=" Soldiers       ~{}".format(number(Game.soldiers, dec=1)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+3, string=" Veterans       ~{}".format(number(Game.veterans, dec=1)), fg=GRAY)
        root_console.print(x=sidebar_x,y=j+4, string=" Disabled       ~{}".format(number(Game.disabled, dec=1)), fg=GRAY)
        root_console.print(x=sidebar_x,y=j+5, string=" Retired        ~{}".format(number(Game.retirees, dec=1)), fg=GRAY)
        root_console.print(x=sidebar_x,y=j+6, string=" Unemployed     ~{}".format(number(Game.workforce, dec=1)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" Homeless       ~{}".format(number(Game.homeless, dec=1)), fg=RED)
        root_console.print(x=sidebar_x,y=j+8, string=" Prisoners      ~{}".format(number(Game.prisoners, dec=1)), fg=RED)
        root_console.print(x=sidebar_x,y=j+9, string=" Illegals       ~{}".format(number(Game.illegals, dec=1)), fg=RED)
        '''root_console.print(x=sidebar_x+30,y=j+0, string="Militia", fg=WHITE)
        root_console.print(x=sidebar_x+30,y=j+1, string="  {} %".format(max(0, Game.militia)), fg=WHITE)'''
        root_console.print(x=sidebar_x+30,y=j+2, string="Business", fg=WHITE)
        root_console.print(x=sidebar_x+30,y=j+3, string="  Growth", fg=WHITE)
        root_console.print(x=sidebar_x+30,y=j+4, string="  {} %".format(Game.business_growth_actual), fg=WHITE)
    if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Population growth: {} / mo.".format(number(Game.population_gross_growth, dec=1, forcedec=True)), fg=WHITE)
        root_console.print(x=sidebar_x,y=j+1, string=" Immigration       {}".format(number(Game.immigration_actual, dec=1, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+2, string=" Births            {}".format(number(Game.births_per_month, dec=1, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+3, string=" Cloning           {}".format(number(Game.cloning_per_month, dec=1, forcedec=True)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+4, string="Population loss:   {} / mo.".format(number(Game.population_gross_loss, dec=1, forcedec=True)), fg=WHITE)
        root_console.print(x=sidebar_x,y=j+5, string=" Emigration        {}".format(number(Game.emigration_actual, dec=1, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+6, string=" Natural death     {}".format(number(Game.natural_deaths_per_month, dec=1, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" Poor health       {}".format(number(Game.health_deaths_per_month, dec=1, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+8, string=" Violence          {}".format(number(Game.murders_per_month, dec=1, forcedec=True)), fg=RED)
        root_console.print(x=sidebar_x,y=j+9, string=" Terrorism         {}".format(number(Game.deaths_per_month_from_terrorists, dec=1, forcedec=True)), fg=RED)
    root_console.print(x=2,y=1+i, string="Population")
    root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.population, dec=1)), fg=(RED if Game.population <= 0 else WHITE))
    root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.population_delta, dec=1, forcedec=True, showpos=True)), fg=(RED if Game.population_growth - Game.population_gross_loss <= 0 else WHITE))
    root_console.print(x=max_x-1,y=1+i, string="{} max. ({} %)".format(number(Game.population_max_actual, dec=1), round(100 * Game.population / max(1, Game.population_max_actual))), fg=(RED if Game.population_growth <= 0 else WHITE))
    libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_POPULATION, COL_POPULATION, COL_UI_BG)
    '''
    # UNEMPLOYED
    i+=1
    root_console.print(x=2,y=1+i, string="Unemployed")
    root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.workforce, dec=1)))
    col = RED if Game.workforce > 0 else WHITE
    root_console.print(x=max_x,y=1+i, string="{} %".format(number(100 * Game.workforce / max(1, Game.population), dec=1)))'''

    # INFRASTRUCTURE
    i+=1
    percentage = round(Game.unused_infrastructure / Game.existing_infrastructure * 100)
    if (Game.mouse_y >= 1+i and Game.mouse_y <= 2+i and Game.mouse_x < stockpile_x - 1):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_INFRASTRUCTURE, COL_INFRASTRUCTURE, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Infrastructure: {}".format(number(Game.existing_infrastructure, dec=2)))
        root_console.print(x=sidebar_x,y=j+2, string=" Built by Construction sector")
        root_console.print(x=sidebar_x,y=j+3, string=" Required to house your population,")
        root_console.print(x=sidebar_x,y=j+4, string="    sustain employment of workers,")
        root_console.print(x=sidebar_x,y=j+5, string="    and defend your state from attacks")
        root_console.print(x=sidebar_x,y=j+6, string=" Each infrastructure point increases")
        root_console.print(x=sidebar_x,y=j+7, string="    monthly upkeep costs")
        root_console.print(x=sidebar_x,y=j+9, string="Infrastructure decay: {} % / mo.".format(number(Game.get_infrastructure_decay_rate(), dec=2, forcedec=True)), fg=RED)
    if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Infra. income net / mo.   {}".format(number(Game.infrastructure_delta, dec=2)), fg=(RED if Game.infrastructure_delta < 0 else GREEN))
        root_console.print(x=sidebar_x,y=j+1, string=" Construction             {}".format(number(Game.infrastructure_growth, dec=2)), fg=GREEN)
        root_console.print(x=sidebar_x,y=j+2, string=" Crumbling infra. (decay) {} / mo.".format(number(Game.infrastructure_income_decay, dec=2)), fg=RED)
    if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Infrastructure:  {}".format(number(Game.existing_infrastructure, dec=2)))
        root_console.print(x=sidebar_x,y=j+1, string="         Unused  {}".format(number(Game.unused_infrastructure, dec=2)), fg=(RED if (percentage <= 5 or percentage >= 30) else WHITE))
        root_console.print(x=sidebar_x,y=j+2, string="Housing Density  {} %".format(number(100 - Game.housing_density, dec=2)))
        if (percentage <= 5):
            root_console.print(x=sidebar_x,y=j+2, string=" Employ more Construction workers".format(number(Game.unused_infrastructure, dec=2), round(Game.unused_infrastructure / Game.existing_infrastructure * 100)), fg=RED)
    root_console.print(x=2,y=1+i, string="Infrastructure")
    root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.existing_infrastructure, dec=1)), fg=(RED if Game.existing_infrastructure <= 0 else WHITE))
    root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.infrastructure_delta, dec=1, showpos=True)), fg=(RED if Game.infrastructure_growth <= 0 else WHITE))
    libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_INFRASTRUCTURE, COL_INFRASTRUCTURE, COL_UI_BG)

    # UNUSED INFRASTRUCTURE
    i+=1
    root_console.print(x=2,y=1+i, string="Unused Infra.")
    '''root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.unused_infrastructure, dec=1)), fg=(RED if Game.unused_infrastructure <= 0 else WHITE))'''
    percentcol = (RED if (percentage <= 9) else WHITE)
    root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(percentage)), fg=percentcol)
    root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.unused_infrastructure_delta, dec=1, showpos=True)), fg=(RED if Game.unused_infrastructure_delta < 0 else WHITE))
    libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_INFRASTRUCTURE, COL_UNUSEDINFRASTRUCTURE, COL_UI_BG)
    if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Last month, the amount of")
        root_console.print(x=sidebar_x,y=j+1, string="    unused (available) infrastructure")
        root_console.print(x=sidebar_x,y=j+2, string="    {} by {}".format("increased" if Game.unused_infrastructure_delta > 0 else "reduced", number(abs(Game.unused_infrastructure_delta), dec=2)), fg=WHITE)
    if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
        root_console.print(x=sidebar_x,y=j+0, string="Existing infrastructure {}".format(number(Game.existing_infrastructure, dec=2)), fg=WHITE)
        root_console.print(x=sidebar_x,y=j+1, string=" Housing                {}".format(number(Game.infrastructure_usage_population, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+2, string=" Agriculture            {}".format(number(Game.infrastructure_usage_agriculture, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+3, string=" Industry               {}".format(number(Game.infrastructure_usage_harvesting, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+4, string=" Science                {}".format(number(Game.infrastructure_usage_science, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+5, string=" Healthcare             {}".format(number(Game.infrastructure_usage_hospitals, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+6, string=" Law Enforcement        {}".format(number(Game.infrastructure_usage_police, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+7, string=" Defense                {}".format(number(Game.infrastructure_usage_defense, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+8, string=" Commercial (business)  {}".format(number(Game.infrastructure_usage_private, dec=2)), fg=RED)
        root_console.print(x=sidebar_x,y=j+9, string="Infrastructure unused:  {}".format(number(Game.unused_infrastructure, dec=2)), fg=percentcol)
        if percentage <= 5:
            root_console.print(x=sidebar_x+37,y=j+9, string="LO", fg=RED)
    
    # RESEARCH
    if Game.age >= 4:
        i+=2
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_RESEARCH, COL_RESEARCH, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Information: {}".format(number(Game.research, dec=2)))
            root_console.print(x=sidebar_x,y=j+2, string=" Represents knowledge, research,")
            root_console.print(x=sidebar_x,y=j+3, string="    talent, and digital information")
            root_console.print(x=sidebar_x,y=j+4, string=" Produced by Innovation sector")
            root_console.print(x=sidebar_x,y=j+6, string=" Used to purchase the technologies")
            root_console.print(x=sidebar_x,y=j+7, string="    introduced in Bills on your desk")
            root_console.print(x=sidebar_x,y=j+9, string="Information decay: {}%".format(number(Game.research_decay, dec=1, forcedec=True)), fg=RED)
        if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Information net / mo.   {}".format(number(Game.research_income, dec=2)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+1, string=" Innovation sector      {}".format(number(Game.research_income_science, dec=2)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Private sector         {}".format(number(Game.research_income_private, dec=2)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" World progress (decay) {}".format(number(Game.research_income_decay, dec=2)), fg=RED)
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Information     {}".format(number(Game.research, dec=2)))
            root_console.print(x=sidebar_x,y=j+1, string="Info. decay     {} % / mo.".format(number(Game.research_decay, dec=2, forcedec=True)), fg=RED)
        root_console.print(x=2,y=1+i, string="Information")
        root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.research, dec=1)))
        root_console.print(x=netmo_x,y=1+i, string="({})".format(number(Game.research_income, dec=1, showpos=True)))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_RESEARCH, COL_RESEARCH, COL_UI_BG)

    # POLLUTION
    if Game.age >= 5:
        i+=1
        if Game.pollution_ugpm3 >= 225:
            col = (255, 64, 255,)
        elif Game.pollution_ugpm3 >= 125:
            col = (255, 32, 127,)
        elif Game.pollution_ugpm3 >= 55:
            col = (255, 64, 64,)
        elif Game.pollution_ugpm3 >= 35:
            col = (255, 127, 64,)
        elif Game.pollution_ugpm3 >= 10:
            col = (255, 215, 0,)
        else:
            col = GREEN
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_POLLUTION, COL_POLLUTION, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Air Pollution: {} [g/m`".format(number(Game.pollution_ugpm3, dec=2, forcedec=True)), fg=col)
            root_console.print(x=sidebar_x,y=j+2, string=" PM2.5 air pollution measured in")
            root_console.print(x=sidebar_x,y=j+3, string="    micrograms per m` of territory")
            root_console.print(x=sidebar_x,y=j+5, string=" Affects happiness and health")
            root_console.print(x=sidebar_x,y=j+7, string=" Affected by population density,")
            root_console.print(x=sidebar_x,y=j+8, string="    wealth, and the industry and")
            root_console.print(x=sidebar_x,y=j+9, string="    environmental sectors")
        if (Game.mouse_y == 1+i and Game.mouse_x >= netmo_x and Game.mouse_x < max_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Pollution net / mo.: {} [g/m`".format(number(get_ugpm3(Game.pollution_income, Game.land), dec=3, forcedec=True)), fg=(GREEN if Game.pollution_income < 0 else RED))
            root_console.print(x=sidebar_x,y=j+1, string=" Environmental       -{} [g/m`".format(number(abs(get_ugpm3(Game.pollution_income_environmental, Game.land)), dec=3, forcedec=True, leadingspace=False)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Population density  +{} [g/m`".format(number(abs(get_ugpm3(Game.pollution_income_density, Game.land)), dec=3, forcedec=True, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+3, string=" Industry sector     +{} [g/m`".format(number(abs(get_ugpm3(Game.pollution_income_industry, Game.land)), dec=3, forcedec=True, leadingspace=False)), fg=RED)
            root_console.print(x=sidebar_x,y=j+4, string=" Other pub. sectors  +{} [g/m`".format(number(abs(get_ugpm3(Game.pollution_income_public, Game.land)), dec=3, forcedec=True, leadingspace=False)), fg=RED)
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Pollution: {} [g/m`".format(number(Game.pollution_ugpm3, dec=2, forcedec=True)), fg=col)
            root_console.print(x=sidebar_x,y=j+2, string="     0-9 [g/m`: Good", fg=(64, 255, 64,))
            root_console.print(x=sidebar_x,y=j+3, string="   10-34 [g/m`: Moderate", fg=(255, 215, 0,))
            root_console.print(x=sidebar_x,y=j+4, string="   35-54 [g/m`: Unhealthy", fg=(255, 127, 0,))
            root_console.print(x=sidebar_x,y=j+5, string="  55-124 [g/m`: Dangerous", fg=(255, 64, 64,))
            root_console.print(x=sidebar_x,y=j+6, string=" 125-225 [g/m`: Health Alert", fg=(255, 32, 127,))
            root_console.print(x=sidebar_x,y=j+7, string="    225+ [g/m`: Health Warning", fg=(255, 64, 255,))
            root_console.print(x=sidebar_x,y=j+9, string="Total Pollution Value: {}".format(number(Game.pollution, dec=2, forcedec=True)), fg=col)
        root_console.print(x=2,y=1+i, string="Pollution")
        root_console.print(x=stockpile_x,y=1+i, string="{} [g/m`".format(number(Game.pollution_ugpm3, dec=3, forcedec=True)))
        root_console.print(x=netmo_x,y=1+i, string="({})".format(number(get_ugpm3(Game.pollution_income, Game.land), dec=3, forcedec=True, showpos=True)))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_POLLUTION, col, COL_UI_BG)

    i+=2
    xoff = 0
    # PRODUCTIVITY
    if Game.age >= 1:
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_PRODUCTIVITY, COL_PRODUCTIVITY, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Productivity: {} %".format(number(Game.get_productivity(), dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Productivity affects rate of")
            root_console.print(x=sidebar_x,y=j+3, string="    production of power & goods from")
            root_console.print(x=sidebar_x,y=j+4, string="    public & private sectors")
            root_console.print(x=sidebar_x,y=j+6, string=" Affected by happiness, health,")
            root_console.print(x=sidebar_x,y=j+7, string="    sanity, crime, trust, housing")
            root_console.print(x=sidebar_x,y=j+8, string="    density, and technologies")
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Productivity:     {} %".format(number(Game.get_productivity(), dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+1, string=" Technology bonus {} %".format(number(Game.productivity_bonus, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Working hours    {} %".format(number(Game.productivity_from_hours, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Happiness        {} % / 60 max.".format(number(Game.productivity_from_happiness, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+4, string=" Health           {} % / 20 max.".format(number(Game.productivity_from_health, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" Sanity           {} % / 20 max.".format(number(Game.productivity_from_sanity, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+6, string=" Trust            {} %".format(number(Game.productivity_from_trust, dec=2, forcedec=True, showpos=True)), fg=(GREEN if Game.productivity_from_trust > 0 else RED))
            root_console.print(x=sidebar_x,y=j+7, string=" Housing Density  {} % / -5 min.".format(number(Game.productivity_from_housing_density, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+8, string=" Crime            {} %".format(number(Game.productivity_from_crime, dec=2, forcedec=True, showpos=True)), fg=RED)
            
        root_console.print(x=2,y=1+i, string="Productivity")
        root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(Game.get_productivity(), dec=1, forcedec=True)), fg=get_col_intensity(Game.productivity, 50, 100))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, ICON_PRODUCTIVITY, COL_PRODUCTIVITY, COL_UI_BG)
        i+=1

    # FERTILITY
    if Game.age >= 3:
        xoff += 1
        Game.fertility_y = 1 + i
        icon = ICON_FERTILITY_100 if Game.fertility >= 8.0 else (ICON_FERTILITY_75 if Game.fertility >= 6.0 else (ICON_FERTILITY_50 if Game.fertility >= 4.0 else ICON_FERTILITY_25))
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, icon, COL_FERTILITY, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Fertility: {} %".format(number(10 * Game.fertility, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Determines birth rate")
            root_console.print(x=sidebar_x,y=j+4, string=" Affected by happiness, health,")
            root_console.print(x=sidebar_x,y=j+5, string="    sanity, and nourishment")
            root_console.print(x=sidebar_x,y=j+9, string="Birth rate: {} / mo.".format(number(Game.births_per_month, dec=2, forcedec=True)))
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x <= netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Fertility:        {} %".format(number(10 * Game.fertility, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+1, string=" Technology bonus {} %".format(number(10 * Game.fertility_from_technology, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Happiness        {} %".format(number(10 * Game.fertility_from_happiness, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Health           {} %".format(number(10 * Game.fertility_from_health, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+4, string=" Sanity           {} %".format(number(10 * Game.fertility_from_sanity, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+5, string=" Max fertility    {} %".format(number(10 * Game.max_fertility, dec=2, forcedec=True)), fg=(RED if Game.fertility >= Game.max_fertility else LTGRAY))
            root_console.print(x=sidebar_x,y=j+6, string="Fertility cap set by FMA policies")
            root_console.print(x=sidebar_x,y=j+7, string="Note you cannot receive a bonus to")
            root_console.print(x=sidebar_x,y=j+8, string="    fertility from happiness unless")
            root_console.print(x=sidebar_x,y=j+9, string="    your health and sanity are low")
        root_console.print(x=2,y=1+i, string="Fertility")
        root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(10 * Game.fertility, dec=1, forcedec=True)), fg=get_col_intensity(10 * Game.fertility, 30, 100))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, icon, COL_FERTILITY, COL_UI_BG)
        i+=1

    # HAPPINESS
    if Game.age >= 3:
        xoff += 1
        icon = ICON_HAPPINESS_100 if Game.happiness >= 75 else (ICON_HAPPINESS_75 if Game.happiness >= 50 else (ICON_HAPPINESS_50 if Game.happiness >= 25 else ICON_HAPPINESS_25))
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, icon, COL_HAPPINESS, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Happiness per capita: {} %".format(number(Game.happiness, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects your population's happiness")
            root_console.print(x=sidebar_x,y=j+4, string=" Affects productivity, fertility,")
            root_console.print(x=sidebar_x,y=j+5, string="    crime, and citizen approval ratings")
            root_console.print(x=sidebar_x,y=j+7, string=" Affected by pop. density, taxes,")
            root_console.print(x=sidebar_x,y=j+8, string="    pollution, career satisfaction, and")
            root_console.print(x=sidebar_x,y=j+9, string="    quality of food, drug & utilities")
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Happiness per capita:  {} %".format(number(Game.happiness, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+1, string=" Tech & policy bonus   {} %".format(number(Game.happiness_bonus + Game.happiness_from_birth_policy + Game.happiness_from_pensions, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Food & drug           {} %".format(number(Game.happiness_from_food, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Environmental         {} %".format(number(Game.happiness_from_environmental, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+4, string=" Career satisfaction   {}{} %".format("+" if Game.happiness_from_jobs > 0 else "-", number(abs(Game.happiness_from_jobs), dec=2, forcedec=True, leadingspace=False)), fg=(RED if Game.happiness_from_jobs < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+5, string=" Taxes                 {} %".format(number(Game.happiness_from_taxes, dec=2, forcedec=True, showpos=True)), fg=(RED if Game.happiness_from_taxes < 0 else GREEN))
            root_console.print(x=sidebar_x,y=j+6, string=" Pollution             {} %".format(number(Game.happiness_from_pollution, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" Population density    {} %".format(number(Game.happiness_from_density, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+8, string=" Income inequality     {} %".format(number(Game.happiness_from_income_distribution, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+9, string="Total Happiness Value: {}".format(number(Game.happiness * Game.population, dec=1)))
            
        root_console.print(x=2,y=1+i, string="Happiness")
        root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(Game.happiness, dec=1, forcedec=True)), fg=get_col_intensity(Game.happiness, 0, 100))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, icon, COL_HAPPINESS, COL_UI_BG)
        '''col = RED if Game.happiness_income <= 0 else WHITE
        root_console.print(x=netmo_x,y=1+i, string="({0:.1f})".format(Game.happiness_income / max(1, Game.population)), fg=col)
        root_console.print(x=max_x,y=1+i, string="{} - {} %".format(max(0, math.floor(Game.happiness_lower_limit)), min(100, math.ceil(Game.happiness_upper_limit))))'''
        i += 1

    # SANITY
    if Game.age >= 5:
        xoff += 1
        icon = ICON_SANITY_100 if Game.mental >= 75 else (ICON_SANITY_75 if Game.mental >= 50 else (ICON_SANITY_50 if Game.mental >= 25 else ICON_SANITY_25))
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, icon, COL_SANITY, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Sanity per capita: {} %".format(number(Game.mental, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects population's mental health")
            root_console.print(x=sidebar_x,y=j+4, string=" Affects productivity, fertility,")
            root_console.print(x=sidebar_x,y=j+5, string="    soldier strength, and crime")
            root_console.print(x=sidebar_x,y=j+7, string=" Affected by population density, threat")
            root_console.print(x=sidebar_x,y=j+8, string="    level and occupational hazards")
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Sanity per capita:  {} %".format(number(Game.mental, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+1, string=" Technology bonus   {} %".format(number(Game.mental_bonus, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Healthcare         {} %".format(number(Game.mental_from_healthcare, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Environmental      {} %".format(number(Game.mental_from_environmental, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+4, string=" Overwork & stress  {} %".format(number(Game.mental_from_jobs_loss, dec=2, forcedec=True, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+5, string=" Pollution          {} %".format(number(Game.mental_from_pollution, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" Grief              {} %".format(number(Game.mental_from_grief, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" War                {} %".format(number(Game.mental_from_war, dec=2, forcedec=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+8, string=" Existential dread  {} % / -{} min.".format(number(Game.mental_from_dread, dec=2, forcedec=True), Game.age_max), fg=RED)
            root_console.print(x=sidebar_x,y=j+9, string="Total Sanity Value: {}".format(number(Game.mental * Game.population, dec=1)))
        root_console.print(x=2,y=1+i, string="Sanity")
        root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(Game.mental, dec=1, forcedec=True)), fg=get_col_intensity(Game.mental, 0, 100))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, icon, COL_SANITY, COL_UI_BG)
        '''col = RED if Game.mental_income <= 0 else WHITE
        root_console.print(x=netmo_x,y=1+i, string="({0:.1f})".format(Game.mental_income / max(1, Game.population)), fg=col)
        root_console.print(x=max_x,y=1+i, string="{} - {} %".format(max(0, math.floor(Game.mental_lower_limit)), min(100, math.ceil(Game.mental_upper_limit))))'''
        i += 1

    # HEALTH
    if Game.age >= 6:
        xoff += 1
        icon = ICON_HEALTH_100 if Game.physical >= 75 else (ICON_HEALTH_75 if Game.physical >= 50 else (ICON_HEALTH_50 if Game.physical >= 25 else ICON_HEALTH_25))
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, icon, COL_HEALTH, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Health per capita: {} %".format(number(Game.physical, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects population's physical health")
            root_console.print(x=sidebar_x,y=j+4, string=" Affects productivity, fertility,")
            root_console.print(x=sidebar_x,y=j+5, string="    soldier strength, and death rate")
            root_console.print(x=sidebar_x,y=j+7, string=" Affected by pollution, nourishment,")
            root_console.print(x=sidebar_x,y=j+8, string="    and occupational hazards")
        if (Game.mouse_y == 1+i and Game.mouse_x >= stockpile_x and Game.mouse_x < netmo_x - 2):
            root_console.print(x=sidebar_x,y=j+0, string="Health per capita:     {} %".format(number(Game.physical, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+1, string=" Technology bonus      {} %".format(number(Game.physical_bonus, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+2, string=" Food & drug           {} %".format(number(Game.physical_from_food_drugs, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+3, string=" Healthcare            {} %".format(number(Game.physical_from_healthcare, dec=2, forcedec=True, showpos=True)), fg=GREEN)
            root_console.print(x=sidebar_x,y=j+4, string=" Overwork & job injury {} %".format(number(Game.physical_from_public + Game.physical_from_private_sector, dec=2, forcedec=True, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+5, string=" Pollution             {} %".format(number(Game.physical_from_pollution, dec=2, forcedec=True, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+6, string=" Pandemic & illness    {} %".format(number(Game.physical_from_pandemic, dec=2, forcedec=True, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+7, string=" Crime & drug abuse    {} %".format(number(Game.physical_from_drug_abuse, dec=2, forcedec=True, showpos=True)), fg=RED)
            root_console.print(x=sidebar_x,y=j+9, string="Total Health Value:    {}".format(number(Game.physical * Game.population, dec=1)))
        root_console.print(x=2,y=1+i, string="Health")
        root_console.print(x=stockpile_x,y=1+i, string="{} %".format(number(Game.physical, dec=1, forcedec=True)), fg=get_col_intensity(Game.physical, 0, 100))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, icon, COL_HEALTH, COL_UI_BG)
        '''col = RED if Game.physical_income <= 0 else WHITE
        root_console.print(x=netmo_x,y=1+i, string="({0:.1f})".format(Game.physical_income / max(1, Game.population)), fg=col)
        root_console.print(x=max_x,y=1+i, string="{} - {} %".format(max(0, math.floor(Game.physical_lower_limit)), min(100, math.ceil(Game.physical_upper_limit))))'''
        i+=1

    # CRIME
    if Game.age >= 9:
        xoff += 1
        icon = ICON_CRIME_100 if Game.crime >= 15 else (ICON_CRIME_75 if Game.crime >= 10 else (ICON_CRIME_50 if Game.crime >= 5 else ICON_CRIME_25))
        if (Game.mouse_y == 1+i and Game.mouse_x < stockpile_x - 1):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, icon, COL_CRIME, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Crime: {}".format(number(Game.crime, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Represents the amount of organized")
            root_console.print(x=sidebar_x,y=j+3, string="    and petty crime, as well as the")
            root_console.print(x=sidebar_x,y=j+4, string="    corruption of the upper class")
            root_console.print(x=sidebar_x,y=j+6, string=" Caused by low sanity, low happiness,")
            root_console.print(x=sidebar_x,y=j+7, string="    and high population density")
            root_console.print(x=sidebar_x,y=j+8, string=" Affects productivity greatly")
        root_console.print(x=2,y=1+i, string="Crime")
        root_console.print(x=stockpile_x,y=1+i, string="{}".format(number(Game.crime, dec=1, forcedec=True)), fg=get_col_intensity(Game.crime, 0, 20, reverse=True))
        libtcodpy.console_put_char_ex(root_console, stockpile_x - 1, 1+i, icon, COL_CRIME, COL_UI_BG)
        '''root_console.print(x=netmo_x,y=1+i, string="({0:.1f})".format(Game.crime_income / max(1, Game.population)))
        root_console.print(x=max_x,y=1+i, string="{} - {} %".format(max(0, math.floor(Game.crime_lower_limit)), min(100, math.ceil(Game.crime_upper_limit))))'''
        i+=1

    SPACE=8
    ypos = 47
    i = ypos
    g = 0
    if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+2)):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_TERRITORY, COL_TERRITORY, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Territory:       {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+32,y=j+0, string="km")
        libtcodpy.console_put_char_ex(root_console, sidebar_x+34, j+0, ord('}'), WHITE, COL_UI_BG)
        '''root_console.print(x=sidebar_x+3,y=j+0, string=" Tropical land    {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+0, string=" Temperate land   {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+0, string=" Continental land {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+0, string=" Arid land        {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+1, string=" Fresh water      {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+1, string=" Salt water       {}".format(number(Game.land)))
        root_console.print(x=sidebar_x+3,y=j+1, string=" Salt water       {}".format(number(Game.land)))'''
        root_console.print(x=sidebar_x,y=j+1,   string=" Population max.    {}".format(number(Game.population_max_actual, dec=1)))
        root_console.print(x=sidebar_x,y=j+2,   string=" Population density {}".format(number(round(Game.population_density))))
        root_console.print(x=sidebar_x+30,y=j+2, string="/ km")
        libtcodpy.console_put_char_ex(root_console, sidebar_x+34, j+2, ord('}'), WHITE, COL_UI_BG)
        root_console.print(x=sidebar_x,y=j+3,   string=" Development        {} %".format(number(round(100 * Game.population / Game.population_max_actual))))
        root_console.print(x=sidebar_x,y=j+5, string=" Represents how much territory your")
        root_console.print(x=sidebar_x,y=j+6, string="    city / nation controls")
        root_console.print(x=sidebar_x,y=j+7, string=" Affects maximum population")
        root_console.print(x=sidebar_x,y=j+8, string=" Affected by war and diplomacy")
    libtcodpy.console_put_char_ex(root_console, 2, 1+i, ICON_TERRITORY, COL_TERRITORY, COL_UI_BG)
    root_console.print(x=4,y=1+i, string="{}".format(number(Game.land, dec=1)))
    # UNEMPLOYMENT
    g += 2
    col = (RED if Game.unemployment_rate >= 10 else (GREEN if Game.unemployment_rate <= 5 and Game.unemployment_rate >= 3 else WHITE))
    if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
        libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_UNEMPLOYMENT, COL_UNEMPLOYMENT, COL_UI_BG)
        root_console.print(x=sidebar_x+3,y=j+0, string="Unemployment rate: {} %".format(number(Game.unemployment_rate)), fg=col)
        root_console.print(x=sidebar_x,y=j+2, string=" Represents the percentage of your")
        root_console.print(x=sidebar_x,y=j+3, string="    population which is currently not")
        root_console.print(x=sidebar_x,y=j+4, string="    employed in the public or private")
        root_console.print(x=sidebar_x,y=j+5, string="    sector. Does not count prisoners,")
        root_console.print(x=sidebar_x,y=j+6, string="    retirees, or illegal immigrants.")
    libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_UNEMPLOYMENT, COL_UNEMPLOYMENT, COL_UI_BG)
    root_console.print(x=SPACE*g + 4,y=1+i, string="{}%".format(number(Game.unemployment_rate, dec=1)), fg=col)
    if Game.age >= AGE_RECONSTRUCTION:
        g += 1
    # BUSINESS GROWTH
        if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_BUSINESS, COL_BUSINESS, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Business growth: {} %".format(number(Game.business_growth_actual)))
            root_console.print(x=sidebar_x,y=j+2, string=" Represents the power of your private")
            root_console.print(x=sidebar_x,y=j+3, string="    sector")
            root_console.print(x=sidebar_x,y=j+5, string=" Affects the rate at which new")
            root_console.print(x=sidebar_x,y=j+6, string="    employees are allocated to the")
            root_console.print(x=sidebar_x,y=j+7, string="    private sector")
            root_console.print(x=sidebar_x,y=j+9, string=" Affected by technologies")
        libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_BUSINESS, COL_BUSINESS, COL_UI_BG)
        root_console.print(x=SPACE*g + 4,y=1+i, string="{}%".format(number(Game.business_growth_actual, dec=1)))
    # TRUST
    g += 1
    if Game.age >= AGE_TRUST:
        if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_TRUST, COL_TRUST, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Trust: {}".format(number(Game.trust_actual)))
            root_console.print(x=sidebar_x,y=j+2, string=" Represents patriotism, trust in your")
            root_console.print(x=sidebar_x,y=j+3, string="    policies, & diplomatic tension")
            root_console.print(x=sidebar_x,y=j+5, string=" Affects behavior of other nations,")
            root_console.print(x=sidebar_x,y=j+6, string="    businesses, and foreign investors")
            root_console.print(x=sidebar_x,y=j+8, string=" Affected by technologies, agency")
            root_console.print(x=sidebar_x,y=j+9, string="    settings, and war")
        libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_TRUST, COL_TRUST, COL_UI_BG)
        root_console.print(x=SPACE*g + 4,y=1+i, string="{}".format(number(Game.trust_actual, dec=1)))
    if Game.age >= AGE_RECONSTRUCTION:
    # WEALTH
        g += 1
        if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_WEALTH, COL_WEALTH, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Wealth: {}".format(number(Game.wealth_actual)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects the richness of you and your")
            root_console.print(x=sidebar_x,y=j+3, string="    population, and the value of your")
            root_console.print(x=sidebar_x,y=j+4, string="    country's currency")
            root_console.print(x=sidebar_x,y=j+5, string=" Affects immigration, emigration,")
            root_console.print(x=sidebar_x,y=j+6, string="    income from private sector, taxes;")
            root_console.print(x=sidebar_x,y=j+7, string="    also sets the standard for")
            root_console.print(x=sidebar_x,y=j+8, string="    wages of your working class")
            root_console.print(x=sidebar_x,y=j+9, string=" Affected by technologies and war")
        libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_WEALTH, COL_WEALTH, COL_UI_BG)
        root_console.print(x=SPACE*g + 4,y=1+i, string="{}".format(number(Game.wealth_actual, dec=1)))
    if Game.age >= AGE_PROSPEROUS:
    # INFLUENCE
        g += 1
        if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_INFLUENCE, COL_INFLUENCE, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Influence: {}".format(number(Game.influence_actual)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects the military and economic")
            root_console.print(x=sidebar_x,y=j+3, string="    might of your nation")
            root_console.print(x=sidebar_x,y=j+4, string=" Affects export market value, and")
            root_console.print(x=sidebar_x,y=j+5, string="    success rates of:")
            root_console.print(x=sidebar_x,y=j+6, string="  - war campaigns")
            root_console.print(x=sidebar_x,y=j+7, string="  - diplomatic treaties")
            root_console.print(x=sidebar_x,y=j+8, string=" Affected by technologies and war")
        libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_INFLUENCE, COL_INFLUENCE, COL_UI_BG)
        root_console.print(x=SPACE*g + 4,y=1+i, string="{}".format(number(Game.influence_actual, dec=1)))
    # INCOME INEQUALITY
        g += 1
        if (Game.mouse_y == 1+i and Game.mouse_x > g*SPACE and Game.mouse_x <= SPACE*(g+1)):
            libtcodpy.console_put_char_ex(root_console, sidebar_x+1, j+0, ICON_INCOME_INEQUALITY, COL_INCOME_INEQUALITY, COL_UI_BG)
            root_console.print(x=sidebar_x+3,y=j+0, string="Income Inequality: {} : 1".format(number(Game.income_inequality_actual, dec=2, forcedec=True)))
            root_console.print(x=sidebar_x,y=j+2, string=" Reflects the distribution of wealth")
            root_console.print(x=sidebar_x,y=j+3, string="    as a ratio of upper : lower class")
            root_console.print(x=sidebar_x,y=j+4, string="    income")
            root_console.print(x=sidebar_x,y=j+5, string=" Affects happiness and tax revenue")
            root_console.print(x=sidebar_x,y=j+6, string=" Affected by high civilian taxing")
            root_console.print(x=sidebar_x,y=j+7, string="    rates, low investor taxing rates,")
            root_console.print(x=sidebar_x,y=j+8, string="    high wealth & business growth")
        libtcodpy.console_put_char_ex(root_console, SPACE*g + 2, 1+i, ICON_INCOME_INEQUALITY, COL_INCOME_INEQUALITY, COL_UI_BG)
        root_console.print(x=SPACE*g + 4,y=1+i, string="{}".format(number(Game.income_inequality_actual, dec=1, forcedec=True)))

def _draw_top_walls(root_console, age_x):
    col = COL_UI_DARK
    # Age fancy background
    for x in range(24):
        cc = (1 + 0.075*(12 - abs(12 - x)))
        libtcodpy.console_put_char_ex(root_console, age_x+x, 0, 205, (round(128 * cc), round(107 * cc), round(75 * cc),), COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, age_x, 0, 222, col, COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, age_x+23, 0, 223, col, COL_UI_BG)
    # top wall
    for x in range(50):
        libtcodpy.console_put_char_ex(root_console, 50+x, 2, 205, col, COL_UI_BG)
    for x in range(49):
        k = max(0, x - 29)
        factor = (20-k)/20
        libtcodpy.console_put_char_ex(root_console, x, 2, 196, (round(128 * factor), round(107 * factor), round(75 * factor),), COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, 50, 2, 222, col, COL_UI_BG)
def _draw_walls(root_console):
    col = COL_UI_DARK
    # Attributes top walls
    for x in range(80):
        libtcodpy.console_put_char_ex(root_console, x, 25, 196, col, COL_UI_BG)
        libtcodpy.console_put_char_ex(root_console, x, 27, 196, COL_UI_DEEP, COL_UI_BG)
    #Technologies
    for x in range(40):
        libtcodpy.console_put_char_ex(root_console, 40+x, 8+10, 205, col, COL_UI_BG)
    # market -> sectors divider
    for x in range(40):
        libtcodpy.console_put_char_ex(root_console, x, 7, 205, col, COL_UI_BG)
    # market -> info divider
    for x in range(30):
        k = max(0, x - 10)
        factor = (20-k)/20
        libtcodpy.console_put_char_ex(root_console, 40+x, 7, 196, (round(128*factor), round(107*factor), round(75*factor),), COL_UI_BG)
    # market -> info divider (fancy)
    for x in range(9):
        libtcodpy.console_put_char_ex(root_console, 71+x, 7, 205, col, COL_UI_BG)
    # market -> info divider (fancy transition)
    libtcodpy.console_put_char_ex(root_console, 71, 7, 222, col, COL_UI_BG)
    # sectors -> info divider
    for y in range(17):
        libtcodpy.console_put_char_ex(root_console, 39, 8+y, 179, col, COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, 39, 7, 194, col, COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, 39, 8+17, 193, col, COL_UI_BG)
    libtcodpy.console_put_char_ex(root_console, 39, 8+10, 198, col, COL_UI_BG)
    # Attributes bottom wall
    col = COL_UI_DARK
    for x in range(80):
        libtcodpy.console_put_char_ex(root_console, x, 47, 196, COL_UI_DEEP, COL_UI_BG)
        if x % 6 == 2:
            libtcodpy.console_put_char_ex(root_console, x, 49, 225, col, COL_UI_BG)
        else:
            libtcodpy.console_put_char_ex(root_console, x, 49, 222+(x % 3), col, COL_UI_BG)

def check_inputs(Game):
    Game.mouse_clicking = False
    Game.mouse_released = False
    for event in tcod.event.get():
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown(sym=sym, scancode=scancode, mod=mod, repeat=repeat):
                if (sym==tcod.event.KeySym.LSHIFT or sym==tcod.event.KeySym.RSHIFT):
                    Game.shift_held = True
                if (sym==tcod.event.KeySym.LCTRL or sym==tcod.event.KeySym.RCTRL):
                    Game.ctrl_held = True
                if (sym==tcod.event.KeySym.LALT or sym==tcod.event.KeySym.RALT):
                    Game.alt_held = True
                if sym==tcod.event.KeySym.SPACE:
                    Game.paused = not Game.paused
                #print(f"KeyDown: {sym=}, {scancode=}, {mod=}, {repeat=}")
            case tcod.event.KeyUp(sym=sym, scancode=scancode, mod=mod, repeat=repeat):
                if (sym==tcod.event.KeySym.LSHIFT or sym==tcod.event.KeySym.RSHIFT):
                    Game.shift_held = False
                if (sym==tcod.event.KeySym.LCTRL or sym==tcod.event.KeySym.RCTRL):
                    Game.ctrl_held = False
                if (sym==tcod.event.KeySym.LALT or sym==tcod.event.KeySym.RALT):
                    Game.alt_held = False
                #print(f"KeyUp: {sym=}, {scancode=}, {mod=}, {repeat=}")
            case tcod.event.MouseButtonDown(button=button, pixel=pixel, tile=tile):
                if button==1:
                    Game.mouse_clicking = True
                    Game.mouse_held = True
            case tcod.event.MouseButtonUp(button=button, pixel=pixel, tile=tile):
                if button==1:
                    Game.mouse_released = True
                    Game.mouse_held = False
                #print(f"MouseButtonDown: {button=}, {pixel=}, {tile=}")
            case tcod.event.MouseMotion(pixel=pixel, pixel_motion=pixel_motion, tile=tile, tile_motion=tile_motion):
                Game.mouse_x, Game.mouse_y = pixel
                Game.mouse_x = Game.mouse_x // Game.tile_w
                Game.mouse_y = Game.mouse_y // Game.tile_h
                #print(f"MouseMotion: {pixel=}, {pixel_motion=}, {tile=}, {tile_motion=}")
        '''case tcod.event.Event() as event:
                pass
                #print(event)  # Show any unhandled events.'''
        '''case tcod.event.KeyDown(sym=sym) if sym in Game.KEY_COMMANDS:
                pass
                #print(f"Command: {KEY_COMMANDS[sym]}")'''
            
    if Game.mouse_released:
        buttonList.attempt_click_release(Game, Game.mouse_x, Game.mouse_y)
    elif Game.mouse_clicking:
        buttonList.attempt_clicks(Game, Game.mouse_x, Game.mouse_y)
        buttonList.reset_hold_times()
    if Game.mouse_held:
        buttonList.attempt_hold_clicks(Game, Game.mouse_x, Game.mouse_y)


def display(Game, context, root_console):
    sidebar_x = SIDEBARX
    j = INFOY
    age_x = AGEX

    if Game.tab_groups[2] == TAB_DASHBOARD:
        
        _draw_walls(root_console)
        
        _draw_market(Game, context, root_console)

        if Game.tab_groups[0] == TAB_SECTORS:
            _draw_sectors_tab(Game, context, root_console)
        if Game.tab_groups[0] == TAB_AGENCIES:
            _draw_agencies_tab(Game, context, root_console)
        if Game.tab_groups[0] == TAB_AGENCIES2:
            _draw_agencies2_tab(Game, context, root_console)

        if Game.tab_groups[1] == TAB_TECHS:
            _draw_technologies_tab(Game, context, root_console)
        if Game.tab_groups[1] == TAB_ADVISORY:
            _draw_advisory_tab(Game, context, root_console)
        
        _draw_attributes(Game, context, root_console)
        
    _draw_top_walls(root_console, age_x)
    _draw_header(Game, context, root_console, age_x)

    buttonList.draw_all(Game, root_console, Game.mouse_x, Game.mouse_y)

    # DRAW
    context.present(root_console)
    root_console.clear(bg=COL_UI_BG)




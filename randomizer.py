from distutils.dir_util import copy_tree
from toga.style.pack import *
from bs4 import BeautifulSoup
import random
import time
import toga
import json
import sys
import os

# pyinstaller sets sys.frozen to true, so this is used to check if you are
# running the built executable or the script on it's own
if getattr( sys, 'frozen', False ):
    base_path = sys._MEIPASS
    ots_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)
    ots_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\outtheresomewhere"

# JSON object containing all potential levels and core placements
with open(os.path.join(base_path, 'potential_core_spots.json')) as coresFile:
    levels_and_cores = json.loads(coresFile.read())

# List of the levels that contain a core in the vanilla game
vanilla_levels = ["10_5.oel", "11_6.oel", "15_5.oel", "16_3.oel", "16_6.oel", "18_3.oel", "24_3.oel", "30_6.oel", "31_4.oel", "4_5.oel", "9_4.oel"]


# Removes the core from a level
def removeCore(level_path):
    with open(level_path, 'r+') as levelFile:
        soup = BeautifulSoup(levelFile.read(), 'xml')
        soup.Objects.col_core1.decompose()
        levelFile.seek(0)
        levelFile.write(soup.prettify())
        levelFile.truncate()


# Adds the given core to the given level
def insertCore(level_path, core_str):
    with open(level_path, 'r+') as levelFile:
        soup = BeautifulSoup(levelFile.read(), 'xml')
        xml_node = BeautifulSoup(core_str, 'xml')
        soup.Objects.append(xml_node.col_core1)
        levelFile.seek(0)
        levelFile.write(soup.prettify())
        levelFile.truncate()


def build(app):
    # EVENT HANDLERS
    def generate_seed(widget):
        random_seed = random.getrandbits(64)
        seed_input.value = random_seed

    # Creates two copies of the folder containing all the levels, one for backup and one which has
    # every core removed which is used whenever the randomizer is going to insert the cores.
    def init(widget):
        copy_tree(os.path.join(ots_path, 'level'), os.path.join(ots_path, 'level (backup)'))
        copy_tree(os.path.join(ots_path, 'level'), os.path.join(ots_path, 'level (cleaned)'))
        for level in vanilla_levels:
            removeCore(os.path.join(ots_path, 'level (cleaned)', level))

    # Copies over the "clean" version of the levels, picks eleven random levels and a core
    # within each of them and then adds them to that level.
    def randomize(widget):
        copy_tree(os.path.join(ots_path,'level (cleaned)'), os.path.join(ots_path, 'level'))
        if seed_input.value:
            random.seed(seed_input.value)
        potential_levels = sorted([level for level in levels_and_cores.keys()])

        if exclude_switch.is_on:
            potential_levels.remove('4_5.oel')

        random_levels = random.sample(potential_levels, 11)
        for level in random_levels:
            core = random.choice(levels_and_cores[level])
            insertCore(os.path.join(ots_path, 'level', level), core)

    # Copies the backup folder to the normal level folder to restore the levels to normal
    def restore(widget):
        copy_tree(os.path.join(ots_path, 'level (backup)'), os.path.join(ots_path, 'level'))

    # GUI ELEMENTS #
    # INIT BUTTON #
    init_button = toga.Button('Initialize files (run only once)', on_press=init, style=Pack(height=30))

    # RANDOM SEED #
    random_seed_box = toga.Box()

    seed_button = toga.Button('Generate seed', on_press=generate_seed,style=Pack(height=30, padding_top=5))
    seed_input = toga.TextInput(style=Pack(padding=10, flex=1))
    random_seed_box.add(seed_input)
    random_seed_box.add(seed_button)

    # EXCLUDE CHECKBOX #
    exclude_switch = toga.Switch('Exclude 4_5.oel (A New Hope)', is_on=True, style=Pack(padding=(5,10,5,10), flex=1))

    # RANDOMIZE BUTTON #
    rand_button = toga.Button('Randomize collectibles', on_press=randomize, style=Pack(height=40, padding_top=10))

    # RESTORE FROM BACKUP BUTTON #
    restore_button = toga.Button('Restore levels to normal', on_press=restore, style=Pack(height=40))

    # MAIN LAYOUT
    main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
    main_box.add(init_button)
    main_box.add(random_seed_box)
    main_box.add(exclude_switch)
    main_box.add(rand_button)
    main_box.add(restore_button)

    app.main_window.size = (350, 240)

    return main_box


def main():
    return toga.App('OTS Collectibles Randomizer', 'com.ots.randomizer', startup=build, icon=os.path.join(base_path, 'treeman.ico'))


if __name__ == '__main__':
    main().main_loop()

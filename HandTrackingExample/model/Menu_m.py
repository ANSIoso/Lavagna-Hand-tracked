from model.MenuOptions import MenuOptions


class MenuM:
    # class used that define how the menu works

    # possible section of the menu
    INITIAL = 0
    COLORS = 1
    THICKNESS = 2

    # section menu items
    option_initial = [MenuOptions.switch_mode, MenuOptions.delete_all, MenuOptions.change_colors, MenuOptions.pencil_thickness]
    option_colors = [MenuOptions.white, MenuOptions.red, MenuOptions.blue, MenuOptions.yellow]
    option_thickness = [MenuOptions.thin, MenuOptions.normal, MenuOptions.thick]

    options = {
        INITIAL: option_initial,
        COLORS: option_colors,
        THICKNESS: option_thickness
    }

    def __init__(self):
        self.actual_menu_option = []
        self.actual_choice = 0
        self.selection_time = None
        self.actual_section = self.INITIAL

        # at the beginning load in the menu the initial option
        self.load_option(self.actual_section)

        # field used to understand if the menù is opened
        self.open = False

        # field used to understand the position of the menù
        #self.menu_pos_x = 0
        #self.menu_pos_y = 0

    def load_option(self, chose):
        # method used to load all the option of a specific section

        # - clear all the actual option
        # - reset the actual option to the first
        # - set the actual chose to the category that I want to load
        self.actual_menu_option.clear()
        self.actual_choice = 0

        self.actual_section = chose

        # - load all the option of a category
        for option in self.options[chose]:
            self.actual_menu_option.append(option)

        # - at the end add the option to close the menù
        self.actual_menu_option.append(MenuOptions.exit)

    def next_choice(self):
        # method used to go at the next option in the menu (if it is available)
        new_choice = self.actual_choice + 1
        if new_choice >= len(self.actual_menu_option):
            return

        self.actual_choice = new_choice

    def previous_choice(self):
        # method used to go at the previous option in the menu (if it is available)
        new_choice = self.actual_choice - 1
        if new_choice < 0:
            return

        self.actual_choice = new_choice

    def open_menu(self):
        self.open = True
        self.load_option(self.INITIAL)

    def close_menu(self):
        self.open = False

    def get_choice(self):
        return self.actual_menu_option[self.actual_choice]
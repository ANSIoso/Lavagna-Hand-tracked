from model.MenuOptions import MenuOptions


class MenuM:
    INITIAL = 0
    COLORS = 1
    THICKNESS = 2

    option_initial = [MenuOptions.switch_mode, MenuOptions.change_colors, MenuOptions.pencil_thickness]
    option_colors = [MenuOptions.red, MenuOptions.blue, MenuOptions.yellow]
    option_thickness = [MenuOptions.thin, MenuOptions.normal, MenuOptions.thick]

    options = {
        INITIAL: option_initial,
        COLORS: option_colors,
        THICKNESS: option_thickness
    }

    def __init__(self):
        self.actual_menu_option = []
        self.actual_choice = 0
        self.actual_section = self.INITIAL

        self.load_option(self.actual_section)

    def load_option(self, chose):
        self.actual_menu_option.clear()
        self.actual_choice = 0

        self.actual_section = chose

        for option in self.options[chose]:
            self.actual_menu_option.append(option)

        self.actual_menu_option.append(MenuOptions.exit)

    def next_choice(self):
        new_choice = self.actual_choice + 1
        if new_choice >= len(self.actual_menu_option):
            return

        self.actual_choice = new_choice

    def previous_choice(self):
        new_choice = self.actual_choice - 1
        if new_choice < 0:
            return

        self.actual_choice = new_choice

    def get_choice(self):
        return self.actual_menu_option[self.actual_choice]
import customtkinter as ctk
import os
import json

# Get the directory path for the file currently being executed
# to make it independent from current working directory and
# ensure the settings.json file being created in the same
# folder as all the other scripts
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))


class SettingsManager:
    def __init__(self):
        self.settings = None

    def save_settings(self):
        if self.settings:
            with open(MAIN_DIR + "/settings.json", "w") as f:
                json.dump(self.settings, f)

    def load_settings(self):
        if not os.path.isfile(MAIN_DIR + "/settings.json"):
            with open(MAIN_DIR + "/settings.json", "w") as f:
                json.dump(
                    {
                        "exclude_chars": "",
                        "appearance_mode": "System",
                        "scaling": "100%",
                    },
                    f,
                )

        with open(MAIN_DIR + "/settings.json", "r") as f:
            self.settings = json.load(f)


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, window_dimensions, **kwargs):
        super().__init__(master, **kwargs)

        self.geometry = window_dimensions

        config = SettingsManager()

        self.settings_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.settings_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.exclude_chars_label = ctk.CTkLabel(
            self, text="Characters to exclude:", anchor="w"
        )
        self.exclude_chars_label.grid(row=1, column=0, padx=20, pady=10)
        self.exclude_chars = ctk.CTkEntry(self)
        self.exclude_chars.grid(row=2, column=0, padx=20)

        self.appearance_mode_label = ctk.CTkLabel(
            self, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            anchor="center",
        )
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=20)

        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=10)
        self.scaling_optionmenu = ctk.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
            anchor="center",
        )
        self.scaling_optionmenu.grid(row=6, column=0, padx=20)

        self.save_settings_button = ctk.CTkButton(
            self,
            text="Save Settings",
            anchor="center",
            command=self.save_settings_event,
        )
        self.save_settings_button.grid(row=8, column=0, padx=20, pady=(10, 20))

        """
        ----------------------------------------
        Load default or stored settings from file
        ----------------------------------------
        """
        # Set default values
        # self.appearance_mode_optionmenu.set("Dark")
        # self.scaling_optionmenu.set("100%")

        config.load_settings()

        # Insert stored characters that are to be excluded into entry field
        self.exclude_chars.delete(0, "end")
        self.exclude_chars.insert(0, config.settings["exclude_chars"])

        self.appearance_mode_optionmenu.set(config.settings["appearance_mode"])
        ctk.set_appearance_mode(config.settings["appearance_mode"])

        self.scaling_optionmenu.set(config.settings["scaling"])
        scaling = int(config.settings["scaling"].replace("%", "")) / 100
        ctk.set_widget_scaling(scaling)

    """
    ----------------------------------------
    Function definitions
    ----------------------------------------
    """

    # Taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # Initial function taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
    def change_scaling_event(self, new_scaling: str):
        if new_scaling == "80%":
            self.geometry("934x485")
        elif new_scaling == "90%":
            self.geometry("1026x540")
        elif new_scaling == "100%":
            self.geometry("1146x598")
        elif new_scaling == "110%":
            self.geometry("1256x654")
        elif new_scaling == "120%":
            self.geometry("1372x714")
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def save_settings_event(self):
        new_config = SettingsManager()
        new_config.settings = {
            "exclude_chars": self.exclude_chars.get(),
            "appearance_mode": self.appearance_mode_optionmenu.get(),
            "scaling": self.scaling_optionmenu.get(),
        }
        new_config.save_settings()

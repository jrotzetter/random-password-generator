# import tkinter
import customtkinter as ctk
import secrets
import string
# from CTkToolTip import * # appearance transitions don't change background of tooltip. See issues: #22 and #33
# https://github.com/Akascape/CTkToolTip/issues/22
# https://github.com/Akascape/CTkToolTip/issues/33
from ctk_IntSpinbox import IntSpinbox
from settings_manager import SettingsManager
import webbrowser
from CTkMenuBar import CTkMenuBar
from CTkMessagebox import CTkMessagebox

# ctk.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        config = SettingsManager()

        # Create app frame
        self.center_window(1080, 480)
        # self.geometry("720x480")
        self.title("Random Password Generator")
        self.minsize(500, 350)

        
        """
        ----------------------------------------
        Define the menu bar
        ----------------------------------------
        """
        menu = CTkMenuBar(self)
        menu.grid(row=0, column=0, sticky="new", columnspan=2)
        menu.add_cascade("About", command=self.show_about)
        menu.add_cascade("Check Github for updates", command=self.check_updates)
        menu.add_cascade("Exit", command=self.ask_exit)


        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        

        """
        ----------------------------------------
        Define the sidebar "Settings" frame
        ----------------------------------------
        """
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.settings_label = ctk.CTkLabel(self.sidebar_frame, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.exclude_chars_label = ctk.CTkLabel(self.sidebar_frame, text="Characters to exclude:", anchor="w")
        self.exclude_chars_label.grid(row=1, column=0, padx=20, pady=10)
        self.exclude_chars = ctk.CTkEntry(self.sidebar_frame)
        self.exclude_chars.grid(row=2, column=0, padx=20)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=20)

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=10)
        self.scaling_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=6, column=0, padx=20)

        self.save_settings_button = ctk.CTkButton(self.sidebar_frame, text="Save Settings", anchor="w", command=self.save_settings_event)
        self.save_settings_button.grid(row=8, column=0, padx=20, pady=(10, 20))

        
        """
        ----------------------------------------
        Define the "password length" frame
        ----------------------------------------
        """
        self.input_frame = ctk.CTkFrame(self, width=350, height=40)
        self.input_frame.grid(row=1, column=1, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame_title = ctk.CTkLabel(self.input_frame, text="Desired password length?", font=ctk.CTkFont(weight='bold'))
        self.input_frame_title.grid(row=0, padx=10)
        
        self.spinbox = IntSpinbox(self.input_frame, width=150, step_size=1)
        self.spinbox.grid(row=1, column=0, padx=10, pady=10)


        """
        ----------------------------------------
        Define the "Options" slider frame
        ----------------------------------------
        """
        slider_font = ctk.CTkFont(size=14, weight='bold')

        self.options_frame = ctk.CTkFrame(self, width=350, height=40)
        self.options_frame.grid(row=2, column=1)
        self.options_frame_title = ctk.CTkLabel(self.options_frame, text="Options", bg_color='transparent', font=ctk.CTkFont(weight='bold'))
        self.options_frame_title.grid(columnspan=3)

        self.special_chars = ctk.CTkLabel(self.options_frame, text="Number of special characters:")
        self.special_chars.grid(row=1, column=0)
        self.slider_special_chars = ctk.CTkSlider(self.options_frame, from_=0, to=10, number_of_steps=10, command=lambda value: self.show_value(value, slider=self.slider_special_chars))
        self.slider_special_chars.grid(row=3, column=0, padx=(20, 10), pady=(5, 10), sticky="ew")
        self.slider_special_chars.set(2)
        # self.tooltip_special_chars = CTkToolTip(self.slider_special_chars, message="2", corner_radius=9, bg_color="gray50")
        self.special_chars_label = ctk.CTkLabel(self.options_frame, text=int(self.slider_special_chars.get()), font=slider_font, corner_radius=8, fg_color="gray50", width=35)
        self.special_chars_label.grid(row=2, column=0)

        self.upper_chars = ctk.CTkLabel(self.options_frame, text="Number of uppercase letters:")
        self.upper_chars.grid(row=1, column=1)
        self.slider_upper_chars = ctk.CTkSlider(self.options_frame, from_=0, to=10, number_of_steps=10, command=lambda value: self.show_value(value, slider=self.slider_upper_chars))
        self.slider_upper_chars.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_upper_chars.set(2)
        # self.tooltip_upper_chars = CTkToolTip(self.slider_upper_chars, message="2", corner_radius=9)
        self.upper_case_label = ctk.CTkLabel(self.options_frame, text=int(self.slider_upper_chars.get()), font=slider_font, corner_radius=8, fg_color="gray50", width=35)
        self.upper_case_label.grid(row=2, column=1)

        self.digits = ctk.CTkLabel(self.options_frame, text="Number of digits:")
        self.digits.grid(row=1, column=2)
        self.slider_digits = ctk.CTkSlider(self.options_frame, from_=0, to=10, number_of_steps=10, command=lambda value: self.show_value(value, slider=self.slider_digits))
        self.slider_digits.grid(row=3, column=2, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_digits.set(2)
        # self.tooltip_digits = CTkToolTip(self.slider_digits, message="2", corner_radius=9)
        self.digits_label = ctk.CTkLabel(self.options_frame, text=int(self.slider_digits.get()), font=slider_font, corner_radius=8, fg_color="gray50", width=35)
        self.digits_label.grid(row=2, column=2)


        """
        ----------------------------------------
        Define the generated password frame
        ----------------------------------------
        """
        self.pw_frame = ctk.CTkFrame(self, border_color=None, border_width=0, bg_color='transparent')
        self.pw_frame.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
        self.pw_frame.grid_columnconfigure(0, weight=1)
        self.pw_frame_title = ctk.CTkLabel(self.pw_frame, text="Generated password", font=ctk.CTkFont(weight='bold'), bg_color='transparent')
        self.pw_frame_title.grid(row=0, column=0)

        # Entry box for returned password
        self.pw_entry = ctk.CTkEntry(self.pw_frame, placeholder_text=None, border_width=0, bg_color='transparent', font=("consolas", 18), justify='center')
        self.pw_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        
        """
        ----------------------------------------
        Define the lower buttons frame
        ----------------------------------------
        """
        self.button_frame = ctk.CTkFrame(self, width=350, height=40)
        self.button_frame.grid(row=4, column=1, pady=10)
        self.button_frame.columnconfigure((0, 1), weight=1)

        # 'Generate password' button
        self.pw_button = ctk.CTkButton(self.button_frame, text="Generate new password", command=self.generate_password)
        self.pw_button.grid(row=0, column=0, padx=10, pady=10)

        # 'Copy to clipboard' button
        self.cp_button = ctk.CTkButton(self.button_frame, text="Copy To Clipboard", command=self.cp_clipboard)
        self.cp_button.grid(row=0, column=1, padx=10)

        
        """
        ----------------------------------------
        Load default or stored settings from file
        ----------------------------------------
        """
        # Set default values
        # self.appearance_mode_optionmenu.set("Dark")
        # self.scaling_optionmenu.set("100%")

        # Load stored settings
        config.load_settings()

        # Insert stored characters that are to be excluded into entry field
        self.exclude_chars.delete(0, 'end')
        self.exclude_chars.insert(0, config.settings["exclude_chars"])

        self.appearance_mode_optionmenu.set(config.settings["appearance_mode"])
        ctk.set_appearance_mode(config.settings["appearance_mode"])
        
        self.scaling_optionmenu.set(config.settings["scaling"])
        scaling = int(config.settings["scaling"].replace("%","")) / 100
        ctk.set_widget_scaling(scaling)


    """
    ----------------------------------------
    Function definitions
    ----------------------------------------
    """
    def center_window(self, windowWidth, windowHeight):
        # Get screen width and height
        widthScreen = self.winfo_screenwidth()
        heightScreen = self.winfo_screenheight()

        # Calculate x and y coordinates for the main window
        x = (widthScreen/2) - (windowWidth/2)
        y = (heightScreen/2) - (windowHeight/2)

        # Set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))

    def show_value(self, value, slider):
        if slider == self.slider_special_chars:
            # self.tooltip_special_chars.configure(message=str(int(value)))
            self.special_chars_label.configure(text=int(value))
        elif slider == self.slider_upper_chars:
            # self.tooltip_upper_chars.configure(message=str(int(value)))
            self.upper_case_label.configure(text=int(value))
        elif slider == self.slider_digits:
            # self.tooltip_digits.configure(message=str(int(value)))
            self.digits_label.configure(text=int(value))

    def generate_password(self):
        # Clear entry box
        self.pw_entry.delete(0, 'end')

        # Get password length
        pw_length = int(self.spinbox.get())

        if (pw_length < 8):
            # tkinter.messagebox.showwarning("Warning", "Password must be at least 8 characters long!")
            CTkMessagebox(title="Warning", message="Password must be at least 8 characters long!", icon="warning")
            return
        
        special_req = int(self.slider_special_chars.get())
        upper_req = int(self.slider_upper_chars.get())
        digit_req = int(self.slider_digits.get())

        pw_req = sum((special_req, upper_req, digit_req))

        if (pw_length <= pw_req):
            # tkinter.messagebox.showwarning("Warning", 'Password length is too short to meet all conditions set in "Options"!')
            CTkMessagebox(title="Error",
                          message='Password length is too short to meet all conditions set in "Options"!',
                          icon="cancel",
                          option_1="OK")
            return

        # Partially based on Steve Gibson's "Perfect Paper Password" system https://www.grc.com/ppp.htm
        special_characters = '!"#$%&\'()*+,-./:;<=>?@[]^_{|}~'

        glyphs = string.ascii_letters + string.digits + special_characters

        chars_to_remove  = self.exclude_chars.get()
        if (chars_to_remove != ""):
            glyphs = glyphs.translate(str.maketrans('', '', chars_to_remove))
            if (not any(c.islower() for c in glyphs) or
                not any(c.isupper() for c in glyphs) or
                not any(c in special_characters for c in glyphs) or
                sum(c.isdigit() for c in glyphs) < 1):
                # tkinter.messagebox.showwarning("Warning", 'Too many characters have been excluded!')
                CTkMessagebox(title="Error", message='Too many characters have been excluded!', icon="cancel")
                return
        
        # # Generate an alphanumeric password of lenght pw_length with at least
        # # one lowercase character, at least one uppercase character, at least
        # # one special character and at least three digits
        # while True: 
        #     password = ''.join(secrets.choice(glyphs) for i in range(pw_length))
        #     if (any(c.islower() for c in password) and any(c.isupper()
        #     for c in password) and any(c in special_characters for c in password) and sum(c.isdigit() for c in password) >= 3):
        #         print(password) 
        #         break
        while True: 
            password = ''.join(secrets.choice(glyphs) for i in range(pw_length))
            min_criteria_met = (
                sum(c.isupper() for c in password) == upper_req and 
                sum(c in special_characters for c in password) == special_req and 
                sum(c.isdigit() for c in password) == digit_req)
            
            if (any(c.islower() for c in password) and min_criteria_met):
                print(password)
                break
        
        # Output password to screen
        self.pw_entry.insert(0, password)

    def cp_clipboard(self):
        # Clear clipboard
        self.clipboard_clear()
        # Copy to clipboard
        self.clipboard_append(self.pw_entry.get())

    # Taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # Taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def save_settings_event(self):
        new_config = SettingsManager()
        new_config.settings = {
            "exclude_chars": self.exclude_chars.get(),
            "appearance_mode": self.appearance_mode_optionmenu.get(),
            "scaling": self.scaling_optionmenu.get()
        }
        new_config.save_settings()
    
    def show_about(self):
        # tkinter.messagebox.showinfo(title="About", message="Random Password Generator\n \nAuthor: jrotzetter \nVersion: 1.0 \nLicense: MIT")
        CTkMessagebox(self, title="About", message="Random Password Generator\n \nAuthor: jrotzetter \nVersion: 1.0 \nLicense: MIT", icon="info")

    def check_updates(self):
        url = "https://github.com/jrotzetter/random-password-generator"
        webbrowser.open(url,new=1)

    def ask_exit(self):
        # answer = tkinter.messagebox.askokcancel(title="Exit?", message="Are you sure you wish to close the program?")
        # if answer:
            # self.destroy()
        selected_option = CTkMessagebox(title="Exit?", message="Are you sure you wish to close the program?",
                        icon="question", option_1="Cancel", option_3="Yes")
        answer = selected_option.get()
        if answer=="Yes":
            self.destroy()


# Run app
if __name__ == "__main__":
    app = App()
    # app.eval('tk::PlaceWindow . center')
    app.mainloop()
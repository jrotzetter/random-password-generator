import customtkinter as ctk
import secrets
import string
from sidebar_frame import SidebarFrame
from options_frame import OptionsFrame
import webbrowser
import CTkMenuBar as ctkmbar
import CTkMessagebox as ctkmbx
import CTkToolTip as ctktltp  # appearance transitions don't change background
# of tooltip in v0.8. See issues: #22 and #33
# https://github.com/Akascape/CTkToolTip/issues/22
# https://github.com/Akascape/CTkToolTip/issues/33


# ctk.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.MAX_PW_LENGTH = 100
        self.NUM_CHAR_SETS = 4
        self.CHAR_SET_LENGTH = self.MAX_PW_LENGTH / self.NUM_CHAR_SETS

        # Create app frame
        self.center_window(1140, 520)
        # self.geometry("720x480")
        self.title("Random Password Generator")
        self.minsize(900, 432)

        self.grid_columnconfigure(1, weight=1)  # center first column
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)  # space out rows for fullscreen

        """
        ----------------------------------------
        Define the menu bar
        ----------------------------------------
        """
        menu = ctkmbar.CTkMenuBar(self)
        menu.grid(row=0, column=0, sticky="new", columnspan=2)
        menu.add_cascade("About", command=self.show_about)
        menu.add_cascade("Check Github for updates", command=self.check_updates)
        menu.add_cascade("Exit", command=self.ask_exit)

        """
        ----------------------------------------
        Define the sidebar "Settings" frame
        ----------------------------------------
        """
        self.sidebar_frame = SidebarFrame(
            self, window_dimensions=self.geometry, width=140, corner_radius=0
        )
        self.sidebar_frame.grid(row=1, column=0, rowspan=5, sticky="news")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        """
        ----------------------------------------
        Define the "Password length" and "Options" slider frames
        ----------------------------------------
        """
        self.pw_options = OptionsFrame(
            self, char_set_len=self.CHAR_SET_LENGTH, fg_color="transparent"
        )
        self.pw_options.grid(row=1, column=1, pady=10)
        self.pw_options.grid_columnconfigure(0, weight=1)

        """
        ----------------------------------------
        Define the randomizer buttons frame
        ----------------------------------------
        """
        self.randomizer_frame = ctk.CTkFrame(self)
        self.randomizer_frame.grid(row=2, column=1, pady=10)
        self.randomizer_frame.columnconfigure((0, 1, 2), weight=1)

        # 'Generate password' button
        self.pw_button = ctk.CTkButton(
            self.randomizer_frame,
            text="Generate password",
            command=self.generate_password,
        )
        self.pw_button.grid(row=0, column=0, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.pw_button,
            message="Generate password with current values",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
            border_width=2,
        )

        # 'Randomize' button
        self.randomize_button = ctk.CTkButton(
            self.randomizer_frame, text="Randomize", command=self.randomize
        )
        self.randomize_button.grid(row=0, column=1, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.randomize_button,
            message="Randomize sliders within current password length",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
            border_width=2,
        )

        # 'Randomize All' button
        self.randomize_all_button = ctk.CTkButton(
            self.randomizer_frame,
            text="Randomize All",
            command=self.randomize_all,
        )
        self.randomize_all_button.grid(row=0, column=3, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.randomize_all_button,
            message="Randomize sliders and password length",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
            border_width=2,
        )

        """
        ----------------------------------------
        Define the generated password frame
        ----------------------------------------
        """
        self.pw_frame = ctk.CTkFrame(
            self, border_color=None, border_width=0, bg_color="transparent"
        )
        self.pw_frame.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        self.pw_frame.grid_columnconfigure(0, weight=1)
        self.pw_frame_title = ctk.CTkLabel(
            self.pw_frame,
            text="Generated password",
            font=ctk.CTkFont(weight="bold"),
            bg_color="transparent",
        )
        self.pw_frame_title.grid(row=0, column=0)

        # Entry box for returned password
        self.pw_entry = ctk.CTkEntry(
            self.pw_frame,
            placeholder_text=None,
            border_width=0,
            bg_color="transparent",
            font=("consolas", 18),
            justify="center",
        )
        self.pw_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        """
        ----------------------------------------
        Define the "Copy to clipboard" button frame
        ----------------------------------------
        """
        self.button_frame = ctk.CTkFrame(self, width=350, height=40)
        self.button_frame.grid(row=4, column=1, pady=10)
        self.button_frame.columnconfigure((0, 1), weight=1)

        # 'Copy to clipboard' button
        self.cp_button = ctk.CTkButton(
            self.button_frame, text="Copy to clipboard", command=self.cp_clipboard
        )
        self.cp_button.grid(row=0, column=1, padx=10, pady=10)

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
        x = (widthScreen / 2) - (windowWidth / 2)
        y = (heightScreen / 2) - (windowHeight / 2)

        # Set the dimensions of the app window and where it is placed
        self.geometry("%dx%d+%d+%d" % (windowWidth, windowHeight, x, y))

    def show_about(self):
        ctkmbx.CTkMessagebox(
            self,
            title="About",
            message="Random Password Generator\n \nAuthor: jrotzetter \nVersion: 1.1.0 \nLicense: MIT",
            icon="info",
        )

    def check_updates(self):
        url = "https://github.com/jrotzetter/random-password-generator"

        selected_option = ctkmbx.CTkMessagebox(
            title="Check for updates?",
            message="Do you wish to check the Github repository for updates in a...",
            icon="question",
            option_1="Cancel",
            option_2="...new browser tab?",
            option_3="...new browser window?",
            width=600,
            option_focus=1,  # select option 1 by default when Enter key is pressed
        )
        answer = selected_option.get()
        if answer == "...new browser window?":
            webbrowser.open(url, new=1)
        elif answer == "...new browser tab?":
            webbrowser.open(url, new=2)

    def ask_exit(self):
        selected_option = ctkmbx.CTkMessagebox(
            title="Exit?",
            message="Are you sure you wish to close the program?",
            icon="question",
            option_1="Cancel",
            option_3="Yes",
            option_focus=1,
        )
        answer = selected_option.get()
        if answer == "Yes":
            self.destroy()

    def generate_password(self):
        def exclude_chars_set(chars_set, exclude_set):
            new_chars_set = chars_set.translate(str.maketrans("", "", exclude_set))
            return new_chars_set

        # Clear entry box
        self.pw_entry.delete(0, "end")

        # Get password length
        # pw_length = int(self.pw_length_label.cget("text"))
        pw_length = int(self.pw_options.pw_length_label.cget("text"))

        if pw_length < 8:
            ctkmbx.CTkMessagebox(
                title="Warning",
                message="Password must be at least 8 characters long!",
                icon="warning",
            )
            return

        # Get slider values
        special_req = int(self.pw_options.slider_special_chars.get())
        lower_req = int(self.pw_options.slider_lower_chars.get())
        upper_req = int(self.pw_options.slider_upper_chars.get())
        digit_req = int(self.pw_options.slider_digits.get())

        # Partially based on Steve Gibson's "Perfect Paper Password" system https://www.grc.com/ppp.htm
        special_chars = "!\"#$%&'()*+,-./:;<=>?@[]^_{|}~"
        lower_chars = string.ascii_lowercase
        upper_chars = string.ascii_uppercase
        digit_chars = string.digits

        chars_to_remove = self.sidebar_frame.exclude_chars.get()
        # If there are characters to exclude, remove them from their respective
        # character set before checking that none of them are completely empty after
        if chars_to_remove != "":
            special_chars = exclude_chars_set(special_chars, chars_to_remove)
            lower_chars = exclude_chars_set(string.ascii_lowercase, chars_to_remove)
            upper_chars = exclude_chars_set(string.ascii_uppercase, chars_to_remove)
            digit_chars = exclude_chars_set(string.digits, chars_to_remove)
            if "" in [special_chars, lower_chars, upper_chars, digit_chars]:
                ctkmbx.CTkMessagebox(
                    title="Error",
                    message="One or more complete character sets have been excluded!",
                    icon="cancel",
                )
                return

        # Individually add the required number of characters per set
        pass_list = []
        pass_list += [secrets.choice(special_chars) for _ in range(special_req)]
        pass_list += [secrets.choice(lower_chars) for _ in range(lower_req)]
        pass_list += [secrets.choice(upper_chars) for _ in range(upper_req)]
        pass_list += [secrets.choice(digit_chars) for _ in range(digit_req)]
        # Randomly shuffle the entire character list, then combine into a single string
        secrets.SystemRandom().shuffle(pass_list)
        password = "".join(pass_list)

        # Output password to screen
        self.pw_entry.insert(0, password)

    def randsum(self, sum_limit: int, values: int, value_limit: int):
        # Function to get a list of n='values' random numbers, which are all below or
        # equal to 'value_limit' and the sum of the list does not exceed 'sum_limit'

        upper_lim = int(value_limit + 1)

        # Generate a first batch of values
        nums = [secrets.randbelow(upper_lim) for _ in range(values)]

        # Filter out the numbers that cause the total sum to exceed the limit
        while sum(nums) != sum_limit:
            # Replace one of the numbers with a new random number,
            # hoping it reduces the total sum enough
            i = secrets.randbelow(len(nums))
            new_num = secrets.randbelow(upper_lim)
            while new_num > value_limit:
                new_num = secrets.randbelow(upper_lim)
            nums[i] = new_num
        return nums

    def randomize_sliders(self, pw_length):
        random_values = self.randsum(
            pw_length, self.NUM_CHAR_SETS, self.CHAR_SET_LENGTH
        )
        self.pw_options.slider_special_chars.set(random_values[0])
        self.pw_options.slider_lower_chars.set(random_values[1])
        self.pw_options.slider_upper_chars.set(random_values[2])
        self.pw_options.slider_digits.set(random_values[3])

        for value, slider in [
            (random_values[0], self.pw_options.slider_special_chars),
            (random_values[1], self.pw_options.slider_lower_chars),
            (random_values[2], self.pw_options.slider_upper_chars),
            (random_values[3], self.pw_options.slider_digits),
        ]:
            self.pw_options.show_value(value, slider)
        self.generate_password()

    def randomize(self):
        current_pw_length = int(self.pw_options.pw_length_label.cget("text"))
        self.randomize_sliders(current_pw_length)

    def randomize_all(self):
        random_pw_length = secrets.SystemRandom().randint(8, self.MAX_PW_LENGTH)
        self.randomize_sliders(random_pw_length)

    def cp_clipboard(self):
        # Clear clipboard
        self.clipboard_clear()
        # Copy to clipboard
        self.clipboard_append(self.pw_entry.get())


# Run app
if __name__ == "__main__":
    app = App()
    # app.eval('tk::PlaceWindow . center')
    app.mainloop()

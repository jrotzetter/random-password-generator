import customtkinter as ctk
import secrets
import string
import CTkMessagebox as ctkmbx
import CTkToolTip as ctktltp  # appearance transitions don't change background
# of tooltip in v0.8. See issues: #22 and #33
# https://github.com/Akascape/CTkToolTip/issues/22
# https://github.com/Akascape/CTkToolTip/issues/33


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master, char_set_len, **kwargs):
        super().__init__(master, **kwargs)

        self.char_set_len = char_set_len

        """
        ----------------------------------------
        Define the "Password length" frame
        ----------------------------------------
        """
        self.pwd_length_frame = ctk.CTkFrame(self, width=350, height=40)
        self.pwd_length_frame.grid(row=1, column=1, pady=10)

        self.pwd_length_frame_title = ctk.CTkLabel(
            self.pwd_length_frame,
            text="Password length",
            font=ctk.CTkFont(weight="bold"),
        )
        self.pwd_length_frame_title.grid(row=0, column=0, padx=10)

        self.pwd_length_label = ctk.CTkLabel(
            self.pwd_length_frame,
            text="8",
            corner_radius=8,
            fg_color="gray50",
            width=48,
            font=ctk.CTkFont(weight="bold", size=16),
        )
        self.pwd_length_label.grid(row=1, column=0, padx=10, pady=(0, 10))

        """
        ----------------------------------------
        Define the "Options" slider frame
        ----------------------------------------
        """
        slider_font = ctk.CTkFont(size=14, weight="bold")

        self.options_frame = ctk.CTkFrame(self, width=350, height=40)
        self.options_frame.grid(row=2, column=1, pady=10, padx=10)
        self.options_frame_title = ctk.CTkLabel(
            self.options_frame,
            text="Options",
            bg_color="transparent",
            font=ctk.CTkFont(weight="bold"),
        )
        self.options_frame_title.grid(columnspan=4)

        """
        Special characters
        """
        self.special_chars = ctk.CTkLabel(
            self.options_frame, text="Number of special characters:"
        )
        self.special_chars.grid(row=1, column=0)
        self.slider_special_chars = ctk.CTkSlider(
            self.options_frame,
            from_=0,
            to=self.char_set_len,
            number_of_steps=self.char_set_len,
            command=lambda value: self.show_value(
                value, slider=self.slider_special_chars
            ),
        )
        self.slider_special_chars.grid(
            row=3, column=0, padx=(20, 10), pady=(10, 20), sticky="ew"
        )
        self.slider_special_chars.set(2)
        self.special_chars_label = ctk.CTkLabel(
            self.options_frame,
            text=int(self.slider_special_chars.get()),
            font=slider_font,
            corner_radius=8,
            fg_color="gray50",
            width=35,
        )
        self.special_chars_label.grid(row=2, column=0)

        """
        Lowercase characters
        """
        self.lower_chars = ctk.CTkLabel(
            self.options_frame, text="Number of lowercase letters:"
        )
        self.lower_chars.grid(row=1, column=1)
        self.slider_lower_chars = ctk.CTkSlider(
            self.options_frame,
            from_=0,
            to=self.char_set_len,
            number_of_steps=self.char_set_len,
            command=lambda value: self.show_value(
                value, slider=self.slider_lower_chars
            ),
        )
        self.slider_lower_chars.grid(
            row=3, column=1, padx=(20, 10), pady=(10, 20), sticky="ew"
        )
        self.slider_lower_chars.set(2)
        self.lower_chars_label = ctk.CTkLabel(
            self.options_frame,
            text=int(self.slider_lower_chars.get()),
            font=slider_font,
            corner_radius=8,
            fg_color="gray50",
            width=35,
        )
        self.lower_chars_label.grid(row=2, column=1)

        """
        Uppercase characters
        """
        self.upper_chars = ctk.CTkLabel(
            self.options_frame, text="Number of uppercase letters:"
        )
        self.upper_chars.grid(row=1, column=2)
        self.slider_upper_chars = ctk.CTkSlider(
            self.options_frame,
            from_=0,
            to=self.char_set_len,
            number_of_steps=self.char_set_len,
            command=lambda value: self.show_value(
                value, slider=self.slider_upper_chars
            ),
        )
        self.slider_upper_chars.grid(
            row=3, column=2, padx=(20, 10), pady=(10, 20), sticky="ew"
        )
        self.slider_upper_chars.set(2)
        self.upper_chars_label = ctk.CTkLabel(
            self.options_frame,
            text=int(self.slider_upper_chars.get()),
            font=slider_font,
            corner_radius=8,
            fg_color="gray50",
            width=35,
        )
        self.upper_chars_label.grid(row=2, column=2)

        """
        Digits
        """
        self.digits = ctk.CTkLabel(self.options_frame, text="Number of digits:")
        self.digits.grid(row=1, column=3)
        self.slider_digits = ctk.CTkSlider(
            self.options_frame,
            from_=0,
            to=self.char_set_len,
            number_of_steps=self.char_set_len,
            command=lambda value: self.show_value(value, slider=self.slider_digits),
        )
        self.slider_digits.grid(
            row=3, column=3, padx=(20, 10), pady=(10, 20), sticky="ew"
        )
        self.slider_digits.set(2)
        self.digits_label = ctk.CTkLabel(
            self.options_frame,
            text=int(self.slider_digits.get()),
            font=slider_font,
            corner_radius=8,
            fg_color="gray50",
            width=35,
        )
        self.digits_label.grid(row=2, column=3)

    def show_value(self, value, slider):
        # Function to update displayed slider values and password length
        if slider == self.slider_special_chars:
            self.special_chars_label.configure(text=int(value))
        elif slider == self.slider_lower_chars:
            self.lower_chars_label.configure(text=int(value))
        elif slider == self.slider_upper_chars:
            self.upper_chars_label.configure(text=int(value))
        elif slider == self.slider_digits:
            self.digits_label.configure(text=int(value))

        special_req = int(self.slider_special_chars.get())
        lower_req = int(self.slider_lower_chars.get())
        upper_req = int(self.slider_upper_chars.get())
        digit_req = int(self.slider_digits.get())

        pwd_req = sum((special_req, lower_req, upper_req, digit_req))
        self.pwd_length_label.configure(text=int(pwd_req))


class RandomPassword(ctk.CTkFrame):
    def __init__(self, master, sidebar, **kwargs):
        super().__init__(master, **kwargs)

        self.sidebar_frame = sidebar

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)  # space out rows for fullscreen

        self.MAX_PWD_LENGTH = 100
        self.NUM_CHAR_SETS = 4
        self.CHAR_SET_LENGTH = self.MAX_PWD_LENGTH / self.NUM_CHAR_SETS

        """
        ----------------------------------------
        Define the "Password length" and "Options" slider frames
        ----------------------------------------
        """
        self.pwd_options = OptionsFrame(self, char_set_len=self.CHAR_SET_LENGTH)
        self.pwd_options.grid(row=1, column=1, pady=10)

        """
        ----------------------------------------
        Define the randomizer buttons frame
        ----------------------------------------
        """
        self.randomizer_frame = ctk.CTkFrame(self)
        self.randomizer_frame.grid(row=2, column=1, pady=10)

        # 'Generate password' button
        self.pwd_button = ctk.CTkButton(
            self.randomizer_frame,
            text="Generate password",
            command=self.generate_password,
        )
        self.pwd_button.grid(row=0, column=0, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.pwd_button,
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
        self.pwd_frame = ctk.CTkFrame(
            self, border_color=None, border_width=0, bg_color="transparent"
        )
        self.pwd_frame.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        self.pwd_frame.grid_columnconfigure(0, weight=1)
        self.pwd_frame_title = ctk.CTkLabel(
            self.pwd_frame,
            text="Generated password",
            font=ctk.CTkFont(weight="bold"),
            bg_color="transparent",
        )
        self.pwd_frame_title.grid(row=0, column=0)

        # Entry box for returned password
        self.pwd_entry = ctk.CTkEntry(
            self.pwd_frame,
            placeholder_text=None,
            border_width=0,
            bg_color="transparent",
            font=("consolas", 18),
            justify="center",
        )
        self.pwd_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

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

    def generate_password(self):
        def exclude_chars_set(chars_set, exclude_set):
            new_chars_set = chars_set.translate(str.maketrans("", "", exclude_set))
            return new_chars_set

        # Clear entry box
        self.pwd_entry.delete(0, "end")

        # Get password length
        pwd_length = int(self.pwd_options.pwd_length_label.cget("text"))

        if pwd_length < 8:
            ctkmbx.CTkMessagebox(
                title="Warning",
                message="Password must be at least 8 characters long!",
                icon="warning",
            )
            return

        # Get slider values
        special_req = int(self.pwd_options.slider_special_chars.get())
        lower_req = int(self.pwd_options.slider_lower_chars.get())
        upper_req = int(self.pwd_options.slider_upper_chars.get())
        digit_req = int(self.pwd_options.slider_digits.get())

        # Special characters partially based on Steve Gibson's
        # "Perfect Paper Password" system https://www.grc.com/ppp.htm
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
        self.pwd_entry.insert(0, password)

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

    def randomize_sliders(self, pwd_length):
        random_values = self.randsum(
            pwd_length, self.NUM_CHAR_SETS, self.CHAR_SET_LENGTH
        )
        self.pwd_options.slider_special_chars.set(random_values[0])
        self.pwd_options.slider_lower_chars.set(random_values[1])
        self.pwd_options.slider_upper_chars.set(random_values[2])
        self.pwd_options.slider_digits.set(random_values[3])

        for value, slider in [
            (random_values[0], self.pwd_options.slider_special_chars),
            (random_values[1], self.pwd_options.slider_lower_chars),
            (random_values[2], self.pwd_options.slider_upper_chars),
            (random_values[3], self.pwd_options.slider_digits),
        ]:
            self.pwd_options.show_value(value, slider)
        self.generate_password()

    def randomize(self):
        current_pwd_length = int(self.pwd_options.pwd_length_label.cget("text"))
        self.randomize_sliders(current_pwd_length)

    def randomize_all(self):
        random_pwd_length = secrets.SystemRandom().randint(8, self.MAX_PWD_LENGTH)
        self.randomize_sliders(random_pwd_length)

    def cp_clipboard(self):
        # Clear clipboard
        self.clipboard_clear()
        # Copy to clipboard
        self.clipboard_append(self.pwd_entry.get())

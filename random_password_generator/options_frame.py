import customtkinter as ctk


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master, char_set_len, **kwargs):
        super().__init__(master, **kwargs)

        self.char_set_len = char_set_len

        """
        ----------------------------------------
        Define the "Password length" frame
        ----------------------------------------
        """
        self.pw_length_frame = ctk.CTkFrame(self, width=350, height=40)
        self.pw_length_frame.grid(row=1, column=1, pady=10)
        self.pw_length_frame.grid_columnconfigure(0, weight=1)
        self.pw_length_frame_title = ctk.CTkLabel(
            self.pw_length_frame,
            text="Password length",
            font=ctk.CTkFont(weight="bold"),
        )
        self.pw_length_frame_title.grid(row=0, column=0, padx=10)

        self.pw_length_label = ctk.CTkLabel(
            self.pw_length_frame,
            text="8",
            corner_radius=8,
            fg_color="gray50",
            width=48,
            font=ctk.CTkFont(weight="bold", size=16),
        )
        self.pw_length_label.grid(row=1, column=0, padx=10, pady=(0, 10))

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

        pw_req = sum((special_req, lower_req, upper_req, digit_req))
        self.pw_length_label.configure(text=int(pw_req))

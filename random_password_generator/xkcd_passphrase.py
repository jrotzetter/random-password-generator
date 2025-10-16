import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import secrets
import os
import re
import CTkMessagebox as ctkmbx
import CTkToolTip as ctktltp

# Get the directory path for the file currently being executed
# to make it independent from current working directory
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))


class XKCDPassphrase(ctk.CTkFrame):
    def __init__(self, master, sidebar, **kwargs):
        super().__init__(master, **kwargs)

        self.sidebar_frame = sidebar

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 4, 5, 6), weight=1)

        """
        ----------------------------------------
        Define the "wordlist" frame
        ----------------------------------------
        """
        self.selected_wordlist = MAIN_DIR + "/5000-more-common.txt"

        self.wordlist_frame = ctk.CTkFrame(self)
        self.wordlist_frame.grid(row=0, column=0, pady=10)

        self.wordlist_button = ctk.CTkButton(
            self.wordlist_frame,
            text="Select Wordlist",
            command=self.select_wordlist,
            width=175,
        )
        self.wordlist_button.grid(row=0, column=0, padx=10, pady=10)

        self.selected_wordlist_name = ctk.CTkLabel(
            self.wordlist_frame,
            text="Default Wordlist",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
        )
        self.selected_wordlist_name.grid(row=1, column=0, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.wordlist_button,
            "Note: Selected file should contain one word per line",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
            border_width=2,
            delay=0,
        )

        """
        ----------------------------------------
        Define the "Words" slider frame
        ----------------------------------------
        """
        self.words_frame = ctk.CTkFrame(self)
        self.words_frame.grid(row=1, column=0)

        self.num_words = tk.IntVar()

        self.words = ctk.CTkLabel(self.words_frame, text="Number of words:")
        self.words.grid(row=1, column=0)
        self.slider_words = ctk.CTkSlider(
            self.words_frame,
            from_=4,
            to=10,
            number_of_steps=6,
            command=None,
            variable=self.num_words,
        )
        self.slider_words.grid(
            row=3, column=0, padx=(20, 10), pady=(10, 20), sticky="ew"
        )
        self.slider_words.set(4)
        self.words_label = ctk.CTkLabel(
            self.words_frame,
            text=int(self.slider_words.get()),
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            fg_color="gray50",
            width=35,
            textvariable=self.num_words,
        )
        self.words_label.grid(row=2, column=0)

        """
        ----------------------------------------
        Define the "Generate passphrase" frame
        ----------------------------------------
        """
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, pady=10)

        # 'Generate passphrase' button
        self.pphr_button = ctk.CTkButton(
            self.buttons_frame,
            text="Generate passphrase",
            command=self.generate_passphrase,
            width=175,
        )
        self.pphr_button.grid(row=0, column=1, padx=10, pady=10)

        self.initial_passphrase = ""

        self.separator = ctk.CTkOptionMenu(
            self.buttons_frame,
            values=[
                "Whitespace",
                "No Separator",
                "Symbols",
                "Digits",
                "Symbols + Digits",
            ],
            command=self.modify_passphrase,
            anchor="center",
            width=175,
        )
        self.separator.grid(row=0, column=2, padx=10, pady=10)

        ctktltp.CTkToolTip(
            self.separator,
            message=" How should the words be separated?",
            bg_color=("gray86", "gray17"),
            corner_radius=8,
            border_width=2,
        )

        """
        ----------------------------------------
        Define the generated passphrase frame
        ----------------------------------------
        """
        self.pphr_frame = ctk.CTkFrame(
            self, border_color=None, border_width=0, bg_color="transparent"
        )
        self.pphr_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.pphr_frame.grid_columnconfigure(0, weight=1)
        self.pphr_frame_title = ctk.CTkLabel(
            self.pphr_frame,
            text="Generated passphrase",
            font=ctk.CTkFont(weight="bold"),
            bg_color="transparent",
        )
        self.pphr_frame_title.grid(row=0, column=0)

        # Entry box for returned password
        self.pphr_entry = ctk.CTkEntry(
            self.pphr_frame,
            placeholder_text=None,
            border_width=0,
            bg_color="transparent",
            font=("consolas", 18),
            justify="center",
        )
        self.pphr_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        """
        ----------------------------------------
        Define the "Copy to clipboard" button frame
        ----------------------------------------
        """
        self.cp_button_frame = ctk.CTkFrame(self, width=350, height=40)
        self.cp_button_frame.grid(row=6, column=0, pady=10)
        self.cp_button_frame.columnconfigure(0, weight=1)

        # 'Copy to clipboard' button
        self.cp_button = ctk.CTkButton(
            self.cp_button_frame, text="Copy to clipboard", command=self.cp_clipboard
        )
        self.cp_button.grid(row=0, column=0, padx=10, pady=10)

    """
    ----------------------------------------
    Function definitions
    ----------------------------------------
    """

    def select_wordlist(self):
        self.file_path = filedialog.askopenfilename(
            initialdir=".", title="Select a wordlist"
        )
        if self.file_path:
            file = os.path.basename(self.file_path)
            self.selected_wordlist_name.configure(text="Selected file: " + file)
            self.selected_wordlist = self.file_path

    def modify_passphrase(self, selected_separator):
        def exclude_chars_set(chars_set, exclude_set):
            new_chars_set = chars_set.translate(str.maketrans("", "", exclude_set))
            return new_chars_set

        def random_replace(words: str, separator_choice: str):
            # Function to replace every whitespace between words with a different
            # randomly chosen character from separator_choice
            words = words.split(" ")
            result = ""

            separator_choice = exclude_chars_set(
                separator_choice, exclude_set=self.sidebar_frame.exclude_chars.get()
            )
            if len(separator_choice) == 0:
                ctkmbx.CTkMessagebox(
                    title="Error",
                    message="The complete character set has been excluded!",
                    icon="cancel",
                )
                return None
            else:
                for word in words:
                    result += word + secrets.choice(separator_choice)
                return result

        # Clear entry box
        self.pphr_entry.delete(0, "end")

        initial_passphrase = self.initial_passphrase

        if not initial_passphrase == "":
            # Inspired by the Openwall Linux passwdqc toolset
            symbols_separator = "!\"#$%&'()*+,-./:;<=>?@[]^_{|}"
            digits_separator = "0123456789"
            simdig_separator = "!\"#$%&'()*+,-./:;<=>?@[]^_{|}0123456789"

            if selected_separator == "No Separator":
                passphrase = re.sub("\\s", "", initial_passphrase)
            elif selected_separator == "Whitespace":
                passphrase = initial_passphrase
            elif selected_separator == "Symbols":
                passphrase = random_replace(initial_passphrase, symbols_separator)
            elif selected_separator == "Digits":
                passphrase = random_replace(initial_passphrase, digits_separator)
            elif selected_separator == "Symbols + Digits":
                passphrase = random_replace(initial_passphrase, simdig_separator)
            if isinstance(passphrase, str):
                # Output passphrase to screen
                self.pphr_entry.insert(0, passphrase)
            else:
                return

    def generate_passphrase(self):
        # Clear entry box
        self.pphr_entry.delete(0, "end")

        with open(self.selected_wordlist) as f:
            words = [word.strip() for word in f]
            passphrase = " ".join(
                secrets.choice(words) for i in range(int(self.slider_words.get()))
            )
            # Output passphrase to screen
            self.pphr_entry.insert(0, passphrase)
            self.initial_passphrase = passphrase
            self.modify_passphrase(selected_separator=self.separator.get())

    def cp_clipboard(self):
        # Clear clipboard
        self.clipboard_clear()
        # Copy to clipboard
        self.clipboard_append(self.pphr_entry.get())

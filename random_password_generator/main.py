import customtkinter as ctk
from sidebar_frame import SidebarFrame
from random_password import RandomPassword
from xkcd_passphrase import XKCDPassphrase
import webbrowser
import CTkMenuBar as ctkmbar
import CTkMessagebox as ctkmbx

# ctk.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.MAX_PWD_LENGTH = 100
        self.NUM_CHAR_SETS = 4
        self.CHAR_SET_LENGTH = self.MAX_PWD_LENGTH / self.NUM_CHAR_SETS

        # Create app frame
        self.center_window(1145, 598)
        # self.geometry("720x480")
        self.title("Random Password Generator")
        self.minsize(934, 485)

        self.grid_columnconfigure(1, weight=1)  # center first column
        self.grid_rowconfigure(1, weight=1)

        """
        ----------------------------------------
        Define the menu bar
        ----------------------------------------
        """
        menu = ctkmbar.CTkMenuBar(self)
        menu.grid(row=0, column=0, sticky="new", columnspan=2)
        menu.add_cascade("About", command=self.show_about)
        menu.add_cascade("Check Github for updates", command=self.check_updates)
        menu.add_cascade("About Special Characters", command=self.show_symbols)
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
        Define the Tabview frame
        ----------------------------------------
        """
        self.tabview = ctk.CTkTabview(self, anchor="center")
        self.tabview.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="news")
        self.tabview.add("Random Password")
        self.tabview.add("XKCD Passphrase")

        """
        Define the Random Password tab
        """
        rpg_tab = self.tabview.tab("Random Password")
        rpg_tab.grid_columnconfigure(1, weight=1)
        rpg_tab.grid_rowconfigure((0), weight=1)
        self.rpg = RandomPassword(rpg_tab, sidebar=self.sidebar_frame)
        self.rpg.grid(row=0, column=1, sticky="news")

        """
        Define the XKCD Passphrase tab
        """
        xkcd_tab = self.tabview.tab("XKCD Passphrase")
        xkcd_tab.grid_columnconfigure(1, weight=1)
        xkcd_tab.grid_rowconfigure((0), weight=1)
        self.xkcd = XKCDPassphrase(xkcd_tab, sidebar=self.sidebar_frame)
        self.xkcd.grid(row=0, column=1, sticky="news")

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
            message="Random Password Generator\n \nAuthor: jrotzetter \nVersion: 2.0.0 \nLicense: MIT",
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

    def show_symbols(self):
        ctkmbx.CTkMessagebox(
            self,
            title="About Special Characters",
            message="The following ASCII Punctuations & Symbols are included by default:\n"
            "! \" # $ % & ' ( ) * + , - . / : ; < = > ? @ [ ] ^ _ { | } ~",
            icon="info",
            width=500,
        )

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


# Run app
if __name__ == "__main__":
    app = App()
    # app.eval('tk::PlaceWindow . center')
    app.mainloop()

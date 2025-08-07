"""
Tune-Grabber Main file. Designed to allow youtube_to_mp3 to work independently
as CLI program. 

USE OF DOWNLOADER FILE IS DEPRICATED.

Not all events are shown in the event viewer. The console of the actual files still
outputs however.

Whenever writing to the event monitor be sure to enable the textbox, write, and then disable
the textbox. 

TODO fix the AudioQuality setting so that it doesn't need to be changed each time
TODO add a save button for the settings 
TODO error catching
"""

import tkinter as tk
import youtube_to_mp3
import threading
from PIL import Image, ImageTk
import INI_parser
import platform
import os

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.window = root
        self.window.title("Tune Grabber")

        self.url_box_frame()
        self.event_monitor_frame()
        self.settings_button()    

    def url_box_frame(self):
        """
        Url box grid section and buttons with associated actions (Download, Clear, Cancel)

        TODO should make actual frame for this to group these widgets (tk.Frame). It is NOT actual frame
        """

        url_header = (tk.Label(self.window, text="Enter URLS below. Use a newline to separate"))
        url_header.grid(row=0, column=0, columnspan=3, sticky="nesw")

        self.url_textbox = tk.Text(
            self.window,
            height = 30,
            width = 50,
        )

        self.url_textbox.grid(
            row=1,
            column=0,
            columnspan=3,
            rowspan=3,
            padx=10,
            pady=10
        )

        ###DOWNLOAD BUTTON###

        dl_button = tk.Button(
            self.window,
            height=2,
            width=10,
            text="Download",
            bg="#1fdb2b",
            activebackground="#0d5912",
            command=lambda:self.download()
        )

        dl_button.grid(
            row=4,
            column=0,
            padx=10,
            pady=10
        )

        ###CLEAR BUTTON FOR URLS###

        clear_button_urls = tk.Button(
            self.window,
            height=2,
            width=10,
            text="Clear",
            bg="#949191",
            activebackground="#2f302f",
            command=lambda:self.clear(self.url_textbox, editable="yes")
        )

        clear_button_urls.grid(
            row=4,
            column=1,
            padx=10,
            pady=10,
        )

        ###CANCEL BUTTON###

        cancel_button = tk.Button(
            self.window,
            height=2,
            width=10,
            text="Cancel",
            bg="#b02c39",
            activebackground="#82212a",
            command=lambda:self.cancel()
        )

        cancel_button.grid(
            row=4,
            column=2,
            padx=10,
            pady=10
        )

    def event_monitor_frame(self):
        em_header = tk.Label(self.window, text="Event Monitor")
        em_header.grid(row=0, column=3, columnspan=2, sticky="nesw")

        self.event_monitor = tk.Text(
            self.window,
            height=30,
            width=50,
            state=tk.DISABLED,
            relief=tk.SUNKEN,
        )


        self.event_monitor.grid(
            row=1,
            column=3,
            columnspan=2,
            rowspan=3,
            padx=10,
            pady=10
        )

        ###CLEAR BUTTON FOR EVENT MONITOR###

        clear_button_event = tk.Button(
            self.window,
            height=2,
            width=10,
            text="Clear",
            bg="#949191",
            activebackground="#2f302f",
            command=lambda:self.clear(self.event_monitor, editable="no")
        )

        clear_button_event.grid(
            row=4,
            column=3,
            padx=10,
            pady=10,
            columnspan=2
        )

    def settings_button(self):
        photo = Image.open("settings-icon.png")
        photo = photo.resize((20,20))
        photo = ImageTk.PhotoImage(photo)
        photo

        set_button = tk.Button(
            self.window,
            image=photo,
            relief=tk.FLAT,
            height=20,
            width=20,
            command=lambda:self.open_settings()
        )
        set_button.image = photo   #Prevents the garbage collection of the image
        set_button.grid(
            row=0,
            column=4,
            sticky="e",
            padx=10,
            pady=10,

        )

    def open_settings(self):
        settings = Settings()
        settings.window.grab_set()
        self.window.wait_window(settings)

    def download(self):
        """
        TODO fix thread; VERBOSE
        """
        def parse_tb(urls):
            """
            Takes each url from the UI textbox and parses it. Then
            calls the dowloader function for each URL

            :PARAM: urls to youtube videos from the UI
            :RETURNS: list of urls
            """

            urls = urls.replace(" ", "")
            url_list = urls.split("\n")
            return url_list
        def run_yt():
            """
            Runs the youtube_to_mp3 file to handle the downloads and file cleaning

            Because the threading library does not allow for returns on threads, a return 
            list is initialized
            """

            returns = []
            input = self.url_textbox.get("1.0", "end-1c")
            url_list = parse_tb(input)
            for url in url_list:
                self.display_status(url=url)


                success, error = youtube_to_mp3.youtube_to_mp3(url, ini)
                youtube_to_mp3.clean_files(ini)
                returns.append(success)
                returns.append(error)

                success = returns[0]
                error = returns[1]
                self.display_status(url=url, success=success, error=error)

                youtube_to_mp3.clean_files(ini)

        x = threading.Thread(target=run_yt, args=())
        x.start()

    def cancel(self):
        self.window.destroy()

    def display_status(self, url, **kwargs):
        """
        Displays the status of the Download to the event monitor of the GUI.
        *note that more information is printed in the terminal*


        :PARAMS: 
        - url: url of a given video
        - success: success state, bool
        - error: error message associated with download

        """

        if "success" in kwargs:
            if kwargs["success"] == True:
                message = (f"{url} Successfully Downloaded!")
            elif kwargs["success"] == False:
                message = (f"{url} ERROR: FAILED TO DOWNLOAD {kwargs['error']}")
        else:
            message = (f"{url}: Downloading...")


        message = message + "\n" + "\n"
        self.event_monitor.configure(state=tk.NORMAL)
        self.event_monitor.insert(tk.END, message)
        self.event_monitor.configure(state=tk.DISABLED)

    def clear(self, text_box, editable = "no"):
        """
        Clears the text box of any writing

        :PARAMS: a given textbox: either event monitor or user input area
        """
        if editable == "no":
            text_box.configure(state=tk.NORMAL)
            text_box.delete("1.0", tk.END)
            text_box.configure(state=tk.DISABLED)

        if editable == "yes":
            text_box.delete("1.0", tk.END)

class Settings(tk.Frame):
    #TODO make it show the current settings
    def __init__(self):
        super().__init__()
        self.window = tk.Toplevel()
        self.window.title("Settings")
        self.window.resizable(False, False)
        settings_header = (tk.Label(self.window, text="Settings"))
        settings_header.grid(row=0, column=0, columnspan=5, sticky="nesw")

        
        self.window.protocol("WM_DELETE_WINDOW", self.closed)
        self.audio_quality()
        self.download_path()
        self.no_playlist()
        self.save_button()

    def closed(self):
        """
        This is the x button at the top. Have a "Would you like to save your settings" option when they try to close
        """
        self.window.destroy()

    def audio_quality(self):
        # def selection():
        #     print(str(self.selected_option.get()))
        #     ini.change_setting("AudioQuality", str(selected_option.get()))

        audio_quality_label = (tk.Label(self.window, text="Audio Quality"))
        audio_quality_label.grid(row=1, column=0, columnspan=1, sticky="nesw")

        self.selected_option = tk.IntVar()  #This stores the option that the user selected 


        values = {"96": 96, "160":160, "256": 256, "320": 320}

        pos = 1
        for (text, value) in values.items():
            radio_button = tk.Radiobutton(self.window, variable=self.selected_option, text=text, value = value)
            radio_button.grid(row=1, column = pos)
            pos += 1

    def download_path(self):
        download_path_label = (tk.Label(self.window, text="Download Path"))
        download_path_label.grid(row=2, column=0, columnspan=1, sticky="nesw")

        self.download_path_textbox =  tk.Text(
            self.window,
            height= 1,
        )

        self.download_path_textbox.insert(tk.END, ini.find_value("DownloadPath"))

        self.download_path_textbox.grid(
            row=2,
            column=1,
            columnspan=4,
            padx=10,
            pady=10
        )

    def no_playlist(self):
        print(ini.find("NoPlaylist"))
        if ini.find("NoPlaylist") == "True":
            value = True
        else:
            value = False

        self.checkbox_var = tk.BooleanVar(value=value)
        self.no_playlist_checkbox = tk.Checkbutton(self.window, text="Download whole playlist", variable = self.checkbox_var)
        self.no_playlist_checkbox.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            columnspan=2,
            sticky="w"
        )

    def save_button(self):
        save_button_set = tk.Button(
            self.window,
            height=2,
            width=10,
            text="Save",
            bg="#40BD1D",
            activebackground="#007c00",
            command=lambda:self.save()
        )

        save_button_set.grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
            columnspan=5
        )

    def save(self):
        """
        Saves the users selections
        """

        ### AudioQuality Setting ###

        if int(self.selected_option.get()) != 0:   #Prevents the overwrite of 0 when the user does not make a selection
            print(str(self.selected_option.get()))
            ini.change_setting("AudioQuality", str(self.selected_option.get()))

        ### DownloadPath Setting ###
        
        print(self.download_path_textbox.get("1.0", "end-1c"))
        ini.change_setting("DownloadPath", self.download_path_textbox.get("1.0", "end-1c"))


        ### NoPlaylist Setting ###

        print(self.checkbox_var.get())
        ini.change_setting("NoPlaylist", str(self.checkbox_var.get()))

        self.closed()

def main():
    global ini
    ini = INI_parser.INI("settings.ini")


    def change_download_path():
        """
        Detects the os and changes the download path accordingly. Only runs if the download path was at the
        default value "DownloadPath"
        """

        if ini.find_value("DownloadPath") == "DownloadPath":
            user = os.getlogin()
            if platform.system() == "Windows":
                print("Running on Windows")
                download_path = "/Users/" + user + "/Downloads/"

            elif platform.system() == "Linux":
                print("Running on Linux")
                download_path = "/home/" + user + "/Downloads/"

            else:
                print(platform.system())
                print("Unsupported platform: Currently supported on only Linux and Windows")
            
            
            ini.change_setting("DownloadPath", download_path)



    change_download_path()
    root = tk.Tk()
    root.resizable(False, False)
    root.configure(background="#d7d7d9")

    start_app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()


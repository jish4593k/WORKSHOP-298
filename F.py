import os
import json
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Label, Button, StringVar, END, Listbox, Scrollbar, VERTICAL

ACGHost = "acg.sugling.in"
iPhone5URLPath = '/'
ReqeustHeaders = {"U: "*/*"}

class ImageDownloader:
    def __init__(self, master):
        self.master = master
        master.title("ACG Image Downloader")

        self.queue = []
        self.downloaded_count = 0

        self.label_status = Label(master, text="Status: Idle")
        self.label_status.pack()

        self.listbox = Listbox(master, selectmode="browse", height=10, width=50)
        self.listbox.pack()

        self.scrollbar = Scrollbar(master, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.start_button = Button(master, text="Start Download", command=self.start_download)
        self.start_button.pack()

    def fetch_image_list(self):
        response = requests.get(f"  ",
                                headers=ReqeustHeaders)
        data = response.json()
        all_imgs = [img["imgs"] for img in data["data"]]
        return [item for sublist in all_imgs for item in sublist]

    def download_image(self, filename):
        save_path = f'D}'

        if os.path.isfile(save_path):
            self.queue.append(f"{filename} - Skipped (Already Exist)")
        else:
            response = requests.get(f"e}", headers=ReqeustHeaders)
            image_data = response.content

            with open(save_path, "wb") as file:
                file.write(image_data)

            self.downloaded_count += 1
            self.queue.append(f"{filename} - Downloaded")

        self.update_status()

    def update_status(self):
        self.label_status.config(text=f"Status: Downloaded {self.downloaded_count}/{len(self.queue)} images")
        self.listbox.delete(0, END)
        for item in self.queue:
            self.listbox.insert(END, item)
        self.listbox.yview(END)

    def start_download(self):
        self.queue = []
        self.downloaded_count = 0
        self.update_status()

        image_list = self.fetch_image_list()

        with ThreadPoolExecutor(max_workers=15)

# This Python file uses the following encoding: utf-8
import os
import sys
from os.path import dirname
from typing import Any

import customtkinter
from customtkinter.windows.widgets.theme import ThemeManager
from PIL import Image, ImageTk

import models

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    application_path = dirname(dirname(sys.executable))
else:
    application_path = dirname(__file__)


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    PATH_TO_LIGHT_CLOSE_CROSS = os.path.join(
        application_path, "image/icon-close-500-black.png")
    PATH_TO_DARK_CLOSE_CROSS = os.path.join(
        application_path, "image/icon-close-500-white.png")

    def __init__(self, master: Any, json_data: models.JSONReader, application_path: str, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.json_data = json_data
        self.vcmd = (self.register(self._callback))

        self.grid_columnconfigure((0, 1), weight=1)

        self._client_frame_list = []

        self.close_img = customtkinter.CTkImage(light_image=Image.open(self.PATH_TO_LIGHT_CLOSE_CROSS),
                                                dark_image=Image.open(self.PATH_TO_DARK_CLOSE_CROSS), size=(20, 20))
        self.plus_btn = customtkinter.CTkButton(
            master=self, text="+", command=lambda: self._add_item(len(self._client_frame_list)))

        for i in range(len(self.json_data.get_clients_data())):
            self._add_item(i)
            self._populate_item_with_data(
                self.json_data.get_clients_data()[i], i)

        if len(self._client_frame_list) == 0:
            self.plus_btn.grid(row=0, column=0, columnspan=2,
                               padx=(20, 5), pady=(0, 10), sticky="nsew")

    def get_client_frame_list_ignoring_none(self) -> list[models.CustomClientFrame]:
        return [x for x in self._client_frame_list if x is not None]

    def _add_item(self, idx: int) -> None:
        self.client_frame = models.CustomClientFrame(self, corner_radius=0)

        self.client_frame.grid(row=len(self._client_frame_list),
                               column=0, columnspan=2, pady=(0, 32), padx=5, sticky="nsew")
        self.client_frame.grid_rowconfigure(0, weight=1)

        self.client_frame.grid_columnconfigure(0, weight=0)
        self.client_frame.grid_columnconfigure(
            (1, 2, 3, 4, 5, 6), weight=8, uniform="fred")

        self.client_frame.count = customtkinter.CTkLabel(
            self.client_frame, text=f"{len(self._client_frame_list) + 1}.")
        self.client_frame.name_entry = customtkinter.CTkEntry(
            self.client_frame, placeholder_text="Enter name", fg_color="transparent")
        self.client_frame.api_id_entry = customtkinter.CTkEntry(
            self.client_frame, placeholder_text="Enter API_ID", fg_color="transparent")
        self.client_frame.api_hash_entry = customtkinter.CTkEntry(
            self.client_frame, placeholder_text="Enter API_HASH", fg_color="transparent")
        self.client_frame.gpt_prompt_label = customtkinter.CTkLabel(
            self.client_frame, text="GPT prompt:")
        self.client_frame.gpt_prompt = customtkinter.CTkTextbox(self.client_frame, height=50, fg_color="transparent", border_color=ThemeManager.theme[
                                                                "CTkEntry"]["border_color"], text_color=ThemeManager.theme["CTkEntry"]["text_color"], border_width=ThemeManager.theme["CTkEntry"]["border_width"])
        self.client_frame.step_counter = customtkinter.CTkEntry(
            self.client_frame, validate="all", validatecommand=(self.vcmd, '%P'), fg_color="transparent")
        self.client_frame.step_counter_label = customtkinter.CTkLabel(
            self.client_frame, text="Number of ignored post between execution:")
        self.client_frame.checkbox_active = customtkinter.CTkCheckBox(master=self.client_frame, checkbox_height=28, checkbox_width=28, height=28, text="Active", fg_color=ThemeManager.theme["CTkEntry"]["fg_color"], border_color=ThemeManager.theme[
                                                                      "CTkEntry"]["border_color"], border_width=ThemeManager.theme["CTkEntry"]["border_width"], checkmark_color=ThemeManager.theme["CTkCheckBox"]["hover_color"], hover_color="grey")
        self.client_frame.ban_list_btn = customtkinter.CTkButton(master=self.client_frame, fg_color="transparent", text="Bans", border_width=2, text_color=(
            "gray10", "#DCE4EE"), command=self._open_ban_list, height=28)
        self.client_frame.remove_btn = customtkinter.CTkButton(master=self.client_frame, fg_color="transparent", image=self.close_img, height=28, width=28, text="Delete", text_color=(
            "gray10", "#DCE4EE"), command=lambda: self._remove_item(idx), compound="right", hover_color=("#e63946", "#e63946"))

        self.client_frame.count.grid(
            row=0, column=0, pady=(0, 10), padx=(0, 5), sticky="nsw")
        self.client_frame.name_entry.grid(
            row=0, column=1, columnspan=2, padx=(0, 5), pady=(0, 10), sticky="nsew")
        self.client_frame.api_id_entry.grid(
            row=0, column=3, columnspan=2, padx=(5, 5), pady=(0, 10), sticky="nsew")
        self.client_frame.api_hash_entry.grid(
            row=0, column=5, columnspan=2, padx=(5, 0),  pady=(0, 10), sticky="nsew")
        self.client_frame.gpt_prompt_label.grid(
            row=1, column=1, pady=(0, 0), padx=5, sticky="w")
        self.client_frame.gpt_prompt.grid(
            row=2, column=1, columnspan=6, pady=(0, 10), sticky="nsew")
        self.client_frame.step_counter.grid(
            row=4, column=1, columnspan=1, padx=(0, 5), pady=(0, 10), sticky="nsew")
        self.client_frame.step_counter_label.grid(
            row=3, column=1, columnspan=2, pady=(0, 0), padx=5, sticky="w")
        self.client_frame.checkbox_active.grid(
            row=4, column=3, padx=(5, 5), pady=(0, 10), sticky="nsew")
        self.client_frame.ban_list_btn.grid(
            row=4, column=4, padx=(20, 20), pady=(0, 0), sticky="ne")
        self.client_frame.remove_btn.grid(
            row=4, column=6, pady=(0, 0), sticky="ne")

        self._client_frame_list.append(self.client_frame)
        self.plus_btn.grid(row=len(self._client_frame_list), column=0,
                           columnspan=2, padx=(20, 5), pady=(0, 10), sticky="nsew")

    def _remove_item(self, idx: int) -> None:
        curr_client_frame = self._client_frame_list[idx]
        curr_client_frame.count.destroy()
        curr_client_frame.name_entry.destroy()
        curr_client_frame.api_id_entry.destroy()
        curr_client_frame.api_hash_entry.destroy()
        curr_client_frame.gpt_prompt_label.destroy()
        curr_client_frame.step_counter.destroy()
        curr_client_frame.step_counter_label.destroy()
        curr_client_frame.checkbox_active.destroy()
        curr_client_frame.ban_list_btn.destroy()
        curr_client_frame.remove_btn.destroy()
        curr_client_frame.destroy()
        self._client_frame_list[idx] = None

    def _populate_item_with_data(self, clients_data: dict, idx: int) -> None:
        name = clients_data["name"]
        api_id = clients_data["apiId"]
        api_hash = clients_data["apiHash"]
        gpt_prompt = clients_data["gptPrompt"]
        is_active = clients_data["isActive"]
        count_of_ignored_post_between_executions = clients_data[
            "countOfIgnoredPostBetweenExecutions"]

        if len(name) > 0:
            self._client_frame_list[idx].name_entry.insert(0, name)
        if len(str(api_id)) > 0:
            self._client_frame_list[idx].api_id_entry.insert(0, api_id)
        if len(api_hash) > 0:
            self._client_frame_list[idx].api_hash_entry.insert(0, api_hash)
        if len(gpt_prompt) > 0:
            self._client_frame_list[idx].gpt_prompt.insert("0.0", gpt_prompt)
        if is_active:
            self._client_frame_list[idx].checkbox_active.select()
        if count_of_ignored_post_between_executions is not None:
            self._client_frame_list[idx].step_counter.insert(
                0, count_of_ignored_post_between_executions)

    def _callback(self, P: str) -> bool:
        if str.isdigit(P) or P == "":
            return True
        return False

    def _open_ban_list(self) -> None:
        new_window = customtkinter.CTkToplevel(app)
        new_window.title("Ban list")
        new_window.geometry(f"{480}x{480}")
        new_window.wm_attributes("-topmost", -1)


class App(customtkinter.CTk):
    TITLE = "InvaderTG"
    PATH_TO_ICON = os.path.join(application_path, "image/red_tg_logo.png")

    def __init__(self) -> None:
        super().__init__()

        self.title(self.TITLE)
        self.geometry(f"{1100}x{580}")

        self.icon_path = ImageTk.PhotoImage(file=self.PATH_TO_ICON)
        self.wm_iconbitmap()
        self.iconphoto(False, self.icon_path)

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure((2, 3, 4), weight=1)

        json_reader = models.JSONReader(application_path)
        json_writer = models.JSONWriter(application_path)

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="InvaderTG", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, width=200)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, width=200)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, width=200)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event, width=200)
        self.appearance_mode_optionemenu.grid(
            row=10, column=0, padx=20, pady=(10, 10))

        self.settings_label = customtkinter.CTkLabel(
            self, text="Settings", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.settings_label.grid(
            row=0, column=1, columnspan=3, padx=20, pady=(20, 10), sticky="nw")
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter OpenAI ChatGPT API key")
        self.entry.grid(row=1, column=1, columnspan=3, padx=(
            20, 20), pady=(10, 20), sticky="nsew")

        api_key = json_reader.get_open_ai_api_key()
        if api_key is not None and len(api_key) > 0:
            self.entry.insert(0, api_key)

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            self, json_data=json_reader, label_text="Accounts details", application_path=application_path)
        self.scrollable_label_button_frame.grid(
            row=2, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(0, 20), sticky="nsew")

        self.save_btn = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=(
            "gray10", "#DCE4EE"), text="Save", command=lambda: json_writer.write_json_data(self.scrollable_label_button_frame.get_client_frame_list_ignoring_none(), self.entry.get()))
        self.save_btn.grid(row=5, column=3, padx=(
            20, 20), pady=(0, 10), sticky="nsew")

        self.sidebar_button_3.configure(
            state="disabled", text="Disabled CTkButton")
        self.appearance_mode_optionemenu.set("System ")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()

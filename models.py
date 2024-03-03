import json
from tkinter import END
from typing import Any, Optional, Tuple

import customtkinter


class CustomClientFrame(customtkinter.CTkFrame):
    count: customtkinter.CTkLabel
    name_entry: customtkinter.CTkEntry
    api_id_entry: customtkinter.CTkEntry
    api_hash_entry: customtkinter.CTkEntry
    gpt_prompt_label: customtkinter.CTkLabel
    gpt_prompt: customtkinter.CTkTextbox
    step_counter: customtkinter.CTkEntry
    step_counter_label: customtkinter.CTkLabel
    checkbox_active: customtkinter.CTkCheckBox
    ban_list_btn: customtkinter.CTkButton
    remove_btn: customtkinter.CTkButton

    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color,
                         border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)


class JSONReader:
    def __init__(self, application_path) -> None:
        with open(application_path + '/view.json', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_data(self) -> dict:
        return self.data

    def get_clients_data(self) -> list[dict]:
        return self.data["clients"]

    def get_open_ai_api_key(self) -> Optional[str]:
        if len(self.data["apiKeys"]) > 0:
            return self.data["apiKeys"][0]["key"]
        return None


class JSONWriter:
    def __init__(self, application_path) -> None:
        self.application_path = application_path

    def write_json_data(self, list_data: list[CustomClientFrame], api_key: str) -> None:
        data = {
            "clients": [],
            "apiKeys": []
        }

        for i, entry in enumerate(list_data):
            client_entry = {
                "id": i,
                "name": entry.name_entry.get(),
                "apiId": int(entry.api_id_entry.get()),
                "apiHash": entry.api_hash_entry.get(),
                "gptPrompt": entry.gpt_prompt.get("0.0", END),
                "isActive": entry.checkbox_active.get(),
                "countOfIgnoredPostBetweenExecutions": entry.step_counter.get(),
                "banListId": []
            }
            data["clients"].append(client_entry)

        api_keys_entry = {
            "id": 0,
            "key": api_key
        }
        data["apiKeys"].append(api_keys_entry)
        with open(self.application_path + '/view.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

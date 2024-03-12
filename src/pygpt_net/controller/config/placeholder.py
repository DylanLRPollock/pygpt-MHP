#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.03.12 06:00:00                  #
# ================================================== #

class Placeholder:
    def __init__(self, window=None):
        """
        Configuration placeholder options controller

        :param window: Window instance
        """
        self.window = window

    def apply(self, option: dict):
        """
        Apply placeholders to option

        :param option: Option dict
        """
        if option['type'] == 'dict' and 'keys' in option:
            for key in option['keys']:
                item = option['keys'][key]
                if type(item) is dict:
                    if "type" in item:
                        if item["type"] == "combo":
                            if "use" in item and item["use"] is not None:
                                item["keys"] = self.apply_by_id(item["use"])
        elif option['type'] == 'cmd' and 'params_keys' in option:
            for key in option['params_keys']:
                item = option['params_keys'][key]
                if type(item) is dict:
                    if "type" in item:
                        if item["type"] == "combo":
                            if "use" in item and item["use"] is not None:
                                item["keys"] = self.apply_by_id(item["use"])
        elif option['type'] == 'combo':
            if "use" in option and option["use"] is not None:
                option["keys"] = self.apply_by_id(option["use"])

    def apply_by_id(self, id: str) -> list:
        """
        Apply placeholders by id

        :param id: Placeholder options id
        """
        if id == "presets":
            return self.get_presets()
        elif id == "models":
            return self.get_models()
        elif id == "langchain_providers":
            return self.get_langchain_providers()
        elif id == "llama_index_providers":
            return self.get_llama_index_providers()
        elif id == "llama_index_loaders":
            return self.get_llama_index_loaders()
        elif id == "llama_index_loaders_file":
            return self.get_llama_index_loaders(type="file")
        elif id == "llama_index_loaders_web":
            return self.get_llama_index_loaders(type="web")
        elif id == "vector_storage":
            return self.get_vector_storage()
        elif id == "var_types":
            return self.get_var_types()
        elif id == "agent_modes":
            return self.get_agent_modes()
        elif id == "idx":
            return self.get_idx()
        else:
            return []

    def get_langchain_providers(self) -> list:
        """
        Get langchain placeholders list

        :return: placeholders list
        """
        ids = self.window.core.llm.get_ids("langchain")
        data = []
        data.append({'_': '---'})
        for id in ids:
            data.append({id: id})
        return data

    def get_llama_index_providers(self) -> list:
        """
        Get llama placeholders list

        :return: placeholders list
        """
        ids = self.window.core.llm.get_ids("llama_index")
        data = []
        data.append({'_': '---'})
        for id in ids:
            data.append({id: id})
        return data

    def get_llama_index_loaders(self, type: str = "all") -> list:
        """
        Get data loaders placeholders list

        :param type: data type
        :return: placeholders list
        """
        data = []
        choices = self.window.controller.idx.common.get_loaders_choices() # list
        for choice in choices:
            if type == "all":
                data.append(choice)
            elif type == "file":
                key = list(choice.keys())[0]
                if key.startswith("file_"):
                    data.append(choice)
            elif type == "web":
                key = list(choice.keys())[0]
                if key.startswith("web_"):
                    data.append(choice)
        return data

    def get_vector_storage(self) -> list:
        """
        Get vector storage placeholders list

        :return: placeholders list
        """
        ids = self.window.core.idx.storage.get_ids()
        data = []
        for id in ids:
            data.append({id: id})
        return data

    def get_var_types(self) -> list:
        """
        Get langchain placeholders list

        :return: placeholders list
        """
        types = ["str", "int", "float", "bool", "dict", "list", "None"]
        data = []
        for type in types:
            data.append({type: type})
        return data

    def get_presets(self) -> list:
        """
        Get presets placeholders list

        :return: Presets placeholders list
        """
        presets = self.window.core.presets.get_all()
        data = []
        data.append({'_': '---'})
        for id in presets:
            if id.startswith("current."):  # ignore "current" preset
                continue
            data.append({id: id})  # TODO: name
        return data

    def get_models(self) -> list:
        """
        Get models placeholders list

        :return: Models placeholders list
        """
        models = self.window.core.models.get_all()
        data = []
        data.append({'_': '---'})
        for id in models:
            data.append({id: id})  # TODO: name
        return data

    def get_agent_modes(self) -> list:
        """
        Get modes placeholders list

        :return: Models placeholders list
        """
        modes = ["chat", "completion", "vision", "langchain", "llama_index"]
        data = []
        for id in modes:
            data.append({id: id})  # TODO: name
        return data

    def get_idx(self) -> list:
        """
        Get indexes placeholders list

        :return: Indexes placeholders list
        """
        indexes = self.window.core.idx.get_idx_ids()
        data = []
        data.append({'_': '---'})
        for id in indexes:
            data.append({id: id})
        return data

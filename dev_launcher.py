import os
import sys
import time
import inspect
import json

import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

from functools import partial
from threading import Thread

from devlauncher.tools import ToolHandler

class LauncherGridLayout(GridLayout):
    app_console = StringProperty()
    wait_between_launches = 2
    RUNNING = 0
    STOPPED = 1

    def cout(self, _message):
        if (_message):
            self.app_console += _message + "\n"

    def writeToConsole(self, _proc_name, _toggle_val):
        write_text = _proc_name + " started"
        
        if _toggle_val == 1 and _proc_name:
            write_text = _proc_name + " stopped"

        self.cout(write_text)
        
    def getButtonText(self, _proc_name, _toggle_val=1):
        return_text = "Stop\n" + _proc_name
        
        if _toggle_val == 1 and _proc_name:
            return_text = "Start\n" + _proc_name
        return return_text

    def launcherConfig(self):
        file_name = "tool_info.json"
        json_file = open(file_name)
        json_data = json.load(json_file)

        self.tools = json_data['tools']
        self.project_dir = json_data['projects'][0]['path']
        
        json_file.close()
        
        self.thandler = ToolHandler()

        # change cwd
        os.chdir(self.project_dir)
            
    def __init__(self, **kwargs):
        super(LauncherGridLayout, self).__init__(**kwargs)
        self.launcherConfig()

        self.layout = self.ids['layout_tools']

        for tool in self.tools:
            try:
                name = tool['name']
                path = tool['path']
                
                btn = Button(text=self.getButtonText(name), font_size=24)
                
                btn_callback = partial(self.clicked, name)
                
                btn.bind(on_press=btn_callback)
                
                self.layout.add_widget(btn)
                
                self.thandler.newTool(name, path)
            except Exception as err:
                print "Error adding tools: " + str(err)

    def clicked(self, name, instance):
        # for a process type, start or stop it
        try:
            nameDefaultAll = "All"
            if name == nameDefaultAll: # a hard coded default for every tool
                print "Text: " + instance.text
                if "Start" in instance.text:
                    instance.text = self.getButtonText(name, self.RUNNING)
                else:
                    instance.text = self.getButtonText(name, self.STOPPED)
            
                for widget in self.layout.children:
                    widget_name = widget.text.split("\n")[1]
                    if widget_name != nameDefaultAll:
                        self.launch(widget_name, widget)
                        waiter().start()
            else:
                self.launch(name, instance)
        except Exception as err:
            print "Error launching tool: " + str(err)

    def launch(self, name, instance):
        if self.thandler.isBeingUsed(name):
            if self.thandler.returnTool(name):
                instance.text = self.getButtonText(name, self.STOPPED)
                self.writeToConsole(name, self.STOPPED)
        else:
            if self.thandler.useTool(name):
                instance.text = self.getButtonText(name, self.RUNNING)
                self.writeToConsole(name, self.RUNNING)

class waiter(Thread):
    def run(self):
        time.sleep(5)


class LauncherApp(App):    
    def build(self):        
        return LauncherGridLayout()

if __name__ == '__main__':
    launcher = LauncherApp()
    launcher.run()
    


"""
@author Sami Hindi
@date 30.09.2022
@version 0.0.1
@description Hacking-Tool
@license MIT License (/LICENSE)
"""

"""
Import necessary modules and libraries for flash to run.
colored -> Color text in terminal
requests -> Make HTTP requests
os -> Operating system functions
sys -> System-specific parameters and functions
json -> Read and access JSON files
time -> Time access and conversions
functions -> Local functions file
socket -> For port scanning
os -> Operating System's Functionality
requests -> Make HTTP requests
"""
from termcolor import colored
import json
import functions
import socket
import os
import requests

class Action:
    """
    Base class for all actions, includes all the things a Hacking Tool needs.
    """
    def __init__(self, action: str, args: list) -> None:
        self.__open_ports = []
        self.__closed_ports = []
        self.__existing_directories = []
        self.__non_existing_directories = []
        self.__available_actionsStr = json.load(open("../metadata/json/actions.json", "r"))["actions"]
        self.__available_actions = []
        for i in self.__available_actionsStr:
            self.__available_actions.append(i["action"])

        print(colored("Checking the provided information ...", "blue"))

        # Check if the action is valid
        if action not in self.__available_actions:
            functions.quit("Invalid action.")

        # Check if the action has any arguments
        if len(args) == 0:
            functions.quit("No arguments provided.")

        # Check if the action has the correct number of arguments
        amountOfProvidedArgs = len(args)
        amountOfRequiredArgs = len(self.__available_actionsStr[self.__available_actions.index(action)]["args"])
        if amountOfProvidedArgs != amountOfRequiredArgs:
            functions.quit("Invalid number of arguments.")
        print(colored("SUCCESS: The provided information is valid.", "green"))
        self.__action = action
        self.__args = args
        
    @property
    def action(self) -> str:
        """
        Returns the action provided.
        """
        return self.__action

    @property
    def args(self) -> list:
        """
        Returns the arguments for the action.
        """
        return self.__args

    @property
    def available_actions(self) -> list:
        """
        Returns the available actions.
        """
        return self.__available_actions

    @property
    def open_ports(self) -> list:
        """
        Returns the open ports.
        """
        return self.__open_ports

    @property
    def existing_directories(self) -> list:
        """
        Returns the existing directories.
        """
        return self.__existing_directories

    @property
    def non_existing_directories(self) -> list:
        """
        Returns the non-existing directories.
        """
        return self.__non_existing_directories

    def log(self, file_name: str, data: str) -> None:
        """
        The log() function is used to log data to a file.
        :param file_name: Name of the file
        :param data: Data to be logged
        :return None
        """
        if not os.path.isdir("../logs"):
            os.mkdir("../logs")
        with open("../logs/" + file_name + ".log", "w") as f:
            f.write(data)

    def scan_ports(self, ip: str, port_range: str, logging) -> int:
        """
        The scan_ports() function is used to scan a range of ports on a given IP address.
        :param ip: IP address
        :param range: Range of ports
        :return int
        """
        return_value = 0
        print(colored("INFO: Scanning ports on " + ip + " ...", "blue"))
        ports = port_range.split("-")
        for port in range(int(ports[0]), int(ports[1]) + 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect((ip, port))
                print(colored("SUCCESS: Port " + str(port) + " is open.", "green"))
                self.__open_ports.append(port)
                s.close()
            except:
                print(colored("FAILURE: Port " + str(port) + " is closed.", "red"))
                self.__closed_ports.append(port)
                return_value = 1
        print(colored("INFO: Finished scanning ports on " + ip + ".", "blue"))
        if logging:
            file_name = "result_ps_" + ip + "_" + port_range
            content = str("Open ports: \n" + str(self.__open_ports) + "\n\n\n\n" + "Closed ports: \n" + str(self.__closed_ports))
            self.log(file_name, data=content)
        return return_value

    def scan_directories(self, ip: str, wordlist: str, logging) -> int:
        """
        The scan_directories() function is used to scan a range of ports on a given IP address.
        :param ip: IP address
        :param port: Port
        :return int
        """
        return_value = 0
        # Check if provided wordlist is a valid file
        if not os.path.isfile(wordlist):
            functions.quit("FAILURE: Invalid wordlist.")
        print(colored("INFO: Scanning directories on " + ip + " ...", "blue"))
        with open(wordlist, "r") as f:
            lines = f.readlines()
            for dir in lines:
                dir = dir.strip()
                try:
                    r = requests.get("http://" + ip + "/" + dir)
                    if r.status_code == 200:
                        print(colored("SUCCESS: Directory " + dir + " exists.", "green"))
                        self.__existing_directories.append(dir)
                    else:
                        print(colored("FAILURE: Directory " + dir + " does not exist.", "red"))
                        self.__non_existing_directories.append(dir)
                        return_value = 1
                except:
                    print(colored("FAILURE: Directory " + dir + " does not exist.", "red"))
                    self.__non_existing_directories.append(dir)
                    return_value = 1    
        
        print(colored("INFO: Finished scanning directories on " + ip + ".", "blue"))
        if logging:
            file_name = "result_sd_" + ip + "_" + wordlist
            content = str("Existing directories: \n" + str(self.__existing_directories) + "\n\n\n\n" + "Non-existing directories: \n" + str(self.__non_existing_directories))
            self.log(file_name, content)
        return return_value

    def perform(self) -> int:
        """
        Performs the action.
        Redirect to other Python file to perform the action
        """
        print(colored("INFO: Performing action ...", "blue"))
        status = 0
        is_log = bool(input("Do you want to log the output? (true/false): "))
        if self.__action == "ps":
            # Instructions for when the user wants to scan ports
            status = self.scan_ports(ip=self.args[0], port_range=self.args[1], logging=is_log)
        elif self.__action == "ds":
            # Instructions for when the user wants to scan directories
            status = self.scan_directories(ip=self.args[0], wordlist=self.args[1], logging=is_log)

        return status

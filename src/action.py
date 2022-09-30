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
"""
from termcolor import colored
import json
import functions
import socket

class Action:
    """
    Base class for all actions, includes all the things a Hacking Tool needs.
    """
    def __init__(self, action: str, args: list) -> None:
        self.__open_ports = []
        self.__closed_ports = []
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
            with open("../logs/result.log", "w") as f:
                f.write("Open ports: \n" + str(self.__open_ports) + "\n\n")
                f.write("Closed ports: " + str(self.__closed_ports))
        return return_value

    def perform(self) -> int:
        """
        Performs the action.
        Redirect to other Python file to perform the action
        """
        print(colored("INFO: Performing action ...", "blue"))
        status = 0
        if self.__action == "ps":
            is_log = bool(input("Do you want to log the output? (true/false): "))
            status = self.scan_ports(ip=self.args[0], port_range=self.args[1], logging=is_log)
        return status

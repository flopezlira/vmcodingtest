"""
These classes implement the Bridge design pattern
The bridge design pattern was used because there
may be different implementations of functions for each OS
"""


from __future__ import annotations

import os.path
import pathlib
import socket
import subprocess
from abc import ABC, abstractmethod
from ctypes import Union
from ipaddress import IPv4Address, IPv6Address

import requests

try:
    from src.logger import logger
except ImportError:
    from logger import logger


class VmwareTask:
    """
    This class is only used to pass the corresponding function implementation
    """

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation

    def create_text_file(self, file_path):
        return self.implementation.create_text_file(file_path)

    def ping_url(self, ip: Union[IPv4Address, IPv6Address]):
        return self.implementation.ping_url(ip)

    def request_and_get(self, ip):
        return self.implementation.request_and_get(ip)

    def run_test_batch(self, file_name):
        return self.implementation.run_test_batch(file_name)


class Implementation(ABC):
    """
    Abstract methods to be implemented in functions
    WindowsImplementation and LinuxMacImplementation
    """

    @abstractmethod
    def validate_path(self, path) -> ABC:
        pass

    @abstractmethod
    def create_text_file(self, path) -> ABC:
        pass

    @abstractmethod
    def ping_url(self, ip: Union[IPv4Address, IPv6Address]) -> bool:
        pass

    @abstractmethod
    def request_and_get(self, ip) -> bool:
        pass

    @abstractmethod
    def run_test_batch(self, file_name) -> bool:
        pass


class WindowsImplementation(Implementation):
    """
    Implementation of functions for Windows
    """

    def validate_path(self, file_path) -> bool:
        if os.path.exists(file_path):
            if os.access(os.path.dirname(file_path), os.W_OK):
                return True
        return False

    def create_text_file(self, path) -> bool:
        if not self.validate_path(path):
            raise OSError("File path does not exist or no permissions to write")
        file_name = pathlib.Path(os.path.dirname(path), "Hello.txt")
        try:
            with open(file_name, "w") as f:
                f.write("Hello")
        except FileExistsError:
            logger.info("File already exists")
            return False
        except OSError:
            logger.error("Error creating file")
            return False
        return True

    def ping_url(self, ip: Union[IPv4Address, IPv6Address]) -> bool:
        command = ["ping", "-n", "1", ip]
        return subprocess.call(command) == 0

    def request_and_get(self, ip: Union[IPv4Address, IPv6Address]) -> bool:
        try:
            dns_ptr = socket.gethostbyaddr(str(ip))
        except socket.error as e:
            logger.error(f"{ip} does not has a valid dns ptr {e} ")
            return False
        logger.info(f"dns_ptr is {dns_ptr}")
        try:
            result = requests.get("http://" + dns_ptr[0], timeout=10)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting url {e}")
            return False
        logger.info(f"Status code {result.status_code}")
        # The assumption is that any code, i.e. 200..404 is valid.
        # It could be changed for something more specific
        return True

    def run_test_batch(self, file_name) -> bool:
        cwd = os.getcwd()
        logger.info(f"Executing {file_name} at {cwd}")
        if os.path.isfile(file_name):
            try:
                p = subprocess.Popen(file_name, cwd)
                stdout, stderror = p.communicate()
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Error executing {file_name} at {cwd}")
                return False
        else:
            logger.error(f"File {file_name} does not exist")
            return False


class LinuxMacImplementation(Implementation):
    """
    Implementation of functions for Linux and Mac
    """

    def validate_path(self, file_path) -> bool:
        if os.path.exists(file_path):
            return True
        return False

    def create_text_file(self, path) -> bool:
        if not self.validate_path(path):
            logger.error("File path does not exist")
            return False
        file_name = pathlib.Path(path, "Hello.txt")
        try:
            with open(file_name, "w") as f:
                f.write("Hello")
        except FileExistsError:
            logger.info(
                "File already exists. No need to create again"
            )  # Could be deleted and then created
            return True
        except PermissionError:
            logger.error("You don't have permission to write the file")
            return False
        except OSError as e:
            logger.error("Error creating file", e)
            return False
        return True

    def ping_url(self, ip: Union[IPv4Address, IPv6Address]) -> bool:
        response = os.system("ping -c 1 " + str(ip))
        if response == 0:
            return True
        return False

    def request_and_get(self, ip: Union[IPv4Address, IPv6Address]) -> bool:
        try:
            dns_ptr = socket.gethostbyaddr(str(ip))
        except socket.error as e:
            logger.error(f"{ip} does not has a valid dns ptr {e} ")
            return False
        logger.info(f"dns_ptr is {dns_ptr}")
        try:
            result = requests.get("http://" + dns_ptr[0], timeout=10)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting url {e}")
            return False
        logger.info(f"Status code {result.status_code}")
        # The assumption is that any code, i.e. 200..404 is valid.
        # It could be changed for something more specific
        return True

    def run_test_batch(self, file_name) -> bool:
        logger.info(f"Executing {file_name}")
        if os.path.isfile(file_name):
            try:
                os.system("sh " + file_name)
                return True
            except OSError as e:
                logger.error(f"Error trying to run {file_name} {e}")
                return False
        else:
            logger.error(f"File {file_name} does not exist")
            return False


def run_tasks(
    task: VmwareTask,
    file_path: str,
    ip: Union[IPv4Address, IPv6Address],
    file_name: str,
) -> bool:
    """
    Control logic for all the process
    """
    success = True
    if not task.create_text_file(file_path):
        logger.error("Error creating text file")
        success = False
    else:
        logger.info("Success creating text file ")
    if not task.ping_url(ip):
        logger.error("Ping failed")
        success = False
    else:
        logger.info("Success pinging")
    if not task.request_and_get(ip):
        logger.error("Request get failed")
        success = False
    else:
        logger.info("Success requesting and getting")
    if not task.run_test_batch(file_name):
        logger.error("Running test batch failed")
        success = False
    else:
        logger.info("Success running test batch")
    return success

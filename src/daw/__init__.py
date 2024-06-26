from abc import ABC, abstractmethod
from pathlib import Path, PurePath
from types import NoneType
from platform import system

from .consts import DAWS
from .errors import UnsupportedDaws, WrongOsBuddy


class DawApp(ABC):
    """
    Abstract Base Class for a single instance of a DAW application, e.g. one 
    for Cubase 12, another for Cubase 13, another for Pro Tools 11, another for 
    Pro Tools 12, etc...
    """
    def __init__(self, name: str, path: Path, version: int):
        self.__check(name)
        self.path: Path = path
        self.version: int = version

    # This might not be needed, or could better be put in `Daw()`.
    # def __check(self, name):
    #     match = [daw for daw in DAWS if daw.name == self.name]
    #     if len(match) != 1:
    #         if len(match) == 0:
    #             raise UnsupportedDaw(f"The DAW {name} is not supported by this library!")
    #         # TODO: not sure what to do here. Panic? This shouldn't ever happen.
    #         if len(match) > 1:
    #             pass
    #     else:
    #         daw = match[0]
    #         self.name = daw.name
    #         self.developer = daw.developer
    #         self.operating_systems = daw.operating_systems

    def is_open(self) -> bool: 
        return True if len([proc for proc in psutil.process_iter(["pid", "name", "username"]) if f"{self.name} {self.version}" in proc.name() and proc.is_running()]) > 0 else False


class Daw(ABC):
    """
    Abstract base class for all DAWs (Cubase, Reaper, etc).
    """
    def __init__(self, name: str | NoneType = None):
        self.name = name

    # FIXME:
    def __get_installed(self) -> DawApp | list[DawApp] | NoneType:
        """
        Gets all instances of `daw`.
        """
        default_path = self.__get_default_path()
        try:
            default_path.resolve(strict=True)
        except FileNotFoundError as error:
            raise error
        else:
            if daw is not None:
                if isinstance(daw, list):
                    # TODO:
                    # for d in daw:
                else:
                    # TODO: adapt to be DAW-agnostic
                    installations: list[CubaseApp] = []
                    app_paths = [ file for file in get_default_path().iterdir() if file.is_dir() and daw in file.name ]
                    for p in app_paths:
                        extracted_number: list = [
                            char for char in p.stem.split() if char.isdigit()
                        ]
                        version_number = int(extracted_number[0])
                        app = CubaseApp(p, version_number)
                        installations.append(app)
                    return installations
            # TODO: get all installations of all DAWs
            else:
                pass

    # TODO: make some `@abstractmethod`s. 
    # These not only provide an opportunity to force the subclass to have to 
    # define the methods marked with this decorator, but also their presence 
    # effectively makes this class a read-only template from which to make Daw 
    # objects from, and prevents it from being instantiated itself.
    # This is a great way to deal with functionality that is essential to all 
    # DAWs, but the execution of that functionality is DAW-specific.
    # ...or perhaps go with Protocol instead? See: https://www.youtube.com/watch?v=xvb5hGLoK0A

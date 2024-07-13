from typing import List, Union
import os

class BaseInputs:
    def check(self) -> bool:
        for key, inp in self.__dict__.items():
            if isinstance(inp, list):
                for i in inp:
                    i.check()
            else:
                inp.check()

        return True


class BaseOutputs:
    def set_values(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                getattr(self, key).value = value
            else:
                raise AttributeError(f"{key} is not a valid attribute of {self.__class__.__name__}")

        return self

    def check(self) -> bool:
        for key, output in self.__dict__.items():
            if isinstance(output, list):
                for i in output:
                    i.check()
            else:
                output.check()
        return True

class FileInput:
    def __init__(self, 
                 value: str,
                 description: str,
                 min_size: int,
                 max_size: int,
                 suffix: List[str],
                 required = True,
                 ):
        self.value = value
        self.description = description
        self.min_size = min_size
        self.max_size = max_size
        self.suffix = suffix
        self.required = required

    def check(self) -> bool:
        if (self.value is None or self.value == "") and self.required == False:
            return True

        if not isinstance(self.value, str):
            raise TypeError(f"Expected {self.description} to be a string, got {type(self.value)}")

        if not os.path.exists(self.value):
            raise FileNotFoundError(f"File {self.value} not found")

        if os.path.getsize(self.value) < self.min_size:
            raise ValueError(f"File {self.value} is too small. Expected at least {self.min_size} bytes, got {os.path.getsize(self.value)} bytes")

        if os.path.getsize(self.value) > self.max_size:
            raise ValueError(f"File {self.value} is too large. Expected at most {self.max_size} bytes, got {os.path.getsize(self.value)} bytes")

        if not any([self.value.endswith(suffix) for suffix in self.suffix]):
            raise ValueError(f"File {self.value} has an invalid suffix. Expected one of {self.suffix}, got {self.value.split('.')[-1]}")

        return True

class StringInput:
    def __init__(self, 
                 value: str,
                 description: str,
                 min_length: int,
                 max_length: int,
                 choices: List[str],
                 ):
        self.value = value
        self.description = description
        self.min_length = min_length
        self.max_length = max_length
        self.choices = choices

    def check(self) -> bool:
        if not isinstance(self.value, str):
            raise TypeError(f"Expected {self.description} to be a string, got {type(self.value)}")

        if len(self.value) < self.min_length:
            raise ValueError(f"Expected {self.description} to have at least {self.min_length} characters, got {len(self.value)} characters")

        if len(self.value) > self.max_length:
            raise ValueError(f"Expected {self.description} to have at most {self.max_length} characters, got {len(self.value)} characters")

        if len(self.choices) > 0 and self.value not in self.choices:
            raise ValueError(f"Expected {self.description} to be one of {self.choices}, got {self.value}")

        return True

class FloatInput:
    def __init__(self, 
                 value: float,
                 description: str,
                 min_value: float,
                 max_value: float,
                 ):
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def check(self) -> bool:
        if not isinstance(self.value, float):
            raise TypeError(f"Expected {self.description} to be a float, got {type(self.value)}")

        if self.value < self.min_value:
            raise ValueError(f"Expected {self.description} to be at least {self.min_value}, got {self.value}")

        if self.value > self.max_value:
            raise ValueError(f"Expected {self.description} to be at most {self.max_value}, got {self.value}")

        return True

class IntegerInput:
    def __init__(self, 
                 value: int,
                 description: str,
                 min_value: int,
                 max_value: int,
                 ):
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def check(self) -> bool:
        if not isinstance(self.value, int):
            raise TypeError(f"Expected {self.description} to be an integer, got {type(self.value)}")

        if self.value < self.min_value:
            raise ValueError(f"Expected {self.description} to be at least {self.min_value}, got {self.value}")

        if self.value > self.max_value:
            raise ValueError(f"Expected {self.description} to be at most {self.max_value}, got {self.value}")

        return True

class BooleanInput:
    def __init__(self, 
                 value: bool,
                 description: str,
                 ):
        self.value = value
        self.description = description

    def check(self) -> bool:
        if not isinstance(self.value, bool):
            raise TypeError(f"Expected {self.description} to be a boolean, got {type(self.value)}")

        return True


class FileOutput:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: str = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a string, got None")

        if not isinstance(self.value, str):
            raise TypeError(f"Expected {self.description} to be a string, got {type(self.value)}")

        return True

class FileOutputList:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: List[str] = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a list of strings, got None")

        if not isinstance(self.value, list):
            raise TypeError(f"Expected {self.description} to be a list of strings, got {type(self.value)}")

        for v in self.value:
            if not os.path.exists(v):
                raise FileNotFoundError(f"File {v} not found")

        return True

class StringOutput:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: str = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a string, got None")

        if not isinstance(self.value, str):
            raise TypeError(f"Expected {self.description} to be a string, got {type(self.value)}")

        return True

class StringOutputList:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: List[str] = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a list of strings, got None")

        if not isinstance(self.value, list):
            raise TypeError(f"Expected {self.description} to be a list of strings, got {type(self.value)}")

        for v in self.value:
            if not isinstance(v, str):
                raise TypeError(f"Expected {self.description} to be a list of strings, got {type(v)}")

        return True

class FloatOutput:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: float = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a float, got None")

        if not isinstance(self.value, float):
            raise TypeError(f"Expected {self.description} to be a float, got {type(self.value)}")

        return True

class FloatOutputList:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: List[float] = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a list of floats, got None")

        if not isinstance(self.value, list):
            raise TypeError(f"Expected {self.description} to be a list of floats, got {type(self.value)}")

        for v in self.value:
            if not isinstance(v, float):
                raise TypeError(f"Expected {self.description} to be a list of floats, got {type(v)}")

        return True

class IntegerOutput:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: int = None,
                 ):
        self.value = value
        self.description = description
        self.required = required

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be an integer, got None")

        if not isinstance(self.value, int):
            raise TypeError(f"Expected {self.description} to be an integer, got {type(self.value)}")

        return True

class IntegerOutputList:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: List[int] = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a list of integers, got None")

        if not isinstance(self.value, list):
            raise TypeError(f"Expected {self.description} to be a list of integers, got {type(self.value)}")

        for v in self.value:
            if not isinstance(v, int):
                raise TypeError(f"Expected {self.description} to be a list of integers, got {type(v)}")

        return True

class BooleanOutput:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: bool = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a boolean, got None")

        if not isinstance(self.value, bool):
            raise TypeError(f"Expected {self.description} to be a boolean, got {type(self.value)}")

        return True

class BooleanOutputList:
    def __init__(self, 
                 description: str,
                 required: bool = True,
                 value: List[bool] = None,
                 ):
        self.description = description
        self.required = required
        self.value = value

    def check(self) -> bool:
        if self.required and self.value is None:
            raise ValueError(f"Expected {self.description} to be a list of booleans, got None")

        if not isinstance(self.value, list):
            raise TypeError(f"Expected {self.description} to be a list of booleans, got {type(self.value)}")

        for v in self.value:
            if not isinstance(v, bool):
                raise TypeError(f"Expected {self.description} to be a list of booleans, got {type(v)}")

        return True

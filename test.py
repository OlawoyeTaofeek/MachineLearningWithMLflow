from functools import wraps
from inspect import signature
from typing import get_type_hints


def ensure_annotations(func):
    """
    Custom decorator that enforces type hints at runtime.
    Raises TypeError if input or output types do not match the annotations.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get function signature and annotations
        sig = signature(func)
        type_hints = get_type_hints(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # ✅ Check argument types
        for name, value in bound_args.arguments.items():
            if name in type_hints and not isinstance(value, type_hints[name]):
                raise TypeError(
                    f"Argument '{name}' must be {type_hints[name].__name__}, "
                    f"but got {type(value).__name__}."
                )

        # 🏃 Call the actual function
        result = func(*args, **kwargs)

        # 🔄 Check return type
        if 'return' in type_hints and not isinstance(result, type_hints['return']):
            raise TypeError(
                f"Return value must be {type_hints['return'].__name__}, "
                f"but got {type(result).__name__}."
            )

        return result

    return wrapper


@ensure_annotations
def add_numbers(a: int, b: int) -> int:
    return a + b


@ensure_annotations
def greet_user(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."


# ✅ Works perfectly
print(add_numbers(3, 5))                 # 8
print(greet_user("Taofeek", 25))         # Hello Taofeek, you are 25 years old.

# ❌ Raises TypeError
# print(add_numbers(3, "5"))             # TypeError: Argument 'b' must be int, but got str.
# print(greet_user("Taofeek", "twenty")) # TypeError: Argument 'age' must be int, but got str.

from functools import wraps
from inspect import signature
from typing import get_type_hints, get_origin, get_args, Union


def check_type(name, value, expected_type):
    """Recursively checks if a value matches the expected type."""
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # ✅ Handle Union (including Optional)
    if origin is Union:
        if not any(check_type(name, value, arg) for arg in args):
            raise TypeError(f"Argument '{name}' must be one of {args}, got {type(value).__name__}")
        return True

    # ✅ Handle Lists
    if origin is list:
        if not isinstance(value, list):
            raise TypeError(f"Argument '{name}' must be a list, got {type(value).__name__}")
        if args:
            for i, item in enumerate(value):
                check_type(f"{name}[{i}]", item, args[0])
        return True

    # ✅ Handle Dictionaries
    if origin is dict:
        if not isinstance(value, dict):
            raise TypeError(f"Argument '{name}' must be a dict, got {type(value).__name__}")
        if args:
            key_type, val_type = args
            for k, v in value.items():
                check_type(f"{name} key", k, key_type)
                check_type(f"{name}[{k}]", v, val_type)
        return True

    # ✅ Handle Tuples
    if origin is tuple:
        if not isinstance(value, tuple):
            raise TypeError(f"Argument '{name}' must be a tuple, got {type(value).__name__}")
        if args and len(args) == len(value):
            for i, (item, t) in enumerate(zip(value, args)):
                check_type(f"{name}[{i}]", item, t)
        return True

    # ✅ Handle custom classes and basic types
    if not isinstance(value, expected_type):
        raise TypeError(f"Argument '{name}' must be {expected_type}, got {type(value).__name__}")
    return True


def ensure_annotations(func):
    """Enhanced decorator enforcing runtime type checks, including complex and custom types."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        type_hints = get_type_hints(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # ✅ Check arguments
        for name, value in bound_args.arguments.items():
            if name in type_hints:
                check_type(name, value, type_hints[name])

        # 🏃 Call the function
        result = func(*args, **kwargs)

        # 🔄 Check return type
        if 'return' in type_hints:
            check_type("return", result, type_hints['return'])

        return result

    return wrapper

from typing import List, Dict, Optional, Union, Tuple


# ✅ Custom class example
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


@ensure_annotations
def process_users(users: List[User]) -> int:
    return len(users)


@ensure_annotations
def combine_data(data: Dict[str, List[int]]) -> int:
    return sum(sum(lst) for lst in data.values())


@ensure_annotations
def flexible_function(x: Union[int, str], y: Optional[List[int]]) -> str:
    return f"x: {x}, y: {y}"


@ensure_annotations
def process_tuple(data: Tuple[int, str, List[float]]) -> str:
    return f"Processed {data}"


# ✅ Tests that should pass
print(process_users([User("Alice", 30), User("Bob", 25)]))  # 2
print(combine_data({"scores": [10, 20, 30]}))              # 60
print(flexible_function(10, None))                        # x: 10, y: None
print(flexible_function("Hello", [1, 2, 3]))               # x: Hello, y: [1, 2, 3]
print(process_tuple((1, "Data", [0.1, 0.2])))              # Processed (1, 'Data', [0.1, 0.2])


# ❌ Tests that should fail (raise TypeError)
# process_users(["Alice", "Bob"])                         # Fails: str instead of User
# combine_data({"scores": [10, "20"]})                    # Fails: str instead of int in list
# flexible_function(10, ["not", "int"])                   # Fails: str instead of int in list
# process_tuple((1, "Data", [0.1, "invalid"]))             # Fails: str instead of float

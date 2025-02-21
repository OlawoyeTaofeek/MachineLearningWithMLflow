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


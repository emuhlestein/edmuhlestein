# app/core/forms.py
import inspect
from typing import Type, Any
from fastapi import Form
from pydantic import BaseModel


def as_form(cls: Type[BaseModel]):
    """
    Allows using a Pydantic model with FastAPI's Form(...) parameters.
    Dynamically creates Form fields for each model attribute.
    """
    # Create a list of Form parameters matching the model's fields
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=Form(field.default if field.default is not None else ...),
            annotation=field.annotation,
        )
        for field_name, field in cls.model_fields.items()
    ]

    # Inner function that FastAPI will call
    def _as_form(**data: Any) -> BaseModel:
        return cls(**data)

    # Attach the signature so FastAPI sees the parameters correctly
    _as_form.__signature__ = inspect.Signature(new_params)

    # Attach the method to the class
    setattr(cls, "as_form", classmethod(_as_form))

    return cls
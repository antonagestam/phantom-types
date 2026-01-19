from phantom.errors import MissingDependency


def require_pydantic() -> None:
    try:
        import pydantic_core  # noqa: F401
    except ImportError:
        raise MissingDependency(
            "pydantic>=2 is required for Pydantic schema generation. "
            "Install it with: pip install phantom-types[pydantic]"
        ) from None

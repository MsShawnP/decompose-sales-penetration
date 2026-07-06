"""Decompose views — one module per tab, each with layout() and register_callbacks()."""

from app.views import detail, penetration, which_lever

__all__ = ["which_lever", "penetration", "detail"]

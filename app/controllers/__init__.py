"""Controllers module for the Flask Todo List application."""
from .index_controller import blueprint as index_blueprint
from .todo_controller import blueprint as todo_blueprint

__all__ = ['index_blueprint', 'todo_blueprint']

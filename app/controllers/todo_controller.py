from typing import Optional
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.wrappers import Response
from app.models import ToDo, Action

blueprint = Blueprint("todo", __name__, url_prefix="/todo")

def verify_todo_name(todo_name: Optional[str]) -> Optional[str]:
    """Validate the to-do name and return an error message if invalid."""
    if not todo_name:
        return "Missing to-do name"
    elif len(todo_name) > 255:
        return "Too long to-do name"
    
    return None


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == "POST":
        todo_name = request.form.get("todo-name")
        error = verify_todo_name(todo_name)

        if error == None:
            ToDo().insert_data({"text": todo_name})

            # Add log
            Action().insert_data({"type": "todo-create", "ip": request.remote_addr})

            flash("Successfully added a new to-do!")
            return redirect(url_for("index.index"))

    return render_template("create-todo.html", error=error)
        
@blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    rows = ToDo().find_data({"id": id}, 1)
    if len(rows) == 0:
        flash("To-do with this ID wasn't found!")
        return redirect(url_for("index.index"))
    
    error = None
    if request.method == "POST":
        todo_name = request.form.get("todo-name")
        todo_state = request.form.get("todo-state") == "on" and 1 or 0
        error = verify_todo_name(todo_name)

        if error == None:
            ToDo().update_data({"text": todo_name, "state": todo_state}, {"id": id})

            # Add log
            Action().insert_data({"type": "todo-update", "ip": request.remote_addr, "details": f'updated_id={id}'})

            flash(f'Successfully updated to-do with ID: {id}')
            return redirect(url_for("index.index"))

    return render_template("update-todo.html", error=error, row=rows[0])

@blueprint.get('/delete/<int:id>')
def delete(id: int):
    def rollback(message: str) -> Response:
        flash(message)
        return redirect(url_for("index.index"))

    rows = ToDo().find_data({"id": id}, 1)
    if len(rows) == 0:
        return rollback("To-do with this ID wasn't found!")
    
    ToDo().delete_data({"id": id})
    return rollback(f'Successfully deleted to-do with ID: {id}')
    
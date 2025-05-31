from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from app.models import ToDo, Action
from app.utils import csv_encode

blueprint = Blueprint("index", __name__, url_prefix="/")

# Constants
DATA_LIMIT = 100

@blueprint.get("/")
def index():
    """Render the home page with a list of todos."""
    return render_template("index.html", entries=ToDo().select_data(DATA_LIMIT))

@blueprint.get("/export")
def export():
    """Export the todo list as a CSV file."""
    entries = ToDo().select_data()
    if not entries:
        flash("No to-do's were found to export!")
        return redirect(url_for("index.index"))

    # Add log entry for the export
    Action().insert_data({
        "type": "export", 
        "ip": request.remote_addr, 
        "details": f'exported_entries={len(entries)}'
    })

    return Response(
        csv_encode(entries),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=todo-list.csv"}
    )
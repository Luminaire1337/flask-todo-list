from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from app.models import ToDo, Action
from app.utils import csv_encode

blueprint = Blueprint("index", __name__, url_prefix="/")

# Consts
DATA_LIMIT = 100

@blueprint.get("/")
def index():
    return render_template("index.html", entries=ToDo().select_data(DATA_LIMIT))

@blueprint.get("/export")
def export():
    entries = ToDo().select_data()
    if len(entries) == 0:
        flash("No to-do's were found to export!")
        return redirect(url_for("index.index"))

    # Add log
    Action().insert_data({"type": "export", "ip": request.remote_addr, "details": f'exported_entries={len(entries)}'})

    return Response(
        csv_encode(entries),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=todo-list.csv"}
    )
from typing import Optional
from flask import Blueprint, request, flash, redirect, url_for
from app.models import Action
from app.models.review import Review

blueprint = Blueprint("review", __name__, url_prefix="/review")

def validate_string(value: Optional[str], field_name: str, max_length: int) -> Optional[str]:
    """Validate a string value and return an error message if invalid."""
    if not value:
        return f"Missing {field_name}"
    elif len(value) > max_length:
        return f"Too long {field_name}"
    return None

@blueprint.route('/', methods=['POST'])
def index():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        title = request.form.get("title")
        content = request.form.get("content")
        rating = request.form.get("rating")
        error = validate_string(username, "username", 255) or \
                validate_string(title, "title", 255) or \
                validate_string(content, "content", 1000) or \
                (rating is None or not rating.isdigit() or not (1 <= int(rating) <= 5)) and "Invalid rating"
        if not error:
            Review().insert_data({
                "username": username,
                "title": title,
                "content": content,
                "rating": int(rating) if rating is not None else 0
            })

            # Add log
            Action().insert_data({"type": "review-create", "ip": request.remote_addr})

            flash("Successfully added a new review!")
            return redirect(url_for("index.index"))

    flash(error or "An unknown error occurred")
    return redirect(url_for("index.index"))
        
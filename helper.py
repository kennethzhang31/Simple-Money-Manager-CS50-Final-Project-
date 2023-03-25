from functools import wraps
from flask import redirect, render_template, request, session

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def category_check(category):
    if category == "food_drink":
        code = "fa-solid fa-utensils"
        return code
    elif category == "health":
        code = "fa-solid fa-kit-medical"
        return code
    elif category == "education":
        code = "fa-solid fa-book"
        return code
    elif category == "self_imprv":
        code = "fa-solid fa-person"
        return code
    elif category == "clothing":
        code = "fa-solid fa-shirt"
        return code
    elif category == "transport":
        code = "fa-solid fa-bus"
        return code
    elif category == "others":
        code = "fa-solid fa-star"
        return code


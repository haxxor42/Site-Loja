from functools import wraps
from flask import session, redirect, url_for
from services.user_service import get_user_by_id


def login_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):

        user_id = session.get("user_id")

        if not user_id:
            return redirect(url_for("auth.login"))

        user = get_user_by_id(user_id)

        if user is None:
            session.clear()
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)
    
    return decorator_function

    
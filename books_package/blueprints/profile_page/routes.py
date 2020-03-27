from flask import Blueprint, render_template, session, redirect

profile_page = Blueprint("profile_page", __name__, template_folder="templates", url_prefix="/profile")

@profile_page.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")
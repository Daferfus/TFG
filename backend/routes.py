# from flask import (
#     Flask,
#     url_for,
#     render_template,
#     redirect
# )
# from .forms import ContactForm


# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     """Standard `contact` form."""
#     form = ContactForm()
#     if form.validate_on_submit():
#         return redirect(url_for("success"))
#     return render_template(
#         "contact.jinja2",
#         form=form,
#         template="form-template"
#     )

# @app.route('/')
# def home():
#     """Landing page."""
#     return render_template(
#         'home.html',
#         title="Jinja Demo Site",
#         description="Smarter page templates with Flask & Jinja."
#     )
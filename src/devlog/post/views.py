from flask import abort, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required

from . import post_bp
from ..models import Blog
from .forms import PostForm


@post_bp.route("/inblog/<int:blog_id>", methods=["POST", "GET"])
@login_required
def create(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(404)
    form = None
    if request.method == "POST":
        form = PostForm()
        if form.validate_on_submit():
            form.save()
            flash(gettext("your blog post has been saved"), category="success")
            return redirect(url_for("blog.display", blog_id=blog.id))
    context = {"blog": blog, "form": form or PostForm()}
    return render_template("post/create.jinja", **context)

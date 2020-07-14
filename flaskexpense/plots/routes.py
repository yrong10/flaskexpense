from datetime import date, datetime, time, timedelta

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.sql import label

from flaskexpense import db
from flaskexpense.expenses.forms import DateForm
from flaskexpense.expenses.utils import todate
from flaskexpense.models import Expense
from flaskexpense.plots.utils import plot_bar_chart, plot_pie_chart

plots = Blueprint("plots", __name__)


@plots.route("/bar")
@login_required
def bar_chart():
    form = DateForm()
    end_date = date.today()
    end_date = datetime.combine(end_date, time.min)
    start_date = end_date - timedelta(days=30)
    start = request.args.get("start_date", start_date, type=todate)
    end = request.args.get("end_date", end_date, type=todate)
    form.start_date.data = start
    form.end_date.data = end
    if form.validate():
        start = form.start_date.data
        end = form.end_date.data
        return redirect(url_for("bar_chart", start=start, end=end))
    expenses = (
        db.session.query(Expense.category, label("total", func.sum(Expense.price)))
        .filter_by(user=current_user)
        .filter(Expense.date.between(start, end))
        .group_by(Expense.category)
        .order_by("total")
        .all()
    )
    if not expenses:
        return render_template("dashboard/plot.html", form=form)
    categories = []
    totals = []
    for category, total in expenses:
        categories.append(category)
        totals.append(total)

    script, div = plot_bar_chart(totals, categories)
    return render_template("dashboard/plot.html", script=script, div=div, form=form)


@plots.route("/pie")
@login_required
def pie_chart():
    form = DateForm()
    end_date = date.today()
    end_date = datetime.combine(end_date, time.min)
    start_date = end_date - timedelta(days=30)
    start = request.args.get("start_date", start_date, type=todate)
    end = request.args.get("end_date", end_date, type=todate)
    form.start_date.data = start
    form.end_date.data = end
    if form.validate():
        start = form.start_date.data
        end = form.end_date.data
        return redirect(url_for("pie_chart", start=start, end=end))
    expenses = (
        db.session.query(Expense.category, label("total", func.sum(Expense.price)))
        .filter_by(user=current_user)
        .filter(Expense.date.between(start, end))
        .group_by(Expense.category)
        .order_by("total")
        .all()
    )
    if not expenses:
        return render_template("dashboard/plot.html", form=form)
    x = {}
    for category, total in expenses:
        x[category] = round(total, 2)

    script, div = plot_pie_chart(x)
    return render_template("dashboard/plot.html", script=script, div=div, form=form)

from datetime import date, datetime, time, timedelta

from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.sql import label

from flaskexpense import db
from flaskexpense.expenses.forms import DateForm, ExpenseForm
from flaskexpense.expenses.utils import todate
from flaskexpense.models import Expense

expenses = Blueprint("expenses", __name__)


@expenses.route("/dashboard")
@login_required
def dashboard():
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
        return redirect(url_for("expenses.dashboard", start=start, end=end))
    page = request.args.get("page", 1, type=int)
    show_expenses = (
        Expense.query.filter_by(user=current_user)
        .filter(Expense.date.between(start, end))
        .order_by(Expense.date.desc())
        .paginate(page=page, per_page=8)
    )
    total_price = (
        db.session.query(func.sum(Expense.price).label("total"))
        .filter_by(user=current_user)
        .filter(Expense.date.between(start, end))
        .first()
    )[0]
    for expense in show_expenses.items:
        expense.date = expense.date.date()
    return render_template(
        "dashboard/dashboard.html",
        expenses=show_expenses,
        total_price=total_price,
        form=form,
    )


@expenses.route("/expense/new", methods=["GET", "POST"])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            date=form.date.data,
            category=form.category.data,
            price=form.price.data,
            user=current_user,
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("expenses.dashboard"))
    return render_template("dashboard/create.html", form=form, form_title="Add Expense")


@expenses.route("/expense/<int:expense_id>/update", methods=["GET", "POST"])
@login_required
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.name = form.name.data
        expense.date = form.date.data
        expense.category = form.category.data
        expense.price = form.price.data
        db.session.commit()
        return redirect(url_for("expenses.dashboard"))
    elif request.method == "GET":
        form.name.data = expense.name
        form.date.data = expense.date
        form.category.data = expense.category
        form.price.data = expense.price
    return render_template(
        "dashboard/create.html", form=form, form_title="Edit Expense"
    )


@expenses.route("/expense/<int:expense_id>/delete", methods=["GET", "POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("expenses.dashboard"))

from crypt import methods
from pickletools import read_unicodestring1
from turtle import update
from flask import Flask, render_template, redirect, url_for, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('home.html')



@app.route('/budget')
def get_budget():

    expenses = fetch_data()
    return render_template('budget.html', expenses = expenses)


@app.route('/budget/new', methods=['GET', 'POST'])
def budget_new():

    if request.method == 'GET':
        return render_template('budget-new.html')

    else:
        budget_list = fetch_data()
        new_budget_item = {}

        new_expense = request.form['new_expense']
        new_vendor = request.form['new_vendor']
        new_category = request.form['new_category']
        new_amount = request.form['new_amount']
        new_paidby = request.form['new_paidby']
        new_id = budget_list[len(budget_list) - 1]['id'] + 1

        new_budget_item['expense'] = new_expense
        new_budget_item['vendor'] = new_vendor
        new_budget_item['category'] = new_category
        new_budget_item['amount'] = new_amount
        new_budget_item['paidby'] = new_paidby
        new_budget_item['id'] = new_id      

        budget_list.append(new_budget_item)

        df = pd.DataFrame(budget_list).set_index('id') 
        df.to_csv('/Users/Enzo/pyth-15/LAB_3/budget.csv')

        return redirect(url_for('get_budget'))



@app.route('/budget/<id>', methods=['GET', 'POST'])
def edit_budget_item(id):

    budget_list = fetch_data()
    selected_expense = None

    for expense in budget_list:
        if expense['id'] == int(id):
            selected_expense = expense
            break

    if request.method == 'GET':
        return render_template('budget-edit.html', selected_expense = selected_expense)
    else:
        edited_item = {
            'id': selected_expense['id'],
            'expense': request.form['new_expense'],
            'vendor': request.form['new_vendor'],
            'category': request.form['new_category'],
            'amount': request.form['new_amount'],
            'paidby': request.form['new_paidby']
        }
        update_expense(budget_list, edited_item)
        df = pd.DataFrame(budget_list).set_index('id')
        df.to_csv('/Users/Enzo/pyth-15/LAB_3/budget.csv')
        return redirect(url_for('get_budget'))



@app.route('/budget/<id>/delete', methods=['POST', 'DELETE'])
def delete_item(id):
    delete_expense(request.form['delete'])
    return redirect(url_for('get_budget'))



def fetch_data():
    data = pd.read_csv('/Users/Enzo/pyth-15/LAB_3/budget.csv')
    return data.to_dict('records')

def update_expense(budget_list, edited_item):
    for line in range(len(budget_list)):
        if edited_item['id'] == budget_list[line]['id']:
            budget_list[line] = edited_item
            break
    return budget_list

def delete_expense(id):
    budget_list = fetch_data()
    new_budget_list = [line for line in budget_list if not(line['id'] == int(id))]
    df = pd.DataFrame(new_budget_list).set_index('id')
    df.to_csv('/Users/Enzo/pyth-15/LAB_3/budget.csv')




if __name__ == '__main__':
    app.run(debug=True)
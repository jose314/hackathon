from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from queries import *

app =  Flask(__name__)
db = SQL("sqlite:///accountingLite.db")

@app.route('/')
def index():
    balanceSheets = getBalanceSheets(db)
    return render_template("index.html", balanceSheets = balanceSheets)


@app.route('/history')
def history():
    transactions = getTransactions(db)
    return render_template("history.html", transactions = transactions)


@app.route('/configuration')
def configuration():
    accounts = getAccounts(db)
    return render_template("configuration.html", accounts =accounts)


@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/addBalanceSheet')
def addBalanceSheet():
    name = request.args.get('name')
    idBS = createBalanceSheet(db, name)
    return redirect("/")

@app.route('/addAccount')
def addAccount():
    name = request.args.get('name')
    description = request.args.get('description')
    typeA = request.args.get('type')
    createAccount(db, name, description,typeA)
    return redirect("/configuration")

@app.route("/addTransaction")
def addTransaction():
    idBS = request.args.get('idBS')
    idAccount1 = request.args.get('asset')
    idAccount2 = request.args.get('inasset')
    amount = request.args.get('amount')
    createTransaction(db, idAccount1, idBS, amount)
    createTransaction(db, idAccount2, idBS, amount)
    return redirect('/balanceSheet/' + idBS)

@app.route('/balanceSheet/<int:idBS>')
def balanceSheet(idBS):
    transactions = getTransactionsByBalanceSheetR(db, idBS)
    balSheet = getBalanceSheetById(db, idBS)

    assets = getAccountsByType(db, 1)
    liabilities = getAccountsByType(db, 2)
    capitals = getAccountsByType(db, 3)
    Tassets = getTotalAssets(db, idBS)
    Tliabilities = getTotalLiabilities(db, idBS)
    Tcapitals = getTotalCapital(db, idBS)

    return render_template("balanceSheet.html",
    balSheet = balSheet, transactions = transactions, assets = assets, liabilities=liabilities, capitals =capitals,
    Tassets = Tassets, Tliabilities=Tliabilities, Tcapitals =Tcapitals)
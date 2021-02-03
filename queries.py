from cs50 import SQL

def getTypeAccount(db):
    rows = db.execute("select * from type_account")
    return rows

def createBalanceSheet(db, name):
    idBalanceSheet = db.execute("INSERT INTO balance_sheet (name, date) VALUES(?, DATETIME('NOW'))", name)
    return idBalanceSheet

def getBalanceSheets(db):
    rows = db.execute("select * from balance_sheet")
    return rows

def getBalanceSheetById(db, idBS):
    rows = db.execute("select * from balance_sheet WHERE id=?", idBS)
    return rows[0]

def deleteBalanceSheets(db, idBS):
    res = db.execute("delete from balance_sheet where id = ?", idBS)
    return res

def updateBalanceSheet(db, idBS, name):
    res = db.execute("UPDATE balance_sheet SET name=? WHERE id=?", name, idBS)
    return res

def getAccounts(db):
    rows= db.execute("select * from account")
    return rows

def getAccountsByType(db, idT):
    rows= db.execute("select * from account where type_id = ?", idT)
    return rows


def createAccount(db, name, description,typeAccount, value=1000):
    idAccount=db.execute('''
        INSERT INTO account (name, description, value, type_id, status)
        VALUES(:n, :d, :v, :ti, :s)
    ''', n = name, d = description, ti= typeAccount, v = value, s = "ENABLED")

def updateAccountName(db, idA, name):
    res = db.execute("UPDATE account SET name=? WHERE id=?", name, idA)
    return res

def updateAccountDescription(db, idA, description):
    res = db.execute("UPDATE account SET description=? WHERE id=?", description, idA)
    return res

def updateAccountValue(db, idA, value):
    res = db.execute("UPDATE account SET value=? WHERE id=?", value, idA)
    return res

def updateAccountType(db, idA, typeId):
    res = db.execute("UPDATE account SET type_id=? WHERE id=?", typeId, idA)
    return res

def updateAccountStatus(db, idA, status):
    res = db.execute("UPDATE account SET name=? WHERE id=?", status, idA)
    return res

def deleteAccount(db, idA):
    res = db.execute("delete from account where id = ?", idA)
    return res


def getTransactionsByBalanceSheetR(db, idT):
    rows= db.execute('''
                    SELECT t.account_id, a.name AS nameAccount, SUM(t.value) AS total, ta.id AS typeAccount
                    FROM transactions t
                        INNER JOIN account a ON t.account_id = a.id
                        INNER JOIN type_account ta ON a.type_id = ta.id
                        WHERE balance_sheet_id = ?
                        GROUP BY t.account_id, nameAccount, typeAccount
                    ''', idT)
    return rows

def getTransactionsByBalanceSheet(db, idT):
    rows= db.execute('''
                    select t.*, a.name as nameAccount, ta.id as typeAccount
                    from transactions t
                    inner join account a on t.account_id = a.id
                    inner join type_account ta on a.type_id = ta.id
                    where balance_sheet_id = ?
                    ''', idT)
    return rows



def getTransactions(db):
    rows= db.execute('''
                    select t.*, a.name as nameAccount, ta.id as typeAccount, bs.name as nameBalance
                    from transactions t
                    inner join account a on t.account_id = a.id
                    inner join type_account ta on a.type_id = ta.id
                    inner join balance_sheet bs on t.balance_sheet_id = bs.id
                    order by t.date desc
                    ''')
    return rows


def getTotalAssets(db, idBS):
    rows = db.execute('''
            SELECT sum(t.value) as total FROM transactions t
            inner join account a on t.account_id = a.id
            inner join type_account ta on a.type_id = ta.id
            where balance_sheet_id = ? and ta.id = 1

    ''', idBS)
    if not rows[0]["total"]:
        return  0.0

    return rows[0]["total"]

def getTotalCapital(db, idBS):
    rows = db.execute('''
            SELECT sum(t.value) as total FROM transactions t
            inner join account a on t.account_id = a.id
            inner join type_account ta on a.type_id = ta.id
            where balance_sheet_id = ? and ta.id = 3

    ''', idBS)
    if not rows[0]["total"]:
        return  0.0

    return rows[0]["total"]

def getTotalLiabilities(db, idBS):
    rows = db.execute('''
            SELECT sum(t.value) as total FROM transactions t
            inner join account a on t.account_id = a.id
            inner join type_account ta on a.type_id = ta.id
            where balance_sheet_id = ? and ta.id = 2

    ''', idBS)
    if not rows[0]["total"]:
        return  0.0

    return rows[0]["total"]

def createTransaction(db, idA, idBS, value):
    res = db.execute('''
        INSERT INTO transactions (account_id, balance_sheet_id, value, date)
        VALUES(:ida, :idbs, :v, DATETIME('NOW'))
        ''', ida = idA, idbs = idBS, v = value)
    return res

def updateTransactionValue(db, idT, value):
    res = db.execute("UPDATE transactions SET value = ? WHERE id=?", value, idT)
    return res

def deleteTransaction(db, idT):
    res = db.execute("DELETE FROM transactions WHERE id =?", idT)

from app.models import Transaction, User
from app import db


def add_transaction(user_id, amount, current_balance):
    if user_id in transaction_flag.flag:
        if transaction_flag.flag[user_id] == 1:
            return -1
                
    transaction_flag.flag[user_id] = 1

    user = User.query.filter_by(id=user_id).first()

    current_balance+=amount

    User.query.filter_by(id=user_id).update(dict(current_balance=current_balance))
    transaction = Transaction(amount=amount, user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    transaction_flag.flag[user_id] = 0
    return 1

def get_transactions(user_id):
    transactions = Transaction.query.filter(Transaction.user_id==user_id).all()
    tran_list = []
    
    for tran in transactions:
        tran_dic = dict(
            timestamp=tran.timestamp,
            amount=tran.amount,
            transaction_type="credited"
        )
        if tran.amount <0:
            tran_dic["amount"] = -1*tran.amount
            tran_dic["transaction_type"] = "debited"

        tran_list.append(tran_dic)
    
    return tran_list

class transaction_flag():
    flag = {}
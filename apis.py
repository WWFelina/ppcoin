from flask import Flask, render_template, request
from blockchain import Blockchain
app = Flask(__name__)


@app.route('/transaction/', methods=['post', 'get'])
def transaction():
    message = ''
    if request.method == 'POST':
        sender = request.form.get('From')  
        receiver = request.form.get('To')
        amount = request.form.get('Amount')

        blockchain.new_transaction(sender, receiver, amount)
        print(blockchain.pending_transactions)

        message = f"New Transaction added! \n {sender} sent {amount} to {receiver}"

    return render_template('transaction.html', message=message)

@app.route('/balance/', methods=['post', 'get'])
def balance():
    message = ''
    if request.method == 'POST':
        print(blockchain.pending_transactions)
        blockchain.add_block()
        print(blockchain.pending_transactions)
        print(blockchain.get_balance('A'))
        user = request.form.get('User') 
        balance = blockchain.get_balance(user)
        message = f"{user} has {balance} PP in their wallet!"

    return render_template('balance.html', message=message)


if __name__ == "__main__":
    blockchain = Blockchain()
    app.run(debug=True)
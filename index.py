from flask import Flask, jsonify, request
import json
import requests
app = Flask(__name__)

store = [
    {
        'id': 1,
        'item': 'maize_fertilizer',
        'price': 200
    },
    {
        'id': 2,
        'item': 'corn_fertilizer',
        'price': 300
    }
]

@app.route('/', methods=['GET'])
def get_items():
    return jsonify(items)

# {
# 	"itemId": 1,
# 	"name":"'customer",
# 	"paymentOption": "card",
# 	"quantity": 2
# } this is the example object front frontend

@app.route('/purchase', methods=['POST'])
def purchase():
    itemId = request.get_json().get('itemId')
    for item in store:
        for key, values in item.items():
            print(key, values)
            if key == 'id':
                if values == itemId:
                    soldItem = item
                    break
    if not soldItem:
        return jsonify({'message': 'item does not exist'})

    emailData = {
        "name": request.get_json().get('name'),
        "item": soldItem.name,
        "paymentOption": request.get_json().get('paymentOption'),
        "itemName": soldItem.name,
        "itemPrice": soldItem.price,
        "total": request.get_json().get('quantity') * soldItem.price,
    }

    return requests.post(
		"https://api.mailgun.net/v3/sandboxc124857d76b943478004fec6bdbdfe76.mailgun.org/messages",
		auth=("api", "07545992aa71ac27330cc627a5126ee2-9dfbeecd-da67d304"),
		data={"from": "Mailgun Sandbox <postmaster@sandboxc124857d76b943478004fec6bdbdfe76.mailgun.org>",
			"to": "Davis Kabiswa <dkabitswa@gmail.com>",
			"subject": "Ezy Agric item Purchase",
			"template": "provider",
			"h:X-Mailgun-Variables": json.dumps(emailData, indent='\t')})

if __name__ == '__main__':
    app.run()

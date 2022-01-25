from flask import Flask, jsonify
import csv
from datetime import datetime, timedelta

app = Flask(__name__)
product_data = []
product_data_map = {}
transaction_data = []

@app.route("/")
def root():
    return jsonify({"product_data": product_data, "transaction_data": transaction_data})


@app.route("/assignment/transaction/<transaction_id>")
def transaction(transaction_id):
	"""
	returns transaction data for given transaction Id
	"""
	try:

		for transaction in transaction_data:
			if transaction_id == transaction["transaction_id"]:
				transaction["product_name"] = product_data_map[transaction["product_id"]]["product_name"]
				del transaction["product_id"]
				return jsonify(transaction)

		return jsonify({"error": f"No data available with transaction_id: {transaction_id}"})

	except ValueError:
		return jsonify({"error": f"Invalid parameter: '{last_n_days}', integer expected"})


@app.route("/assignment/transactionSummaryByProducts/<last_n_days>")
def transactionSummaryByProducts(last_n_days):
	"""
	returns transaction summary data of last given days
	"""
	try:
		last_n_days = int(last_n_days)

		summary = []
		last_n_day_date_time = datetime.now() - timedelta(int(last_n_days))

		for transaction in transaction_data:

			if transaction["transaction_date_time"] > last_n_day_date_time:
				summary.append({
					"product_name": product_data_map[transaction["product_id"]]["product_name"],
					"total_amount": transaction["transaction_amount"]
					})

		data = {"summary" : summary}

		return jsonify(data)
	except ValueError:
		return jsonify({"error": f"Invalid parameter: '{last_n_days}', integer expected"})


@app.route("/assignment/transactionSummaryByManufacturingCity/<last_n_days>")
def transactionSummaryByManufacturingCity(last_n_days):
	"""
	returns transaction summary data of last given days
	"""
	try:
		last_n_days = int(last_n_days)

		summary = []
		last_n_day_date_time = datetime.now() - timedelta(int(last_n_days))

		for transaction in transaction_data:

			if transaction["transaction_date_time"] > last_n_day_date_time:
				summary.append({
					"city_name": product_data_map[transaction["product_id"]]["product_manufacturing_city"],
					"total_amount": transaction["transaction_amount"]
					})


		data = {"summary" : summary}

		return jsonify(data)

	except ValueError:
		return jsonify({"error": f"Invalid parameter: '{last_n_days}', integer expected"})


def readCSV():
	"""
	populates the data from csv files at when server starts/restarts
	"""

	with open('ProductReference.csv') as csv_file:
	    data_ = csv.reader(csv_file, delimiter=',')
	    first_line = True
	    for row in data_:
	      	if not first_line:
		        product_data.append({
		          "product_id": row[0],
		          "product_name": row[1],
		          "product_manufacturing_city": row[2]
		        })
	      	else:
	        	first_line = False
	with open('Transaction_20180101101010.csv') as csv_file:
	    data_ = csv.reader(csv_file, delimiter=',')
	    first_line = True
	    for row in data_:
	      	if not first_line:
		        transaction_data.append({
		          "transaction_id": row[0],
		          "product_id": row[1],
		          "transaction_amount": row[2],
		          "transaction_date_time": datetime.strptime(row[3], '%d/%m/%Y %H:%M')  # row[3]
		        })
	      	else:
	        	first_line = False

def make_product_map():
	"""
	populates a map, useful in getting indexed product data by its Id
	"""

	for product in product_data:
		if product["product_id"] not in product_data_map:
			product_data_map[product["product_id"]] = product


if __name__ == '__main__':
	readCSV()
	make_product_map()
	app.run(host='localhost', port=5000)
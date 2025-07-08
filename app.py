from salesorderdetails.getsalesorderdetails import getbySalesOrderID

# Sales ID Tracker
@app.route('/getbySalesOrderId', methods=['GET'])
def getbySalesbyOrderId():
    # Get query parameters
    salesorderid = request.args.get('salesorderid')
    tableformat = request.args.get('tableformat')

    try:
        if salesorderid and tableformat:
            salesorderdetails = getbySalesOrderID(salesorderid=salesorderid,format_type=tableformat)
            salesorderdetails = json.loads(salesorderdetails)
            return jsonify(salesorderdetails), 200
        else:
            return jsonify({"error": "Error: Please Provide Inputs salesorderid and tableformat (grid or export)"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to the GraphQL endpoint. Error: {e}"}), 500

import httpx
 
FID ="https://keysphereservice-amer.usl-sit-r2-np.kob.dell.com/findby"
FOID="https://fulfilmentorder-amer.usl-sit-r2-np.kob.dell.com/fulfillmentorderdata"
# Replace with your actual API URL
API_URL = "https://salesorderheaderfulfillment-amer.usl-sit-r2-np.kob.dell.com/soheader"

salesorder_query = """
query MyQuery {
  getBySalesorderids(salesorderIds: "1004543337") {
    result {
      fulfillment {
        fulfillmentId
      }
      salesOrder {
        salesOrderId
        buid
        region
      }
      workOrders {
        woId
      }
      fulfillmentOrders {
        foId
      }
      asnNumbers {
        snNumber
      }
    }
  }
}
"""
soaorder_query = """
query MyQuery {
  getSoheaderBySoids(salesOrderIds: "1004543337") {
    buid
    ppDate
  }
}
"""

# foid_query = """
# query MyQuery($foId: String!) {
#   getAllFulfillmentHeadersByFoId(foId: $foId) {
#     foId
#     forderline {
#       shipFromFacility
#       shipToFacility
#     }
#   }
# }
# """


def post_api(URL, query, variables):
    if variables:
        response = httpx.post(API_URL, json={"query": query, "variables": variables}, verify=False)
    else:
        response = httpx.post(URL, json={"query": query}, verify=False)
    print(response.json())
    return response.json()

 
def transform_keys(data):
    def convert(key):
        parts = key.split("_")
        return ''.join(part.capitalize() for part in parts)
    return {convert(k): v for k, v in data.items()}
   
def fetch_and_clean():
    # response = httpx.get(API_URL, verify=False)
    # response = httpx.post(API_URL, json={"query": query}, verify=False)
    # print(response.json())
    # exit()



    # fullfillment=post_api(API_URL=FID, query=fullfilmentquery_query)
    soaorder=post_api(URL=API_URL, query=soaorder_query, variables=None)

    salesorder=post_api(URL=FID, query=salesorder_query, variables=None)

    result_list = salesorder.get("data", {}).get("getBySalesorderids", {}).get("result", [])

    if result_list:
        #fetch
        fulfillment = result_list[0].get("fulfillment", {})
        fulfillment_id = fulfillment.get("fulfillmentId")

        if fulfillment_id:
            print(f"Fulfillment ID found: {fulfillment_id}")
            fulfillment_query = """
            query MyQuery($fulfillment_id: String!) {
            getFulfillmentsById(fulfillmentId: $fulfillment_id) {
                soHeaderRef
                fulfillments {
                systemQty
                shipByDate
                salesOrderLines {
                    lob
                }
                }
            }
            }
            """
            variables = {"fulfillment_id": fulfillment_id}
            salesorder=post_api(URL=API_URL, query=fulfillment_query, variables=variables)
        else:
            print("Fulfillment ID is missing or null.")
        
        #fetch
        fulfillment_orders = result_list[0].get("fulfillmentOrders", [])
        print(fulfillment_orders)
        if fulfillment_orders and fulfillment_orders[0].get("foId"):
            foId = fulfillment_orders[0]["foId"]
            print("foId found:", foId)
            foid_query = """
            query MyQuery($foId: String!) {
            getAllFulfillmentHeadersByFoId(foId: $foId) {
                foId
                forderline {
                shipFromFacility
                shipToFacility
                }
            }
            }
            """            
            varss = {"foId": foId}
            foid_output=post_api(URL='https://fulfilmentorder-amer.usl-sit-r2-np.kob.dell.com/fulfillmentorderdata', query=foid_query, variables=varss)
        else:
            print("foId is missing or null.")

    else:
        print("No results found.")
    exit()

    # raw_data = response.json()
    # response.raise_for_status()
    # print(raw_data)

    # If response is a list of objects
    if isinstance(raw_data, list):
        return [transform_keys(item) for item in raw_data]
    elif isinstance(raw_data, dict):
        return transform_keys(raw_data)
    else: return raw_data
    # unexpected
    # Run the function
if __name__ == "__main__":
    cleaned = fetch_and_clean()
    print(cleaned)

import httpx
 
# Replace with your actual API URL
API_URL = "https://salesorderheaderfulfillment-amer.usl-sit-r2-np.kob.dell.com/soheader"
 
def transform_keys(data):
    def convert(key): parts = key.split("_")
        return ''.join(part.capitalize() for part in parts)
    return {convert(k): v for k, v in data.items()}
   
def fetch_and_clean():
    response = httpx.get(API_URL)
    response.raise_for_status()
    raw_data = response.json()
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

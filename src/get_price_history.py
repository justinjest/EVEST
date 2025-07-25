import requests

# Tritanium = type_id 34
# The Forge = region_id 10000002
def get_price_history(type_id=34, region_id=10000002):
    url = f"https://esi.evetech.net/latest/markets/{region_id}/history/?type_id={type_id}"
    response = requests.get(url)

    if response.status_code == 200:
        history = response.json()
        return history
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    data = get_price_history()

    if data:
        print(f"Fetched {len(data)} days of price history.")
        
        # Most recent entry (today)
        today = data[-1]
        print("\nMost recent entry:")
        print(today)

        # Calculate 30-day average price
        last_30 = data[-30:]  # Slice the last 30 days
        avg_30 = sum(day["average"] for day in last_30) / len(last_30)

        print(f"\n30-day Average Price: {avg_30:.2f} ISK")
        print(f"Today's Price: {today['average']:.2f} ISK")

        # Simple analysis
        if today["average"] < avg_30 * 0.90:
            print("It's a BUY opportunity. Price is more than 10% below average.")
        elif today["average"] > avg_30 * 1.10:
            print("It's a SELL opportunity. Price is more than 10% above average.")
        else:
            print("Hold steady. Price is within normal range.")
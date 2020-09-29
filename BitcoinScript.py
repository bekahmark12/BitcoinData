import requests
import statistics
import os
import psycopg2
import sys
import json

connection = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='horses12')
cursor = connection.cursor()

# class Bitcoin:
#     def __init__(self, url=None, closing_price=None, percent_change=None, avg_closing=None, max_price=None, min_price=None):
#         self._closing_price = closing_price
#         self._percent_change = percent_change
#         self._avg_closing = avg_closing
#         self._max_price = max_price
#         self._min_price = min_price

    # def __str__(self):
    #     return f" Closing Price: {self._closing_price} \nPercent of Change: {self._percent_change} \nAverage Closing: {self._avg_closing} \nMax Price: {self._max_price} \nMin Price: {self._min_price}"

class BitcoinAPI:
    def __init__(self, api_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start={{start_date}}&end={{end_date}}"):
        self._api_url = api_url

    def get_bitcoin_data(self):
        prices_data = []
        percent_changes = []

        start_date = input("Enter a start date (in format YYYY-MM-DD): ")
        end_date = input("Enter an end date (in format YYY-MM-DD): ")
        working_url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date}&end={end_date}"
        response = requests.get(working_url).json()
        yesterday_price = 0

        for key in response['bpi']:
            current_price = response['bpi'][key]
            print("Closing Price: " + key + " " + str(response['bpi'][key]))

            # Daily Increase/Decrease:
            delta = (current_price - yesterday_price)
            yesterday_price = current_price
            percent_change = delta / current_price
            prices_data.append(current_price)
            percent_changes.append(percent_change)
            print("Percent of Change: " + str(percent_change))

        #Total Increase/Decrease
        # total_change = sum(percent_change)
        avg_closing_price = statistics.mean(prices_data)
        prices_min = min(prices_data)
        prices_max = max(prices_data)

        # print(str(total_change))
        print(str(avg_closing_price))
        print(str(prices_min))
        print(str(prices_max))

        return response['bpi']


def main():
    api = BitcoinAPI()
    print("Powered by CoinDesk: https://www.coindesk.com/price/bitcoin")
    exit_request = 1

    while exit_request == 1:
        choice = int(input("1 to see bitcoin data \n2 to exit"))
        if choice == 1:
            if sys.argv[1] == "-cache=db":
                bitcoin_data = api.get_bitcoin_data()
                database(bitcoin_data)
            elif sys.argv[1]== "-cache=file":
                content = api.get_bitcoin_data()
                file(content)
            elif sys.argv[1] == "-cache=none":
                none()
            elif sys.argv[1] != "-cache=none" or "-cache=file" or "-cache=db":
                bitcoin_data = api.get_bitcoin_data()
                database(bitcoin_data)
            else:
                exit_request = 0
                connection.close()
        else:
            exit(0)

def database(bitcoin_list):
    sql = """INSERT INTO bitcoin_data (bitcoin_date, closing_price)
            VALUES  ((%s), (%s))"""
    print(bitcoin_list)
    for key, value in bitcoin_list.items():
        cursor.execute(sql, (str(key), str(value)))
    connection.commit()

def file(content):
    # try:
    #     file = open('bitcoin.json', 'r')
    #     previous_content = json.loads(file.read())
    #     file.close()
    # 
    #     previous_content.extend(content)
    # 
    #     file = open('bitcoins.json', 'w')
    # 
    #     file.write(json.dumps(previous_content))
    #     file.close()
    file = open('bitcoins.json', 'w')
    file.write(json.dumps(content))
    file.close()

def none():
    pass

main()


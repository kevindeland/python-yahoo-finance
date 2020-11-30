## Yahoo Finance HTML Scraper

from bs4 import BeautifulSoup
import requests
import pandas as pd


BASEURL = "https://finance.yahoo.com/quote"

def getFinancials(ticker):
    
    # print('--------------------')
    # print(ticker)
    # print('--------------------')
    
    financials = "financials"
    financialsCI = requests.get("{}/{}/{}".format(BASEURL, ticker, financials))
    
    financialsContent = financialsCI.content
    soup = BeautifulSoup(financialsContent, features="html.parser")

    totalRevenue = soup.find("div", {"data-test": "fin-col"})
    labelsRow = soup.find("div", {"class": "D(tbr)"})

    labelsColumns = labelsRow.children
    # print(labelsColumns)

    data = []
    labels = []
    for col in labelsColumns:
        labels.append(col.text)

    dataTable = soup.find("div", {"class": "D(tbrg)"})
    dataRow = dataTable.find_all("div", {"data-test": "fin-row"})
    for row in dataRow:
        drow = []
        row2 = row.find("div", {"class": "D(tbr)"})

        ## Here is a loop inside of a loop
        for cell in row2:
            drow.append(cell.text)

        data.append(drow)

    df = pd.DataFrame(data,columns=labels)

    return df


def getKeyStatistics(ticker):

    response = requests.get("{}/{}/{}".format(BASEURL, ticker, "key-statistics"))
    content = response.content
    soup = BeautifulSoup(content, features="html.parser")

    table = soup.find("table", {"class": "D(itb)"})
    thead = table.find("thead")

    ## firstTable = soup.find("table")
    print(thead)
    


tickers = ["CI", "UNH", "ANTM", "CNC", "HCA"]

tickerDFs = []

getKeyStatistics("CI")

import sys
sys.exit()
for t in tickers:
    df = getFinancials(t)

    f = open("data/{}.csv".format(t), "a")
    f.write(df.to_csv())
    f.close()
    ## print(df.to_csv())


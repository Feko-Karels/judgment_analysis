import requests
from bs4 import BeautifulSoup

#Hier Daten angeben
FROM_YEAR = 2000
UNTIL_YEAR = 2022
UNTIL_MONTH = 8    #Nur beendete Monate


BASE_URL = "https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en"  # &Datum=2022-1&Seite=0
BASE_URL_URTEIL = "https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/"

links = []
#Erstelle Request Links für Seiten
for year in range(FROM_YEAR, UNTIL_YEAR+1):
    url_year = BASE_URL + "&Datum=" + str(year)
    for month in range(1, 13):

        if year == UNTIL_YEAR and month == UNTIL_MONTH +1 :
            break

        url_month = url_year + "-" + str(month)

        print(url_month)
        page = 0
        last = False
        while not last:

            url_page = url_month + "&Seite=" + str(page)

            # GET-Request ausführen
            response = requests.get(url_page)

            # BeautifulSoup HTML-Dokument aus dem Quelltext parsen
            html = BeautifulSoup(response.text, 'html.parser')

            results = html.find_all("td", class_="EAz")
            results_last = html.find_all("img", title="Letzte Seite")

            if results_last:
                last = True

            #Erstelle Request Links fuer PDF Ergebnisse
            i = 0
            for element in results:
                i += 1
                link = element.select("a")
                href = link[0]['href']
                #baue einheitlichen Dateiname
                filename = str(year)+"_"+str(month)+"_" + str(page) + "_" + str(i) + ".pdf"
                tupel = (href, filename)
                links.append(tupel)
            page += 1

print(links)

def download_pdf(url, file_name, headers):

    # Send GET request
    response = requests.get(url, headers=headers)
    # Save the PDF
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)



# Define HTTP Headers
headers = {
    "User-Agent": "Chrome/51.0.2704.103",
}

for link in links:
    url = BASE_URL_URTEIL + link[0] + "&Blank=1.pdf"
    file_name = link[1]
    download_pdf(url, file_name, headers)
    print("Downloaded: " + file_name + " from: " + url)

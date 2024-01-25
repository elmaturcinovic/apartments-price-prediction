from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import unicodedata
import time
import pandas as pd
import numpy as np

# Funkcija koja simbole "✓" iz podataka iz oglasa pretvara u Boolean vrijednost
def value(attr):
    if attr == "✓":
        return True
    else:
        return False

# Inicijalizacija Safari WebDriver-a
driver = webdriver.Safari()

URL = "https://olx.ba/pretraga?attr=313034284e616d6a65c5a174656e293a373031322850726f64616a6129&attr_encoded=1&category_id=23&listing_type=sell&canton=9&cities=&page="
stanovi_urls, data, stranice_urls = [], [], []

# Učitavanje prve stranice kako bi se dobio podatak o broju stranica(pages) kroz koje će se iterirati
result = driver.get(URL + "1")
wait = WebDriverWait(driver, 10)
result_soup = BeautifulSoup(driver.page_source, "html.parser")
number_of_pages = int(result_soup.find("h1", class_="search-title").find("b").text)//40 + 1

# Iteriranje kroz stranice(pages)
for i in range(1, number_of_pages + 1):
    
    # Prikupljanje url-ova oglasa sa i-te stranice
    urls_per_page = []
    result = driver.get(URL + str(i))
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    result_soup = BeautifulSoup(driver.page_source, "html.parser")
    
    cards = result_soup.find("div", class_="articles sm:px-md sm:pt-md md:grid-mobile lg:grid-desktop-md xl:grid-desktop up:grid-desktop sm:grid-mobile").find_all("div", class_="w-full flex cardd")
    for card in cards:
        url_item = card.find("a")["href"]
        urls_per_page.append(url_item)
    
    # Iteriranje kroz sve oglase jedne stranice, prikupljanje i formatiranje podataka iz oglasa
    for url_item in urls_per_page:
        try:
            result = driver.get("https://olx.ba" + url_item)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "w-full")))
            result_soup = BeautifulSoup(driver.page_source, "html.parser")
            title = result_soup.find("h2", class_="main-title-listing").text if result_soup.find("h2", class_="main-title-listing") is not None else ""
            price = result_soup.find("span", class_="price-heading vat").text
            details = result_soup.find("div", class_="sm:p-md central-inner sm:pb-lg pb-xl ql-editor").text if result_soup.find("div", class_="sm:p-md central-inner sm:pb-lg pb-xl ql-editor") is not None else ""
            print(title)
            properties = {}
            props1= result_soup.find("div", class_="required-attributes mb-lg").find_all("div", class_="flex flex-col w-full")
            for prop in props1:
                prop_label = prop.find_all("td")[0].text.strip()
                prop_value = prop.find_all("td")[1].text.strip()
                properties[prop_label] = prop_value 
                print(prop_label, ": ", prop_value)
            
            props = result_soup.find("table", class_="w-full").find_all("tr")
            for prop in props:
                prop_label = prop.find_all("td")[0].text.strip()
                prop_value = prop.find_all("td")[1].text.strip()
                properties[prop_label] = prop_value 
                print(prop_label, ": ", prop_value)

            kvadratura = properties["Kvadrata"] if "Kvadrata" in properties else ""
            broj_soba = properties["Broj soba"] if "Broj soba" in properties else ""
            sprat = properties["Sprat"] if "Sprat" in properties else ""
            namjesten = properties["Opremljenost"] if "Opremljenost" in properties else ""
            vrsta_grijanja = properties["Vrsta grijanja"] if "Vrsta grijanja" in properties else ""
            stanje = properties["Stanje"] if "Stanje" in properties else ""
            vrsta_oglasa = properties["Vrsta oglasa"] if "Vrsta oglasa" in properties else ""
            adresa = properties["Adresa"] if "Adresa" in properties else ""
            kvadratura_balkona = properties["Kvadratura balkona"] if "Kvadratura balkona" in properties else ""
            godina_izgradnje = properties["Godina izgradnje"] if "Godina izgradnje" in properties else ""
            vrsta_poda = properties["Vrsta poda"] if "Vrsta poda" in properties else ""
            balkon = value(properties["Balkon"]) if "Balkon" in properties else ""
            blindirana_vrata = value(properties["Blindirana vrata"]) if "Blindirana vrata" in properties else ""
            internet = value(properties["Internet"]) if "Internet" in properties else ""
            kablovska_tv = value(properties["Kablovska TV"]) if "Kablovska TV" in properties else ""
            kanalizacija = value(properties["Kanalizacija"]) if "Kanalizacija" in properties else ""
            klima = value(properties["Klima"]) if "Klima" in properties else ""
            lift = value(properties["Lift"]) if "Lift" in properties else ""
            novogradnja = value(properties["Novogradnja"]) if "Novogradnja" in properties else ""
            struja = value(properties["Struja"]) if "Struja" in properties else ""
            voda = value(properties["Voda"]) if "Voda" in properties else ""
            tel_prikljucak = value(properties["Telefonski priključak"]) if "Telefonski priključak" in properties else ""
            datum_objave = properties["Datum objave"] if "Datum objave" in properties else ""
            primarna_orijentacija = properties["Primarna orjentacija"] if "Primarna orjentacija" in properties else ""
            uknjizeno_zk = value(properties["Uknjiženo / ZK"]) if "Uknjiženo / ZK" in properties else ""
            kucni_ljubimci = value(properties["Kućni ljubimci"]) if "Kućni ljubimci" in properties else ""
            plin = value(properties["Plin"]) if "Plin" in properties else ""
            podrum_tavan = value(properties["Podrum/Tavan"]) if "Podrum/Tavan" in properties else ""
            video_nadzor = value(properties["Video nadzor"]) if "Video nadzor" in properties else ""
            ostava_spajz = value(properties["Ostava/špajz"]) if "Ostava/špajz" in properties else ""
            alarm = value(properties["Alarm"]) if "Alarm" in properties else ""
            balkon = value(properties["Balkon"]) if "Balkon" in properties else ""
            nedavno_adaptiran = value(properties["Nedavno adaptiran"]) if "Nedavno adaptiran" in properties else ""

            data.append([title, price, kvadratura, broj_soba, sprat, namjesten, stanje, vrsta_grijanja, vrsta_oglasa, adresa, kvadratura_balkona, godina_izgradnje, vrsta_poda, balkon, blindirana_vrata, internet, kablovska_tv, kanalizacija, klima,lift,novogradnja,struja, voda, tel_prikljucak,datum_objave, primarna_orijentacija, uknjizeno_zk, kucni_ljubimci, plin, podrum_tavan, video_nadzor, ostava_spajz, alarm, balkon, nedavno_adaptiran, details])
        except:
            pass
        
# Inicijalizacija dataframe-a i eksprtovanje u .csv formatu
df = pd.DataFrame(data, columns = ['title', 'cijena', 'kvadratura', 'broj_soba', 'sprat', 'namjesten', 'stanje', 'vrsta_grijanja', 'vrsta_oglasa', 'adresa', 'kvadratura_balkona', 'godina_izgradnje', 'vrsta_poda', 'balkon', 'blindirana_vrata', 'internet', 'kablovska_tv', 'kanalizacija', 'klima', 'lift', 'novogradnja', 'struja', 'voda', 'tel_prikljucak','datum_objave', 'primarna_orijentacija', 'uknjizeno_zk', 'kucni_ljubimci', 'plin', 'podrum_tavan', 'video_nadzor', 'ostava_spajz', 'alarm', 'balkon', 'nedavno_adaptiran', 'details'])
df.to_csv('stanovi_namjesteni.csv')
    
    
    



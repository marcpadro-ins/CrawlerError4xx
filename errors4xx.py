import csv
import requests
import concurrent.futures
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtenir_urls_pagina(driver, url):
    """
    Obté totes les URLs d'una pàgina web.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    except:
        return set()
    
    enllacos = driver.find_elements(By.TAG_NAME, "a")
    return {enllac.get_attribute("href") for enllac in enllacos if enllac.get_attribute("href")}

def detectar_errors_4xx(domini, max_urls):
    """
    Explora un domini de manera recursiva i detecta errors 4XX amb paral·lelisme.
    """
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Mode sense interfície per ser més ràpid
    driver = webdriver.Firefox(options=options)

    urls_visitades = set()
    errors_4xx = []
    domini_base = urlparse(domini).netloc

    session = requests.Session()  # Ús d'una sessió per optimitzar les peticions

    def rastrejar(url, origen):
        if url in urls_visitades or len(urls_visitades) >= max_urls:
            return

        urls_visitades.add(url)
        print(f"[🔍] Explorant: {url} ({len(urls_visitades)}/{max_urls})")

        try:
            resposta = session.get(url, timeout=5)
            codi = resposta.status_code

            if 400 <= codi < 500:
                print(f"[❌] Error {codi} en {url}")
                errors_4xx.append((url, codi, origen))
            
            if codi == 200 and urlparse(url).netloc == domini_base:
                noves_urls = obtenir_urls_pagina(driver, url)
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [executor.submit(rastrejar, nova_url, url) for nova_url in noves_urls if len(urls_visitades) < max_urls]
                    concurrent.futures.wait(futures)
        
        except requests.RequestException as e:
            print(f"[⚠️] No es pot accedir a {url}: {e}")
    
    rastrejar(domini, "INICI")
    driver.quit()
    return errors_4xx


def generar_informe(errors_4xx, nom_fitxer="informe_errors.csv"):
    """
    Genera un fitxer CSV amb els errors 4XX detectats.
    """
    with open(nom_fitxer, mode="w", newline="", encoding="utf-8") as fitxer:
        escritor = csv.writer(fitxer)
        escritor.writerow(["URL amb error", "Codi d'error HTTP", "Pàgina d'origen"])
        escritor.writerows(errors_4xx)
    print(f"\n✅ Informe generat: {nom_fitxer}")

# 🔹 Executar el crawler
domini = "https://www.vidalibarraquer.net/"
max_urls = 50  # Nombre màxim de URLs a explorar
errors_trobats = detectar_errors_4xx(domini, max_urls)
generar_informe(errors_trobats)
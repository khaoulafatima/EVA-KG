from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


def scrape_pdf_html(url: str, download_dir: str = None, pdf_dir: str = None, html_dir: str = None,
                    wait_second: float = 2) -> bool:
    """
    :param url: collegamento della risorsa sul sito https://hudoc.echr.coe.int/eng
    :param download_dir: directory in cui salvare i file.
        Se non viene specificata una cartella differente per pdf e html vengono create le caretelle pdf e html
        In generale è consigliato specificare una cartella diversa per i pdf e gli html
    :param pdf_dir: directory in cui salvare i pdf
    :param html_dir: directory in cui salvare gli html
    :param wait_second: secondi di attesa tra un'operazione e l'altra.
        Utile per evitare errori dovuti a connessione lenta e tempo di caricamento in generale
    :return: True se il è andato tutto a buon fine, False altrimenti
    """
    if "https://hudoc.echr.coe.int/eng" not in url:
        print("URL non valido")
        return False

    if pdf_dir is None:
        pdf_dir = download_dir + "/pdf"
    if html_dir is None:
        html_dir = download_dir + "/html"

    if not os.path.isdir(pdf_dir):
        os.mkdir(pdf_dir)
    if not os.path.isdir(html_dir):
        os.mkdir(html_dir)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.abspath(pdf_dir),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    driver = None

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(wait_second)

        pdf_xpath = "//*[@id=\"pdfbutton\"]"
        element = driver.find_element(By.XPATH, pdf_xpath)
        time.sleep(wait_second)
        element.click()

        time.sleep(wait_second)
        file_name = max([pdf_dir + "/" + f for f in os.listdir(pdf_dir)], key=os.path.getctime)
        if "/null.htm" in file_name:
            raise Exception("File non scaricato")
        file_name = file_name.replace("\\", "/")
        file_name = file_name.split("/")[-1]
        file_name = file_name.replace(".pdf", "")

        cd_xpath = "//*[@id=\"notice\"]/a/div[2]"
        element = driver.find_element(By.XPATH, cd_xpath)
        element.click()
        time.sleep(wait_second)

        page_source = driver.page_source
        if page_source is not None:
            with open(html_dir + "/" + file_name + ".html", "w", encoding="utf-8") as f:
                f.write(page_source)

        driver.quit()
        return True

    except Exception as e:
        if os.path.isfile(pdf_dir + "/null.htm"):
            os.remove(pdf_dir + "/null.htm")
        if os.path.isfile(html_dir + "/null.htm.html"):
            os.remove(html_dir + "/null.htm.html")

        if "max" not in str(e):
            print(e)

        if wait_second <= 32:
            print("Retrying")
            if driver is not None:
                driver.quit()
            scrape_pdf_html(url, download_dir, pdf_dir, html_dir, wait_second * 2)
        return False

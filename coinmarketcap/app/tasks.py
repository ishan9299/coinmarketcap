from celery import shared_task

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@shared_task
def getData(name):
    driver = webdriver.Chrome()
    url = "https://coinmarketcap.com/currencies/" + name + "/"
    driver.get(url)
    
    price = driver.find_element(By.XPATH, "//span[@class='sc-d1ede7e3-0 fsQm base-text']")
    price_change = driver.find_element(By.XPATH, "//p[@class='sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI']")
    
    body = driver.find_element(By.XPATH, "//div[@class='sc-d1ede7e3-0 bwRagp']")
    js_code = r'''
    dde = document.querySelectorAll(".sc-d1ede7e3-0.hPHvUM.base-text");
    stats = [];
    dde.forEach((element) => {
      let length = element.childNodes.length;
      if (length === 2) {
        stats.push(element.childNodes[1].textContent);
      }
      if (length === 1) {
        stats.push(element.childNodes[0].textContent);
      }
    });
    
    return stats;
    '''
    stats = driver.execute_script(js_code);
    
    market_cap_rank = driver.find_element(By.XPATH, "//*[@id='section-coin-stats']/div/dl/div[1]/div[2]/div/span")
    contracts = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div/a/span[1]")
    address = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div/a/span[2]")
    links = driver.find_elements(By.XPATH, "//div[@class='sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf']")

    url = []
    for link in links:
        url.append(link.find_element(By.TAG_NAME, "a").get_attribute("href"))

    output = {}
    output["price"] = price.text
    output["price_change"] = price_change.text
    output["market_cap"] = stats[0]
    output["volume"] = stats[1]
    output["volume_change"] = stats[2]
    output["circulating_supply"] = stats[3]
    output["total_supply"] = stats[4]
    output["diluted_market_cap"] = stats[6]
    output["contracts"] = [{ "name": contracts.text, "address": address.text }]
    output["official_links"] = [{ "name": "website", "link": url[0]}]
    output["socials"] = [
            { "name": "twitter", "link": url[1] },
            { "name": "telegram", "link": url[2] }
    ]
    
    driver.close()

    return output

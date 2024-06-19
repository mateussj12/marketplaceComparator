import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from misc.imports import *
from web_driver.drivers import get_driver

def send_keys_slowly(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def scrape_americanas():
    browsers = ["firefox", "edge", "chrome"]
    url = "https://www.americanas.com.br"
    driver = None

    for browser in browsers:
        try:
            driver = get_driver(browser, url)
            driver.get(url)
            driver.save_screenshot("pagina_inicial.png")
            
            time.sleep(3)
            
            try:
                    popups = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@target='_blank']"))
                    )

                    if popups:
                        fechar_popup = driver.find_element(By.XPATH, "//a[@class='styles__CloseButton-sc-1yh2j4k-1 iwYXw']")
                        fechar_popup.click()

                    driver.save_screenshot("pagina_inicial_sempoup.png")

            except NoSuchElementException as e:
                print(f"Erro ao lidar com o popup: {e}")

            search_box = driver.find_element(By.XPATH, "//input[@aria-label='Pesquisar']")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            
            time.sleep(1)
            
            search_box.submit()

            time.sleep(3)  # Aguarda o carregamento da página
            products = []

            driver.save_screenshot("pagina_pesquisa.png")

            try:
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col__StyledCol']"))
                )
            except TimeoutException:
                print(f"Timeout ao aguardar elementos com o navegador {browser}. Tentando com o próximo navegador.")
                if driver:
                    driver.quit()
                continue  # Tentar próximo navegador

            if not elements:
                print(f"Nenhum elemento encontrado com o navegador {browser}. Tentando com o próximo navegador.")
                if driver:
                    driver.quit()
                continue

            for element in elements:
                try:
                    name = element.find_element(By.XPATH, ".//h3[@class='product-name']")
                    price = element.find_element(By.XPATH, ".//span[@class='sales-price']")
                    link = element.find_element(By.XPATH, ".//a[@class='inStockCard__Link-sc-1ngt5zo-1']")
                    

                    name = name.text.strip()
                    price = price.text.strip().replace(",", ".")
                    link = element.get_attribute("href")

                    products.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "store": "Americanas"
                    })
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Erro ao extrair dados de um item: {e}")

            if products:
                return products  # Retornar produtos se encontrados

            print(f"Nenhum produto encontrado com o navegador {browser}. Tentando com o próximo navegador.")
            
            if driver:
                driver.quit()
            continue

        except (WebDriverException, ValueError) as e:
            print(f"Erro com o navegador {browser}: {e}")
            if driver:
                driver.quit()
            continue  # Tentar próximo navegador

    print("Nenhum produto encontrado com nenhum dos navegadores.")
    return []


def main():
    try:
        # Realiza o scraping de cada site
        #mercado_livre_products = scrape_mercado_livre()
        #magalu_products = scrape_magalu()
        americanas_products = scrape_americanas()
        #madeira_madeira_products = scrape_madeira_madeira()
        #shopee_products = scrape_shopee()
        #kabum_products = scrape_kabum()
        #leroy_merlin_products = scrape_leroy_merlin()

        # Unir todos os produtos coletados
        all_products = []
        #all_products.extend(mercado_livre_products)
        #all_products.extend(magalu_products)
        all_products.extend(americanas_products)
        #all_products.extend(madeira_madeira_products)
        #all_products.extend(shopee_products)
        #all_products.extend(kabum_products)
        #all_products.extend(leroy_merlin_products)

        # Criar um DataFrame com os resultados
        df = pd.DataFrame(all_products)
        df.to_csv("marketplace_products.csv", index=False)
        print("Dados coletados e salvos em marketplace_products.csv")

    except Exception as e:
        print(f"Erro durante a execução do scraping: {e}")

if __name__ == "__main__":
    main()
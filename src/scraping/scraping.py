import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from misc.imports import *
from web_driver.drivers import *

def send_keys_slowly(element, text, delay=0.1):
    """ Função para enviar texto com atraso entre os caracteres. """
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def scrape_mercado_livre():
    browsers = ["firefox", "edge", "chrome"]
    driver = None

    for browser in browsers:
        try:
            driver = get_driver(browser)
            driver.get("https://www.mercadolivre.com.br")
            driver.save_screenshot("pagina_inicial.png")
            
            time.sleep(3)
            
            search_box = driver.find_element(By.CSS_SELECTOR, ".nav-search-input")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            time.sleep(1)
            search_box.submit()

            time.sleep(3)  # Aguarda o carregamento da página
            products = []

            driver.save_screenshot("pagina_pesquisa.png")

            try:
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
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
                    name = element.find_element(By.CSS_SELECTOR, ".ui-search-item__title")
                    price = element.find_element(By.CSS_SELECTOR, ".ui-search-price__part")
                    link = element.find_element(By.CSS_SELECTOR, "a")
                    

                    name = name.text.strip()
                    price = price.text.strip().replace(",", ".")
                    link = element.get_attribute("href")

                    products.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "store": "Mercado Livre"
                    })
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Erro ao extrair dados de um item: {e}")

            if products:
                del elements
                driver.quit()
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
       
    if driver:
        del elements
        driver.quit()

    print("Nenhum produto encontrado com nenhum dos navegadores.")
    return []


def scrape_magalu():
    browsers = ["firefox", "edge", "chrome"]
    driver = None

    for browser in browsers:
        try:
            driver = get_driver(browser)
            driver.get("https://www.magazineluiza.com.br")
            driver.save_screenshot("pagina_inicial.png")
            
            time.sleep(3)
            
            search_box = driver.find_element(By.XPATH, "//input[@type='search']")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            time.sleep(1)
            search_box.submit()

            time.sleep(3)  # Aguarda o carregamento da página
            products = []

            driver.save_screenshot("pagina_pesquisa.png")

            try:
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@data-testid='product-card-container']"))
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
                    name = element.find_element(By.XPATH, ".//h2[@data-testid='product-title']")
                    price = element.find_element(By.XPATH, ".//p[@data-testid='price-value']")
                    

                    name = name.text.strip()
                    price = price.text.strip().replace(",", ".")
                    link = element.get_attribute("href")

                    products.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "store": "Magazine Luiza"
                    })
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Erro ao extrair dados de um item: {e}")

            if products:
                del elements
                driver.quit()
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

    if driver:
        del elements
        driver.quit()
    
    print("Nenhum produto encontrado com nenhum dos navegadores.")
    
    return []


def scrape_madeira_madeira():
    browsers = ["firefox", "edge", "chrome"]
    url = "https://www.madeiramadeira.com.br"
    driver = None

    for browser in browsers:

        try:
            driver = get_driver(browser)
            driver.get(url)
            
            time.sleep(3)

            driver.save_screenshot("pagina_inicial.png")

            search_box = driver.find_element(By.XPATH, "//input[@class='shopee-searchbar-input__input']")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            
            time.sleep(1)
            
            search_box.submit()

            time.sleep(5)  # Aguarda o carregamento da página
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

def scrape_kabum():
    browsers = ["firefox", "edge", "chrome"]
    url = "https://www.kabum.com.br"
    driver = None

    for browser in browsers:

        try:
            driver = get_driver(browser)
            driver.get(url)
            
            time.sleep(3)

            driver.save_screenshot("pagina_inicial.png")

            search_box = driver.find_element(By.XPATH, "//input[@class='id_search_input']")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            
            time.sleep(1)
            
            search_box.submit()

            time.sleep(5)  # Aguarda o carregamento da página
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

def scrape_leroy_merlin():
    browsers = ["firefox", "edge", "chrome"]
    url = "https://www.leroymerlin.com.br"
    driver = None

    for browser in browsers:

        try:
            driver = get_driver(browser)
            driver.get(url)
            
            time.sleep(3)

            driver.save_screenshot("pagina_inicial.png")

            search_box = driver.find_element(By.XPATH, "//input[@type='search']")
            send_keys_slowly(search_box, "Apple iPhone 15", delay=0.1)
            
            time.sleep(1)
            
            search_box.submit()

            time.sleep(5)  # Aguarda o carregamento da página
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
        mercado_livre_products = scrape_mercado_livre()
        magalu_products = scrape_magalu()
        madeira_madeira_products = scrape_madeira_madeira()
        kabum_products = scrape_kabum()
        leroy_merlin_products = scrape_leroy_merlin()

        # Unir todos os produtos coletados
        all_products = []
        all_products.extend(mercado_livre_products)
        all_products.extend(magalu_products)
        all_products.extend(madeira_madeira_products)
        all_products.extend(kabum_products)
        all_products.extend(leroy_merlin_products)

        # Criar um DataFrame com os resultados
        df = pd.DataFrame(all_products)
        df.to_csv("marketplace_products.csv", index=False)
        print("Dados coletados e salvos em marketplace_products.csv")

    except Exception as e:
        print(f"Erro durante a execução do scraping: {e}")

if __name__ == "__main__":
    main()
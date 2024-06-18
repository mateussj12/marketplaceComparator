import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from misc.imports import *
from web_driver.drivers import get_driver

def send_keys_slowly(element, text, delay=0.1):
    """ Função para enviar texto com atraso entre os caracteres. """
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def scrape_mercado_livre():
    browsers = ["chrome", "firefox", "edge"]
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
    browsers = ["chrome", "firefox", "edge"]
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


'''
def scrape_americanas():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.americanas.com.br")
        search_box = driver.find_element(By.CSS_SELECTOR, "#h_search-input")
        search_box.send_keys("Apple iPhone 15")
        search_box.submit()

        time.sleep(5)  # Aguarda o carregamento da página
        products = []

        # Exemplo de extração de dados (adapte conforme a estrutura HTML atual do site)
        elements = driver.find_elements_by_css_selector(".product-grid-item")

        for element in elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, ".product-title").text
                price = element.find_element(By.CSS_SELECTOR, ".price").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "store": "Americanas"
                })
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Erro ao extrair dados de um item: {e}")

        return products

    except TimeoutException:
        print("Timeout ao tentar carregar a página da Americanas")
        return []

    except Exception as e:
        print(f"Erro durante o scraping da Americanas: {e}")
        return []

    finally:
        driver.quit()


def scrape_madeira_madeira():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.madeiramadeira.com.br")
        search_box = driver.find_element(By.CSS_SELECTOR, ".campoBusca")
        search_box.send_keys("Apple iPhone 15")
        search_box.submit()

        time.sleep(5)  # Aguarda o carregamento da página
        products = []

        # Exemplo de extração de dados (adapte conforme a estrutura HTML atual do site)
        elements = driver.find_elements_by_css_selector(".nm-product-item")

        for element in elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, ".nm-product-name").text
                price = element.find_element(By.CSS_SELECTOR, ".nm-price-value").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "store": "MadeiraMadeira"
                })
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Erro ao extrair dados de um item: {e}")

        return products

    except TimeoutException:
        print("Timeout ao tentar carregar a página da MadeiraMadeira")
        return []

    except Exception as e:
        print(f"Erro durante o scraping da MadeiraMadeira: {e}")
        return []

    finally:
        driver.quit()

def scrape_shopee():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.shopee.com.br")
        search_box = driver.find_element(By.CSS_SELECTOR, ".shopee-searchbar-input__input")
        search_box.send_keys("Apple iPhone 15")
        search_box.submit()

        time.sleep(5)  # Aguarda o carregamento da página
        products = []

        # Exemplo de extração de dados (adapte conforme a estrutura HTML atual do site)
        elements = driver.find_elements_by_css_selector(".shop-search-result-view__item")

        for element in elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, ".shop-search-result-view__item-title").text
                price = element.find_element(By.CSS_SELECTOR, ".shop-search-result-view__item-price").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "store": "Shopee"
                })
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Erro ao extrair dados de um item: {e}")

        return products

    except TimeoutException:
        print("Timeout ao tentar carregar a página do Shopee")
        return []

    except Exception as e:
        print(f"Erro durante o scraping do Shopee: {e}")
        return []

    finally:
        driver.quit()

def scrape_kabum():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.kabum.com.br")
        search_box = driver.find_element(By.CSS_SELECTOR, ".sprocura")
        search_box.send_keys("Apple iPhone 15")
        search_box.submit()

        time.sleep(5)  # Aguarda o carregamento da página
        products = []

        # Exemplo de extração de dados (adapte conforme a estrutura HTML atual do site)
        elements = driver.find_elements_by_css_selector(".sc-fjdhpX")

        for element in elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, ".sc-TOsTZ").text
                price = element.find_element(By.CSS_SELECTOR, ".sc-EHOjeM").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "store": "Kabum"
                })
            except (NoSuchElementException, StaleElementReferenceException) as e:
                 print(f"Erro ao extrair dados de um item: {e}")

        return products

    except TimeoutException:
        print("Timeout ao tentar carregar a página do Kabum")
        return []

    except Exception as e:
        print(f"Erro durante o scraping do Kabum: {e}")
        return []

    finally:
        driver.quit()

def scrape_leroy_merlin():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.leroymerlin.com.br")
        search_box = driver.find_element(By.CSS_SELECTOR, ".lm-search__input")
        search_box.send_keys("Apple iPhone 15")
        search_box.submit()

        time.sleep(5)  # Aguarda o carregamento da página
        products = []

        # Exemplo de extração de dados (adapte conforme a estrutura HTML atual do site)
        elements = driver.find_elements_by_css_selector(".product-item")

        for element in elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, ".product-name").text
                price = element.find_element(By.CSS_SELECTOR, ".product-price").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "store": "Leroy Merlin"
                })
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Erro ao extrair dados de um item: {e}")

        return products

    except TimeoutException:
        print("Timeout ao tentar carregar a página da Leroy Merlin")
        return []

    except Exception as e:
        print(f"Erro durante o scraping da Leroy Merlin: {e}")
        return []

    finally:
        driver.quit()
'''

def main():
    try:
        # Realiza o scraping de cada site
        mercado_livre_products = scrape_mercado_livre()
        magalu_products = scrape_magalu()
        #americanas_products = scrape_americanas()
        #madeira_madeira_products = scrape_madeira_madeira()
        #shopee_products = scrape_shopee()
        #kabum_products = scrape_kabum()
        #leroy_merlin_products = scrape_leroy_merlin()

        # Unir todos os produtos coletados
        all_products = []
        all_products.extend(mercado_livre_products)
        all_products.extend(magalu_products)
        #all_products.extend(americanas_products)
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
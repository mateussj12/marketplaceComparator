import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from misc.imports import *

def get_driver(browser, url):
    
    user_agents = {
    'firefox': UserAgent().firefox,
    'chrome': UserAgent().chrome,
    'edge': UserAgent().edge
    }


    for browser, user_agent in user_agents.items():
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
    
        print(f'{browser} - Status Code: {response.status_code}')
    
        if response.status_code == 200:
            print(f'{browser} - Requisição bem-sucedida!')
            # Aqui você pode processar a resposta
            break  # Interrompe o loop após a primeira requisição bem-sucedida

    print(f'{browser} - Erro ao fazer requisição: {response.status_code}')


    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument(f"user-agent={user_agent}")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-software-rasterizer")
        options.set_preference("general.useragent.override", user_agent)
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument(f"user-agent={user_agent}")
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
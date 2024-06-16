import json
import requests

def get_bling_products(api_key):
    url = f'https://bling.com.br/Api/v2/produtos/json?apikey={api_key}'
    response = requests.get(url)
    return response.json()['retorno']['produtos']

def analyze_prices(marketplace_prices, bling_prices):
    differences = []

    for mp_product in marketplace_prices:
        for bling_product in bling_prices:
            if mp_product['name'] == bling_product['produto']['descricao']:
                bling_price = float(bling_product['produto']['preco'])
                marketplace_price = mp_product['price']
                if marketplace_price < bling_price:
                    differences.append({
                        'name': mp_product['name'],
                        'marketplace_price': marketplace_price,
                        'bling_price': bling_price
                    })

    return differences

def main():
    with open('marketplace_prices.json', 'r') as f:
        marketplace_prices = json.load(f)

    api_key = 'YOUR_BLING_API_KEY'  # Substituir pela sua chave API do Bling
    bling_prices = get_bling_products(api_key)
    differences = analyze_prices(marketplace_prices, bling_prices)

    with open('price_differences.json', 'w') as f:
        json.dump(differences, f)

if __name__ == '__main__':
    main()
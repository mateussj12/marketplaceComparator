import requests

def check_proxy(proxy):
    """
    Verifica se um proxy está funcionando corretamente e não requer autenticação.
    Retorna True se o proxy estiver funcional e False caso contrário.
    """
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        # Realiza uma requisição GET de teste a uma URL qualquer
        response = requests.get("https://www.google.com", proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao testar o proxy {proxy}: {str(e)}")
        return False

def load_proxies_and_check(filename):
    """
    Carrega os proxies do arquivo especificado, verifica cada proxy e remove os que não funcionam ou requerem autenticação.
    Retorna a lista de proxies válidos.
    """
    valid_proxies = []
    
    with open(filename, 'r') as f:
        proxies = f.readlines()
        proxies = [proxy.strip() for proxy in proxies]

    for proxy in proxies:
        # Verifica se o proxy contém autenticação
        if '@' in proxy:
            print(f"Ignorando proxy com autenticação: {proxy}")
            continue
        
        # Testa se o proxy é funcional
        if check_proxy(proxy):
            valid_proxies.append(proxy)
        else:
            print(f"Proxy não funcional ou requer autenticação: {proxy}")

    return valid_proxies

def save_valid_proxies(filename, proxies):
    """
    Salva os proxies válidos em um novo arquivo.
    """
    with open(filename, 'w') as f:
        for proxy in proxies:
            f.write(proxy + '\n')

if __name__ == "__main__":
    input_file = 'src\\proxy\\proxies.txt'  # Nome do arquivo de entrada com os proxies
    output_file = 'src\\proxy\\valid_proxies.txt'  # Nome do arquivo de saída com os proxies válidos
    
    valid_proxies = load_proxies_and_check(input_file)
    save_valid_proxies(output_file, valid_proxies)
    
    print(f"Proxies válidos foram salvos em {output_file}")
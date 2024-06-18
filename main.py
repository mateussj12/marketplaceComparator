# main.py
import subprocess

def main():
    # Executar o script de scraping
    print("Iniciando o scraping...")
    subprocess.run(['python', 'src\\scraping\\scraping.py'])
    
    # Executar o script de análise
    print("Iniciando a análise dos dados...")
    subprocess.run(['python', 'src\\analysis\\analysis.py'])

if __name__ == '__main__':
    main()
# analyze_data.py
import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def analyze_data(df):
    # Exemplo de análise: Mostrar os primeiros 5 registros e estatísticas básicas
    print("Primeiros 5 registros:")
    print(df.head())
    
    print("\nEstatísticas Descritivas:")
    print(df.describe())

def main():
    file_path = 'marketplace_products.csv'
    df = load_data(file_path)
    analyze_data(df)

if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkthemes import ThemedStyle
from ttkwidgets.autocomplete import AutocompleteEntry

# Função para carregar dados do JSON
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para atualizar a Treeview com detalhes do produto selecionado
def update_product_details(event):
    selected_item = treeview_products.selection()[0]
    product_name = treeview_products.item(selected_item, 'text')
    product_details_text.delete('1.0', tk.END)
    
    # Encontrar o produto selecionado nos dados carregados
    selected_product = None
    for store, products in products_data.items():
        for product in products:
            if product['nome'] == product_name:
                selected_product = product
                break
        if selected_product:
            break
    
    if selected_product:
        product_details_text.insert(tk.END, f'Nome: {selected_product["nome"]}\n')
        product_details_text.insert(tk.END, f'Categoria: {selected_product["categoria"]}\n')
        
        # Inserir preços por loja
        for loja in ['Loja A', 'Loja B', 'Loja C']:
            preco = next((p['preco'] for p in products_data[loja] if p['nome'] == selected_product['nome']), '-')
            product_details_text.insert(tk.END, f'{loja}: R$ {preco:.2f}\n')
        
        product_details_text.insert(tk.END, f'Frete: {selected_product.get("frete", "Não informado")}\n')

# Função para pesquisar produtos na Treeview
def search_products(event=None):
    search_query = search_entry.get().strip().lower()
    
    # Limpar a Treeview
    treeview_products.delete(*treeview_products.get_children())
    
    # Preencher a Treeview com produtos correspondentes à pesquisa
    for store, products in products_data.items():
        for product in products:
            if search_query in product['nome'].lower():
                treeview_products.insert('', tk.END, text=product['nome'], values=(product['categoria'], 
                                                                                   get_price(product, 'Loja A'), 
                                                                                   get_price(product, 'Loja B'), 
                                                                                   get_price(product, 'Loja C')))
    
    if not treeview_products.get_children():
        messagebox.showinfo('Produto não encontrado', f'Não foram encontrados produtos que correspondem a "{search_query}".')

# Função auxiliar para obter o preço do produto por loja
def get_price(product, store):
    for p in products_data[store]:
        if p['nome'] == product['nome']:
            return p['preco']
    return '-'

# Criar a janela principal
root = tk.Tk()
root.title('Dashboard de Produtos de Marketplace')
root.geometry('1000x600')

# Criar estilo temático
style = ThemedStyle(root)
style.set_theme('breeze')  # Escolha um tema da ttkthemes

# Carregar dados do JSON
json_file_path = 'src\\base\\dados.json'  # Caminho do seu arquivo JSON
products_data = load_data_from_json(json_file_path)

# Criar frame principal dividido em esquerda e direita
frame_main = ttk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

# Criar frame esquerdo para a lista de produtos e pesquisa
frame_left = ttk.Frame(frame_main, width=300)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Criar campo de pesquisa
search_label = ttk.Label(frame_left, text='Pesquisar Produto:')
search_label.pack(pady=5)

search_entry = AutocompleteEntry(frame_left, completevalues=[product['nome'] for products in products_data.values() for product in products])
search_entry.bind('<Return>', search_products)
search_entry.pack(pady=5, padx=10, fill=tk.BOTH)

search_button = ttk.Button(frame_left, text='Pesquisar', command=search_products)
search_button.pack(pady=5)

# Criar Treeview para exibir lista de produtos
treeview_products = ttk.Treeview(frame_left, columns=('Categoria', 'Loja A', 'Loja B', 'Loja C'), show='headings', height=20)
treeview_products.heading('Categoria', text='Categoria')
treeview_products.heading('Loja A', text='Loja A')
treeview_products.heading('Loja B', text='Loja B')
treeview_products.heading('Loja C', text='Loja C')
treeview_products.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Preencher a Treeview com todos os produtos inicialmente
for store, products in products_data.items():
    for product in products:
        treeview_products.insert('', tk.END, text=product['nome'], values=(product['categoria'], 
                                                                           get_price(product, 'Loja A'), 
                                                                           get_price(product, 'Loja B'), 
                                                                           get_price(product, 'Loja C')))

# Criar frame direito para os detalhes do produto
frame_right = ttk.Frame(frame_main)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Label para detalhes do produto
label_details = ttk.Label(frame_right, text='Detalhes do Produto', font=('Helvetica', 16, 'bold'))
label_details.pack(pady=10)

# Texto para exibir detalhes do produto selecionado
product_details_text = tk.Text(frame_right, height=10, width=50, wrap=tk.WORD)
product_details_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Atualizar detalhes do produto ao selecionar na Treeview principal
treeview_products.bind('<ButtonRelease-1>', update_product_details)

# Executar a aplicação
root.mainloop()
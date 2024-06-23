import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkthemes import ThemedStyle
from ttkwidgets.autocomplete import AutocompleteEntry
import os

# Função para carregar dados do JSON
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para atualizar a Treeview com detalhes do produto selecionado
def update_product_details(event):
    selected_items = treeview_products.selection()
    if selected_items:
        selected_item = selected_items[0]
        product_name = treeview_products.item(selected_item, 'text')
        product_details_text.delete('1.0', tk.END)
        valor_zero = 0

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
            for loja in lojas:
                preco = get_price(product_name, loja)
                product_details_text.insert(tk.END, f'{loja}: {preco}\n')

            product_details_text.insert(tk.END, f'Frete: {selected_product.get("frete", "Não informado")}\n')

# Função para pesquisar produtos na Treeview
def search_products(event=None):
    search_query = search_entry.get().strip().lower()

    # Limpar a Treeview
    treeview_products.delete(*treeview_products.get_children())

    # Preencher a Treeview com produtos correspondentes à pesquisa
    listed_products = set()
    for store, products in products_data.items():
        for product in products:
            product_key = (product['nome'], product['categoria'])
            if search_query in product['nome'].lower() and product_key not in listed_products:
                values = [product['nome'], product['categoria']]
                for loja in lojas:
                    values.append(get_price(product['nome'], loja))
                treeview_products.insert('', tk.END, text=product['nome'], values=values)
                listed_products.add(product_key)

    if not treeview_products.get_children():
        messagebox.showinfo('Produto não encontrado', f'Não foram encontrados produtos que correspondem a "{search_query}".')

# Função auxiliar para obter o preço do produto por loja
def get_price(product_name, store):
    valor_zero = 0
    for product in products_data.get(store, []):
        if product['nome'] == product_name:
            preco = product['preco']
            return f"R$ {preco:.2f}"
    return f"R$ {valor_zero:.2f}"

# Função para ordenar a Treeview por uma coluna específica
def treeview_sort_column(treeview, col, reverse):
    data = [(treeview.set(item, col), item) for item in treeview.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, item) in enumerate(data):
        treeview.move(item, '', index)
    treeview.heading(col, text=f'{col.upper()} ▼' if not reverse else f'{col.upper()} ▲',
                    command=lambda: treeview_sort_column(treeview, col, not reverse))
    update_row_colors(treeview)            

# Função para ordenar a Treeview por preço específico da loja
def treeview_sort_store(treeview, store, reverse):
    data = [(get_price(treeview.item(item, 'text'), store), item) for item in treeview.get_children('')]
    data.sort(reverse=reverse, key=lambda x: float(x[0].replace('R$', '').strip()))
    for index, (val, item) in enumerate(data):
        treeview.move(item, '', index)
    treeview.heading(store, text=f'{store.upper()} ▼' if not reverse else f'{store.upper()} ▲',
                    command=lambda: treeview_sort_store(treeview, store, not reverse))
    update_row_colors(treeview)

# Função para verificar mudanças no arquivo JSON
def check_json_modifications():
    global products_data
    current_mod_time = os.path.getmtime(json_file_path)
    if current_mod_time > last_mod_time['json']:
        last_mod_time['json'] = current_mod_time
        products_data = load_data_from_json(json_file_path)
        update_autocomplete_list()
        search_products()
    root.after(1000, check_json_modifications)

# Função para atualizar a lista de autocompletar
def update_autocomplete_list():
    complete_values = [product['nome'] for store, products in products_data.items() for product in products]
    search_entry.set_completion_list(complete_values)

# Criar a janela principal
root = tk.Tk()
root.title('Sistema de Comparação de Preços')
root.geometry('1000x600')
root.state('zoomed')

# Criar estilo temático
style = ThemedStyle(root)
style.set_theme('breeze')  # Escolha um tema da ttkthemes

# Carregar dados do JSON
json_file_path = 'src\\base\\dados.json'  # Caminho do seu arquivo JSON
products_data = load_data_from_json(json_file_path)

# Identificar todas as lojas
lojas = list(products_data.keys())

# Criar frame principal dividido em esquerda e direita
frame_main = ttk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

# Criar header
frame_header = ttk.Frame(frame_main, height=50)
frame_header.pack(side=tk.TOP, fill=tk.X)

label_titulo = ttk.Label(frame_header, text='Header do Aplicativo', font=('Roboto', 16), anchor='w')
label_titulo.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X)

# Criar frame esquerdo para a lista de produtos e pesquisa
frame_left = ttk.Frame(frame_main, width=1500)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=25, pady=25)

frame_left.pack_propagate(False)

# Criar frame direito para os detalhes do produto
frame_right = ttk.Frame(frame_main, width=525)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=10, pady=10)
frame_right.pack_propagate(False)  # Impede que o frame redimensione automaticament

# Criar footer
frame_footer = ttk.Frame(frame_main, height=50)
frame_footer.pack(side=tk.BOTTOM, fill=tk.X)

# Criar campo de pesquisa
search_label = ttk.Label(frame_right, text='Pesquisar Produto:')
search_label.pack(pady=5)

# Criar campo de entrada de pesquisa com autocompletar
search_entry = AutocompleteEntry(frame_right, completevalues=[product['nome'] for store, products in products_data.items() for product in products])
search_entry.bind('<Return>', search_products)
search_entry.pack(pady=5, padx=10, fill=tk.BOTH)

search_button = ttk.Button(frame_right, text='Pesquisar', command=search_products)
search_button.pack(pady=5)


def configure_treeview_style(treeview):
    # Configurar a fonte e a altura das linhas para todos os itens da Treeview
    style = ttk.Style()
    style.configure("Treeview", font=('Roboto', 10), rowheight=30)
    
    bold_font = ('Roboto', 10, 'bold')
    style.configure("Treeview.Heading", font=bold_font)

    style.configure("Treeview.Treeview", background="#E1E1E1", fieldbackground="#E1E1E1", rowheight=25)
    style.layout("Treeview.Treeview", [('Treeitem.padding', {'sticky': 'nswe', 'children':
                [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                 ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                 ('Treeitem.text', {'side': 'left', 'sticky': ''})]})])

# Criar Treeview para exibir lista de produtos
columns = ['Nome', 'Categoria'] + lojas
treeview_products = ttk.Treeview(frame_left, columns=columns, show='headings', height=35)
treeview_products.heading('Nome', text='Nome'.upper(), command=lambda: treeview_sort_column(treeview_products, 'Nome', False))
treeview_products.heading('Categoria', text='Categoria'.upper(), command=lambda: treeview_sort_column(treeview_products, 'Categoria', False))
for loja in lojas:
    treeview_products.heading(loja, text=loja.upper(), command=lambda loja=loja: treeview_sort_store(treeview_products, loja, False))
treeview_products.pack(pady=10, padx=10, fill=tk.BOTH)

# Ajustar largura das colunas
treeview_products.column('Nome', width=150)
treeview_products.column('Categoria', width=50)
for loja in lojas:
    treeview_products.column(loja, width=50)

# Preencher a Treeview com todos os produtos inicialmente
listed_products = set()
for store, products in products_data.items():
    for i, product in enumerate(products):
        product_key = (product['nome'], product['categoria'])
        if product_key not in listed_products:
            values = [product['nome'], product['categoria']]
            for loja in lojas:
                price = get_price(product['nome'], loja)
                values.append(price)
            # Alternar cores de fundo
            tag = 'even' if (i + 1) % 2 == 0 else 'odd'
            item_id = treeview_products.insert('', tk.END, text=product['nome'], values=values, tags=(tag,))
            listed_products.add(product_key)

def update_row_colors(treeview):
    children = treeview.get_children('')
    for index, child in enumerate(children):
        tag = 'even' if (index + 1) % 2 == 0 else 'odd'
        treeview.item(child, tags=(tag,))

# Label para detalhes do produto
label_details = ttk.Label(frame_right, text='Detalhes do Produto', font=('Roboto', 16))
label_details.pack(pady=10)

# Texto para exibir detalhes do produto selecionado
product_details_text = tk.Text(frame_right, height=10, width=50, wrap=tk.WORD)
product_details_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Atualizar detalhes do produto ao selecionar na Treeview principal
treeview_products.bind('<ButtonRelease-1>', update_product_details)

# Verificar mudanças no arquivo JSON periodicamente
last_mod_time = {'json': os.path.getmtime(json_file_path)}
root.after(1000, check_json_modifications)

# Aplicar tags para alternar as cores de fundo das linhas
configure_treeview_style(treeview_products)
treeview_products.tag_configure('even', background='#F5F5F5')
treeview_products.tag_configure('odd', background='#DCDCDC')

# Executar a aplicação
root.mainloop()

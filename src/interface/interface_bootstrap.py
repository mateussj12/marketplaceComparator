import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.dialogs.dialogs import Messagebox
import json
from ttkwidgets.autocomplete import AutocompleteEntry
import os
from datetime import datetime

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
        product_details_text.delete('1.0', ttk.END)
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
            product_details_text.insert(ttk.END, 'PRODUTO: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product["nome"]}\n\n')
            product_details_text.insert(ttk.END, 'CATEGORIA: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product["categoria"]}\n\n')
            product_details_text.insert(ttk.END, 'URL: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product.get("link", "Link não informado")}\n\n')
            product_details_text.insert(ttk.END, 'FRETE: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product.get("frete", "Não informado")}\n\n')
            product_details_text.insert(ttk.END, 'VALOR MÉDIO: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product.get("media", "Valor médio não definido")}\n\n')
            product_details_text.insert(ttk.END, 'DESCRIÇÃO: ', 'bold')
            product_details_text.insert(ttk.END, f'{selected_product.get("descricao", "Descrição não informada")}\n\n')           

# Função para pesquisar produtos na Treeview
def search_products(event=None):
    search_query = search_entry.get().strip().lower()

    # Limpar a Treeview
    treeview_products.delete(*treeview_products.get_children())

    # Preencher a Treeview com produtos correspondentes à pesquisa
    listed_products = set()
    for store, products in products_data.items():
        for i, product in enumerate(products):
            product_key = (product['nome'], product['categoria'])
            if search_query in product['nome'].lower() and product_key not in listed_products:
                values = [product['nome'], product['categoria']]
                for loja in lojas:
                    values.append(get_price(product['nome'], loja))
                   # Alternar cores de fundo
                tag = 'even' if (i + 1) % 2 == 0 else 'odd'
                treeview_products.insert('', ttk.END, text=product['nome'], values=values, tags=(tag,))
                listed_products.add(product_key)

    if not treeview_products.get_children():
        ttk.messagebox.showinfo('Produto não encontrado', f'Não foram encontrados produtos que correspondem a "{search_query}".')

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

def dialog_info():
    def show_info_message():
        Messagebox.show_info(title='Sobre', 
                             parent=None, 
                             alert=True, 
                             message=
                             'Sistema de Comparação de Preços - Versão 1.0\n' 
                             'Desenvolvedor: Mateus Santos de Jesus\n'
                             'Contato: (61) 98379-0917\n' 
                             'Localidade: Brasília - DF.\n' 
                             '© 2024 Todos os direitos reservados.')
    return show_info_message 

def update_datetime_label():
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    datetime_label.config(text=now)
    root.after(1000, update_datetime_label)

# Criar a janela principal
root = ttk.Window(themename="pulse")
root.title('Sistema de Comparação de Preços')
root.geometry('1000x600')
root.state('zoomed')

# Carregar dados do JSON
json_file_path = 'src\\base\\dados.json'  # Caminho do seu arquivo JSON
products_data = load_data_from_json(json_file_path)

# Identificar todas as lojas
lojas = list(products_data.keys())

# Criar frame principal dividido em esquerda e direita
frame_main = ttk.Frame(root)
frame_main.pack(fill=ttk.BOTH, expand=True)

# Criar header button
frame_header_button = ttk.Frame(frame_main, height=50)
frame_header_button.pack(side=ttk.TOP, fill=ttk.X)

# Criar header
frame_header = ttk.Frame(frame_main, height=50)
frame_header.pack(side=ttk.TOP, fill=ttk.X)   

info_button = ttk.Button(frame_header_button, text='Sobre', command=dialog_info())
info_button.pack(side='left', padx=35, pady=15)

# Adicionar rótulo de data e hora no topo
datetime_label = ttk.Label(frame_header_button, text='', font=('Roboto', 12, 'bold'), foreground='#593196', padding=5)
datetime_label.pack(side=ttk.RIGHT, padx=15, pady=(15, 0))

# Iniciar atualização do rótulo de data e hora
update_datetime_label()

label_titulo = ttk.Label(frame_header, text='TABELA COMPARATIVA DE PREÇOS', font=('Roboto', 12, 'bold'), anchor='w')
label_titulo.pack(side=ttk.LEFT, padx=35, pady=(5, 3), fill=ttk.X)

# Criar frame esquerdo para a lista de produtos e pesquisa
frame_left = ttk.Frame(frame_main, width=1350)
frame_left.pack(side=ttk.LEFT, fill=ttk.BOTH, padx=(35, 0), pady=(10, 15))
frame_left.pack_propagate(False)

# Criar frame direito para os detalhes do produto
frame_right = ttk.Frame(frame_main, width=675)
frame_right.pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=False, padx=(0, 10), pady=10)
frame_right.pack_propagate(False)  # Impede que o frame redimensione automaticamente

# Criar footer
frame_footer = ttk.Frame(root, height=50)
frame_footer.pack(side=ttk.BOTTOM, fill=ttk.X)

# Configurar expansão das células
frame_footer.grid_columnconfigure(0, weight=1)

# Configurar a fonte e a altura das linhas para todos os itens da Treeview
style = ttk.Style()
style.configure("Treeview", font=('Roboto', 10), rowheight=30)
    
bold_font = ('Roboto', 10, 'bold')
style.configure("Treeview.Heading", font=bold_font)

# Criar campo de pesquisa
search_label = ttk.Label(frame_right, text='PESQUISAR PRODUTO: ', font=('roboto', 10, 'bold'))
search_label.grid(row=0, column=0, padx=0, pady=(0, 10))

# Criar campo de entrada de pesquisa com autocompletar
search_entry = AutocompleteEntry(frame_right, completevalues=[product['nome'] for store, products in products_data.items() for product in products])
search_entry.bind('<Return>', search_products)
search_entry.grid(row=0, column=1, padx=0, pady=(0, 10), ipadx=60, ipady=0)

search_button = ttk.Button(frame_right, text='Pesquisar', command=search_products)
search_button.grid(row=0, column=2, padx=10, pady=(0, 10))

# Criar Treeview para exibir lista de produtos
columns = ['Produto', 'Categoria'] + lojas
treeview_products = ttk.Treeview(frame_left, columns=columns, show='headings', height=35)
treeview_products.heading('Produto', text='Produto'.upper(), command=lambda: treeview_sort_column(treeview_products, 'Produto', False))
treeview_products.heading('Categoria', text='Categoria'.upper(), command=lambda: treeview_sort_column(treeview_products, 'Categoria', False))
for loja in lojas:
    treeview_products.heading(loja, text=loja.upper(), command=lambda loja=loja: treeview_sort_store(treeview_products, loja, False))
treeview_products.pack(pady=0, padx=0, fill=ttk.BOTH)

# Ajustar largura das colunas
treeview_products.column('Produto', width=100, anchor="w")
treeview_products.column('Categoria', width=50, anchor="w")
for loja in lojas:
    treeview_products.column(loja, width=50, anchor="center")

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
            treeview_products.insert('', ttk.END, text=product['nome'], values=values, tags=(tag,))
            listed_products.add(product_key)

def update_row_colors(treeview):
    children = treeview.get_children('')
    for index, child in enumerate(children):
        tag = 'even' if (index + 1) % 2 == 0 else 'odd'
        treeview.item(child, tags=(tag,))

treeview_products.bind('<ButtonRelease-1>', update_product_details)

# Label para detalhes do produto
label_details = ttk.Label(frame_right, text='DETALHES DO PRODUTO', font=('Roboto', 10, 'bold'))
label_details.pack(padx=(0, 0), pady=(60,3), fill=ttk.BOTH)

# Texto para exibir detalhes do produto selecionado
product_details_text = ttk.Text(frame_right, height=18, width=50, wrap=ttk.WORD, )
product_details_text.tag_configure('bold', font=('Roboto', 10, 'bold'), foreground='#593196')
product_details_text.pack(padx=(2, 10), pady=5, fill=ttk.BOTH)

# Label para detalhes do produto
label_info_system = ttk.Labelframe(frame_right, text="DETALHES DO SISTEMA")
label_info_system.pack(padx=(2, 10), pady=(10, 5), fill=ttk.BOTH, expand=True)

# Texto para exibir detalhes do produto selecionado
system_details_text = ttk.Text(label_info_system, height=5, width=20, wrap=ttk.WORD)
system_details_text.tag_configure('bold', font=('Roboto', 10, 'bold'), foreground='#ffffff')
system_details_text.pack(padx=(10, 10), pady=5, fill=ttk.BOTH)

# Texto para exibir detalhes do produto selecionado
store_details_text = ttk.Text(label_info_system, height=5, width=20, wrap=ttk.WORD)
store_details_text.tag_configure('bold', font=('Roboto', 10, 'bold'), foreground='#ffffff')
store_details_text.pack(padx=(10, 10), pady=5, fill=ttk.BOTH)

# Texto para exibir detalhes do produto selecionado
category_details_text = ttk.Text(label_info_system, height=5, width=20, wrap=ttk.WORD)
category_details_text.tag_configure('bold', font=('Roboto', 10, 'bold'), foreground='#ffffff')
category_details_text.pack(padx=(10, 10), pady=5, fill=ttk.BOTH)

# Texto para exibir detalhes do produto selecionado
system_prod_alter_text = ttk.Text(label_info_system, height=8, width=20, wrap=ttk.WORD)
system_prod_alter_text.tag_configure('bold', font=('Roboto', 10, 'bold'), foreground='#ffffff')
system_prod_alter_text.pack(padx=(10, 10), pady=5, fill=ttk.BOTH)

# Verificar mudanças no arquivo JSON periodicamente
last_mod_time = {'json': os.path.getmtime(json_file_path)}
root.after(1000, check_json_modifications)

treeview_products.tag_configure('even', background='#F5F5F5')
treeview_products.tag_configure('odd', background='#DCDCDC')

# Executar a aplicação
root.mainloop()
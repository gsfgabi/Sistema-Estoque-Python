from pywebio.input import input, input_group, TEXT, select
from pywebio.output import put_text, put_table, put_html, put_markdown, style, put_buttons
from pywebio.platform.tornado import start_server

# Banco de dados simulado
categorias = [
    "Ferramentas Manuais",
    "Ferramentas Elétricas",
    "Materiais de Construção",
    "Equipamentos de Segurança",
]
itens = [
    {"categoria": "Ferramentas Manuais", "nome": "Martelo", "quantidade": "10"},
    {"categoria": "Ferramentas Manuais", "nome": "Chave de fenda", "quantidade": "20"},
    {"categoria": "Ferramentas Manuais", "nome": "Alicate", "quantidade": "4"},
    {"categoria": "Ferramentas Manuais", "nome": "Serrote", "quantidade": "15"},
    {"categoria": "Ferramentas Manuais", "nome": "Chave Inglesa", "quantidade": "10"},
    {"categoria": "Ferramentas Elétricas", "nome": "Furadeira", "quantidade": "5"},
    {"categoria": "Ferramentas Elétricas", "nome": "Parafusadeira", "quantidade": "4"},
    {"categoria": "Ferramentas Elétricas", "nome": "Serra Eletrica", "quantidade": "3"},
    {"categoria": "Ferramentas Elétricas", "nome": "Esmerilhadeira", "quantidade": "7"},
    {"categoria": "Materiais de Construção", "nome": "Cimento", "quantidade": "50"},
    {"categoria": "Materiais de Construção", "nome": "Areia", "quantidade": "200"},
    {"categoria": "Materiais de Construção", "nome": "Tijolo", "quantidade": "100"},
    {"categoria": "Materiais de Construção", "nome": "Cal", "quantidade": "30"},
    {"categoria": "Equipamentos de Segurança", "nome": "Capacete", "quantidade": "30"},
    {"categoria": "Equipamentos de Segurança", "nome": "Luvas", "quantidade": "50"},
    {"categoria": "Equipamentos de Segurança", "nome": "Óculos de Proteção", "quantidade": "20"},
    {"categoria": "Equipamentos de Segurança", "nome": "Botina", "quantidade": "15"},
]

# Função para exibir cabeçalho estilizado
def exibir_cabecalho():
    put_html("""
    <h1 style="text-align: center; color: #4CAF50; font-family: Arial;">
        Sistema de Estoque
    </h1>
    <hr style="border: 1px solid #ddd;">
    """)

# Função para login
def login():
    user = input("Usuário: ", type=TEXT)
    if user.lower() == "admin":
        return True
    else:
        style(put_text("Usuário inválido. Tente novamente."), 'color: red; font-weight: bold;')
        return False

# Funções de operações
def criar_categoria():
    categoria = input("Digite o nome da nova categoria:", type=TEXT)
    categorias.append(categoria)
    style(put_text(f'✅ Categoria "{categoria}" criada com sucesso.'), 'color: green; font-weight: bold;')

def adicionar_item():
    if not categorias:
        style(put_text("⚠️ Não há categorias disponíveis. Crie uma categoria primeiro."), 'color: orange; font-weight: bold;')
        return

    categoria = select("Selecione a categoria:", options=categorias)
    nome_item = input("Digite o nome do item:", type=TEXT)
    quantidade = input("Digite a quantidade:", type=TEXT)
    itens.append({"categoria": categoria, "nome": nome_item, "quantidade": quantidade})
    style(put_text(f'✅ Item "{nome_item}" adicionado com sucesso.'), 'color: green; font-weight: bold;')

def exibir_estoque():
    if not itens:
        put_text("⚠️ O estoque está vazio.")
    else:
        # Ordena a lista de itens pela categoria
        itens_ordenados = sorted(itens, key=lambda item: item["categoria"])
        
        # Cria a tabela com cabeçalho
        table_data = [["Categoria", "Item", "Quantidade"]]
        for item in itens_ordenados:
            table_data.append([item["categoria"], item["nome"], item["quantidade"]])
        
        # Exibe a tabela
        put_table(table_data)

def listar_categorias():
    if not categorias:
        style(put_text("⚠️ Não há categorias cadastradas."), 'color: orange; font-weight: bold;')
    else:
        categorias_ordenadas = sorted(categorias) 
        put_markdown("### Categorias Cadastradas:")
        for categoria in categorias_ordenadas:
            put_text(f"- {categoria}")

def remover_item():
    global itens
    if not itens:
        style(put_text("⚠️ Não há itens para remover."), 'color: orange; font-weight: bold;')
        return

    item_nome = input("Digite o nome do item que deseja remover:", type=TEXT)
    itens = [item for item in itens if item["nome"].lower() != item_nome.lower()]
    style(put_text(f'❌ Item "{item_nome}" removido com sucesso.'), 'color: red; font-weight: bold;')

def atualizar_item():
    global itens
    if not itens:
        style(put_text("⚠️ Não há itens para atualizar."), 'color: orange; font-weight: bold;')
        return

    item_nome = input("Digite o nome do item que deseja atualizar:", type=TEXT)
    for item in itens:
        if item["nome"].lower() == item_nome.lower():
            novo_nome = input(f"Digite o novo nome para '{item_nome}':", type=TEXT)
            nova_quantidade = input(f"Digite a nova quantidade para '{item_nome}':", type=TEXT)
            item["nome"] = novo_nome
            item["quantidade"] = nova_quantidade
            style(put_text(f'✅ Item "{item_nome}" atualizado com sucesso.'), 'color: green; font-weight: bold;')
            return
    style(put_text(f'⚠️ Item "{item_nome}" não encontrado.'), 'color: orange; font-weight: bold;')

# Menu principal
def sistema_estoque_app():
    exibir_cabecalho()
    if not login():
        return

    while True:
        action = select("Escolha uma ação:", options=[
            'Escolha uma ação:',
            'Criar categoria',
            'Adicionar item',
            'Exibir estoque completo',
            'Listar categorias',
            'Remover item',
            'Atualizar item',
            'Sair'
        ])

        if action == 'Criar categoria':
            criar_categoria()
        elif action == 'Adicionar item':
            adicionar_item()
        elif action == 'Exibir estoque completo':
            exibir_estoque()
        elif action == 'Listar categorias':
            listar_categorias()
        elif action == 'Remover item':
            remover_item()
        elif action == 'Atualizar item':
            atualizar_item()
        elif action == 'Sair':
            style(put_text("🔒 Saindo do sistema. Até mais!"), 'color: blue; font-weight: bold;')
            break

# Inicia o servidor
if __name__ == "__main__":
    start_server(sistema_estoque_app, port=8080)

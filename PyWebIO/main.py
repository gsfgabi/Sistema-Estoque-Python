from pywebio.input import input, input_group, TEXT, select
from pywebio.output import put_text, put_table, put_html, put_markdown, style, put_buttons
from pywebio.platform.tornado import start_server
from pywebio.input import actions
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def exibir_cabecalho():
    put_html("""
    <h1 style="text-align: center; color: #4CAF50; font-family: Arial;">
        Sistema de Estoque
    </h1>
    <hr style="border: 1px solid #ddd;">
    """)

# Função para login
def login():
    credenciais = {"admin": "12345"}  
    user = input("Usuário:", type=TEXT)
    senha = input("Senha:", type=TEXT)
    if user in credenciais and credenciais[user] == senha:
        style(put_text(f'✅ Bem-vindo, {user}!'), 'color: green; font-weight: bold;')
        return True
    else:
        style(put_text("❌ Usuário ou senha inválidos. Tente novamente."), 'color: red; font-weight: bold;')
        return False


# Funções de operações

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
        itens_ordenados = sorted(itens, key=lambda item: item["categoria"])
        
        table_data = [["Categoria", "Item", "Quantidade"]]
        for item in itens_ordenados:
            table_data.append([item["categoria"], item["nome"], item["quantidade"]])
        
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
    item = next((i for i in itens if i["nome"].lower() == item_nome.lower()), None)
    if not item:
        style(put_text(f'⚠️ Item "{item_nome}" não encontrado.'), 'color: orange; font-weight: bold;')
        return

    confirmacao = actions(
        f'Tem certeza de que deseja remover "{item_nome}"?',
        buttons=[{'label': 'Sim', 'value': 'yes'}, {'label': 'Não', 'value': 'no'}]
    )
    if confirmacao == 'yes':
        itens = [i for i in itens if i["nome"].lower() != item_nome.lower()]
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

def pesquisar_item():
    if not itens:
        style(put_text("⚠️ O estoque está vazio."), 'color: orange; font-weight: bold;')
        return

    pesquisa = input("Digite o nome ou parte do nome do item:", type=TEXT)
    resultados = [item for item in itens if pesquisa.lower() in item["nome"].lower()]
    
    if resultados:
        put_markdown("### Resultados da Pesquisa:")
        put_table([["Categoria", "Item", "Quantidade"]] + [[i["categoria"], i["nome"], i["quantidade"]] for i in resultados])
    else:
        style(put_text(f'⚠️ Nenhum item encontrado para "{pesquisa}".'), 'color: orange; font-weight: bold;')      

def salvar_relatorio_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Estoque"

    ws.append(["Categoria", "Item", "Quantidade"])

    for item in itens:
        ws.append([item["categoria"], item["nome"], item["quantidade"]])

    wb.save("estoque.xlsx")
    style(put_text("✅ Relatório salvo como 'estoque.xlsx'."), 'color: green; font-weight: bold;')    

def salvar_relatorio_pdf():
    c = canvas.Canvas("estoque.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(200, 750, "Relatório de Estoque")

    y_position = 730
    for item in itens:
        c.drawString(50, y_position, f"{item['categoria']} - {item['nome']} - {item['quantidade']}")
        y_position -= 20

        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750

    c.save()
    style(put_text("✅ Relatório salvo como 'estoque.pdf'."), 'color: green; font-weight: bold;')    

# Menu principal
def sistema_estoque_app():
    exibir_cabecalho()
    if not login():
        return

    while True:
        action = select("Escolha uma ação:", options=[
            'Escolha uma ação:',
            'Exibir estoque completo',
            'Listar categorias',
            'Adicionar item',
            'Remover item',
            'Atualizar item',
            'Salvar relatório completo',
            'Sair'
        ])

        if action == 'Exibir estoque completo':
            exibir_estoque()
        elif action == 'Listar categorias':
            listar_categorias()
        elif action == 'Adicionar item':
            adicionar_item()
        elif action == 'Remover item':
            remover_item()
        elif action == 'Atualizar item':
            atualizar_item()
        elif action == 'Salvar relatório completo':
            formato_relatorio = select("Escolha o formato do relatório:", options=[
                'Excel',
                'PDF'
            ])
            if formato_relatorio == 'Excel':
                salvar_relatorio_excel()
            elif formato_relatorio == 'PDF':
                salvar_relatorio_pdf()
        elif action == 'Sair':
            style(put_text("🔒 Saindo do sistema. Até mais!"), 'color: blue; font-weight: bold;')
            break

# Inicia o servidor
if __name__ == "__main__":
    start_server(sistema_estoque_app, port=8080)

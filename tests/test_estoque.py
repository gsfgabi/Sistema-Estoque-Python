import os
import pytest
from codigo.A import Estoque
from unittest import mock
import json


@pytest.fixture
def estoque_teste():
    """Fixture que cria um arquivo temporário de estoque para teste."""
    arquivo_teste = "tests/estoque_teste.json"
    
    estoque = Estoque(arquivo=arquivo_teste)
    
    estoque.estoque_padrao()  # Inicializa o estoque com dados padrão
    estoque.salvar_estoque()  # Salva o estoque no arquivo
    
    yield estoque  # Permite o uso do estoque no teste
    
    if os.path.exists(arquivo_teste):
        os.remove(arquivo_teste)  # Remove o arquivo após o teste


def test_estoque_padrao(estoque_teste):
    """Testa se o estoque padrão é carregado corretamente."""
    assert "ferramentas_manuais" in estoque_teste.estoque, "Categoria 'ferramentas_manuais' não encontrada no estoque."
    assert "martelo" in estoque_teste.estoque["ferramentas_manuais"], "Item 'martelo' não encontrado na categoria 'ferramentas_manuais'."

def test_adicionar_item_com_resposta_usuario(estoque_teste):
    """Testa a adição de um item em uma categoria inexistente com a interação do usuário."""
    # Simulando o input do usuário (1 para sim, 2 para não)
    with mock.patch('builtins.input', return_value='1'):  
        estoque_teste.adicionar_item("materiais_invalidos", "prego")
    
    # Verifica se a categoria foi criada e o item foi adicionado
    assert "materiais_invalidos" in estoque_teste.estoque, "Categoria 'materiais_invalidos' não foi criada."
    assert "prego" in [item.lower() for item in estoque_teste.estoque["materiais_invalidos"]], \
        "Item 'prego' não foi adicionado à nova categoria 'materiais_invalidos'."

def test_adicionar_item_categoria_nao_adicionar(estoque_teste):
    """Testa a adição de um item em uma categoria inexistente com a resposta do usuário 'não'."""
    # Simulando o input do usuário (2 para não)
    with mock.patch('builtins.input', return_value='2'):  
        estoque_teste.adicionar_item("materiais_invalidos", "prego")
    
    # Verifica se a categoria não foi criada e o item não foi adicionado
    assert "materiais_invalidos" not in estoque_teste.estoque, "Categoria 'materiais_invalidos' foi criada indevidamente."
    assert "prego" not in [item.lower() for item in estoque_teste.estoque.get("materiais_invalidos", [])], \
        "Item 'prego' foi adicionado indevidamente à categoria."

def test_remover_item(estoque_teste):
    """Testa a remoção de um item existente."""
    estoque_teste.remover_item("ferramentas_manuais", "martelo")
    assert "martelo" not in [item.lower() for item in estoque_teste.estoque["ferramentas_manuais"]], \
        "Item 'martelo' não foi removido da categoria 'ferramentas_manuais'."

def test_remover_item_inexistente(estoque_teste):
    """Testa a remoção de um item que não existe na categoria."""
    estoque_teste.remover_item("ferramentas_manuais", "prego")
    # O sistema deve notificar que o item não foi encontrado
    assert "prego" not in [item.lower() for item in estoque_teste.estoque["ferramentas_manuais"]], \
        "Item 'prego' não deveria estar na categoria."

def test_remover_item_categoria_inexistente(estoque_teste):
    """Testa a remoção de um item de uma categoria inexistente."""
    estoque_teste.remover_item("materiais_invalidos", "martelo")
    # O sistema deve notificar que a categoria não existe
    assert "martelo" in [item.lower() for item in estoque_teste.estoque.get("ferramentas_manuais", [])], \
        "Categoria 'materiais_invalidos' não deveria existir."

def test_atualizar_item(estoque_teste):
    """Testa a atualização de um item."""
    estoque_teste.adicionar_item("ferramentas_manuais", "parafuso")
    estoque_teste.atualizar_item("ferramentas_manuais", "parafuso", "porca")
    
    assert "porca" in [item.lower() for item in estoque_teste.estoque["ferramentas_manuais"]], \
        "Item 'porca' não foi adicionado à categoria 'ferramentas_manuais'."
    assert "parafuso" not in [item.lower() for item in estoque_teste.estoque["ferramentas_manuais"]], \
        "Item 'parafuso' não foi removido da categoria 'ferramentas_manuais'."

def test_atualizar_item_inexistente(estoque_teste):
    """Testa a atualização de um item inexistente."""
    estoque_teste.atualizar_item("ferramentas_manuais", "inexistente", "novo_item")
    # O item 'inexistente' não deve ser atualizado
    assert "novo_item" not in [item.lower() for item in estoque_teste.estoque["ferramentas_manuais"]], \
        "Item 'novo_item' não deveria ter sido adicionado."

def test_categoria_vazia(estoque_teste):
    """Testa a situação em que uma categoria fica vazia após remoção dos itens."""
    estoque_teste.remover_item("ferramentas_manuais", "martelo")
    estoque_teste.remover_item("ferramentas_manuais", "chave de fenda")
    assert "ferramentas_manuais" in estoque_teste.estoque, \
        "Categoria 'ferramentas_manuais' não deveria ser removida antes de estar vazia."
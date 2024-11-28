# Sistema de Estoque 

## ✨ **Sobre o Projeto**

Este sistema foi desenvolvido como parte de um projeto acadêmico na disciplina de **Qualidade e Teste de Software**, com o objetivo de criar um **sistema de gestão de estoque funcional e bem testado**. O projeto passou por um ciclo completo de melhorias, desde a análise inicial do código até a entrega final.

> **🎯 Objetivo:** Refatorar e aprimorar um código inicial com diversos problemas, utilizando boas práticas de desenvolvimento, organização e ferramentas modernas.

---

## 🔍 **Experiência do Projeto**

Durante este projeto, tivemos a oportunidade de:
- 📊 **Analisar o código original** para identificar problemas.
- 🔨 **Refatorar e implementar melhorias**, aprendendo e aplicando novas bibliotecas Python.
- ✅ **Criar testes automatizados** para validar as funcionalidades.
- 💻 **Desenvolver uma interface web interativa**, conectada à lógica do sistema.

---

## ⚙️ **Ferramentas e Tecnologias Utilizadas**

- **Python 3.8+**: Linguagem base do projeto.
- **PyWebIO**: Para criar a interface web interativa.
- **OpenPyXL**: Manipulação de arquivos Excel.
- **ReportLab**: Geração de relatórios em PDF.
- **PyTest**: Criação e execução de testes automatizados.
- **Black**: Formatação automática para garantir código limpo e consistente.

---

## 📂 **Estrutura de Pastas**

```
.
├── codigo/
│   └── a.py            # Código principal com classes e funções.
├── pywebio/
│   └── main.py         # Interface web interativa.
├── tests/
│   └── test_estoque.py # Testes automatizados para validação.
├── README.md           # Documentação do projeto.
```

---

## 🚀 **Como Executar**

### 1. **Pré-requisitos**
- Certifique-se de ter o **Python 3.8+** instalado.
- Instale as dependências:
  ```bash
  pip install pywebio openpyxl reportlab pytest black
  ```

### 2. **Executar a Interface Web**
1. Navegue até o diretório `pywebio`:
   ```bash
   cd pywebio
   ```
2. Execute o servidor:
   ```bash
   python main.py
   ```
3. Abra o navegador em `http://localhost:8080`.

### 3. **Executar os Testes Automatizados**
1. Navegue até o diretório `tests`:
   ```bash
   cd tests
   ```
2. Execute os testes:
   ```bash
   pytest
   ```

### 4. **Formatação do Código com Black**
1. Para garantir que o código está bem formatado, execute:
   ```bash
   black .
   ```
2. O **Black** ajustará automaticamente o código conforme os padrões PEP 8.

## 📜 **Descrição dos Arquivos**

### **`codigo/a.py`**

Arquivo principal com a implementação das classes e funções para gerenciamento do estoque.

#### Exemplo de Código
```python
class Estoque:
    def adicionar_item(self, categoria: str, item: str) -> None:
        categoria = categoria.strip().lower()
        item = item.strip().lower()

        if categoria in self.estoque:
            # Se a categoria já existe, adiciona o item
            if item not in [i.lower() for i in self.estoque[categoria]]:
                self.estoque[categoria].append(item)
                print(f"Item '{item}' adicionado à categoria '{categoria}'.")
            else:
                print(f"O item '{item}' já existe na categoria '{categoria}'.")
        else:
            # A categoria não existe, então pergunta ao usuário se deseja criar uma nova categoria
            print(f"A categoria '{categoria}' não existe.")
            resposta = input(
                "Deseja criar essa categoria e adicionar o item? (1 - Sim / 2 - Não): "
            )

            if resposta == "1":
                self.estoque[categoria] = [item]
                print(f"Categoria '{categoria}' criada e item '{item}' adicionado.")
            elif resposta == "2":
                print(
                    f"A categoria '{categoria}' não foi criada e o item '{item}' não foi adicionado."
                )
            else:
                print(
                    "Opção inválida. A categoria não foi criada e o item não foi adicionado."
                )
        self.salvar_estoque()
```

---

### **`pywebio/main.py`**

Arquivo que conecta a lógica do estoque à interface web.

#### Exemplo de Código
```python
from pywebio.input import input, select
from pywebio.output import put_text
from codigo.a import Estoque

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
```

---

### **`tests/test_estoque.py`**

Testes automatizados para as funções do estoque.

#### Exemplo de Teste
```python
import os
import pytest
from codigo.A import Estoque
from unittest import mock
import json

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
```
---

## 🔧 **Funcionalidades Principais**

1. **Gestão de Estoque:**
   - Adicionar, editar e remover itens, atualizar e exibir relatório completo.
2. **Interface Web (PyWebIO):**
   - Login simples e acesso protegido.
   - Exibição de categorias e itens.
   - Exportação de relatórios em Excel e PDF.
3. **Testes Automatizados:**
   - Cobertura para funções de adição, remoção e manipulação de dados.
   - Validação de cenários críticos e bordas.

### 👨‍🏫 Professore Orientador
- **Juliano Olimpio**

### 👨‍💻 Participantes do Projeto
- [👩‍💻 Gabriella Freitas](https://github.com/gsfgabi)
- [👨‍💻 Wendel Vinicius](https://github.com/Wendel-Vinicius)

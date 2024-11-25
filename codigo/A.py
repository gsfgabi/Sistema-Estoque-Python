import os
import json


class Estoque:
    def __init__(self, arquivo="database/estoque.json"):
        self.arquivo = arquivo
        self.estoque = self.carregar_estoque()

    def estoque_padrao(self):
        """Define as categorias base do estoque."""
        return {
            "ferramentas_manuais": [
                "martelo",
                "chave de fenda",
                "alicate",
                "serrote",
                "chave inglesa",
            ],
            "ferramentas_eletricas": [
                "furadeira",
                "parafusadeira",
                "serra elétrica",
                "esmerilhadeira",
            ],
            "materiais_construcao": ["cimento", "areia", "tijolo", "telha", "cal"],
            "equipamentos_seguranca": [
                "capacete",
                "luva",
                "óculos de proteção",
                "botina",
            ],
        }

    def carregar_estoque(self):
        """Carrega o estoque do arquivo JSON ou cria um novo se não existir."""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Erro ao ler o arquivo '{self.arquivo}'. Criando estoque padrão."
                )
        print(f"Arquivo '{self.arquivo}' não encontrado. Criando estoque padrão.")
        estoque = self.estoque_padrao()
        self.salvar_estoque(estoque)
        return estoque

    def salvar_estoque(self, estoque=None):
        """Salva o estoque no arquivo JSON."""
        if estoque is None:
            estoque = self.estoque
        with open(self.arquivo, "w") as f:
            json.dump(estoque, f, indent=4)
        print(f"Estoque salvo no arquivo '{self.arquivo}'.")

    def item_existe(self, item):
        item = item.strip().lower()
        for categoria, itens in self.estoque.items():
            if item in [i.lower() for i in itens]:
                print(f"Item '{item}' encontrado na categoria '{categoria}'.")
                return categoria
        print(f"Item '{item}' não encontrado no estoque.")
        return None

    def exibir_estoque(self):
        print("\n--- Estoque Atual ---")
        if not self.estoque:
            print("O estoque está vazio.")
        else:
            for categoria, itens in self.estoque.items():
                print(f"\n{categoria.capitalize()}:")
                for item in itens:
                    print(f"- {item}")
        print("\n")

    def listar_categorias(self):
        print("\n--- Categorias no Estoque ---")
        for categoria in self.estoque:
            print(f"- {categoria.capitalize()}")
        print("\n")

    def exibir_categoria(self, categoria):
        categoria = categoria.strip().lower()
        if categoria in self.estoque:
            print(f"\nItens na categoria '{categoria}':")
            for item in self.estoque[categoria]:
                print(f"- {item}")
        else:
            print(f"A categoria '{categoria}' não existe no estoque.")
        print("\n")

    def adicionar_item(self, categoria: str, item: str) -> None:
        """
        Adiciona um item a uma categoria existente ou cria uma nova categoria, com a opção de confirmação do usuário.
        """
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
                # Se o usuário escolher 'Sim', cria a categoria e adiciona o item
                self.estoque[categoria] = [item]
                print(f"Categoria '{categoria}' criada e item '{item}' adicionado.")
            elif resposta == "2":
                # Se o usuário escolher 'Não', apenas informa que nada será feito
                print(
                    f"A categoria '{categoria}' não foi criada e o item '{item}' não foi adicionado."
                )
            else:
                print(
                    "Opção inválida. A categoria não foi criada e o item não foi adicionado."
                )

        # Salva o estoque após a modificação
        self.salvar_estoque()

    def remover_item(self, categoria, item):
        """Remove um item de uma categoria no estoque."""
        if categoria in self.estoque:
            itens = self.estoque[categoria]
            item_lower = item.lower()

            # Remover item ignorando diferenças de maiúsculas e minúsculas
            itens_filtrados = [i for i in itens if i.lower() != item_lower]

            if len(itens_filtrados) != len(itens):  # Verifica se algo foi removido
                self.estoque[categoria] = itens_filtrados
                print(f"Item '{item}' removido da categoria '{categoria}'.")
                self.salvar_estoque()
            else:
                print(f"Item '{item}' não encontrado na categoria '{categoria}'.")
        else:
            print(f"Categoria '{categoria}' não encontrada.")

    def atualizar_item(self, categoria, item_antigo, item_novo):
        categoria = categoria.strip().lower()
        item_antigo = item_antigo.strip().lower()
        item_novo = item_novo.strip().lower()
        if categoria in self.estoque and item_antigo in self.estoque[categoria]:
            index = self.estoque[categoria].index(item_antigo)
            self.estoque[categoria][index] = item_novo
            print(
                f"Item '{item_antigo}' atualizado para '{item_novo}' na categoria '{categoria}'."
            )
        else:
            print(f"Item '{item_antigo}' não encontrado na categoria '{categoria}'.")
        self.salvar_estoque()

    def relatorio_completo(self):
        print("\n--- Relatório Completo do Estoque ---")
        total_itens = sum(len(itens) for itens in self.estoque.values())
        print(f"Total de categorias: {len(self.estoque)}")
        print(f"Total de itens: {total_itens}")
        for categoria, itens in self.estoque.items():
            print(f"\nCategoria '{categoria.capitalize()}':")
            for item in itens:
                print(f"- {item}")
        print("\n")


def menu_principal():
    sistema_estoque = Estoque()

    while True:
        print("\n--- Menu do Sistema de Estoque ---")
        print("1. Exibir estoque completo")
        print("2. Listar categorias")
        print("3. Exibir itens de uma categoria")
        print("4. Adicionar item")
        print("5. Remover item")
        print("6. Atualizar item")
        print("7. Exibir relatório completo")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema_estoque.exibir_estoque()
        elif opcao == "2":
            sistema_estoque.listar_categorias()
        elif opcao == "3":
            categoria = input("Digite o nome da categoria: ").strip().lower()
            sistema_estoque.exibir_categoria(categoria)
        elif opcao == "4":
            categoria = (
                input("Digite a categoria para adicionar o item: ").strip().lower()
            )
            item = input("Digite o nome do item que deseja adicionar: ").strip().lower()
            sistema_estoque.adicionar_item(categoria, item)
        elif opcao == "5":
            categoria = (
                input("Digite a categoria do item que deseja remover: ").strip().lower()
            )
            item = input("Digite o nome do item que deseja remover: ").strip().lower()
            sistema_estoque.remover_item(categoria, item)
        elif opcao == "6":
            categoria = input("Digite a categoria do item: ").strip().lower()
            item_antigo = (
                input("Digite o nome do item a ser atualizado: ").strip().lower()
            )
            item_novo = input("Digite o novo nome do item: ").strip().lower()
            sistema_estoque.atualizar_item(categoria, item_antigo, item_novo)
        elif opcao == "7":
            sistema_estoque.relatorio_completo()
        elif opcao == "8":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()

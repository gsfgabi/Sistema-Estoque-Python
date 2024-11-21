
# Sistema de gerenciamento de estoque - Ferramentas
class Estoque:
    def __init__(self):
        self.estoque = {
            "ferramentas_manuais": ["martelo", "chave de fenda", "alicate", "serrote", "chave inglesa"],
            "ferramentas_eletricas": ["furadeira", "parafusadeira", "serra elétrica", "esmerilhadeira"],
            "materiais_construcao": ["cimento", "areia", "tijolo", "telha", "cal"],
            "equipamentos_seguranca": ["capacete", "luva", "óculos de proteção", "botina"],
        }

    def item_existe(self, item):
        for categoria, itens in self.estoque.items():
            if item in itens:
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
        if categoria in self.estoque:
            print(f"\nItens na categoria '{categoria}':")
            for item in self.estoque[categoria]:
                print(f"- {item}")
        else:
            print(f"A categoria '{categoria}' não existe no estoque.")
        print("\n")

    def adicionar_item(self, categoria, item):
        if categoria in self.estoque:
            if item not in self.estoque[categoria]:
                self.estoque[categoria].append(item)
                print(f"Item '{item}' adicionado à categoria '{categoria}'.")
            else:
                print(f"O item '{item}' já existe na categoria '{categoria}'.")
        else:
            print(f"A categoria '{categoria}' não existe. Criando nova categoria.")
            self.estoque[categoria] = [item]
            print(f"Categoria '{categoria}' criada e item '{item}' adicionado.")

    def remover_item(self, categoria, item):
        if categoria in self.estoque:
            if item in self.estoque[categoria]:
                self.estoque[categoria].remove(item)
                print(f"Item '{item}' removido da categoria '{categoria}'.")
                if not self.estoque[categoria]:  
                    del self.estoque[categoria]
                    print(f"Categoria '{categoria}' removida por estar vazia.")
            else:
                print(f"Item '{item}' não encontrado na categoria '{categoria}'.")
        else:
            print(f"A categoria '{categoria}' não existe no estoque.")

    def atualizar_item(self, categoria, item_antigo, item_novo):
        if categoria in self.estoque and item_antigo in self.estoque[categoria]:
            index = self.estoque[categoria].index(item_antigo)
            self.estoque[categoria][index] = item_novo
            print(f"Item '{item_antigo}' atualizado para '{item_novo}' na categoria '{categoria}'.")
        else:
            print(f"Item '{item_antigo}' não encontrado na categoria '{categoria}'.")

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
            categoria = input("Digite o nome da categoria: ").lower()
            sistema_estoque.exibir_categoria(categoria)
        elif opcao == "4":
            categoria = input("Digite a categoria para adicionar o item: ").lower()
            item = input("Digite o nome do item que deseja adicionar: ").lower()
            sistema_estoque.adicionar_item(categoria, item)
        elif opcao == "5":
            categoria = input("Digite a categoria do item que deseja remover: ").lower()
            item = input("Digite o nome do item que deseja remover: ").lower()
            sistema_estoque.remover_item(categoria, item)
        elif opcao == "6":
            categoria = input("Digite a categoria do item: ").lower()
            item_antigo = input("Digite o nome do item a ser atualizado: ").lower()
            item_novo = input("Digite o novo nome do item: ").lower()
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

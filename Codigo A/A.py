class Estoque:
    """
    Classe que representa o sistema de gerenciamento de estoque.
    """
    def __init__(self):
        self.estoque: Dict[str, List[str]] = {
            "ferramentas_manuais": ["martelo", "chave de fenda", "alicate", "serrote", "chave inglesa"],
            "ferramentas_eletricas": ["furadeira", "parafusadeira", "serra elétrica", "esmerilhadeira"],
            "materiais_construcao": ["cimento", "areia", "tijolo", "telha", "cal"],
            "equipamentos_seguranca": ["capacete", "luva", "óculos de proteção", "botina"],
        }

    def _validar_categoria(self, categoria: str) -> bool:
        """
        Verifica se uma categoria existe no estoque.
        """
        if categoria not in self.estoque:
            print(f"A categoria '{categoria}' não existe no estoque.")
            return False
        return True

    def item_existe(self, item: str) -> str:
        """
        Verifica se um item existe no estoque e retorna a categoria, se encontrado.
        """
        for categoria, itens in self.estoque.items():
            if item in itens:
                print(f"Item '{item}' encontrado na categoria '{categoria}'.")
                return categoria
        print(f"Item '{item}' não encontrado no estoque.")
        return ""

    def exibir_estoque(self) -> None:
        """
        Exibe o estoque completo, organizado por categoria.
        """
        print("\n--- Estoque Atual ---")
        if not self.estoque:
            print("O estoque está vazio.")
        else:
            for categoria, itens in self.estoque.items():
                print(f"\n{categoria.capitalize()}:")
                for item in itens:
                    print(f"- {item}")

    def listar_categorias(self) -> None:
        """
        Lista todas as categorias existentes no estoque.
        """
        print("\n--- Categorias no Estoque ---")
        for categoria in self.estoque:
            print(f"- {categoria.capitalize()}")

    def exibir_categoria(self, categoria: str) -> None:
        """
        Exibe os itens de uma categoria específica.
        """
        if self._validar_categoria(categoria):
            print(f"\nItens na categoria '{categoria}':")
            for item in self.estoque[categoria]:
                print(f"- {item}")

    def adicionar_item(self, categoria: str, item: str) -> None:
        """
        Adiciona um item a uma categoria existente ou cria uma nova categoria.
        """
        if not categoria or not item:
            print("Categoria e item não podem ser vazios.")
            return
        if categoria in self.estoque:
            if item not in self.estoque[categoria]:
                self.estoque[categoria].append(item)
                print(f"Item '{item}' adicionado à categoria '{categoria}'.")
            else:
                print(f"O item '{item}' já existe na categoria '{categoria}'.")
        else:
            self.estoque[categoria] = [item]
            print(f"Categoria '{categoria}' criada e item '{item}' adicionado.")

    def remover_item(self, categoria: str, item: str) -> None:
        """
        Remove um item de uma categoria. Remove a categoria se ela ficar vazia.
        """
        if self._validar_categoria(categoria):
            if item in self.estoque[categoria]:
                self.estoque[categoria].remove(item)
                print(f"Item '{item}' removido da categoria '{categoria}'.")
                if not self.estoque[categoria]:
                    del self.estoque[categoria]
                    print(f"Categoria '{categoria}' removida por estar vazia.")
            else:
                print(f"Item '{item}' não encontrado na categoria '{categoria}'.")

    def atualizar_item(self, categoria: str, item_antigo: str, item_novo: str) -> None:
        """
        Atualiza um item dentro de uma categoria.
        """
        if self._validar_categoria(categoria):
            if item_antigo in self.estoque[categoria]:
                index = self.estoque[categoria].index(item_antigo)
                self.estoque[categoria][index] = item_novo
                print(f"Item '{item_antigo}' atualizado para '{item_novo}' na categoria '{categoria}'.")
            else:
                print(f"Item '{item_antigo}' não encontrado na categoria '{categoria}'.")

    def relatorio_completo(self) -> None:
        """
        Gera um relatório completo do estoque, mostrando categorias e itens.
        """
        print("\n--- Relatório Completo do Estoque ---")
        total_itens = sum(len(itens) for itens in self.estoque.values())
        print(f"Total de categorias: {len(self.estoque)}")
        print(f"Total de itens: {total_itens}")
        for categoria, itens in self.estoque.items():
            print(f"\nCategoria '{categoria.capitalize()}':")
            for item in itens:
                print(f"- {item}")


def menu_principal() -> None:
    """
    Menu interativo para o sistema de estoque.
    """
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

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            sistema_estoque.exibir_estoque()
        elif opcao == "2":
            sistema_estoque.listar_categorias()
        elif opcao == "3":
            categoria = input("Digite o nome da categoria: ").lower().strip()
            sistema_estoque.exibir_categoria(categoria)
        elif opcao == "4":
            categoria = input("Digite a categoria para adicionar o item: ").lower().strip()
            item = input("Digite o nome do item que deseja adicionar: ").lower().strip()
            sistema_estoque.adicionar_item(categoria, item)
        elif opcao == "5":
            categoria = input("Digite a categoria do item que deseja remover: ").lower().strip()
            item = input("Digite o nome do item que deseja remover: ").lower().strip()
            sistema_estoque.remover_item(categoria, item)
        elif opcao == "6":
            categoria = input("Digite a categoria do item: ").lower().strip()
            item_antigo = input("Digite o nome do item a ser atualizado: ").lower().strip()
            item_novo = input("Digite o novo nome do item: ").lower().strip()
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

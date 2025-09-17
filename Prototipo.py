# =========================================================
# Projeto Python - InovaREA CRUD (versão melhorada)
# =========================================================
# Este programa simula o gerenciamento de dados da plataforma InovaREA.
# Funcionalidades: Cadastrar, Listar, Buscar, Atualizar e Excluir registros.
# Inclui: Validação, tratamento de erros, logs e dashboard.
# =========================================================

# Base de dados (lista de dicionários)
registros = []
proximo_id = 1  # ID automático


# =========================================================
# Funções utilitárias
# =========================================================

def log(acao, detalhe=""):
    """Exibe no console um log da ação realizada."""
    print(f"[LOG] {acao} - {detalhe}")


def dashboard():
    """Exibe estatísticas básicas dos registros."""
    print("\n=== DASHBOARD INOVAREA ===")
    print(f"Total de registros: {len(registros)}")
    if registros:
        print(f"Último cadastrado: {registros[-1]['nome']}")
    print("=" * 30)


# =========================================================
# Funções do CRUD
# =========================================================

def cadastrar(nome, descricao):
    """Cria um novo registro."""
    global proximo_id
    if not nome.strip() or not descricao.strip():
        return "Erro: Nome e descrição não podem ser vazios."
    
    novo = {"id": proximo_id, "nome": nome.strip(), "descricao": descricao.strip()}
    registros.append(novo)
    log("CADASTRO", f"ID {proximo_id} - {nome}")
    proximo_id += 1
    return f"Registro '{nome}' cadastrado com sucesso!"


def listar():
    """Lista todos os registros."""
    if not registros:
        return "Nenhum registro encontrado."
    
    resultado = "\n=== LISTA DE REGISTROS ===\n"
    for r in registros:
        resultado += f"ID: {r['id']} | Nome: {r['nome']} | Descrição: {r['descricao']}\n"
    return resultado


def buscar(termo):
    """Busca registros por ID ou nome."""
    encontrados = []
    for r in registros:
        if str(r["id"]) == str(termo) or termo.lower() in r["nome"].lower():
            encontrados.append(r)
    
    if not encontrados:
        return "Nenhum registro encontrado."
    
    resultado = "\n=== RESULTADOS DA BUSCA ===\n"
    for r in encontrados:
        resultado += f"ID: {r['id']} | Nome: {r['nome']} | Descrição: {r['descricao']}\n"
    return resultado


def atualizar(id_registro, novo_nome, nova_descricao):
    """Atualiza um registro existente."""
    try:
        for r in registros:
            if r["id"] == id_registro:
                if novo_nome.strip():
                    r["nome"] = novo_nome.strip()
                if nova_descricao.strip():
                    r["descricao"] = nova_descricao.strip()
                log("ATUALIZAÇÃO", f"ID {id_registro}")
                return f"Registro ID {id_registro} atualizado com sucesso!"
        return "Erro: Registro não encontrado."
    except Exception as e:
        return f"Erro ao atualizar: {e}"


def excluir(id_registro):
    """Exclui um registro existente."""
    try:
        for r in registros:
            if r["id"] == id_registro:
                registros.remove(r)
                log("EXCLUSÃO", f"ID {id_registro}")
                return f"Registro ID {id_registro} excluído com sucesso!"
        return "Erro: Registro não encontrado."
    except Exception as e:
        return f"Erro ao excluir: {e}"
    finally:
        pass


# =========================================================
# Menu Principal
# =========================================================

def menu():
    while True:
        dashboard()
        print("=== MENU PRINCIPAL ===")
        print("1. Cadastrar registro")
        print("2. Listar registros")
        print("3. Buscar registro")
        print("4. Atualizar registro")
        print("5. Excluir registro")
        print("0. Sair")
        print("=" * 30)

        opcao = input("Escolha uma opção: ")
        print()

        if opcao == "1":
            nome = input("Digite o nome: ")
            descricao = input("Digite a descrição: ")
            print(cadastrar(nome, descricao))

        elif opcao == "2":
            print(listar())

        elif opcao == "3":
            termo = input("Digite o ID ou parte do nome para buscar: ")
            print(buscar(termo))

        elif opcao == "4":
            try:
                id_registro = int(input("Digite o ID do registro que deseja atualizar: "))
                novo_nome = input("Novo nome (ou deixe vazio): ")
                nova_descricao = input("Nova descrição (ou deixe vazio): ")
                print(atualizar(id_registro, novo_nome, nova_descricao))
            except ValueError:
                print("Erro: o ID deve ser um número inteiro.")

        elif opcao == "5":
            try:
                id_registro = int(input("Digite o ID do registro que deseja excluir: "))
                print(excluir(id_registro))
            except ValueError:
                print("Erro: o ID deve ser um número inteiro.")

        elif opcao == "0":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")


# =========================================================
# Execução principal
# =========================================================

if __name__ == "__main__":
    menu()

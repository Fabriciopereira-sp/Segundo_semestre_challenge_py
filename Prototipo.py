# =========================================================
# InovaREA - CRUD com Submenus
# Sprint 3 – Computational Thinking Using Python
# =========================================================

import json
import os
import re
from datetime import datetime

DATA_FILE = "data.json"
LOG_FILE = "log.txt"

registros = []   # lista de dicionários
proximo_id = 1   # ID automático
_ultimo_backup = None  # guarda última ação para desfazer


# -----------------------------
# Funções de apoio
# -----------------------------
def log(acao, detalhe=""):
    """Escreve log no console e em arquivo"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{ts} | {acao} | {detalhe}"
    print(f"[LOG] {linha}")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except:
        pass


def validar_nome(nome):
    """Nome deve ter 2 a 60 caracteres"""
    if not isinstance(nome, str):
        return False
    nome = nome.strip()
    if not (2 <= len(nome) <= 60):
        return False
    if not re.search(r"[A-Za-z0-9À-ÿ]", nome):
        return False
    return True


def validar_descricao(desc):
    """Descrição deve ter 3 a 200 caracteres"""
    if not isinstance(desc, str):
        return False
    return 3 <= len(desc.strip()) <= 200


def carregar():
    """Carrega dados do JSON"""4
    global registros, proximo_id
    if not os.path.exists(DATA_FILE):
        registros, proximo_id = [], 1
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            registros = json.load(f)
        ids = [r.get("id", 0) for r in registros]
        proximo_id = (max(ids) + 1) if ids else 1
    except:
        registros, proximo_id = [], 1


def salvar():
    """Salva dados no JSON"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log("ERRO_SAVE", str(e))
    finally:
        
        log("FINALIZADO", "Ação de salvar concluída")


def dashboard():
    """Mostra estatísticas rápidas"""
    ativos = [r for r in registros if r.get("ativo", True)]
    inativos = [r for r in registros if not r.get("ativo", True)]
    print("\n=== DASHBOARD ===")
    print(f"Total: {len(registros)} | Ativos: {len(ativos)} | Inativos: {len(inativos)}")
    if registros:
        ultimo = max(registros, key=lambda r: r.get("criado_em", ""))
        print(f"Último cadastrado: {ultimo.get('nome')} (ID {ultimo.get('id')})")
    print("=" * 40)


def pausar():
    input("\nPressione ENTER para continuar...")


# -----------------------------
# CRUD
# -----------------------------
def cadastrar(nome, descricao):
    """Adiciona um novo registro"""
    global proximo_id
    if not validar_nome(nome):
        return "Erro: Nome inválido."
    if not validar_descricao(descricao):
        return "Erro: Descrição inválida."
    novo = {
        "id": proximo_id,
        "nome": nome.strip(),
        "descricao": descricao.strip(),
        "ativo": True,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
        "atualizado_em": None
    }
    registros.append(novo)
    proximo_id += 1
    salvar()
    return f"Registro '{novo['nome']}' cadastrado com sucesso!"


def listar(mostrar_inativos=False):
    """Lista registros"""
    itens = registros if mostrar_inativos else [r for r in registros if r.get("ativo", True)]
    if not itens:
        return "Nenhum registro encontrado."
    saida = ["\n=== LISTA DE REGISTROS ==="]
    for r in itens:
        status = "ativo" if r.get("ativo", True) else "inativo"
        saida.append(f"ID: {r['id']} | {r['nome']} | {status} | {r['descricao']}")
    return "\n".join(saida)


def buscar(termo):
    """Busca por ID ou nome/descrição"""
    termo = termo.lower().strip()
    achados = [r for r in registros if str(r["id"]) == termo or
               termo in r["nome"].lower() or termo in r["descricao"].lower()]
    if not achados:
        return "Nenhum registro encontrado."
    saida = ["\n=== RESULTADOS DA BUSCA ==="]
    for r in achados:
        status = "ativo" if r.get("ativo", True) else "inativo"
        saida.append(f"ID: {r['id']} | {r['nome']} | {status} | {r['descricao']}")
    return "\n".join(saida)


def atualizar(id_registro, novo_nome, nova_descricao):
    """Atualiza um registro existente"""
    global _ultimo_backup
    for r in registros:
        if r["id"] == id_registro:
            _ultimo_backup = ("update", r.copy())
            if novo_nome.strip():
                if not validar_nome(novo_nome):
                    return "Erro: Nome inválido."
                r["nome"] = novo_nome.strip()
            if nova_descricao.strip():
                if not validar_descricao(nova_descricao):
                    return "Erro: Descrição inválida."
                r["descricao"] = nova_descricao.strip()
            r["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
            salvar()
            return f"Registro ID {id_registro} atualizado!"
    return "Erro: Registro não encontrado."


def alternar_ativo(id_registro, status):
    """Ativa ou inativa um registro"""
    for r in registros:
        if r["id"] == id_registro:
            r["ativo"] = status
            r["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
            salvar()
            return f"Registro {id_registro} agora está {'ativo' if status else 'inativo'}."
    return "Erro: Registro não encontrado."


def excluir(id_registro):
    """Exclui registro de forma definitiva"""
    global _ultimo_backup
    for i, r in enumerate(registros):
        if r["id"] == id_registro:
            _ultimo_backup = ("delete", r.copy())
            del registros[i]
            salvar()
            return f"Registro ID {id_registro} excluído."
    return "Erro: Registro não encontrado."


def desfazer_ultima_acao():
    """Desfaz última exclusão ou atualização"""
    global _ultimo_backup
    if not _ultimo_backup:
        return "Não há ação para desfazer."
    tipo, snap = _ultimo_backup
    if tipo == "delete":
        registros.append(snap)
        salvar()
        _ultimo_backup = None
        return f"Exclusão desfeita. ID {snap['id']} restaurado."
    elif tipo == "update":
        for i, r in enumerate(registros):
            if r["id"] == snap["id"]:
                registros[i] = snap
                salvar()
                _ultimo_backup = None
                return f"Atualização desfeita. ID {snap['id']} restaurado."
    return "Nada a desfazer."


# -----------------------------
# Menus
# -----------------------------
def relatorios_menu():
    while True:
        print("\n=== RELATÓRIOS ===")
        print("1. Listar ativos")
        print("2. Listar inativos")
        print("3. Buscar por termo")
        print("0. Voltar")
        op = input("Opção: ")
        if op == "1":
            print(listar(False)); pausar()
        elif op == "2":
            print(listar(True)); pausar()
        elif op == "3":
            termo = input("Digite termo: ")
            print(buscar(termo)); pausar()
        elif op == "0":
            break
        else:
            print("Opção inválida!")


def crud_menu():
    while True:
        print("\n=== CRUD ===")
        print("1. Cadastrar")
        print("2. Listar ativos")
        print("3. Listar todos")
        print("4. Buscar")
        print("5. Atualizar")
        print("6. Inativar/Ativar")
        print("7. Excluir")
        print("8. Desfazer última ação")
        print("0. Voltar")
        op = input("Opção: ")
        if op == "1":
            nome = input("Nome: "); desc = input("Descrição: ")
            print(cadastrar(nome, desc)); pausar()
        elif op == "2":
            print(listar(False)); pausar()
        elif op == "3":
            print(listar(True)); pausar()
        elif op == "4":
            termo = input("Termo: "); print(buscar(termo)); pausar()
        elif op == "5":
            try:
                _id = int(input("ID: "))
                novo_nome = input("Novo nome: ")
                nova_desc = input("Nova descrição: ")
                print(atualizar(_id, novo_nome, nova_desc))
            except ValueError:
                print("Erro: ID deve ser inteiro.")
            pausar()
        elif op == "6":
            try:
                _id = int(input("ID: "))
                status = input("A para ativar, I para inativar: ").upper()
                print(alternar_ativo(_id, status == "A"))
            except ValueError:
                print("Erro: ID inválido.")
            pausar()
        elif op == "7":
            try:
                _id = int(input("ID: "))
                print(excluir(_id))
            except ValueError:
                print("Erro: ID inválido.")
            pausar()
        elif op == "8":
            print(desfazer_ultima_acao()); pausar()
        elif op == "0":
            break
        else:
            print("Opção inválida!")


def menu():
    carregar()
    while True:
        dashboard()
        print("=== MENU PRINCIPAL ===")
        print("1. CRUD")
        print("2. Relatórios")
        print("0. Sair")
        op = input("Opção: ")
        if op == "1":
            crud_menu()
        elif op == "2":
            relatorios_menu()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()

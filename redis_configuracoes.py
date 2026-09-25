"""Menu de configurações armazenadas como chave-valor no Redis."""

import re

import redis as r
from redis.exceptions import RedisError

PREFIXO = "config:"
PADRAO_NOME = re.compile(r"^[a-zA-Z0-9_-]+$")


def criar_cliente_redis():
    """Cria o cliente Redis e confirma que o servidor está acessível."""
    cliente = r.Redis(host="localhost", port=6379, decode_responses=True)
    cliente.ping()
    return cliente


def normalizar_nome(nome):
    """Valida o nome e devolve a chave Redis no padrão config:<nome>."""
    nome = nome.strip()
    if not PADRAO_NOME.fullmatch(nome):
        raise ValueError("Use apenas letras, números, hífen ou underline no nome.")
    return f"{PREFIXO}{nome.lower()}"


def ler_booleano():
    """Lê um booleano e o representa conforme o padrão 1/0 da atividade."""
    while True:
        valor = input("Valor (1 para ativado, 0 para desativado): ").strip()
        if valor in {"1", "0"}:
            return valor
        print("Valor inválido. Digite 1 ou 0.")


def cadastrar_configuracao(cliente):
    nome = input("Nome da configuração: ")
    try:
        chave = normalizar_nome(nome)
    except ValueError as erro:
        print(erro)
        return

    if cliente.exists(chave):
        print("Essa configuração já existe. Use a opção Atualizar.")
        return

    tipo = input("Tipo (1 - booleano, 2 - texto): ").strip()
    if tipo == "1":
        valor = ler_booleano()
    elif tipo == "2":
        valor = input("Valor da configuração: ").strip()
        if not valor:
            print("O valor não pode ficar vazio.")
            return
    else:
        print("Tipo inválido.")
        return

    cliente.set(chave, valor)
    print(f"Configuração '{chave}' cadastrada com sucesso.")


def listar_configuracoes(cliente):
    print("\n--- CONFIGURAÇÕES ---")
    encontrou = False
    for chave in sorted(cliente.scan_iter(match=f"{PREFIXO}*")):
        valor = cliente.get(chave)
        if valor is None:
            continue
        if valor in {"1", "0"}:
            descricao = "ativado" if valor == "1" else "desativado"
            print(f"{chave} = {valor} ({descricao})")
        else:
            print(f"{chave} = {valor}")
        encontrou = True

    if not encontrou:
        print("Nenhuma configuração cadastrada.")


def atualizar_configuracao(cliente):
    nome = input("Nome da configuração: ")
    try:
        chave = normalizar_nome(nome)
    except ValueError as erro:
        print(erro)
        return

    if not cliente.exists(chave):
        print("Configuração não encontrada.")
        return

    tipo = input("Tipo do novo valor (1 - booleano, 2 - texto): ").strip()
    if tipo == "1":
        novo_valor = ler_booleano()
    elif tipo == "2":
        novo_valor = input("Novo valor: ").strip()
        if not novo_valor:
            print("O valor não pode ficar vazio.")
            return
    else:
        print("Tipo inválido.")
        return

    cliente.set(chave, novo_valor)
    print(f"Configuração '{chave}' atualizada com sucesso.")


def remover_configuracao(cliente):
    nome = input("Nome da configuração: ")
    try:
        chave = normalizar_nome(nome)
    except ValueError as erro:
        print(erro)
        return

    if cliente.delete(chave):
        print(f"Configuração '{chave}' removida com sucesso.")
    else:
        print("Configuração não encontrada.")


def menu():
    try:
        cliente = criar_cliente_redis()
    except RedisError as erro:
        print("Não foi possível conectar ao Redis. Verifique se o serviço está ativo.")
        print(f"Detalhes: {erro}")
        return

    acoes = {
        "1": cadastrar_configuracao,
        "2": listar_configuracoes,
        "3": atualizar_configuracao,
        "4": remover_configuracao,
    }

    while True:
        print("\n--- MENU DE CONFIGURAÇÕES ---")
        print("1 - Cadastrar uma chave-valor")
        print("2 - Listar todas as configurações")
        print("3 - Atualizar uma configuração")
        print("4 - Remover uma configuração")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "5":
            print("Encerrando...")
            break
        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        try:
            acao(cliente)
        except RedisError as erro:
            print(f"Erro ao acessar o Redis: {erro}")


if __name__ == "__main__":
    menu()

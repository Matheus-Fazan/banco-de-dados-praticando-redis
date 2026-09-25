# Configurações com Redis

Aplicação de terminal em Python para cadastrar, listar, atualizar e remover
configurações armazenadas no Redis como strings chave-valor. As chaves seguem
o padrão `config:<nome>`. Valores booleanos usam `1` (ativado) e `0`
(desativado); configurações como idioma podem guardar texto, por exemplo
`pt-BR`.

## Como executar

1. Inicie o Redis com Docker:

   ```powershell
   docker compose up -d
   ```

2. Instale a dependência Python:

   ```powershell
   pip install -r requirements.txt
   ```

3. Abra o menu:

   ```powershell
   python redis_configuracoes.py
   ```

O programa conecta ao Redis em `localhost:6379`. As configurações são
persistidas no volume `redis_data` do Docker Compose. Para parar o serviço,
execute `docker compose down`.

## Opções do menu

1. Cadastrar uma configuração booleana ou de texto.
2. Listar as configurações cadastradas.
3. Atualizar uma configuração existente.
4. Remover uma configuração.
5. Sair.

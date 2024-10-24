import json
import time
from pedido import Pedido
import asyncio

def imprime_menu():
    MENU = """

Bem-vindo ao Restaurante Poderoso Chefão

(1) Fazer um pedido (item1,item2,item3,...)
(2) Cardápio
(0) Encerrar o programa

Para fazer um pedido, digite o nome do pedido ou codigo
"""
    print(MENU)


CARDAPIO_DICT = json.load(open("cardapio_itens.json","r"))
CARDAPIO_COMIDAS = []
CARDAPIO_CODIGOS = []
fila_pedidos = asyncio.Queue(maxsize=100)
atendentes = []

def construir_cardapios():
    for item in CARDAPIO_DICT:
        for chave in item:
            if chave == "nome":
                CARDAPIO_COMIDAS.append(item[chave])
            if chave == "codigo":
                CARDAPIO_CODIGOS.append(item[chave])

def check_pedido(pedido,lista):
    if pedido not in lista:
        return False
    return True

def imprime_cardapio():
    for item in CARDAPIO_DICT:
        for chave in item:
            print(f"{chave}: {item[chave]}")
        print("*"*15)

async def atender(fila):
    while True:
        pedido = await fila.get()
        await asyncio.sleep(pedido.id_pedido + 10)
        print(f'Atendendo o pedido {pedido.id_pedido}...')
        fila.task_done()

async def processar_pedidos(pedidos_por_vez):
    
    if fila_pedidos.qsize() == pedidos_por_vez:
        print("Trabalhando nos pedidos ...")
        for _ in range(pedidos_por_vez):
            atendente = asyncio.create_task(atender(fila_pedidos))
            atendentes.append(atendente)
        await fila_pedidos.join()
        for a in atendentes:
            a.cancel()
        await asyncio.gather(*atendentes, return_exceptions=True)

def validar_pedidos(itens):
    check = False
    for item in itens:
        try:
            codigo = int(item)
            check = check_pedido(codigo,CARDAPIO_CODIGOS)
        except:
            item = item.strip()
            check = check_pedido(item,CARDAPIO_COMIDAS)
    return check

async def adicionar_pedido_fila(pedido_valido,itens):
    if pedido_valido:
        pedido = Pedido(itens)
        await fila_pedidos.put(pedido)
        print(f"Pedido {pedido.id_pedido} está em processamento, aguarde :)")
    else:
        print("Pedido inválido")
    
async def app_loop(fila_pedidos,pedidos_por_vez: int):
    while True:
        imprime_menu()
        construir_cardapios()
        if not fila_pedidos.empty():
            await processar_pedidos(pedidos_por_vez)
        try:
            print("\n")
            op = int(input("Digite uma opção: "))
        except ValueError:
            print("Opção inválida")
            print("\n")
            op = int(input("Digite uma opção: "))
        if op == 1:
            pedido_valido = True
            itens = input("Digite os itens desejados (nome ou codigo, separados por vírgula): ").split(",")
            pedido_valido = validar_pedidos(itens)
            await adicionar_pedido_fila(pedido_valido,itens)
            time.sleep(2)
        elif op == 2:
            imprime_cardapio()
            time.sleep(2)
        elif op == 0:
            print("Encerrando o programa")
            time.sleep(2)
            break
    
async def main():
    await app_loop(fila_pedidos,3)

asyncio.run(main())
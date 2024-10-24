from datetime import datetime

count = 1
ids_possiveis = [id for id in range(101)]

def gerar_id_pedido():
    global count
    id = ids_possiveis[count]
    count +=1
    return id

class Pedido:
    def __init__(self,itens: list):
        self.__itens = itens
        self.__id_pedido = gerar_id_pedido()
        self.__timestamp_pedido = datetime.now()
    @property
    def id_pedido(self):
        return self.__id_pedido
    @property
    def timestamp_pedido(self):
        return self.__timestamp_pedido
    def set_itens(self,itens):
        self.__itens = itens
    @property
    def itens(self):
        return self.__itens
    def exibir_pedido(self):
        print(f"Itens: {self.__itens}\nId: {self.__id_pedido}\nTimestamp: {self.__timestamp_pedido}")
        print("-"*100)

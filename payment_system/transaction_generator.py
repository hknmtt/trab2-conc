from random import randint
import time
from threading import Thread

from globals import *
from payment_system.bank import Bank
from utils.transaction import Transaction
from utils.currency import Currency
from utils.logger import LOGGER


class TransactionGenerator(Thread):
    """
    Uma classe para gerar e simular clientes de um banco por meio da geracão de transações bancárias.
    Se você adicionar novos atributos ou métodos, lembre-se de atualizar essa docstring.

    ...

    Atributos
    ---------
    _id : int
        Identificador do gerador de transações.
    bank: Bank
        Banco sob o qual o gerador de transações operará.

    Métodos
    -------
    run():
        ....
    """

    def __init__(self, _id: int, bank: Bank):
        Thread.__init__(self)
        self._id  = _id
        self.bank = bank


    def run(self):
        """
        Esse método deverá gerar transacões aleatórias enquanto o banco (self._bank_id)
        estiver em operação.
        """
        # TODO: IMPLEMENTE AS MODIFICAÇÕES, SE NECESSÁRIAS, NESTE MÉTODO!

        LOGGER.info(f"Inicializado TransactionGenerator para o Banco Nacional {self.bank._id}!")

        operating = banks[self.bank._id].operating

        i = 0
        while operating:
            origin = (self.bank._id, randint(0, accounts_per_bank-1))
            destination_bank = self.bank._id
            destination = (destination_bank, randint(0, accounts_per_bank-1))
            # amount = randint(100, 1000000)
            amount = 100
            new_transaction = Transaction(i, origin, destination, amount, currency=Currency(destination_bank+1))
            banks[self.bank._id].transaction_queue.put(new_transaction) # Usando Queue
            i+=1
            # LOGGER.debug(f"TransactionGenerator {self._id} gerou uma nova transação: {new_transaction}")
            time.sleep(0.2 * time_unit)
            operating = banks[self.bank._id].operating

        LOGGER.info(f"O TransactionGenerator {self._id} do banco {self.bank._id} foi finalizado.")


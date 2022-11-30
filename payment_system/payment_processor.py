import time
from threading import Thread

from globals import *
from payment_system.bank import Bank
from utils.transaction import Transaction, TransactionStatus
from utils.logger import LOGGER


class PaymentProcessor(Thread):
    """
    Uma classe para representar um processador de pagamentos de um banco.
    Se você adicionar novos atributos ou métodos, lembre-se de atualizar essa docstring.

    ...

    Atributos
    ---------
    _id : int
        Identificador do processador de pagamentos.
    bank: Bank
        Banco sob o qual o processador de pagamentos operará.

    Métodos
    -------
    run():
        Inicia thread to PaymentProcessor
    process_transaction(transaction: Transaction) -> TransactionStatus:
        Processa uma transação bancária.
    """

    def __init__(self, _id: int, bank: Bank):
        Thread.__init__(self)
        self._id  = _id
        self.bank = bank


    def run(self):
        """
        Esse método deve buscar Transactions na fila de transações do banco e processá-las 
        utilizando o método self.process_transaction(self, transaction: Transaction).
        Ele não deve ser finalizado prematuramente (antes do banco realmente fechar).
        """
        # TODO: IMPLEMENTE/MODIFIQUE O CÓDIGO NECESSÁRIO ABAIXO !

        LOGGER.info(f"Inicializado o PaymentProcessor {self._id} do Banco {self.bank._id}!")
        queue = banks[self.bank._id].transaction_queue

        while self.bank.operating:
            try:
                transaction = queue.get()
                LOGGER.info(f"Transaction_queue do Banco {self.bank._id}: {queue.qsize()}")
            except Exception as err:
                LOGGER.error(f"Falha em PaymentProcessor.run(): {err}")
            else:
                self.process_transaction(transaction)

            # time.sleep(350 * time_unit)  # Remova esse sleep após implementar sua solução!

        LOGGER.info(f"O PaymentProcessor {self._id} do banco {self.bank._id} foi finalizado.")


    def process_transaction(self, transaction: Transaction) -> TransactionStatus:
        """
        Esse método deverá processar as transações bancárias do banco ao qual foi designado.
        Caso a transferência seja realizada para um banco diferente (em moeda diferente), a 
        lógica para transações internacionais detalhada no enunciado (README.md) deverá ser
        aplicada.
        Ela deve retornar o status da transacão processada.
        """
        # TODO: IMPLEMENTE/MODIFIQUE O CÓDIGO NECESSÁRIO ABAIXO !
        
        LOGGER.info(f"PaymentProcessor {self._id} do Banco {self.bank._id} iniciando processamento da Transaction {transaction._id}!")
        # # Caso a transferencia é nacional(mesmo banco)
        # if transaction.origin[0] == transaction.destination[0]:
        #     # bloqueia ambas as contas de outras transações
        #     if transaction.origin[1] > transaction.destination[1]:
        #         self.bank.lock_account(transaction.origin[1])
        #         self.bank.lock_account(transaction.destination[1])
        #     else:
        #         self.bank.lock_account(transaction.destination[1])
        #         self.bank.lock_account(transaction.origin[1])

        # withdraw da conta origem
        if banks[transaction.origin[0]].accounts[transaction.origin[1]-1].withdraw(transaction.amount):
            # NÃO REMOVA ESSE SLEEP!
            # Ele simula uma latência de processamento para a transação.
            # time.sleep(3 * time_unit)
            # deposit na conta destino
            banks[transaction.destination[0]].accounts[transaction.destination[1]-1].deposit(transaction.amount)
            transaction.status = TransactionStatus.SUCCESSFUL
        else:
            # NÃO REMOVA ESSE SLEEP!
            # Ele simula uma latência de processamento para a transação.
            # time.sleep(3 * time_unit)
            transaction.status = TransactionStatus.FAILED

        # LOGGER.debug(f"PaymentProcessor {self._id} do Banco {self.bank._id} processou a transaction {transaction._id} com status {transaction.status}, conta origem {transaction.origin[0]} {transaction.origin[1]} e conta destino {transaction.destination[0]} {transaction.destination[1]}!")
        # LOGGER.debug(f"id da conta origem: {banks[transaction.origin[0]].accounts[transaction.origin[1]]._id} {transaction.origin[1]}")
        LOGGER.debug(f"PaymentProcessor {self._id} do Banco {self.bank._id} processou a transaction {transaction._id} com status {transaction.status}, conta origem {transaction.origin[0]} {transaction.origin[1]} e conta destino {transaction.destination[0]} {transaction.destination[1]}!")
        # antigo 
        LOGGER.debug(f"Saldo da conta origem: {banks[transaction.origin[0]].accounts[transaction.origin[1]-1].balance}")
        # novo saldo
        LOGGER.debug(f"Saldo da conta destino: {banks[transaction.destination[0]].accounts[transaction.destination[1]-1].balance}")
        time.sleep(3 * time_unit)
        return transaction.status

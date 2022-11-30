import argparse, time, sys
from logging import INFO, DEBUG
from random import randint
from threading import Thread, Semaphore

from globals import *
from payment_system.bank import Bank
from payment_system.payment_processor import PaymentProcessor
from payment_system.transaction_generator import TransactionGenerator
from utils.currency import Currency
from utils.logger import CH, LOGGER


if __name__ == "__main__":
    # Verificação de compatibilidade da versão do python:
    if sys.version_info < (3, 5):
        sys.stdout.write('Utilize o Python 3.5 ou mais recente para desenvolver este trabalho.\n')
        sys.exit(1)

    # Captura de argumentos da linha de comando:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_unit", "-u", help="Valor da unidade de tempo de simulação")
    parser.add_argument("--total_time", "-t", help="Tempo total de simulação")
    parser.add_argument("--debug", "-d", help="Printar logs em nível DEBUG")
    args = parser.parse_args()
    if args.time_unit:
        time_unit = float(args.time_unit)
    if args.total_time:
        total_time = int(args.total_time)
    if args.debug:
        debug = True

    # Configura logger
    if debug:
        LOGGER.setLevel(DEBUG)
        CH.setLevel(DEBUG)
    else:
        LOGGER.setLevel(INFO)
        CH.setLevel(INFO)

    # Printa argumentos capturados da simulação
    LOGGER.info(f"Iniciando simulação com os seguintes parâmetros:\n\ttotal_time = {total_time}\n\tdebug = {debug}\n")
    time.sleep(3)

    # Inicializa variável `tempo`:
    t = 0

    # Inicializa lista de threads de geradores de transações:
    transaction_generators = []
    # Inicializa lista de threads de processadores de transações:
    payment_processors = []
    
    # Cria os Bancos Nacionais e popula a lista global `banks`:
    for i, currency in enumerate(Currency):
        
        # Cria Banco Nacional
        bank = Bank(_id=i, currency=currency)
        
        # Deposita valores aleatórios nas contas internas (reserves) do banco
        bank.reserves.BRL.deposit(randint(100_000_000, 10_000_000_000))
        bank.reserves.CHF.deposit(randint(100_000_000, 10_000_000_000))
        bank.reserves.EUR.deposit(randint(100_000_000, 10_000_000_000))
        bank.reserves.GBP.deposit(randint(100_000_000, 10_000_000_000))
        bank.reserves.JPY.deposit(randint(100_000_000, 10_000_000_000))
        bank.reserves.USD.deposit(randint(100_000_000, 10_000_000_000))
        
        # Adiciona banco na lista global de bancos
        banks.append(bank)

    # Cria as contas de clientes
    for i in range(accounts_per_bank):
        for bank in banks:
            bank.new_account(balance=1_000_000 , overdraft_limit=100_000)

    # for bank in banks:
    #     for account in bank.accounts:
    #         account.info()

    # Inicializa gerador de transações e processadores de pagamentos para os Bancos Nacionais:
    for bank in banks:
        if bank._id == 0:
            transaction_generators.append(TransactionGenerator(_id=0, bank=bank))
        for i in range(payment_processors_per_bank):
            if bank._id == 0:
                payment_processors.append(PaymentProcessor(_id=i, bank=bank))
    
    for bank in banks:
        bank.operating = True

    # Inicializa as threads dos geradores e processadores 
    for transaction_generator in transaction_generators:
        transaction_generator.start()
    for payment_processor in payment_processors:
        payment_processor.start()

    # Enquanto o tempo total de simuação não for atingido:
    while t < total_time:
        # Aguarda um tempo aleatório antes de criar o próximo cliente:
        dt = randint(0, 3)
        time.sleep(dt * time_unit)

        # Atualiza a variável tempo considerando o intervalo de criação dos clientes:
        t += dt

    for bank in banks:
        bank.operating = False

    # Finaliza todas as threads
    for transaction_generator in transaction_generators:
        transaction_generator.join()
    for payment_processor in payment_processors:
        payment_processor.join()


    # Termina simulação. Após esse print somente dados devem ser printados no console.
    LOGGER.info(f"A simulação chegou ao fim!\n")

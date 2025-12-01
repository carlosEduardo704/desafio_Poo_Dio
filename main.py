import abc
from datetime import datetime
from abc import ABC

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
        self._agencia = "0001"

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @property
    def agencia(self):
        return self._agencia

    def sacar(self, valor: float) -> bool:
        saldo = self._saldo
        if valor > saldo:
            print('Valor excede o disponível em conta!')
        elif valor < 0:
            print('Valor Inválido!')
        else:
            saldo -= valor
            print('Saque concluido com sucesso!')
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True

        print("Valor inválido! Depósito Falhou!")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente,  limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        num_de_saques = len(
            [transacao for transacao in self.historico.trasacoes if transacao["tipo"] == "Saque"]
        )

        if valor > self.limite:
            print("Valor excede o disponivel em conta!")
        elif num_de_saques >= self.limite_saques:
            print("Numero de saques excedido!")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f" CLiente: {self.cliente.nome}\n Agencia: {self.agencia}\n Numero da conta: {self.numero}"

class Cliente:
    def __int__(self, endereco: str):
        self._endereco = endereco
        self.contas = []

    @staticmethod
    def realizar_trasacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Transacao(ABC):
    @property
    @abc.abstractmethod
    def valor(self):
        pass

    @abc.abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __int__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
        else:
            return False

class Saque(Transacao):
    def __int__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
        else:
            return False


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def trasacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

# Clase para manipular as assinaturas
class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    # Função para receber dados e inserir no banco de dados
    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription

    # Função para listar todas as assinaturas
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            return results

    # Função para deletar uma assinatura
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    # Função verificar se a assinatura já foi paga no mês
    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
            return False

    # Função para receber um id e retornar a assinatura correspondente
    def pay(self, subscription: Subscription, payment_date: date):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Payments.Subscription.empresa == subscription.empresa)
            results = session.exec(statement).all()

            if self._has_pay(results):
                question = input('Essa conta já foi paga esse mês, deseja pagar novamente ? Y ou N: ')

                if not question.upper() == 'Y':
                    return False
            
        pay = Payments(subscription_id = subscription.id, date=date.today())
        session.add(pay)
        session.commit()

    #Função para retornar o valor total das assinaturas
    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)      
            results = session.exec(statement).all()

        total = 0
        for result in results:
            total += result.valor

        return float(total)

    # Função para receber a data atual e organizar os 12 meses anteriores
    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]
    
    # Função para me retornar os valores das assinaturas dos 12 meses anteriores
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)

                value_for_months.append(value)
        return value_for_months

    # Função para gerar um gráfico com os valores das assinaturas dos 12 meses anteriores
    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)
        last_12_months = list(map(lambda x: x[0], self._get_last_12_months_native()))

        import matplotlib.pyplot as plt
        plt.plot(last_12_months, values_for_months)
        plt.show()
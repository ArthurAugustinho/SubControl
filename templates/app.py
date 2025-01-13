import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal

# Classe para manipular a interface
class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    # Função para iniciar a interface
    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Pagar assinatura
            [6] -> Sair
            ''')

            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay_subscription()
            else:
                break

    # Função para adicionar uma assinatura
    def add_subscription(self):
        empresa = input('Empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data de assinatura: '), '%d/%m/%Y')
        valor = Decimal(input('Valor: '))

        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)
        print('Assinatura adicionada com sucesso.')

    # Função para deletar uma assinatura
    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja excluir')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha a assinatura: '))
        self.subscription_service.delete(choice)
        print('Assinatura excluída com sucesso.')

         # Inativar pagamentos vinculados automaticamente
        with self.subscription_service.engine.connect() as connection:
            result = connection.execute(
                """
                UPDATE payments
                SET status = 'inativo'
                WHERE subscription_id = :subscription_id
                """,
                {"subscription_id": choice}
            )
        print(f'Assinatura excluída e {result.rowcount} pagamentos vinculados inativados com sucesso.')

    # Função para mostrar o valor total das assinaturas
    def total_value(self):
        print(f'Seu valor total mensal em assinaturas: {self.subscription_service.total_value()}')
    
    # Função para pagar uma assinatura
    def pay_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja pagar')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha a assinatura: '))
        subscription = self.subscription_service.get_subscription(choice)
        self.subscription_service.pay(subscription)
        print('Assinatura paga com sucesso.')


# Inicialização da interface
if __name__ == '__main__':
    UI().start()
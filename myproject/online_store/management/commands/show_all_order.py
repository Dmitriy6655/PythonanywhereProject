from online_store.models import Order

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Просмотр заказанных продуктов у клиента." \
           "Нужно ввести id заказа"

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='Order ID')

    def handle(self, *args, **kwargs):
        id_ord = kwargs.get('order_id')
        ord = Order.objects.filter(pk=id_ord).first()
        client = ord.client.name

        self.stdout.write(f'Клиент: \n {client} \n')
        self.stdout.write(f'  All product in order {id_ord }: \n  {ord.product.all()}')

# # получение данных из бд
# def index(request):
#     people = Person.objects.all()
#     return render(request, "index.html", {"people": people})

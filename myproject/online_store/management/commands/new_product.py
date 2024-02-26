from django.core.management.base import BaseCommand
from online_store.models import Client, Goods
from faker import Faker



class Command(BaseCommand):
    help = "Create new Good"

    def add_arguments(self, parser):
        faker = Faker(locale='ru-ru')
        parser.add_argument('--name', default=faker.text(max_nb_chars=8), type=str, help='Name of good')
        parser.add_argument('--descr', default=faker.text(max_nb_chars=80), type=str, help='Description')
        parser.add_argument('--q', default=faker.random_number(digits=3, fix_len=False), type=int, help='quantity')
        parser.add_argument('--price', default=faker.random_number(digits=4), type=float, help='Price')




    def handle(self, *args, **kwargs):
        name = kwargs.get('name')
        descr = kwargs.get('descr')
        amount = kwargs.get('q')
        price = kwargs.get('price')

        print(f'name={type(name)}')
        print(f'descr={type(descr)}')
        print(f'amount={type(amount)}')
        print(f'price={type(price)}')



        new_good = Goods.objects.create(
            name=name,
            description=descr,
            price=price,
            quantity=amount,
            image=None,
            product_added_date='',

        )


        self.stdout.write(f'Good {new_good.name} created')



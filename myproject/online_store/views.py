import logging
import datetime


from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from online_store.models import Client, Order, Goods, Image
from online_store.forms import EditGoodForm, ImageForm

logger = logging.getLogger(__name__)
from .forms import EditGoodForm


def get_clients(request: HttpRequest):
    title = "List CLIENTS"
    clients = Client.objects.all()

    context = {
        'title': title,
        "clients": clients,

    }
    return render(request, "online_store/clients.html", context=context)


def add_product_in_order(id_client: int, id_product: int, amount: int):

    product = Goods.objects.get(pk=id_product)
    total = float(product.price) * float(amount)
    client = Client.objects.get(pk=id_client)

    new_order = Order.objects.create(
        client=client,
        total_price=total,
        date_order=''
    )
    new_order.product.add(product)
    print(f"Заказ {new_order.id}создан.Добавлен продукт {product.name}")



def get_goods(request):
    title = 'Покупка товаров'
    goods = Goods.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        client_id = request.POST['number']
        client = Client.objects.get(pk=client_id)
        id_prod = request.POST['id_prod']
        # print(f'type= {type(id_prod)}')
        # print(f'client_id= {client_id}')
        amount = request.POST['amount']





        buy = Goods.objects.get(pk=id_prod)

        context = {
            'text': 'Клиент:',
            'title': title,
            "goods": goods,
            'client': client,
            'text2': 'Вы купили:',
            'buy': buy,
            'ID_prod': id_prod,
        }
        add_product_in_order(client_id, id_prod, amount)  # Создаем заказ и добавляем продукт в заказ
        return render(request, "online_store/goods_list.html", context=context)

    else:
        context = {
            "clients": clients,
            'text': 'ID клиента:',
            'title': title,
            "goods": goods,
            'text3': 'ID продукта:',
            'text4': 'Клиенты:',
            'client': '',
            'ID_prod': '',
        }
        return render(request, "online_store/goods_list.html", context=context)



def get_orders(request):
    title = 'Заказы'
    host = request.META["HTTP_HOST"]
    path = request.path
    text = f'{host}{path}'
    orders = Order.objects.all()
    prod = Goods.objects.all()
    if request.method == "POST":
        client_id = request.POST['number']
        client = Client.objects.get(id=client_id)
        print(f'Клиент = {client}')

        context = {
            'text': f'{text}',
            'client': f'{client}',
        }
        logger.info(f'context: {context}')
        return render(request, "online_store/orders.html", context=context)


    else:

        client = Client.objects.get(pk=1)

        context = {
            "orders": orders,
            'title': title,
            'client': client,
            'prod': prod,
        }
        logger.info(f'context: {context}')
        return render(request, "online_store/orders.html", context=context)


def get_orders_by_client_id(request, client_id: int):
    orders = Order.objects.filter(client_id=client_id)
    if orders:
        context = '\n'.join(str(order) for order in orders)
    else:
        context = f'У пользователя с id: {client_id} нет заказов'
    logger.info(f'context: {context}')
    return HttpResponse(context)


def delete_client(request, client_id: int):
    client = Client.objects.filter(pk=client_id)
    if client:
        client.delete()
        logger.info(f'Пользователь удален')
        return HttpResponse('Пользователь удален')
    else:
        logger.info(f'Пользователь не найден')
        return HttpResponse('Пользователь не найден')


def delete_goods(request, goods_id: int):
    goods = Goods.objects.filter(pk=goods_id)
    if goods:
        goods.delete()
        logger.info(f'Товар удален')
        return HttpResponse('Товар удален')
    else:
        logger.info(f'Товар не найден')
        return HttpResponse('Товар не найден')


def delete_order(request, order_id: int):
    order = Order.objects.filter(pk=order_id)
    if order:
        order.delete()
        logger.info(f'Заказ удален')
        return HttpResponse('Заказ удален')
    else:
        logger.info(f'Заказ не найден')
        return HttpResponse('Заказ не найден')


def edit_order_goods_id(request, order_id: int, goods_id: int):
    order = Order.objects.filter(pk=order_id).first()
    goods = Goods.objects.filter(pk=goods_id).first()
    if order:
        order.goods_id = goods
        order.save()
        return HttpResponse('Товар в заказе изменен')
    else:
        return HttpResponse('Такой заказ не найден')


def get_client_goods(request, client_id: int):
    COUNT_DAYS = 7
    start = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS)
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client_id=client_id, create_at__gte=start)
    context = {
        'title': 'шаблон',
        'count_days': COUNT_DAYS,
        'client': client,
        'orders': orders,
        'text': f'http://127.0.0.1:8000/get_client_goods/'
    }
    logger.info(f'context: {context}')
    return render(request, 'online_store/client_goods.html', context)


def get_prod_order(list_ord):
    list_prod = set()
    # print(f'prod = {orders7.values()}')

    # выделяем один заказ из всех и добавляем все продукты из заказа в множество
    for order in list_ord:
        # print(f'id = {order.id}')
        order_client = Order.objects.get(pk=order.id)
        # print(f'Продукты в заказе {u.id} = {order_client.product.all()}')
        list_prod.add(order_client.product.all())
    print(f'Продукты в заказе: {list_prod}')
    return list_prod


def client_goods(request):
    title = 'Заказы клиента'
    host = request.META["HTTP_HOST"]
    path = request.path
    text = f'{host}{path}'
    if request.method == "POST":
        client_id = request.POST['number']
        COUNT_DAYS7 = 7
        start = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS7)
        orders7 = Order.objects.filter(client_id=client_id, date_order__gte=start)
        set_product_in_order7 = get_prod_order(orders7)

        COUNT_DAYS30 = 30
        start2 = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS30)
        orders30 = Order.objects.filter(client_id=client_id, date_order__gte=start2)
        set_product_in_order30 = get_prod_order(orders30)

        COUNT_DAYS365 = 365
        start3 = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS365)
        client = Client.objects.get(id=client_id)
        orders365 = Order.objects.filter(client_id=client_id, date_order__gte=start3)
        set_product_in_order365 = get_prod_order(orders365)

        images = Goods.objects.all()
        # url_path = f'{text}{client_id}'
        context = {
            'title': title,
            'client': client,
            'orders7': set_product_in_order7,  # список уникальных продуктов в заказе клиента
            'orders30': set_product_in_order30,
            'orders365': set_product_in_order365,
            'images': images,
            'text': f'{text}'
        }
        logger.info(f'context: {context}')
        return render(request, 'online_store/client_goods.html', context)
    else:
        context = {
            'title': title,
            'text': f'{text}'
        }
        logger.info(f'context: {context}')
        return render(request, 'online_store/client_goods.html', context)


def main(request):
    context = {
        'title': 'Главная страница',
        'goods': Goods.objects.order_by('name', 'description')
    }
    logger.info(f'context: {context}')
    return render(request, 'online_store/index.html', context)


def all_clients(request: HttpRequest) -> HttpResponse:
    # clients_with_order_counts = Client.objects.annotate(order_count=Count("order"))
    clients_with_order_counts = Client.objects.all()
    return render(
        request, "online_store/index.html", context={"clients": clients_with_order_counts}
    )


def orders_by_client(request: HttpRequest, client_pk: int) -> HttpResponse:
    title = "orders_by_client"
    client = get_object_or_404(Client, pk=client_pk)
    orders = client.objects.all()
    all_goods_by_client = set()
    for order in orders:
        all_goods_by_client.update(order.goods.all())
    goods = sorted(list(all_goods_by_client), key=lambda good: good.pk, reverse=True)
    context = {
        'title': title,
        "client": client,
        "orders": orders,
        "goods": goods,
    }
    return render(request, "online_store/orders_by_client.html", context=context)


def order_full(request: HttpRequest, order_pk: int) -> HttpResponse:
    title = "order_full"
    order = get_object_or_404(Order, pk=order_pk)
    goods = order.product.all()
    context = {
        'title': title,
        "order": order,
        "goods": goods,
    }
    return render(request, "online_store/order_full.html", context=context)


def edit_good(request: HttpRequest, good_pk: int) -> HttpResponse:
    title = "форма"
    good = get_object_or_404(Goods, pk=good_pk)
    if request.method == "POST":
        form = EditGoodForm(request.POST, request.FILES)
        if form.is_valid():
            good.name = request.POST["title"]
            good.description = request.POST["description"]
            good.price = request.POST["price"]
            good.amount = request.POST["quantity"]
            if "image" in request.FILES:
                good.image = request.FILES["image"]
            good.save()
            img_obj = good.image
            return render(request, 'online_store/edit_good.html', {'form': form, 'img_obj': img_obj})
        else:
            form = EditGoodForm()
            if form.is_valid():
                good.name = request.POST["title"]
                good.description = request.POST["description"]
                good.price = request.POST["price"]
                good.amount = request.POST["quantity"]
                if "image" in request.FILES:
                    good.image = request.FILES["image"]
                good.save()
            logger.info(f"Good {good.name} edited")
            return render(request, 'online_store/edit_good.html', {'form': form})
            # return redirect("good_full", good_pk=good.pk)
    else:
        form = EditGoodForm(
            initial={
                "title": good.name,
                "description": good.product_description,
                "price": good.price,
                "quantity": good.amount,
            },
        )
    context = {
        'title': title,
        "form": form,
        "good": good,
    }
    return render(request, "online_store/edit_good.html", context=context)


def get_edit_good(request: HttpRequest) -> HttpResponse:
    title = "форма"
    good = get_object_or_404(Goods, pk=1)
    if request.method == "POST":
        form = EditGoodForm(request.POST, request.FILES)
        if form.is_valid():
            good.name = request.POST["title"]
            good.description = request.POST["description"]
            good.price = request.POST["price"]
            good.amount = request.POST["quantity"]
            if "image" in request.FILES:
                good.image = request.FILES["image"]
            good.save()
            logger.info(f"Good {good.name} edited")
            return redirect("good_full", good_pk=good.pk)
    else:
        form = EditGoodForm(
            initial={
                "title": good.name,
                "description": good.description,
                "price": good.price,
                "quantity": good.amount,
            },
        )
    context = {
        'title': title,
        "form": form,
        "good": good,
    }
    return render(request, "online_store/edit_good.html", context=context)


def upload_images(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/upload_images")
    else:
        form = ImageForm

    return render(request, 'online_store/images.html', {'form': form})


def upload_images1(request):
    if request.method == 'GET':
        images = Image.objects.order_by('title')
        return render(request, "online_store/images.html", {"images": images})

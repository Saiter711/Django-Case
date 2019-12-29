from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render

from .forms import OrderForm, ComplaintForm, CommentForm
from .models import Product, Order, Complaint, OrderedProduct, Discount, Comment


# Create your views here.


def index(request):
    return render(request,
                  'sklep/glowna.html'
                  )


def product_list(request):
    products = Product.objects.order_by('id')
    context = {'products': products}

    return render(request,
                  "sklep/list.html",
                  context
                  )


def detail(request, product_id):
    product = Product.objects.get(id = product_id)
    average = 0
    iterator = 0
    context = {"products": product,
               }
    product_comments = []
    comments = list(Comment.objects.order_by('id'))

    for comment in comments:
        if comment.product is not None and comment.product.id == product_id:
            product_comments.append(comment)
    if product_comments:
        for x in product_comments:
            average += x.grade
            iterator += 1
        average /= iterator
    else:
        average = 0
    context['avg'] = format(average, ".2f")
    return render(request,
                  'sklep/szczegol.html',
                  context)


def comments_detail(request, product_id):
    product_comments = []
    comments = list(Comment.objects.order_by('id'))

    for comment in comments:
        if comment.product is not None and comment.product.id == product_id:
            product_comments.append(comment)

    context = {'comments': product_comments,
               'product_id': product_id}

    return render(request, "sklep/comments.html", context)


def _show_table(products, arg):
    products = products if not None else []
    amount_list = list()
    product_list = list()
    if arg is 'order':
        for x in products:
            if x.product.name not in product_list:
                product_list.append(x.product.name)
                amount_list.append(1)
            else:
                id = product_list.index(x.product.name)
                amount_list[id] += 1
    elif arg is 'cart':
        for x in products:
            if x.name not in product_list:
                product_list.append(x.name)
                amount_list.append(1)
            else:
                id = product_list.index(x.name)
                amount_list[id] += 1
    return product_list, amount_list


def order_details(request,order_id):
    order = get_object_or_404(Order, pk = order_id)
    ordered_products = order.get_ordered_products()
    total_price = order.get_total_price()
    amount_list = list()
    product_list = list()
    product_list, amount_list = _show_table(ordered_products, 'order')
    context = {'ordered': ordered_products,
               'total': format(total_price, '.2f'),
               'prolist': product_list,
               'amlist': amount_list,
               }
    if order.discount_code is not None:
        context['discount'] = order.discount_code.discount
        total_price *= (1 - order.discount_code.discount / 100)
        context['total'] = format(total_price, '.2f')
    return render(request,
                  'sklep/order_details.html',
                  context
                  )


def order(request):
    products = _get_products_in_cart(request)

    if request.method =='POST':
        form = OrderForm(request.POST)
        if(form.is_valid()):
            order = Order(
                first_name = form.cleaned_data['first_name'],
                surname = form.cleaned_data['surname'],
                address = form.cleaned_data['address'],
                send = form.cleaned_data['send'],
            )
            if 'Discount_code' in request.POST:
                try:
                    order.discount_code = Discount.objects.get(name=request.POST['Discount_code'])
                except:
                    pass
            order.save()
            for product in products:
                ordered_product = OrderedProduct(
                    product = product, order = order, amount =1
                ).save()
            request.session['cart'] = []
            return HttpResponseRedirect('/order/'+str(order.id))
    else:
        form = OrderForm()
    return render(request, "sklep/order_form.html", {"form": form,
                                                     "products": products
                                                     })


def comment(request, product_id):
    context = {}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if(form.is_valid()):
            product1 = Product.objects.get(id=product_id)
            comment1 = Comment(
                grade = form.cleaned_data['grade'],
                comment = form.cleaned_data['comment'],
                product = product1,
                nickname = form.cleaned_data['nickname'],
            ).save()
            return HttpResponseRedirect('/products/'+str(product_id))
        else:
            context['error'] = True
    else:
        form = CommentForm()
        context['error'] = False
    context['form']= form,
    context['product_id'] = product_id
    return render(request, "sklep/comment_form.html", context)


def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if (form.is_valid()):
            complaint = Complaint(
                name = form.cleaned_data['name'],
                message = form.cleaned_data['message']
            )
            complaint.save()
            return HttpResponseRedirect('/complaint/' + str(complaint.id))
    else:
        form = ComplaintForm()
    return render(request, "sklep/complaint_form.html", {"form": form})


def complaint_details(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    context = {"complaint": complaint}

    return render(request,
                  "sklep/complaint_details.html",
                  context
                  )


def cart(request):
    products_in_cart = _get_products_in_cart(request)

    def sorting(x):
        return x.name
    products_in_cart.sort(key=sorting)
    pro_list, am_list = _show_table(products_in_cart, 'cart')
    all = 0
    for x in products_in_cart:
        all += x.price

    return render(request, "sklep/cart.html", {'products': products_in_cart,
                                               'sum': format(all, '.2f'),
                                               'prolist': pro_list,
                                               'amlist': am_list})


def _get_products_in_cart(request):
    products_in_cart = []
    for item_id in request.session.get('cart', []):
        product = Product.objects.get(pk=item_id)
        products_in_cart.append(product)
    return products_in_cart


def add_to_cart(request):
    if request.method == "POST":
        if 'cart' not in request.session:
            request.session['cart'] = []

        item_id = request.POST['item_id']
        request.session['cart'].append(item_id)
        request.session.modified = True

    return HttpResponseRedirect("/cart")


def modify_cart(request):
    if request.method == "POST":
        if request.POST['value'] is not '':
            if 'cart' not in request.session:
                request.session['cart'] = []
            product = Product.objects.get(name=request.POST['item_name'])
            item_id = str(product.id)
            length = len(request.session['cart'])
            iterator = 0
            for x in range(length):
                if item_id == request.session['cart'][x]:
                    iterator += 1
            for x in range(iterator):
                request.session['cart'].remove(item_id)
            for x in range(int(request.POST['value'])):
                request.session['cart'].append(str(item_id))
            request.session.modified = True
    return HttpResponseRedirect("/cart")


def remove_from_cart(request):
    if request.method == "POST":
        if 'cart' not in request.session:
            request.session['cart'] = []
        product = Product.objects.get(name = request.POST['item_name'])
        item_id = str(product.id)
        length = len(request.session['cart'])
        iterator = 0
        for x in range(length):
            if item_id == request.session['cart'][x]:
                iterator += 1
        for x in range(iterator):
            request.session['cart'].remove(item_id)
        request.session.modified = True
    return HttpResponseRedirect("/cart")

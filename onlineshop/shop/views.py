from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView

from shop.models import Product, ShopBasket, Order
from shop.models import Category
from shop.forms import ProductForm, CategoryForm

def DeleteShoppingBasket(pk):
    product = ShopBasket.objects.get(id=pk)
    product.delete()

def create_order(product, user, quantity, pk):

    Order.objects.create(user=user, product=ShopBasket.objects.get(id=pk).product, quantity=quantity)

    i = Product.objects.get(name=ShopBasket.objects.get(id=pk).product.name)
    i.quantity -= quantity
    i.save()

    DeleteShoppingBasket(pk)



# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        print(request.path)
        return super().get(request, args, kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.is_authenticated:
            return redirect('error1')
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    context_object_name = 'form'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('error2')
        elif not request.user.is_staff:
            return redirect('error1')
        return super().get(request, *args, **kwargs)


class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'create_category.html'
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('error1')
        elif not request.user.is_authenticated:
            return redirect('error2')
        return super().get(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    context_object_name = 'form'
    success_url = reverse_lazy('my-products')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('error2')
        elif request.user.is_active and not request.user.is_superuser and not request.user.is_staff:
            return redirect('error1')
        return super().get(request, *args, **kwargs)


class UpdateCategoryView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'update_category'
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('error2')
        elif not request.user.is_superuser:
            return redirect('error1')
        return super().get(request, *args, **kwargs)


def ProductDeleteView(request, pk):
    if request.user == Product.objects.get(id=pk).creator or request.user.is_superuser:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('product-list')
    else:
        return redirect('arror1')
    return super().get(request, *args, **kwargs)


def CategoryDeleteView(request, pk):
    if request.user.is_superuser:
        category = Category.objects.get(id=pk)
        category.delete()
        return redirect('product-list')
    else:
        return redirect('error1')
    return super().get(request, *args, **kwargs)


def placing_an_order(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        print(name, surname)

        product = ShopBasket.objects.get(id=pk)
        user = request.user
        quantity = ShopBasket.objects.get(id=pk).quantity

        create_order(product, user, quantity, pk)

        return redirect('product-list')
    return render(request, 'placing_an_order.html')


def AddShoppingBasket(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user
    sum = Product.objects.get(id=pk).price

    ShopBasket.objects.create(product=product, user=user, sum=sum)

    return redirect('product-list')

def delete_from_basket(request, pk):
    product = ShopBasket.objects.get(id=pk)
    product.delete()
    return redirect('product-list')

def ShoppingBasket(request):
    context = {'products': ShopBasket.objects.filter(user=request.user)}
    return render(request, 'shopping_basket.html', context)


def MyProductsView(request):
    products = Product.objects.filter(creator=request.user)
    return render(request, 'my_products.html', {"products": products})


class OrdersView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'


class Error1(TemplateView):
    template_name = "errors/you_aren't_admin_or_superuser.html"


class Error2(TemplateView):
    template_name = "errors/please_register_or_login.html"


class Owners(ListView):
    model = User
    template_name = "owners_list.html"
    extra_context = {"owners": User.objects.filter(is_staff=True, is_superuser=False)}


def Owner(request, pk):
    context = {"owner_products": Product.objects.filter(creator=User.objects.get(id=pk))}
    return render(request, 'owner.html', context)

class Orders(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('error2')
        if not request.user.is_superuser:
            return redirect('error1')
        return super().get(request,*args,**kwargs)

class OrderDetail(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('error2')
        if not request.user.is_superuser:
            return redirect('error1')
        return super().get(request,*args,**kwargs)

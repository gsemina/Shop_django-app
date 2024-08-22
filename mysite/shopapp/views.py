"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т д.
"""


import logging
from timeit import default_timer
from csv import DictWriter

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    UserPassesTestMixin,
    LoginRequiredMixin
)
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse
)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from myauth.models import Profile
from .common import save_csv_products
from .forms import GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


log = logging.getLogger(__name__)


class UserOrdersListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения данных о заказах пользователя.
    """
    model = Order
    template_name = "shopapp/user_orders_list.html"

    def get_queryset(self):
        self.owner = get_object_or_404(
            Profile.objects.select_related('user'),
            user_id=self.kwargs["pk"]
        )
        self.queryset = (Order.objects
                         .select_related('user')
                         .filter(user_id=self.owner.user_id))
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        for user in self.queryset:
            context["owner"] = user.user
            return context



@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]

    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]

    ordering_fields = [
        "pk",
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        print("Hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(
                description="Empty response, product by id not found"
            ),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):

        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response
    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    """
        Набор представлений для действий над Order.

        Полный CRUD для сущностей товара
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
            DjangoFilterBackend,
            OrderingFilter,
        ]

    filterset_fields = [
        "delivery_address",
        "promocode",
        "created_at",
        "user",
        "products",

    ]

    ordering_fields = [
        "pk",
        "delivery_address",
        "user",
        "created_at",
        "products",
    ]


class ShopIndexView(View):
    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 5,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering for index")
        print("shop index context", context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class LatestProductsFeed(Feed):
    title = "Product"
    description = "Updates on changes and addition product"
    link = reverse_lazy("shopapp:products-feed")

    def items(self):
        return (Product.objects.filter(archived=False).order_by("-created_at")
                )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

    def item_link(self, item: Product):
        return reverse("shopapp:product_details", kwargs={"pk": item.pk})



class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "description", "price", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        user_created = form.save(commit=False)
        user_created.created_by = self.request.user
        user_created.save()
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = "name", "description", "price", "discount", "preview"
    template_name_suffix = "_update_form"


    def get_success_url(self) -> str:
        return reverse(
            "shopapp:product_details", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return (user.is_superuser or
                (user.has_perm('shopapp.change_product') and
                product.created_by == user))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        return reverse("shopapp:order_details", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


@user_passes_test(lambda u: u.is_staff)
def orders_data_export(request):
    orders = Order.objects.all()
    orders_data = [
        {
            "pk": order.pk,
            "address": order.delivery_address,
            "promocode": order.promocode,
            "user_id": order.user.id,
            "product": list(order.products.values('id')),
        }
        for order in orders
    ]
    return JsonResponse({"orders": orders_data})


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        # elem = products_data[0]
        # name = elem["name"]
        # print("name:", name)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):
    """
    Экспорт данных о заказах выбранного пользователя в формате JSON.
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        cache_key = "user_orders_export"
        orders_data = cache.get(cache_key)

        self.owner = get_object_or_404(
            Profile.objects.select_related('user'),
            user_id=self.kwargs["pk"]
        )

        queryset = (Order.objects.order_by('-pk')
                    .select_related('user')
                    .filter(user_id=self.owner.user_id))
        if orders_data is None:

            orders_data = [
                {
                    "pk": order.id,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,

                    "user": order.user.pk,
                    "products": [product.pk for product in order.products.all()],
                }
                for order in queryset
            ]
            cache.set(cache_key, orders_data, 300)
        return JsonResponse({"orders": orders_data})
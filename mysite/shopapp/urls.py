from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter


from .views import (
    ShopIndexView,
    GroupListView,
    ProductDetailsView,
    ProductsListView,
    ProductsDataExportView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductViewSet,
    LatestProductsFeed,
    OrderUpdateView,
    OrderDeleteView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderDetailView,
    orders_data_export,
    OrderViewSet,
    UserOrdersListView,
    OrdersDataExportView,
)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupListView.as_view(), name="groups-list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/",
         ProductCreateView.as_view(),
         name="product_create"),
    path("products/<int:pk>/",
         ProductDetailsView.as_view(),
         name="product_details"),
    path("products/<int:pk>/update/",
         ProductUpdateView.as_view(),
         name="product_update"),
    path("products/<int:pk>/arhive/",
         ProductDeleteView.as_view(),
         name="product_delete"),
    path("products/export/",
         ProductsDataExportView.as_view(),
         name="products-export"),
    path("products/latest/feed",
         LatestProductsFeed(), name="products-feed"),
    path("orders/",
         OrderListView.as_view(),
         name="orders_list"),
    path("orders/<int:pk>/update/",
         OrderUpdateView.as_view(),
         name="order_update"),
    path("orders/<int:pk>/",
         OrderDetailView.as_view(),
         name="order_details"),
    path("orders/create/",
         OrderCreateView.as_view(),
         name="order_create"),
    path("orders/<int:pk>/delete/",
         OrderDeleteView.as_view(),
         name="order_delete"),
    path("orders/export/", orders_data_export, name="orders_export"),
    path("users/<int:pk>/orders/",
         UserOrdersListView.as_view(),
         name="user_orders"),
    path("users/<int:pk>/orders/export/",
         OrdersDataExportView.as_view(),
         name="user_orders_export"),
]
 from .views import *
from rest_framework import routers
from django.urls import path, include



router = routers.SimpleRouter()
router.register(r'image', ProductImageViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'user', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),
    path('', include(router.urls)),
    path('category/',CategoryListViewSet.as_view(), name='category_list' ),
    path('category/<int:pk>/',CategoryDetailViewSet.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListViewset.as_view(), name='sub_category_list' ),
    path('sub_category/<int:pk>/', SubCategoryDetailViewset.as_view(), name='sub_category_detail'),
    path('product/', ProductListViewset.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailViewSet.as_view(), name='product_detail'),
    path('cart/', CartViewSet.as_view(), name='cart_detail'),
    path('cart_items/',CartItemViewSet.as_view({'get':'list', 'post': 'create'})),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]

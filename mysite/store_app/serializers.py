from .models import (UserProfile, Category, SubCategory,
                     ProductImage, Product, Review, Cart, CartItem, )
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image','article_number']



class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = CategoryListSerializer(many=True, read_only=True)


    class Meta:
        model = Category
        fields = ['category_name',]


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name',]


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    product = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['product','subcategory_name',]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileReviewSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'stars', 'comment','created_date']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    subcategory = SubCategoryListSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','product_image' ,'product_name', 'price', 'subcategory','avg_rating', 'count_people']

    def avg_rating(self, obj):
        return obj.avg_rating()

    def count_people(self, obj):
        return obj.count_people()


class ProductDetailSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    subcategory = SubCategoryListSerializer()
    review = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'subcategory',
                  'article_number','product_image' ,'descriptions', 'video','review','avg_rating','count_people' ]


    def avg_rating(self, obj):
        return obj.avg_rating()

    def count_people(self, obj):
        return obj.count_people()





class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product', 'product_id' ,'quantity','total_price',]

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [ 'id', 'user', 'items','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
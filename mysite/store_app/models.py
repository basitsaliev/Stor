from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(70)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField()
    STATUS_CHOICE = (
        ('gold', 'gold'), #75%
        ('silver', 'silver'), #50%
        ('bronze', 'bronze'), #25%
        ('simple', 'simple') #0%
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICE, default='simple')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

class Category(models.Model):
    category_image = models.ImageField(upload_to="category_image/")
    category_name = models.CharField(max_length=64, unique=True)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    subcategory_name = models.CharField(max_length=64, unique=True)


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product')
    product_name = models.CharField(max_length=56)
    price = models.PositiveSmallIntegerField()
    article_number = models.PositiveSmallIntegerField(unique=True)
    descriptions = models.TextField()
    image = models.ImageField(upload_to='image/')
    video = models.FileField(upload_to='video/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.product_name

    def avg_rating(self):
        ratings = self.review.all()
        if ratings.exists():
            return sum([i.stars for i in ratings]) / ratings.count()
        return 0


    def count_people(self):
        ratings = self.review.all()
        return ratings.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='image/')


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='review')
    comment = models.TextField()
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

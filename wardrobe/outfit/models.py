from django.db import models
from django.contrib.auth.models import User


class ClothingItem(models.Model):

    CATEGORY_CHOICES = [
        ('Top','Top'),
        ('Bottom','Bottom'),
        ('Dress','Dress'),
        ('Outerwear','Outerwear'),
        ('Footwear','Footwear'),
        ('Accessory','Accessory'),
    ]

    SEASON_CHOICES=[
        ('Summer','Summer'),
        ('Winter','Winter'),
        ('Monsoon','Monsoon'),
        ('All Season','All Season'),
    ]

    OCCASION_CHOICES=[
        ('Casual','Casual'),
        ('Formal','Formal'),
        ('Party','Party'),
        ('College','College'),
        ('Office','Office'),
        ('Wedding','Wedding'),
        ('Sports','Sports'),
        ('Travel','Travel'),
    ]

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name=models.CharField(max_length=100)

    category=models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    color=models.CharField(max_length=50)

    size=models.CharField(max_length=20)

    brand=models.CharField(
        max_length=100,
        blank=True
    )

    season=models.CharField(max_length=200)

    occasion=models.CharField(max_length=200)

    image=models.ImageField(
        upload_to='clothing/',
        blank=True,
        null=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Outfit(models.Model):

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name=models.CharField(max_length=100)

    description=models.TextField(
        blank=True
    )

    clothing_items=models.ManyToManyField(
        ClothingItem
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                        verbose_name='Родительская категория', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=100)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/photo', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Тут надо ввести название раздела',
        unique=True,
        verbose_name='Название раздела'
    )

    class Meta:
     ordering = ['id']
     verbose_name = 'Раздел'
     verbose_name_plural = 'Разделы'

     def __str__(self):
         return self.title


class Product(models.Model):
         sections = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
         title = models.CharField(max_length=70, verbose_name='Название')
         image = models.ImageField(upload_to='images', verbose_name='Изображение')
         price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
         year = models.IntegerField(
             validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)],
             verbose_name='Год'
         )
         country = models.CharField(max_length=70, verbose_name='Страна')
         director = models.CharField(max_length=70, verbose_name='Режиссер')
         play = models.IntegerField(
              validators = [MinValueValidator(1)],
              null=True,
              blank=True, #blank - необязательность поля
              verbose_name='Продолжительность',
              help_text='В секундах'
         )
         # установка библиотеки Pillow: Settings -> Python Interpreter -> "+"
         cast = models.TextField(verbose_name='В ролях')
         description = models.TextField(verbose_name='Описание')
         date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

         class Meta:
            ordering = ['title', '-year']
            verbose_name = 'Товар'
            verbose_name_plural = 'Товары'

         def __str__(self):
            return '{0} ({1})'.format(self.title, self.section.title) #Кто я? (Боевики)


class Discount(models.Model):
        code = models.CharField(max_length=10, verbose_name='Код купона')
        value = models.IntegerField(
            validators = [MinValueValidator(1), MaxValueValidator(100)],
            help_text = 'В процентах'
        )

        class Meta:
            ordering = ['-value'] #сортировка скидок, начинающаяся со скидок с самым большим наминалом
            verbose_name = 'Скидка'
            verbose_name_plural = 'Скидки'

        def __str__(self):
            return self.code + ' (' + str(self.value) + '%)' #ABC (25%)


class Order(models.Model): #Заказ
    need_delivery = models.BooleanField(verbose_name='Необходима доставка')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70, verbose_name='Имя')
    phone = models.CharField(max_length=70, verbose_name='Телефон')
    email = models.EmailField()
    address = models.TextField(verbose_name='Адрес',blank=True)
    notice = models.TextField(blank=True, verbose_name='Примечание к заказу')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    date_send = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки')

    STATUSES = [ #список статусов
        ('NEW', 'Новый заказ'),
        ('APR', 'Подтвержден'),
        ('PAY', 'Оплачен'),
        ('CNL', 'Отменен'),
    ]

    status = models.CharField(choices=STATUSES, max_length=3, default='NEW', verbose_name='Статус')

    class Meta:
        ordering = ['-date_order'] #сортировка заказов, начинающаяся со самых свежих заказов
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'ID: ' + str(self.id)


class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name = 'Заказ', on_delete = models.CASCADE)  #models.CASCADE() - удаляет все связанные объектыс ним
    product = models.ForeignKey(Product, verbose_name = 'Товар', on_delete = models.SET_NULL, null = True) #можно удалять из списка один заказ
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Цена', default = 0) #цена за единицу товара)
    count = models.IntegerField(verbose_name = 'Количество', validators = [MinValueValidator(1)], default = 1) #кол-во товара

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

    def __str__(self):
        return 'Заказ (ID {0} {1}: {2} шт.'.format(self.order.id, self.product.title, self.count)
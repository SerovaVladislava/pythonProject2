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
         price = models.DecimalField(max_length=10, decimal_places=2, verbose_name='Цена')



         

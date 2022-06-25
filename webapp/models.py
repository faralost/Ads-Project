from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class ToDeleteAdManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status='DEL')


class Ad(models.Model):
    TO_MODERATE = 'MOD'
    PUBLISHED = 'PUB'
    REJECTED = 'REJ'
    TO_DELETE = 'DEL'

    AD_STATUS_CHOICES = [
        (TO_MODERATE, 'На модерацию'),
        (PUBLISHED, 'Опубликовано'),
        (REJECTED, 'Отклонено'),
        (TO_DELETE, 'На удаление')
    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    piblished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    photo = models.ImageField(null=True, blank=True, upload_to='ad_photos', verbose_name='Фото')
    category = models.ForeignKey(
        'webapp.Category',
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='ads'
    )
    price = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(0),)
    )
    status = models.CharField(
        max_length=3,
        choices=AD_STATUS_CHOICES,
        default=TO_MODERATE,
    )

    objects = models.Manager()
    exclude_to_delete_objects = ToDeleteAdManager()

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return f'{self.name}'


from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Профиль')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name='Аватар')
    github_profile = models.URLField(verbose_name='Ссылка на Гитхаб', null=True, blank=True)
    about = models.TextField(max_length=1000, verbose_name='О себе', null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)
    phone_number = models.CharField(
        max_length=17,
        verbose_name='Номер телефона',
        validators=[RegexValidator(
            regex='^\+[9]{2}?[6] [0-9]{3} [0-9]{3} [0-9]{3}$',
            message='Введите номер телефона в формате +996 ХХХ ХХХ ХХХ'
        )]
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Профиль: {self.user.username}. {self.id}"

    def get_absolute_url(self):
        return reverse('accounts:detail_profile', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


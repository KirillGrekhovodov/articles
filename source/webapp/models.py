from django.db import models
from django.utils.text import slugify

status_choices = [('new', 'Новая'), ('moderated', 'Модерированная'), ('deleted', 'Удаленная')]


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", unique=True)
    description = models.TextField(max_length=2000, verbose_name="Описание", blank=True, null=True)
    title_slug = models.SlugField(max_length=50, verbose_name="Слаг", unique=True)

    def save(self, *args, **kwargs):
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор", default="Неизвестный")
    content = models.TextField(max_length=2000, verbose_name="Контент")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.CharField(max_length=20, verbose_name="Статус", choices=status_choices,
                              default=status_choices[0][0])
    publish_date = models.DateField(null=True, blank=True, verbose_name="Дата публикации")
    category = models.ForeignKey("webapp.Category",
                                 related_name="articles",
                                 on_delete=models.SET_NULL,
                                 verbose_name="Категория",
                                 null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

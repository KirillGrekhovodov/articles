from django.db import models

status_choices = [('new', 'Новая'), ('moderated', 'Модерированная'), ('deleted', 'Удаленная')]


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор", default="Неизвестный")
    content = models.TextField(max_length=2000, verbose_name="Контент")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.CharField(max_length=20, verbose_name="Статус", choices=status_choices, default=status_choices[0][0])

    def __str__(self):
        return f"{self.pk} {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

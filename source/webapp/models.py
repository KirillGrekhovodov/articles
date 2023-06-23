from django.db import models


class Section(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", unique=True)
    description = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.title}"

    class Meta:
        db_table = "sections"
        verbose_name = "Секция"
        verbose_name_plural = "Секции"


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор", default="Неизвестный")
    content = models.TextField(max_length=2000, verbose_name="Контент")
    section = models.ForeignKey("webapp.Section",
                                on_delete=models.RESTRICT,
                                verbose_name="Секция",
                                related_name="articles",
                                null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.pk} {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

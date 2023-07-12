from django.db import models


# Create your models here.

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Status(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")

    def __str__(self):
        return f"{self.pk} {self.title}"


class Type(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")

    def __str__(self):
        return f"{self.pk} {self.title}"


class Todo(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор", default="Неизвестный")
    description = models.TextField(max_length=2000, verbose_name="Описание")
    types = models.ManyToManyField('todo.Type', related_name='todo', blank=True, verbose_name="Типы")
    status = models.ForeignKey("todo.Status", on_delete=models.RESTRICT, related_name="todo", verbose_name="Статус")

    def __str__(self):
        types = self.types.values_list("title", flat=True)
        return f"{self.pk} {self.title}: {self.author} {self.status} {', '.join(types)}"

    class Meta:
        db_table = "todo"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

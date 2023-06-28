from datetime import date

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import status_choices, Article


# def publish_date_validate(value):
#     if value < date.today():
#         raise ValidationError("дата публикации не может быть вчерашним днем")


# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=50, required=True, label="Название",
#                             error_messages={"required": "Поле обязательное"})
#     author = forms.CharField(max_length=50, required=True, label="Автор")
#     content = forms.CharField(max_length=2000, required=True, label="Контент",
#                               widget=widgets.Textarea(
#                                   attrs={"cols": 30, "rows": 5, "class": "test"}))
#     status = forms.ChoiceField(choices=status_choices, label="Статус")
#     publish_date = forms.DateField(required=False, label="Дата публикации",
#                                    widget=widgets.DateInput(attrs={"type": "date"}),
#                                    )
#
#     def clean_publish_date(self):
#         value = self.cleaned_data.get("publish_date")
#         if value < date.today():
#             raise ValidationError("дата публикации не может быть вчерашним днем")
#         return value
#
#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get("title") == cleaned_data.get("content"):
#             raise ValidationError("название и контент не могут быть одинаковыми")
#         return cleaned_data


class ArticleForm(forms.ModelForm):
    publish_date = forms.DateField(required=False, label="Дата публикации",
                                   widget=widgets.DateInput(attrs={"type": "date"}),
                                   )

    class Meta:
        model = Article
        fields = ["title", "author", "content", "status", "publish_date"]
        widgets = {"content": widgets.Textarea(attrs={"cols": 30, "rows": 5, "class": "test"})}
        error_messages = {"title": {"required": "Поле обязательное"}}

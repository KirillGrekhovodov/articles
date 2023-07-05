from django import forms
from django.forms import widgets

from webapp.models import Tag


class ArticleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for v in self.visible_fields():
            v.field.widget.attrs["class"] = "form-control"

    title = forms.CharField(max_length=50, required=True, label="Название")
    author = forms.CharField(max_length=50, required=True, label="Автор")
    content = forms.CharField(max_length=2000, required=True, label="Контент",
                              widget=widgets.Textarea(
                                  attrs={"cols": 30, "rows": 5, "class": "test"}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label="Теги")

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Article, Tag, Comment


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=2000, required=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Длина меньше 5 символов не разрешена")
        return value

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    # test = serializers.CharField(max_length=15, write_only=True)


class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleModelSerializer(serializers.ModelSerializer):
    author = AuthorModelSerializer(read_only=True)
    tags = TagModelSerializer(many=True, read_only=True)
    # tags_ids = serializers.ListField(write_only=True, source="tags")

    tags_list = serializers.ListField(write_only=True, source="tags", required=False)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['tags'] = TagModelSerializer(instance.tags.all(), many=True).data
    #     return data

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop("tags", [])
        article = super().create(validated_data)
        if tags:
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)
        return article

    def update(self, instance, validated_data):
        print(validated_data)
        tags = validated_data.pop("tags", [])
        article = super().update(instance, validated_data)
        if tags:
            tags_list = []
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags_list.append(tag)
            article.tags.set(tags_list)
        return article

    def save(self, **kwargs):
        request = self.context['request']
        print(request.user)
        kwargs['author'] = request.user
        super().save(**kwargs)

    def validate(self, attrs):

        result = super().validate(attrs)
        # print(result.errors)
        return result

    class Meta:
        model = Article
        fields = ["id", "tags", "tags_list", "comments", "author", "created_at", "updated_at", "title", "content"]
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments")

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Длина меньше 5 символов не разрешена")
        return value

from rest_framework import serializers
from .logics.markdown import add_paths_to_markdown
from .logics.rating import get_post_rating
from .models import Posts, Categories, Images
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('pk', 'name')


class PostViewSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    def to_representation(self, instance):
        post = super(PostViewSerializer, self).to_representation(instance)
        post['markdown'] = instance.markdown.replace('[API_URL]', settings.API_URL)
        return post

    class Meta:
        model = Posts
        fields = ('pk',
                  'name',
                  'markdown',
                  'categories',
                  'description')


class PostCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    images = serializers.ListField(child=serializers.ImageField(),
                                   write_only=True,
                                   required=False)
    markdown = serializers.CharField()
    categories = serializers.ListField(child=serializers.IntegerField(),
                                       write_only=True)
    description = serializers.CharField()

    def create(self, validated_data):
        user = self.context['user']

        # создание поста
        post = Posts.objects.create(name=validated_data['name'],
                                    created_by=user,
                                    description=validated_data['description'])

        # создание списка с путями до изображений на сервере
        if 'images' in validated_data:
            images_paths = list()
            for image in validated_data['images']:
                image = Images.objects.create(image=image)
                image.save()
                images_paths.append(image.image.url)

            # вставка в markdown разметку путей
            markdown = add_paths_to_markdown(validated_data['markdown'],
                                             validated_data['images'],
                                             images_paths)
        else:
            markdown = validated_data['markdown']

        # вставка разметки в пост и добавление списка категорий
        post.markdown = markdown
        post.categories.add(*validated_data['categories'])
        post.save()
        return post

    def to_representation(self, instance):
        return PostViewSerializer(instance).data


class PostPreviewSerializer(serializers.Serializer):
    def to_representation(self, instance):
        post = {
            'pk': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'image': settings.API_URL + instance.image.url if instance.image else None,
            'rating': get_post_rating(instance.pk)
        }
        return post


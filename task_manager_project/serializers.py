from django.utils import timezone
from rest_framework import serializers
from .models import *
# from .validators import *


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', "deadline"]

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Task
        fields = '__all__'

#HW12
#Task1
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

#Task2
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        сategory_name = validated_data.get('name')
        if Category.objects.filter(name__iexact=сategory_name).exists():
            raise serializers.ValidationError('The category has already exist')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        pk = instance.pk
        сategory_name = validated_data.get('name')

        if Category.objects.filter(name__iexact=сategory_name).exclude(pk=pk).exists():
            raise serializers.ValidationError('The category has already exist')
        return super().update(instance, validated_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask = SubTaskSerializer()

    class Meta:
        model = Task
        fields = '__all__'

#Task 4
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields ='__all__'

    def validate_deadline(self, data):
        if data < timezone.now():
            raise serializers.ValidationError('Deadline must be in the future')
        return data

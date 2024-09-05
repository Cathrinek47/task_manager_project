from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import *
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


#hw16 Реализовать авторизацию с извлечением текущего пользователя из запроса и применение разрешений на уровне объектов.
#Настроить и интегрировать Swagger для автоматической генерации документации API.

class UserTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class UserSubTaskListView(ListAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

#HW15Настроить JWT (JSON Web Token) аутентификацию с использованием SimpleJWT и реализовать пермишены для защиты API.
# Убедитесь, что только авторизованные пользователи могут выполнять определённые действия.

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Используем exp для установки времени истечения куки
            access_expiry = datetime.fromtimestamp(access_token['exp'])
            refresh_expiry = datetime.fromtimestamp(refresh['exp'])
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False, # Используйте True для HTTPS
                samesite='Lax',
                expires=access_expiry
                )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


#HW14 Реализовать полный CRUD для модели категорий (Categories) с помощью ModelViewSet, добавить кастомный метод для
# подсчета количества задач в каждой категории

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        category_with_tasks_count = Category.objects.annotate(task_count=Count('tasks'))

        data = [
            {
                "id": category.id,
                "category": category.name,
                "task_count": category.task_count
            }
            for category in category_with_tasks_count
        ]
        return Response(data)

#hw13.1 Замена представлений для задач (Tasks) на Generic Views

class TaskListCreatetView(ListCreateAPIView):
    queryset = Task.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # http://127.0.0.1:8000/tasks/?status=new&deadline=2026-01-01

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer

class TasksDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]



#hw13.1 Замена представлений для подзадач (SubTasks) на Generic Views

class SubTaskListCreatetView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # http:/ 127.0.0.1:8000/subtasks/?status=In_progress
    filterset_fields = ['status', 'deadline']
    # http://127.0.0.1:8000/subtasks/?search=SubTask1
    search_fields = ['title', 'description']
    # http://127.0.0.1:8000/subtasks/?ordering
    ordering_fields = ['created_at']
    permission_classes = [IsOwnerOrReadOnly]


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsOwnerOrReadOnly]



#hw11 1 Создайте эндпойнт для создания новой задачи. Задача должна быть создана с полями title, description, status, и deadline.


@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_update_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk)

    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskModelSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TaskDetailSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#hw11 2 Эндпойнт для получения списка задач с фильтрами и пагинацией

# http://127.0.0.1:8000/tasks/status/?status=New&deadline=2026-01-01

@api_view(['GET'])
def get_tasks_filtered(request):
    filters = {}
    status = request.query_params.get('status')
    deadline = request.query_params.get('deadline')

    if status:
        filters['status'] = status

    if deadline:
        filters['deadline'] = deadline

    tasks = Task.objects.filter(**filters)
    serializer = TaskDetailSerializer(tasks, many=True)
    return Response(serializer.data)



# hw11 3 Создайте эндпойнт для получения статистики задач, таких как общее количество задач,
# задач по каждому статусу и количество просроченных задач.

class TaskStatisticView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now(), status__in=['pending', 'in_progress']).count()

        return Response({
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks,
        })

#HW12_Task5

# class SubTaskListCreateView(APIView):
#     def get(self, request):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskSerializer(subtasks, many=True)
#         return Response(serializer.data)
#
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'Subtask is not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = SubTaskCreateSerializer(subtask)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'Subtask is not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'Subtask is not found'}, status=status.HTTP_404_NOT_FOUND)
#         subtask.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

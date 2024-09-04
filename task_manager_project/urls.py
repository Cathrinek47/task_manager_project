from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_manager_project.views import *


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', TaskListCreatetView.as_view(), name='tasks_list_create'),
    path('tasks/status/', get_tasks_filtered, name='filter_tasks'),
    path('tasks/statistic/', TaskStatisticView.as_view(), name='task-stats'),
    path('tasks/<int:pk>/', TasksDetailUpdateDeleteView.as_view(), name='task_detail_update_delete'),
    path('subtasks/', SubTaskListCreatetView.as_view(), name='get_subtask'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_detail_update_delete'),

]

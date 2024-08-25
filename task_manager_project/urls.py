from django.urls import path
from task_manager_project.views import *

urlpatterns = [

    path('tasks/', task_list_create, name='get_tasks'),
    path('tasks/status/', get_tasks_filtered, name='filter_tasks'),
    path('tasks/statistic/', TaskStatisticView.as_view(), name='task-stats'),
    path('tasks/<int:pk>/', task_detail_update_delete, name='task_detail_update_delete'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='get_subtask'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_detail_update_delete'),

]

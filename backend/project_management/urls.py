from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import BoardViewSet, CheckListItemViewSet, InviteViewSet, LabelViewSet, TaskAssigneeViewSet, \
	TaskLabelViewSet, TaskListViewSet, TaskViewSet, WorkspaceMemberViewSet, WorkspaceViewSet, accept_board_invite, \
	accept_workspace_invite

"""
URL configuration for the project_management app.
This module defines the URL patterns for the project_management app, including
nested routes for various resources such as workspaces, members, boards, task lists,
tasks, assignees, checklist items, labels, and invites.
Routes:
- Base routes:
    - /workspaces/
    - /labels/
- Nested routes:
    - /workspaces/{workspace_pk_slug}/members/
    - /workspaces/{workspace_pk_slug}/boards/
    - /workspaces/{workspace_pk_slug}/invites/
    - /workspaces/{workspace_pk_slug}/boards/{board_pk}/task-lists/
    - /workspaces/{workspace_pk_slug}/boards/{board_pk}/task-lists/{tasklist_pk}/tasks/
    - /workspaces/{workspace_pk_slug}/boards/{board_pk}/task-lists/{tasklist_pk}/tasks/{task_pk}/assignees/
    - /workspaces/{workspace_pk_slug}/boards/{board_pk}/task-lists/{tasklist_pk}/tasks/{task_pk}/checklist-items/
    - /workspaces/{workspace_pk_slug}/boards/{board_pk}/task-lists/{tasklist_pk}/tasks/{task_pk}/labels/
"""

app_name = "project_management"

# Base router for top-level resources
router = routers.DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'labels', LabelViewSet, basename='label')

# Nested router for Workspace -> Members
workspace_member_router = NestedSimpleRouter(router, r'workspaces', lookup='workspace')
workspace_member_router.register(r'members', WorkspaceMemberViewSet, basename='workspace-member')

# Nested router for Workspace -> Boards
workspace_board_router = NestedSimpleRouter(router, r'workspaces', lookup='workspace')
workspace_board_router.register(r'boards', BoardViewSet, basename='workspace-board')

# Nested router for Board -> TaskLists
board_tasklist_router = NestedSimpleRouter(workspace_board_router, r'boards', lookup='board')
board_tasklist_router.register(r'task-lists', TaskListViewSet, basename='board-tasklist')

# Nested router for TaskList -> Tasks
tasklist_task_router = NestedSimpleRouter(board_tasklist_router, r'task-lists', lookup='tasklist')
tasklist_task_router.register(r'tasks', TaskViewSet, basename='tasklist-task')

# Nested router for Task -> Assignees
task_assignee_router = NestedSimpleRouter(tasklist_task_router, r'tasks', lookup='task')
task_assignee_router.register(r'assignees', TaskAssigneeViewSet, basename='task-assignee')

# Nested router for Task -> Checklist Items
task_checklist_router = NestedSimpleRouter(tasklist_task_router, r'tasks', lookup='task')
task_checklist_router.register(r'checklist-items', CheckListItemViewSet, basename='task-checklist')

# Nested router for Task -> Labels
task_label_router = NestedSimpleRouter(tasklist_task_router, r'tasks', lookup='task')
task_label_router.register(r'labels', TaskLabelViewSet, basename='task-label')

# Nested router for Workspace -> Invites
workspace_invite_router = NestedSimpleRouter(router, r'workspaces', lookup='workspace')
workspace_invite_router.register(r'invites', InviteViewSet, basename='workspace-invite')

urlpatterns = [
		path('boards/accept/', accept_board_invite, name='board-accept'),
		path('workspaces/accept/', accept_workspace_invite, name='workspace-accept'),

		# Base routes
		path('', include(router.urls)),

		# Nested routes
		path('', include(workspace_member_router.urls)),
		path('', include(workspace_board_router.urls)),
		path('', include(board_tasklist_router.urls)),
		path('', include(tasklist_task_router.urls)),
		path('', include(task_assignee_router.urls)),
		path('', include(task_checklist_router.urls)),
		path('', include(task_label_router.urls)),
		path('', include(workspace_invite_router.urls)),
]

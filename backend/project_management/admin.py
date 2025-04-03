from django.contrib import admin

from project_management.models import Board, BoardInvite, BoardMember, CheckListItem, Label, Task, TaskAssignee, \
	TaskLabel, TaskList, Workspace, WorkspaceInvite, WorkspaceMember


# Register your models here.

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "owner", "created_at", "slug"]
	readonly_fields = ["slug"]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "workspace", "position", "slug"]
	readonly_fields = ["slug"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "task_list", "is_completed"]


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
	pass


@admin.register(WorkspaceInvite)
class WorkspaceInviteAdmin(admin.ModelAdmin):
	pass


@admin.register(BoardInvite)
class BoardInviteAdmin(admin.ModelAdmin):
	pass

@admin.register(TaskAssignee)
class TaskAssigneeAdmin(admin.ModelAdmin):
	pass


@admin.register(CheckListItem)
class CheckListItemAdmin(admin.ModelAdmin):
	pass


@admin.register(TaskLabel)
class TaskLabelAdmin(admin.ModelAdmin):
	pass


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
	pass


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
	pass

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
	pass

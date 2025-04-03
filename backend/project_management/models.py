import uuid

from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
from project_management.managers import CustomBoardManager, CustomWorkspaceManager

app_label = "project_management"


class Workspace(BaseModel):
	"""
	Workspace model to represent a workspace in the project management system.
	Attributes:
		name (CharField): The name of the workspace.
		owner (ForeignKey): The user who created the workspace.
		slug(CharField): The slug of the workspace
	"""

	name = models.CharField(max_length=255)
	slug = models.CharField(max_length=255, blank=True)
	owner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="workspaces")

	objects = CustomWorkspaceManager()

	def __str__(self):
		"""
		Returns a string representation of the workspace.
		Overrides the default __str__ method.
		Returns:
			str: The name of the workspace.
		"""
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.name))
		return super().save(*args, **kwargs)


class WorkspaceMember(BaseModel):
	"""
	WorkspaceMember model to represent a member in a workspace.
	Attributes:
		workspace (ForeignKey): The workspace to which the member belongs.
		member (ForeignKey): The user who is a member of the workspace.
	"""

	workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="members")
	member = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="workspace_members")

	def __str__(self):
		"""
		Returns a string representation of the workspace member.
		Overrides the default __str__ method.
		Returns:
			str: The name of the workspace member.
		"""
		return self.member


class Board(BaseModel):
	"""
	Board model to represent a board in a workspace.
	Attributes:
		name (CharField): The name of the board.
		slug(CharField): The slug of the board
		description (TextField): A description of the board.
		workspace (ForeignKey): The workspace to which the board belongs.
	"""

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="boards")
	position = models.PositiveIntegerField()
	slug = models.CharField(max_length=255, default="", blank=True)

	objects = CustomBoardManager()

	def __str__(self):
		"""
		Returns a string representation of the board.
		Overrides the default __str__ method.
		Returns:
			str: The name of the board.
		"""
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.name))
		return super().save(*args, **kwargs)

	class Meta:
		unique_together = [["workspace", "name"], ["workspace", "position"]]


# pre_save.connect(add_position_to_board, sender=Board, dispatch_uid="add_position_to_board")

class BoardMember(BaseModel):
	"""
	BoardMember model to represent a member in a board.
	Attributes:
		board (ForeignKey): The board to which the member belongs.
		member (ForeignKey): The user who is a member of the board.
	"""

	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="members")
	member = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="board_members")

	def __str__(self):
		"""
		Returns a string representation of the workspace member.
		Overrides the default __str__ method.
		Returns:
			str: The name of the workspace member.
		"""
		return self.member


class TaskList(BaseModel):
	"""
	TaskList model to represent a list of tasks in a board.
	Attributes:
		name (CharField): The name of the list.
		board (ForeignKey): The board to which the list belongs.
		position (PositiveIntegerField): The position of the list in the board.
		description (TextField): A description of the list.
	"""
	name = models.CharField(max_length=255)
	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="task_lists")
	position = models.PositiveIntegerField()
	description = models.TextField(blank=True)

	def __str__(self):
		"""
		Returns a string representation of the list.
		Overrides the default __str__ method.
		Returns:
			str: The name of the list.
		"""
		return self.name


class Task(BaseModel):
	"""
	Task model to represent a task or item in a list.
	Attributes:
		name (CharField): The name of the task.
		description (TextField): A description of the task.
		task_list (ForeignKey): The list to which the task belongs.
		position (PositiveIntegerField): The position of the task in the list.
		due_date (DateField): The due date for the task.
		is_completed (BooleanField): Indicates whether the task is completed.
	"""

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")
	position = models.PositiveIntegerField()
	due_date = models.DateField(null=True, blank=True)
	is_completed = models.BooleanField(default=False)

	def __str__(self):
		"""
		Returns a string representation of the task.
		Overrides the default __str__ method.
		Returns:
			str: The name of the task.
		"""
		return self.name


class TaskAssignee(BaseModel):
	"""
	TaskAssignee model to represent the assignment of a user to a task.
	Attributes:
		task (ForeignKey): The task to which the assignee is assigned.
		assignee (ForeignKey): The user who is assigned to the task.
	"""

	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignees")
	assignee = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="assigned_tasks")

	def __str__(self):
		"""
		Returns a string representation of the task assignee.
		Overrides the default __str__ method.
		Returns:
			str: The name of the task assignee.
		"""
		return f"{self.assignee} assigned to {self.task}"


class CheckListItem(BaseModel):
	"""
	CheckListItem model to represent a checklist item in a task.
	Attributes:
		name (CharField): The name of the checklist item.
		is_completed (BooleanField): Indicates whether the checklist item is completed.
		task (ForeignKey): The task to which the checklist item belongs.
		due_at (DateTimeField): The due date and time for the checklist item.
		assignee (ForeignKey): The user who is assigned to complete the checklist item.
	"""

	name = models.CharField(max_length=255)
	is_completed = models.BooleanField(default=False)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="checklist_items")
	due_at = models.DateTimeField(null=True, blank=True)
	assignee = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="checklist_items")

	def __str__(self):
		"""
		Returns a string representation of the checklist item.
		Overrides the default __str__ method.
		Returns:
			str: The name of the checklist item.
		"""
		return self.name


class Label(BaseModel):
	"""
	Label model to represent a label for categorizing tasks.
	Attributes:
		name (CharField): The name of the label.
		color (CharField): The color code for the label.
	"""

	name = models.CharField(max_length=255)
	color = models.CharField(max_length=7)

	def __str__(self):
		"""
		Returns a string representation of the label.
		Overrides the default __str__ method.
		Returns:
			str: The name of the label.
		"""
		return self.name


class TaskLabel(BaseModel):
	"""
	TaskLabel model to represent the assignment of a label to a task.
	Attributes:
		task (ForeignKey): The task to which the label is assigned.
		label (ForeignKey): The label assigned to the task.
	"""

	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="labels")
	label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="tasks")

	def __str__(self):
		"""
		Returns a string representation of the task label.
		Overrides the default __str__ method.
		Returns:
			str: The name of the task label.
		"""
		return f"{self.label} assigned to {self.task}"


class WorkspaceInvite(BaseModel):
	"""
	Invite model to represent an invitation to join a workspace.
	Attributes:
		workspace (ForeignKey): The workspace for which the invite is sent.
		sender (ForeignKey): The user who sent the invite.
		recipient_email (EmailField): The email address of the recipient.
		token (UUIDField): The token used for accepting the invite.
		is_accepted (BooleanField): Indicates whether the invite has been accepted.
	"""

	workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="workspace_invites")
	sender = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="sent_workspace_invites")
	recipient_email = models.EmailField()

	# Internal fields
	token = models.UUIDField(default=uuid.uuid4, editable=False)
	is_accepted = models.BooleanField(default=False)

	def __str__(self):
		"""
		Returns a string representation of the invite.
		Overrides the default __str__ method.
		Returns:
			str: The email address of the recipient.
		"""
		return self.recipient_email


class BoardInvite(BaseModel):
	"""
	BoardInvite model to represent an invitation to join a board.
	Attributes:
		board (ForeignKey): The board  for which the invite is sent.
		sender (ForeignKey): The user who sent the invite.
		recipient_email (EmailField): The email address of the recipient.
		token (UUIDField): The token used for accepting the invite.
	"""

	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="board_invites")
	sender = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="sent_board_invites")
	recipient_email = models.EmailField()

	# Internal fields
	token = models.UUIDField(default=uuid.uuid4, editable=False)

	def __str__(self):
		"""
		Returns a string representation of the invite.
		Overrides the default __str__ method.
		Returns:
			str: The email address of the recipient.
		"""
		return self.recipient_email

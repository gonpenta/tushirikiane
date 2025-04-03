from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import response, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project_management.emails import BoardInviteEmail, WorkspaceInviteEmail
from .models import Board, BoardInvite, BoardMember, Task, TaskList, Workspace, WorkspaceInvite, WorkspaceMember
from .permissions import IsMemberReadOrOwnerFull
from .serializers import BoardSerializer, EmailInviteSerializer, InviteSerializer, InviteTokenSerializer, \
	TaskListSerializer, TaskSerializer, \
	WorkspaceMemberSerializer, \
	WorkspaceSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
	serializer_class = WorkspaceSerializer
	# permission_classes = [IsMemberReadOrOwnerFull, IsAuthenticated]
	lookup_field = "pk_slug"

	def get_queryset(self):
		# Just a precaution
		if self.request.user.is_anonymous:
			return Workspace.objects.none()

		return Workspace.objects.filter(
			models.Q(owner=self.request.user) | models.Q(members__member=self.request.user)
		).distinct()

	def get_object(self):
		pk = self.kwargs.get("pk_slug")
		return Workspace.objects.get_by_id_or_slug_or_404(pk, queryset=self.get_queryset())

	def perform_create(self, serializer):
		# Automatically set the owner to the current user when creating a workspace
		serializer.save(owner=self.request.user)

	def destroy(self, request, *args, **kwargs):
		workspace = self.get_object()

		if workspace.owner != request.user:
			return response.Response("You can't delete this workspace", status=403)

		serializer = self.get_serializer(instance=workspace)
		workspace.delete()

		return response.Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

	@action(detail=True, methods=["post"])
	def invite(self, request, *args, **kwargs):
		workspace = self.get_object()

		# Check that user is a workspace owner
		if workspace.owner != request.user:
			return response.Response("You can't invite members to this board", status=403)

		serializer = EmailInviteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		emails = serializer.validated_data["emails"]

		for email in emails:
			email = BaseUserManager.normalize_email(email)
			invite_data = {
					"workspace": workspace,
					"recipient_email": email,
					"sender": request.user,
			}
			# Check if the user is already a member of the workspace or invite already exists
			if WorkspaceMember.objects.filter(workspace=workspace,
											  member__email=email).exists() or WorkspaceInvite.objects.filter(
				workspace=workspace, recipient_email=email).exists():
				continue

			invite_obj = WorkspaceInvite.objects.create(**invite_data)
			WorkspaceInviteEmail(request=request, context={"token": invite_obj.token}).send(to=[email])

		return Response({"message": "Invites sent successfully."}, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=["get"])
	def members(self, request, *args, **kwargs):
		workspace = self.get_object()

		members = WorkspaceMember.objects.filter(workspace=workspace)
		serializer = WorkspaceMemberSerializer(members, many=True)
		return Response(serializer.data)


@api_view(http_method_names=["POST"])
def accept_workspace_invite(request, *args, **kwargs):
	serializer = InviteTokenSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	token = serializer.validated_data["token"]
	try:
		invite = WorkspaceInvite.objects.get(token=token)
		workspace = invite.workspace

	except ObjectDoesNotExist:
		return response.Response("Invalid token", status=400)

	if invite.recipient_email != request.user.email:
		return response.Response("Invalid token", status=400)

	membership = WorkspaceMember.objects.create(workspace=workspace, member=request.user)
	invite.delete()

	return Response({"message": "You have been added to the workspace."}, status=status.HTTP_201_CREATED)


class BoardViewSet(viewsets.ModelViewSet):
	serializer_class = BoardSerializer
	permission_classes = [IsAuthenticated]
	lookup_field = "pk_slug"

	def get_queryset(self):
		if self.request.user.is_anonymous:
			return Board.objects.none()

		# If no workspace id is not provided in the url, don't return any boards
		workspace_pk = self.kwargs.get("workspace_pk_slug")
		if not workspace_pk:
			return Board.objects.none()

		# If a workspace Id/slug name was provided, return the boards in that workspace
		workspace = Workspace.objects.get_by_id_or_slug_or_404(workspace_pk)
		if workspace:
			return Board.objects.filter(workspace=workspace)

		return Board.objects.filter(
			models.Q(workspace__members__member=self.request.user) |
			models.Q(workspace__owner=self.request.user)
		).distinct().order_by("position")

	def get_object(self):
		# Get the board by id or slug
		pk = self.kwargs.get("pk_slug")
		return Board.objects.get_by_id_or_slug_or_404(pk, queryset=self.get_queryset())

	def create(self, request, *args, **kwargs):
		workspace_pk = self.kwargs.get("workspace_pk_slug")

		try:
			workspace = Workspace.objects.get_by_id_or_slug_or_404(pk=workspace_pk)
		except NotFound:
			return response.Response("Workspace does not exist", status=400)

		# TODO: Check if the user is a member of the workspace
		if not workspace.members.filter(member=request.user).exists() and workspace.owner != request.user:
			return response.Response("You are not a member of this workspace", status=403)

		last_position = Board.objects.filter(workspace=workspace).aggregate(models.Max("position"))["position__max"]
		position = (last_position + 1) if last_position is not None else 0

		board_data = request.data.copy()
		board_data["position"] = position
		board_data["workspace"] = workspace.id

		serializer = self.get_serializer(data=board_data)
		serializer.is_valid(raise_exception=True)
		board = serializer.save()

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def update(self, request, *args, **kwargs):
		# TODO: Check this
		partial = kwargs.pop("partial", False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		return Response(serializer.data)

	def destroy(self, request, *args, **kwargs):
		board = self.get_object()

		if board.workspace.owner != request.user:
			return response.Response("You can't delete this board", status=403)

		serializer = self.get_serializer(instance=board)
		board.delete()

		return response.Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

	@action(detail=True, methods=["post"])
	def invite(self, request, *args, **kwargs):
		board = self.get_object()

		# Check that user is a workspace owner
		if board.workspace.owner != request.user:
			return response.Response("You can't invite members to this board", status=403)

		serializer = EmailInviteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		emails = serializer.validated_data["emails"]

		for email in emails:
			email = BaseUserManager.normalize_email(email)
			invite_data = {
					"board": board,
					"recipient_email": email,
					"sender": request.user,
			}
			# Check if the user is already a member of the board or invite already exists
			if BoardMember.objects.filter(board=board, member__email=email).exists() or BoardInvite.objects.filter(
					board=board, recipient_email=email).exists():
				continue

			invite_obj = BoardInvite.objects.create(**invite_data)
			BoardInviteEmail(request=request, context={"token": invite_obj.token}).send(to=[email])

		return Response({"message": "Invites sent successfully."}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def accept_board_invite(request, *args, **kwargs):
	serializer = InviteTokenSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)

	token = serializer.validated_data["token"]
	try:
		invite = BoardInvite.objects.get(token=token)
		board = invite.board

	except ObjectDoesNotExist:
		return response.Response("Invalid token", status=400)

	if invite.recipient_email != request.user.email:
		return response.Response("Invalid token", status=400)

	membership = BoardMember.objects.create(board=board, member=request.user)
	invite.delete()

	return Response({"message": "You have been added to the board."}, status=status.HTTP_201_CREATED)


class TaskViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()


class TaskListViewSet(viewsets.ModelViewSet):
	serializer_class = TaskListSerializer
	queryset = TaskList.objects.all()


# TaskAssigneeViewSet,
class TaskAssigneeViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()


# CheckListItemViewSet,
class CheckListItemViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()


# LabelViewSet,
class LabelViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()


# TaskLabelViewSet,
class TaskLabelViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()


# InviteViewSet,
class InviteViewSet(viewsets.ModelViewSet):
	serializer_class = InviteSerializer
	queryset = WorkspaceInvite.objects.all()


# WorkspaceMemberViewSet
class WorkspaceMemberViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = WorkspaceMemberSerializer
	permission_classes = [IsMemberReadOrOwnerFull]

	def get_queryset(self):
		workspace_id = self.kwargs.get("workspace_pk")
		try:
			workspace = Workspace.objects.get_by_id_or_slug_or_404(pk=workspace_id)
		except NotFound:
			return response.Response("Workspace does not exist", status=400)

		return WorkspaceMember.objects.filter(workspace=workspace)

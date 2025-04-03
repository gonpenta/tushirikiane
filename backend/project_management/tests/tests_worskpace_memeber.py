from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from project_management.models import Workspace, WorkspaceMember


class WorkspaceMemberViewSetTestCase(APITestCase):
	def setUp(self):
		"""
		Set up test environment with users and workspace members
		"""
		self.user1 = CustomUser.objects.create_user(
			email="user1@test.com",
			password="testpass123"
		)
		self.user2 = CustomUser.objects.create_user(
			email="user2@test.com",
			password="testpass123"
		)
		self.workspace1 = Workspace.objects.create(
			name="Test Workspace",
			owner=self.user1
		)

		# Create workspace membership
		self.workspace_member = WorkspaceMember.objects.create(
			workspace=self.workspace1,
			member=self.user2
		)

	def test_list_workspace_memberships(self):
		"""
		Test that a user can only see their own workspace memberships
		"""
		self.client.force_authenticate(user=self.user2)

		response = self.client.get(f'/api/workspaces/{self.workspace1.id}/members/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['workspace'], self.workspace1.id)

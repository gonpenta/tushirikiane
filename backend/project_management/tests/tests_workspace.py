from uuid import uuid4

from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from project_management.models import Workspace, WorkspaceInvite, WorkspaceMember


class WorkspaceTestCase(APITestCase):

	def setUp(self):
		"""
		Set up test environment with users and workspaces
		"""
		# Create test users
		self.user1 = CustomUser.objects.create_user(
			email="user1@test.com",
			password="testpass123"
		)
		self.user2 = CustomUser.objects.create_user(
			email="user2@test.com",
			password="testpass123"
		)

		# Create workspaces
		self.workspace1 = Workspace.objects.create(
			name="User1's Workspace",
			owner=self.user1
		)
		self.workspace2 = Workspace.objects.create(
			name="User2's Workspace",
			owner=self.user2
		)

	def test_user_has_default_workspace(self):
		"""
		Test that a default workspace is created for a new user

		Validates:
		- User can retrieve workspaces
		- Exactly one default workspace is created
		- Default workspace has expected properties
		"""
		# Create a test user
		user = CustomUser.objects.create_user(
			email="test@mail.com",
			password="12345"
		)

		# Authenticate the user
		self.client.force_authenticate(user=user)

		# Retrieve workspaces
		url = "/api/workspaces/"
		response = self.client.get(url)

		# Assert the response status code
		self.assertEqual(
			response.status_code,
			status.HTTP_200_OK,
			"Failed to retrieve workspaces with 200 OK status"
		)

		# Assert that the response contains exactly one workspace
		self.assertEqual(
			len(response.data),
			1,
			"Expected exactly one default workspace for a new user"
		)

		# Validate default workspace properties
		default_workspace = response.data[0]
		self.assertIn('id', default_workspace, "Workspace should have an ID")
		self.assertIn('name', default_workspace, "Workspace should have a name")

	def test_create_workspace(self):
		"""
		Test creating a workspace sets the current user as owner
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post('/api/workspaces/', {
				'name': 'New Test Workspace',
		})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		# Verify fields are set correctly
		self.assertEqual(response.data['owner'], self.user1.id)
		self.assertEqual(response.data['name'], 'New Test Workspace')
		# Verify, a slug is automatically set from the name
		self.assertEqual(response.data["slug"], slugify(response.data["name"]))

	def test_fetching_workspace_with_id_or_slug(self):
		"""
		Test fetching a workspace works with both slug and workspace_id
		"""
		self.client.force_authenticate(user=self.user1)
		response1 = self.client.get(f"/api/workspaces/{self.workspace1.id}/")
		response2 = self.client.get(f"/api/workspaces/{self.workspace1.slug}/")

		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response2.status_code, status.HTTP_200_OK)

		self.assertEqual(response1.data["id"], response2.data["id"])

	def test_fetching_invalid_workspace(self):
		"""
		Test fetching an invalid workspace throws and error.
		"""
		self.client.force_authenticate(user=self.user1)
		response1 = self.client.get(f"/api/workspaces/{uuid4()}/")
		self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response1.data["detail"], "Workspace Not Found!")

		response2 = self.client.get("/api/workspaces/random-slug/")
		self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response2.data["detail"], "Workspace Not Found!")

	def test_list_workspaces(self):
		"""
		Test that a user can only see their own workspaces and workspaces they are members of
		"""
		# Add user1 as a member to user2's workspace
		WorkspaceMember.objects.create(
			workspace=self.workspace2,
			member=self.user1
		)

		self.client.force_authenticate(user=self.user1)

		response = self.client.get('/api/workspaces/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Should see 3workspaces - the user has access to
		self.assertEqual(len(response.data), 3)

	def test_fetching_members_of_workspace(self):
		"""
		Test that a user can fetch members of a workspace they belong to
		"""
		self.client.force_authenticate(user=self.user2)

		# Add user2 as a member to user1's workspace
		WorkspaceMember.objects.create(
			workspace=self.workspace1,
			member=self.user2
		)
		response = self.client.get(f'/api/workspaces/{self.workspace1.id}/members/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Should see 1 member - user 2
		self.assertEqual(len(response.data), 1)

	# test only owner can delete a workspace
	def test_delete_workspace(self):
		"""
		Test that a user can delete a workspace they own
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.delete(f'/api/workspaces/{self.workspace1.id}/')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		# Check that the response contains the deleted workspace data
		self.assertEqual(response.data["slug"], str(self.workspace1.slug))

		# Check that the workspace no longer exists
		response = self.client.get(f'/api/workspaces/{self.workspace1.id}/')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	# Test that a user cannot delete a workspace they don't own
	def test_cannot_delete_others_workspace(self):
		"""
		Test that a user cannot delete a workspace they don't own
		"""
		self.client.force_authenticate(user=self.user2)
		# Add user2 as a member to user1's workspace
		WorkspaceMember.objects.create(
			workspace=self.workspace1,
			member=self.user2
		)

		response = self.client.delete(f'/api/workspaces/{self.workspace1.id}/')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		# Check that the workspace does still exists

		response = self.client.get(f'/api/workspaces/{self.workspace1.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], str(self.workspace1.id))

	def test_cannot_access_others_workspace(self):
		"""
		Test that a user cannot access a workspace they don't own or belong to
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.get(f'/api/workspaces/{self.workspace2.id}/')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_can_invite_people_to_workspace(self):
		"""
		Test inviting people to a workspace
		"""

		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/invite/', {
				"emails": ["hello@mail.com", "another@mail.com"],
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_can_invite_people_to_workspace_only_if_owner(self):
		"""
		Test that a user can only invite people to a workspace if they are the owner
		"""
		user2 = CustomUser.objects.create_user(
			email="email@mail.com",
			password="testpass123")

		WorkspaceMember.objects.create(workspace=self.workspace1, member=user2)

		self.client.force_authenticate(user=user2)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/invite/', {
				"emails": ["someemail@mail.com"],
		})

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_can_accept_workspace_invite(self):
		"""
		Test accepting a workspace invite
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/invite/', {
				"emails": ["user2@test.com"]
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		self.client.logout()

		# Simulate accepting the invite
		# Get token from the database
		token = WorkspaceInvite.objects.get(recipient_email="user2@test.com").token

		self.client.force_authenticate(user=self.user2)
		response = self.client.post(f'/api/workspaces/accept/', data={
				"token": token
		}, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

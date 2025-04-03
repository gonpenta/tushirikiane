from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from project_management.models import Board, BoardInvite, Workspace, WorkspaceMember


class BoardViewSetTestCase(APITestCase):
	def setUp(self):
		"""
		Set up test environment with users, workspaces, and boards
		"""
		Board.objects.all().delete()  # Clear boards before each test

		self.user1 = CustomUser.objects.create_user(
			email="user1@test.com",
			password="testpass123"
		)
		self.workspace1 = Workspace.objects.create(
			name="Test Workspace",
			owner=self.user1
		)

		self.board1 = Board.objects.create(workspace=self.workspace1, name="Test Board", position=1)

	def test_create_board(self):
		"""
		Test creating a board in a workspace using the id and slug
		"""
		self.client.force_authenticate(user=self.user1)

		response1 = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/', format="json", data={
				'name': 'New Test Board',
		})

		self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response1.data['name'], 'New Test Board')
		self.assertEqual(response1.data['workspace'], self.workspace1.id)

		response2 = self.client.post(f'/api/workspaces/{self.workspace1.slug}/boards/', format="json", data={
				'name': 'New Test Board 2',
		})
		self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response2.data['name'], 'New Test Board 2')
		self.assertEqual(response2.data['workspace'], self.workspace1.id)

	def test_update_board(self):
		board = Board.objects.create(workspace=self.workspace1, name="board1", position=0)

		self.client.force_authenticate(user=self.user1)

		response = self.client.put(f"/api/workspaces/{self.workspace1.id}/boards/{board.id}/",
								   data={"name": "new name"},
								   format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], str(board.id))
		self.assertEqual(response.data["name"], "new name")

	def test_retrieve_board(self):
		"""
		Test retrieving a board
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.get(f"/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/")
		response1 = self.client.get(f"/api/workspaces/{self.workspace1.slug}/boards/{self.board1.slug}/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], str(self.board1.id))
		self.assertEqual(response.data["name"], self.board1.name)
		self.assertEqual(response.data["id"], response1.data["id"])

	def test_delete_board(self):
		"""
		Test deleting a board
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.delete(f"/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/")

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		self.assertEqual(response.data["slug"], self.board1.slug)

		# Check if the board is deleted
		response = self.client.get(f"/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	# Test that a user cannot delete a board they don't own
	def test_cannot_delete_others_board(self):
		"""
		Test that a user cannot delete a board they don't own
		"""
		user2 = CustomUser.objects.create_user(
			email="user2@mai.com",
			password="<PASSWORD>"
		)

		WorkspaceMember.objects.create(member=user2, workspace=self.workspace1)
		self.client.force_authenticate(user=user2)

		response = self.client.delete(f"/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/")

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		# Check if the board is not deleted
		response = self.client.get(f"/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_board_positioning(self):
		"""
		Test that boards are automatically positioned
		"""
		self.client.force_authenticate(user=self.user1)

		# Create first board
		board1 = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/', {
				'name': 'First Board',
				'description': 'Board Description'
		})
		self.assertEqual(board1.status_code, status.HTTP_201_CREATED)

		# Create second board
		board2 = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/', {
				'name': 'Second Board',
		})
		self.assertEqual(board2.status_code, status.HTTP_201_CREATED)

		self.assertEqual(board1.data['position'], 2)
		self.assertEqual(board2.data['position'], 3)

	def test_board_fetching_by_workspace_slug_or_id(self):
		"""
		Test fetching boards in a workspace
		"""
		self.client.force_authenticate(user=self.user1)
		response1 = self.client.get(f'/api/workspaces/{self.workspace1.id}/boards/')
		response2 = self.client.get(f'/api/workspaces/{self.workspace1.slug}/boards/')

		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response2.status_code, status.HTTP_200_OK)

		self.assertEqual(response1.data, response2.data)

	def test_cannot_create_board_in_non_existent_workspace(self):
		"""
		Test creating a board in a non-existent workspace
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post('/api/workspaces/9999/boards/', {
				'name': 'Impossible Board'
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	# TODO: Add test for creating 2 boards with the same name in the same workspace
	# TODO: Add test for creating 2 boards with the same name in DIFFERENT workspaces

	def test_cannot_create_board_without_name(self):
		"""
		Test creating a board without a name
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/', {
				'description': 'Board Description'
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_create_board_without_workspace(self):
		"""
		Test creating a board without a workspace
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post('/api/workspaces/9999/boards/', {
				'name': 'Impossible Board'
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_create_board_without_authentication(self):
		"""
		Test creating a board without authentication
		"""
		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/', {
				'name': 'New Test Board',
		})

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_cannot_create_board_without_permission(self):
		# TODO: Implement this test
		pass

	# 	Board Invites and acceptance

	def test_can_invite_people_to_board(self):
		"""
		Test inviting people to a board
		"""

		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/invite/', {
				"emails": ["hello@mail.com"]
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_can_only_invite_people_to_board_only_if_owner(self):
		"""
		Test that a user can only invite people to a board if they are the owner or a member of the workspace
		"""
		user2 = CustomUser.objects.create_user(
			email="email@mail.com",
			password="testpass123")

		self.client.force_authenticate(user=user2)

		response1 = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/invite/', {
				"emails": ["someemail@mail.com"],
		})

		self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

	def test_can_accept_board_invite(self):
		"""
		Test accepting a board invite
		"""
		user2 = CustomUser.objects.create_user(
			email="user2@test.com",
			password="testpass123"
		)

		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/workspaces/{self.workspace1.id}/boards/{self.board1.id}/invite/', {
				"emails": ["user2@test.com"]
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		# Simulate accepting the invite
		# Get token from the database
		token = BoardInvite.objects.get(recipient_email="user2@test.com").token
		self.client.logout()

		self.client.force_authenticate(user=user2)
		response = self.client.post(f'/api/boards/accept/', data={
				"token": token
		}, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_accept_board_invite_fails_when_given_invalid_token(self):
		"""
		Test that accepting a board invite fails when given an invalid token
		"""
		self.client.force_authenticate(user=self.user1)

		response = self.client.post(f'/api/boards/accept/', data={
				"token": "invalid_token"
		}, format="json")

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

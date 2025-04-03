# from accounts.models import CustomUser
# from project_management.models import Board, Workspace
# from rest_framework import status
# from rest_framework.test import APITestCase
#
#
# class TaskViewSetTestCase(APITestCase):
# 	def setUp(self):
# 		"""
# 		Set up test environment with users, workspaces, boards, and tasks
# 		"""
# 		self.user1 = CustomUser.objects.create_user(
# 			email="user1@test.com",
# 			password="testpass123"
# 		)
# 		self.workspace1 = Workspace.objects.create(
# 			name="Test Workspace",
# 			owner=self.user1
# 		)
# 		self.board1 = Board.objects.create(
# 			name="Test Board",
# 			workspace=self.workspace1,
# 			position=0
# 		)
#
# 	def test_create_task(self):
# 		"""
# 		Test creating a task
# 		"""
# 		self.client.force_authenticate(user=self.user1)
#
# 		response = self.client.post(f'/api/boards/{self.board1.id}/tasks/', {
# 				'name': 'Test Task',
# 				'board': self.board1.id
# 		})
#
# 		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# 		self.assertEqual(response.data['name'], 'Test Task')
# 		self.assertEqual(response.data['board'], self.board1.id)

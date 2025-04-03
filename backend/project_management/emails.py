from django.conf import settings
from djoser.email import BaseEmailMessage


class BoardInviteEmail(BaseEmailMessage):
	template_name = "emails_templates/board_invite.html"

	def get_context_data(self):
		context = super().get_context_data()

		user = context.get("user")
		context["token"] = context.get("token")
		context["url"] = settings.PROJECT_MANAGEMENT.get("URLS").get("accept_board_invite").format(**context)
		return context


class WorkspaceInviteEmail(BaseEmailMessage):
	template_name = "emails_templates/workspace_invite.html"

	def get_context_data(self):
		context = super().get_context_data()

		user = context.get("user")
		context["token"] = context.get("token")
		context["url"] = settings.PROJECT_MANAGEMENT.get("URLS").get("accept_workspace_invite").format(**context)
		return context

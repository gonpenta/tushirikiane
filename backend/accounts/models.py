import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .signals import create_default_workspace


class CustomUser(AbstractBaseUser, PermissionsMixin):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(_("First Name"), max_length=50)
	middle_name = models.CharField(_("Middle Name"), max_length=50, blank=True, null=True)
	last_name = models.CharField(_("Last Name"), max_length=50)
	email = models.EmailField(_("email address"), unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["first_name", "last_name"]

	objects = CustomUserManager()

	class Meta:
		verbose_name = _("user")
		verbose_name_plural = _("users")

	def __str__(self) -> str:
		return self.email


post_save.connect(create_default_workspace, sender=CustomUser, dispatch_uid="create_default_workspace")

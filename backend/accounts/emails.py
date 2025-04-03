from djoser import email


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "emails/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "emails/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(email.UsernameChangedConfirmationEmail):
    template_name = "emails/username_changed_confirmation.html"


class UsernameResetEmail(email.UsernameResetEmail):
    template_name = "emails/username_reset.html"

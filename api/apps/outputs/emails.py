from mail_factory import factory
from mail_factory.mails import BaseMail


"""
Generate the email body

Templates: /outputs/templates/mails/{{template_name}}/{{lang}}
"""


class ConfirmAccountEmail(BaseMail):
    template_name = "confirm_account_email"
    params = ["user", "domain", "token"]


factory.register(ConfirmAccountEmail)


class ResetPasswordEmail(BaseMail):
    template_name = "reset_password_email"
    params = ["user", "token"]

class SubscriptionEmail(BaseMail):
    template_name = "reset_password_email"
    params = ["user", "token"]



factory.register(ResetPasswordEmail)


class ConfirmResetPasswordEmail(BaseMail):
    template_name = "confirm_reset_password_email"
    params = ["user", "support_mail"]


factory.register(ConfirmResetPasswordEmail)


class InvitationEmail(BaseMail):
    template_name = "invitation_email"
    params = ["user", "token"]


factory.register(InvitationEmail)


class RetrieveWorkspaceEmail(BaseMail):
    template_name = "retrieve_workspace_email"
    params = ["user", "header_url", "domain_url", "workspaces"]


factory.register(RetrieveWorkspaceEmail)

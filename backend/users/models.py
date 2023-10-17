from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from cookingcrafts.constants import User as U


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    BASE_ROLES = ((ADMIN, 'admin'), (USER, 'user'))

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("Username"),
        max_length=U.MAX_USERNAME,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    password = models.CharField(_("Password"),
                                max_length=U.MAX_PASSWORD)
    email = models.EmailField(_("Email address"),
                              max_length=U.MAX_EMAIL_FIELD,
                              unique=True, blank=False)
    first_name = models.CharField(_("First name"),
                                  max_length=U.MAX_FIRST_NAME,
                                  blank=False)
    last_name = models.CharField(_("Last name"),
                                 max_length=U.MAX_LAST_NAME,
                                 blank=False)
    role = models.CharField(_("User Role"), choices=BASE_ROLES,
                            default=USER,
                            max_length=U.MAX_ROLE_NAME)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = _('CookingCrafts Craftsman')
        verbose_name_plural = _('CookingCrafts Craftsmans')


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Fan'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Content Creator'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self) -> str:
        return f'{self.user} -> {self.author}'

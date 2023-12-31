from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager
from distribution.models import EmailDistribution
from .permissions import user_permissions


class CustomUser(AbstractUser, PermissionsMixin):
    """
    A custom user model where the unique identifier is email address.
    Inherits from Django's AbstractUser and PermissionsMixin for
    authentication fields and methods.
    """

    email = models.EmailField(_("email"), unique=True, blank=False)
    phone = PhoneNumberField(_("phone"), null=True, blank=True)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        permissions = user_permissions

    @staticmethod
    def create_profile(user, first_name, last_name, middle_name=None):
        return BaseProfile.objects.create(user=user, first_name=first_name, middle_name=middle_name,
                                          last_name=last_name)

    @staticmethod
    def get_by_id(user_id):
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            CustomUser.objects.filter(id=user_id).delete()
            return True
        return False


class BaseProfile(models.Model):
    """
    An abstract base class for user profiles. This class cannot be instantiated
    and must be inherited by other classes.
    """

    class Meta:
        abstract = True

    class UserGenderChoices(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False)
    gender = models.CharField(max_length=6, choices=UserGenderChoices.choices, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=256, null=True, blank=False)
    middle_name = models.CharField(_("middle name"), max_length=256, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=256, null=True, blank=False)
    photo = models.ImageField(_("photo"), upload_to="profiles/images", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)
    distributions = models.ManyToManyField(EmailDistribution, blank=True, related_name='distributions')

    @property
    def age(self):
        return (timezone.now() - self.date_of_birth).days // 365

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"


class Profile(BaseProfile):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False,
                                related_name="profile")

# class CustomerProfile(BaseProfile):
#     pass


# class SellerProfile(BaseProfile):
#     is_resident = models.BooleanField(default=True, null=False, blank=True)


# class AdminProfile(Profile):
#     user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False,
#                                 related_name="admin_profile")
#     promoted_by = models.ForeignKey(_("Assigned as admin by"), on_delete=models.SET_NULL)
#     promotion_date = models.DateTimeField(auto_created=True, editable=False)
#     demotion_date = models.DateTimeField(blank=True, null=True)
#
#     LEVELS = (
#         (1, 'moderator'),
#         (2, 'admin'),
#         (3, 'super_admin'),
#     )
#
#     level = models.PositiveSmallIntegerField(choices=LEVELS)
#
#     class Meta:
#         verbose_name = _("Admin Profile")
#         verbose_name_plural = _("Admin Profiles")
#
# '''
#     Level 1 - moderator (can only hide reviews, mute users)
#     Level 2 - admin (can crud users, reviews)
#     Level 3 - super_admin (can crud everything and admins)
# '''

# # Admin Level 1 Permissions
# # Reviews permissions
# can_hide_reviews = models.BooleanField(_("Allowed to hide users reviews"), default=False)
# can_edit_reviews = models.BooleanField(_("Allowed to edit users reviews"), default=False)
#
# # Users permissions
# can_edit_users = models.BooleanField(_("Allowed to edit users accounts and profiles"), default=False)
# can_mute_users = models.BooleanField(_("Allowed to mute users accounts"), default=False)
# can_ban_users = models.BooleanField(_("Allowed to ban users accounts"), default=False)
#
# # Products permissions
# can_activate_products = models.BooleanField(_("Allowed to activate products"), default=False)
# can_deactivate_products = models.BooleanField(_("Allowed to deactivate products"), default=False)
#
# can_create_products = models.BooleanField(_("Allowed to activate products"), default=False)
# can_edit_products = models.BooleanField(_("Allowed to activate products"), default=False)
#
# # Admin Level 3 permissions
# can_assign_admins = models.BooleanField(_("Allowed to assign new admins"), default=False)
# can_activate_users = models.BooleanField(_("Allowed to activate users accounts"), default=False)
# can_deactivate_users = models.BooleanField(_("Allowed to deactivate users accounts"), default=False)
#
# can_create_users = models.BooleanField(_("Allowed to create new users accounts"), default=False)
#
# can_delete_users = models.BooleanField(_("Allowed to delete users accounts completely"), default=False)
# can_delete_reviews = models.BooleanField(_("Allowed to delete users reviews"), default=False)

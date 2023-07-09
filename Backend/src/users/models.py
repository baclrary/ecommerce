from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager
from distribution.models import EmailDistribution


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model where the unique identifier is email address.
    Inherits from Django's AbstractBaseUser and PermissionsMixin for
    authentication fields and methods.
    """

    class UserTypeChoices(models.TextChoices):
        SELLER = "seller", _("seller")
        BUYER = "buyer", _("buyer")

    type = models.CharField(
        max_length=6,
        choices=UserTypeChoices.choices,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        _("email"),
        unique=True,
        blank=False
    )
    phone = PhoneNumberField(
        _("phone"),
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @staticmethod
    def create_profile(user, first_name, last_name, middle_name=None):
        return Profile.objects.create(user=user, first_name=first_name, middle_name=middle_name, last_name=last_name)

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


class Profile(models.Model):
    """
    An abstract base class for user profiles. This class cannot be instantiated
    and must be inherited by other classes.
    """
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=256,
        null=True,
        blank=False,
    )
    middle_name = models.CharField(
        _("middle name"),
        max_length=256,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=256,
        null=True,
        blank=False,
    )
    photo = models.ImageField(
        _("photo"),
        upload_to="profiles/images",
        null=True,
        blank=True,
    )
    distributions = models.ManyToManyField(
        EmailDistribution, blank=True
    )

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"


class BuyerProfile(Profile):
    """
    BuyerProfile model that extends Profile with buyer-specific fields.
    """

    class UserGenderChoices(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    gender = models.CharField(
        max_length=6,
        choices=UserGenderChoices.choices,
    )
    date_of_birth = models.DateTimeField(
        auto_now_add=False,
        default=None,
        null=True,
        blank=True,
    )

    def age(self):
        return (timezone.now() - self.date_of_birth).days // 365


class SellerProfile(Profile):
    """
    SellerProfile model that extends Profile with seller-specific fields.
    """
    website = models.URLField()
    is_resident = models.BooleanField(
        default=True,
        null=False,
        blank=True,
    )

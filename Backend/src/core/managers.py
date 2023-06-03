from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    Custom User Manager that extends Django's built-in UserManager to
    provide custom user creation methods. This Manager is used for
    creating regular and super users with an email as the unique identifier instead of a username.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a regular User with the given email and password. """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create and save a SuperUser with the given email and password. """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

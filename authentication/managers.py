from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_superuser(self, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(**other_fields)

    def create_user(self, password=None, **other_fields):
        user = self.model(**other_fields)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

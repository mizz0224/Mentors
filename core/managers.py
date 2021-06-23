from django.db import models

class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        
    def create_user(self, email, name, gender, birthdate, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=email,
            email=email,
            name=name,
            gender=gender,
            birthdate=birthdate,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, gender, birthdate, password):
        user = self.create_user(
            username=email,
            email=email,
            name=name,
            gender=gender,
            birthdate=birthdate,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
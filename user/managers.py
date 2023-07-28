from django.contrib.auth.base_user import BaseUserManager




class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        from user.models import Advisor
        if not username:
            raise ValueError('The username must be set')

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()

        print("oi", extra_fields.get('is_advisor'))
        if extra_fields.get('is_advisor'):
            Advisor.objects.create(user=user)

        # if extra_fields.get('is_mentor'):
        #     Mentor.objects.create(user=user)
        # else:
        #     Mentee.objects.create(user=user)

        return user

    def create_superuser(self, username, password, **extra_fields):
        # from user.models import Mentor, Mentee
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        user = self.create_user(username, password, **extra_fields)

        # if extra_fields.get('is_mentor'):
        #     Mentor.objects.create(user=user)
        # else:
        #     Mentee.objects.create(user=user)

        return user
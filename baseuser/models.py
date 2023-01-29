from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

from company.models import Company


class BaseUserQuerySet(models.QuerySet):
    """
    Custom QuerySet for the BaseUsers model.
    """

    def create_multiple(self, objs):
        """
        Create multiple BaseUsers instances in one go.

        Args:
            objs (List[BaseUsers]): List of BaseUsers instances to be created.
        """
        for obj in objs:
            obj.save()
        return self

    def delete(self):
        """
        Delete multiple BaseUsers instances in one go.

        Also deletes the related User instances.
        """
        for obj in self:
            obj.delete()
        return super(BaseUserQuerySet, self).delete()

    def update(self, *args, **kwargs):
        """
        Update multiple BaseUsers instances in one go.

        Also updates the related User instances.
        """
        for obj in self:
            # update related user's fields
            obj.django_user.username = kwargs.get('username',
                                                  obj.django_user.username)
            obj.django_user.email = kwargs.get('email', obj.django_user.email)
            password = kwargs.get('password')
            if password:
                obj.django_user.set_password(password)
                obj.password = obj.django_user.password  # todo check why the
                # password is not hashed in baseusers
                obj.django_user.save()
                obj.save()
            # update other fields for baseuser model
            for field, value in kwargs.items():
                setattr(obj, field, value)
            obj.django_user.save()
            obj.save()
        return super(BaseUserQuerySet, self).update(*args, **kwargs)


type_choices = [
    ('per', 'Person'),
    ('com', 'Company')
]

company_type = [
    ('pub', 'Public'),
    ('pri', 'Private'),
    ('sel', 'Self-Employed'),
    ('oth', 'Other'),
]


class BaseUsers(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        blank=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE,
                                       related_name='baseuser')
    user_type = models.CharField(max_length=3, choices=type_choices)
    objects = BaseUserQuerySet.as_manager()

    def __str__(self):
        """
        String representation of the BaseUsers instance.
        """
        return f'{self.username}'

    @transaction.atomic()
    def save(self, *args, **kwargs):
        """
        Save method for the BaseUsers model.
        The decorator @transaction.atomic() ensures that all database
        operations within the method are executed within a single
        transaction. This is important because we want to ensure that all
        operations related to creating or updating the BaseUser and User
        models are atomic, meaning that they either all succeed or all fail.
        """
        # Hash the password before saving it
        self.password = make_password(self.password)

        existing_django_users = User.objects.filter(Q(username=self.username) |
                                                    Q(email=self.email))
        """
        Check if a User with the same username or email already exists.
        If yes, relate the existing User instance to the BaseUsers and
        update the fields.
        If no, create a new User with the same fields as the BaseUsers model.
        """
        if existing_django_users:
            # relate the existing User instance to the baseuser and update the
            # fields
            django_user = existing_django_users.first()
            # check if there are any other existing User instances
            other_users = existing_django_users.exclude(id=self.django_user.id)
            try:
                base_user = BaseUsers.objects.get(django_user=django_user)
                base_user.username = self.username
                django_user.username = self.username
                base_user.email = self.email
                django_user.email = self.email
                base_user.password = self.password
                django_user.password = self.password
                django_user.save()
                # delete the other User instances which have the same
                # username or same email
                other_users.delete()

            except BaseUsers.DoesNotExist:
                # check if any of the other existing User instances are related
                # to the baseuser
                for other_user in other_users:
                    try:
                        BaseUsers.objects.get(django_user=other_user)
                        self.django_user.username = self.username
                        self.django_user.email = self.email
                        self.django_user.password = self.password
                        self.django_user.save()
                    except BaseUsers.DoesNotExist:
                        # delete the other User instance, if it is not related
                        # to the baseuser,
                        other_user.delete()
        else:
            # no existing User with the same username or email

            # the update part
            if self.pk:
                django_user = self.django_user
                django_user.username = self.username
                django_user.email = self.email
                django_user.password = self.password
                django_user.save()
                self.django_user = django_user
            # the create part
            else:
                # create a new User with the same fields as the BaseUsers model
                self.django_user = User.objects.create(
                    username=self.username,
                    email=self.email,
                    password=self.password)
        # save the self using the save method of the Model
        super().save(*args, **kwargs)

    def create_multiple(self, objs):
        self.objects.create_multiple(objs)
        super().bulk_create(objs)

    @transaction.atomic()
    def delete(self, *args, **kwargs):
        if self.django_user:
            self.django_user.delete()
        super().delete(*args, **kwargs)


class UserProfile(models.Model):
    base_user = models.OneToOneField(BaseUsers, on_delete=models.CASCADE,

                                     related_name='profile')
    current_company = models.ForeignKey(Company, null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='current_company')
    past_companies = models.ManyToManyField(Company, blank=True,
                                            related_name='past_companies')
    picture = models.ImageField(upload_to='profile_images',
                                default='profile_images/default.jpg')
    about = models.TextField(max_length=250, null=True)


class CompanyProfile(models.Model):
    base_user = models.OneToOneField(BaseUsers, on_delete=models.CASCADE,
                                     related_name='company_profile')
    company = models.OneToOneField(Company, on_delete=models.RESTRICT,
                                   related_name='company_user')
    website = models.URLField()
    number_of_employees = models.IntegerField()
    organization_type = models.CharField(max_length=3, choices=company_type)
    revenue = models.IntegerField()

    def __str__(self):
        return f'{self.company}'

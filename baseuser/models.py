from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models, transaction
from company.models import Company

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


class BaseUsersManager(models.Manager):
    @transaction.atomic
    def update(self, **kwargs):  #todo check why t is not working , this is for the BaseUsers.objects.filter(id=21).update(username='test')
        baseuser_id = kwargs.pop('pk')
        baseuser = BaseUsers.objects.get(id=baseuser_id)
        # Retrieve the related User instance
        django_user = User.objects.get(baseuser_id=baseuser_id)
        # Update the related User instance
        django_user.username = kwargs.get('username')
        django_user.email = kwargs.get('email')
        django_user.save()
        # Update the BaseUsers instance
        super().filter(pk=baseuser_id).update(**kwargs)
#
#     @transaction.atomic
#     def update(self, instance, **kwargs):
#         # # Hash the password before updating
#         # kwargs['password'] = make_password(
#         #     kwargs.get('password'))
#
#         # Update the related User instance
#         instance.django_user.username = kwargs['username']
#
#         instance.django_user.email = kwargs['email']
#
#         instance.django_user.set_password(kwargs['password'])
#         instance.django_user.save()
#
#         # Update the BaseUsers instance
#         instance.username = kwargs['username']
#         # instance.last_name = kwargs.get('last_name', instance.last_name)
#         instance.password = instance.django_user.password
#         # instance.save()
#         instance.save(**kwargs)
#
#         # return instance
#
#     # def create(self, username, email, password, user_type):
#         #     django_user = User.objects.create_user(username=username, email=email, password=password)
#         #     base_user = self.create(username=username, email=email,
#         #                             password=make_password(password),
#         #                             user_type=user_type,
#         #                             django_user_id=django_user.id)
#         #     return base_user
#     @transaction.atomic
#         # def delete(self, *args, **kwargs):  # todo , it is working in the
#         #     # DELETE request and it works for instance.delete() but check how to
#         #     # make it work when performing model.objects.filter(id=id).delete()
#         #     django_user = User.objects.get(username=self.username)
#         #     django_user.delete()
#         #     super().delete(*args, **kwargs)
#
#     def delete(self, instance):
#         # Get the 'django_user' foreign key
#         django_user = instance.django_user
#         # Delete the related 'User' instance
#         django_user.delete()
#         # Delete the 'BaseUsers' instance
#         # instance.delete()

# class BaseUsersManager(models.Manager):
#     @transaction.atomic
#     def update(self, **kwargs):  #todo check why t is not working , this is for the BaseUsers.objects.filter(id=21).update(username='test')
#         baseuser_id = kwargs.pop('pk')
#         baseuser = BaseUsers.objects.get(id=baseuser_id)
#         # Retrieve the related User instance
#         django_user = User.objects.get(baseuser_id=baseuser_id)
#         # Update the related User instance
#         django_user.username = kwargs.get('username')
#         django_user.email = kwargs.get('email')
#         django_user.save()
#         # Update the BaseUsers instance
#         super().filter(pk=baseuser_id).update(**kwargs)
#
#         # def create(self, username, email, password, user_type):
#         #     django_user = User.objects.create_user(username=username, email=email, password=password)
#         #     base_user = self.create(username=username, email=email,
#         #                             password=make_password(password),
#         #                             user_type=user_type,
#         #                             django_user_id=django_user.id)
#         #     return base_user
#         @transaction.atomic
#         def delete(self, *args, **kwargs):  # todo , it is working in the
#             # DELETE request and it works for instance.delete() but check how to
#             # make it work when performing model.objects.filter(id=id).delete()
#             django_user = User.objects.get(username=self.username)
#             django_user.delete()
#             super().delete(*args, **kwargs)

class BaseUsers(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        blank=True)  # todo
    # check why it is not working
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='baseuser')
    user_type = models.CharField(max_length=3, choices=type_choices)

    def __str__(self):

        return f'{self.username}'

    @transaction.atomic
    def save(self, *args, **kwargs):
        # this part is for the put method


        existing_user = User.objects.filter(email=self.email).first()
        print(existing_user)
        if existing_user: # and existing_user.baseuser:#todo
            existing_user.email = ''
        elif existing_user and not existing_user.baseuser:#todo check the
            # case where the django user with this email already exists and
            # whether it is related with a baseuser or no
            existing_user.delete()
        else:
            django_user = User.objects.create_user(username=self.username,
                                                   email=self.email,
                                                   password=self.password)
            self.django_user = django_user
            self.password = self.django_user.password
                # if existing_user.username != self.username:
                #
                #     """ Delete the email if a user exists with it already to make the
                #     # email in the user model unique"""
                #     existing_user.email = ''

        # this part is for the put method and updating the user


            # Delete the existing User instance
            # existing_user.delete()

        if self.pk:
            django_user = self.django_user
            django_user.username = self.username
            django_user.email = self.email
            django_user.set_password(self.password)
            django_user.save()
            self.django_user = django_user
            self.password = django_user.password
        # this part is for the create or Post method
        else:pass

            # super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        django_user = User.objects.get(baseuser=self)
        django_user.delete()
        super().delete(*args, **kwargs)


# class BaseUsers(models.Model):
#     username = models.CharField(max_length=200, null=True)
#     password1 = models.CharField(max_length=200, null=True)
#     password2 = models.CharField(max_length=200, null=True)
#     email = models.EmailField(max_length=200, null=True, unique=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     django_user = models.OneToOneField(User, on_delete=models.CASCADE,
#                                        related_name='baseuser')
#     user_type = models.CharField(max_length=3, choices=type_choices)
#
#     def __str__(self):
#         return f'{self.username}'


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
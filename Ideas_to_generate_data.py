from baseuser.models import BaseUsers
from company.models import Company

"""We can generate the data by many ways , for the baseusers  once we have a
list of the users to create we can loop over it and use the customized
create multiple method or we can write a script to perform this and give it
the parameters (number of users or any thing) or we can run those commands
in the shell"""

persons_to_create = [BaseUsers(username=f'user{i}',
                               email=f'user'f'{i}@example.com',
                               password='password', user_type='per')
                     for i in range(1, 101)]
company_users_to_create = [BaseUsers(username=f'com{i}',
                                     email=f'com{i}@example.com',
                                     password='password', user_type='com')
                           for i in range(1, 101)]
companies_to_create = [Company(name=f'new_com_{i}',
                               location=f'new_location' f'_{i}',
                               description=f'new_description_{i}')
                       for i in range(1, 101)]

# or like this if we do not want to override the company save method
companies = [Company.objects.create(name=f'com_{i}',
                                    location=f'location_{i}',
                                    description=f'description_{i}')
             for i in range(1, 101)]
print(companies_to_create)
""""if we have a list of users (csv or json format we can read the data from
it using pandas and load it into our variable users_to create"""

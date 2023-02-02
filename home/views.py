import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from requests.auth import HTTPBasicAuth

from company.models import Company
from home.forms import SurveyForm  # , CompanyForm
from survey.models import Survey


@login_required
def home_page(request):  # todo move the home with its templates to the home
    # app
    # user_id = request.session.get('user_id')
    # user = User.objects.get(id=user_id)
    # context = {'user': user}
    # return render(request, 'home.html', context)
    return render(request, 'home.html')


basic = HTTPBasicAuth('user1', 'password')


# def users_list(request):
#     """Fetch all users from the API and display in a dropdown list"""
#     # Replace with your authentication credentials
#     basic = HTTPBasicAuth('username', 'password')
#
#     # Replace with the correct API endpoint
#     users = requests.get('http://127.0.0.1:8001/api/v1/users/', auth=basic)
#
#     return render(request, "users_list.html", {"users": users.json()})

@login_required(login_url='loginPage')
def company_list(request):
    """User can view all companies in the system"""
    companies = requests.get('http://127.0.0.1:8001/api/v1/companies/',
                             auth=basic)  # change the port if it is different
    return render(request, "company_list.html",
                  {"companies": companies.json()})


@login_required(login_url='loginPage')
def add_company(request, *args, **kwargs):

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'location': request.POST.get('location'),
            'description': request.POST.get('description'),
            # Add other fields
        }
        response = requests.post(
            'http://127.0.0.1:8001/api/v1/companies/', data=data, auth=basic)
        if response.status_code == 201:
            # Company created successfully
            return redirect('company_list')
        else:
            # Handle error
            return redirect('add_company')
    return render(request, 'add_company.html')

# @login_required(login_url='loginPage')
# def add_company(request, *args, **kwargs):
#     form = CompanyForm()
#     if request.method == 'POST':
#         form = CompanyForm(request.POST)
#         if form.is_valid():
#             data = {
#                 'name': form.cleaned_data.get('name'),
#                 'location': form.cleaned_data.get('location'),
#                 'description': form.cleaned_data.get('description'),
#                 # Add other fields
#             }
#             response = requests.post(
#                 'http://127.0.0.1:8001/api/v1/companies/',
#                  data=data, auth=basic)
#             # if response.status_code == 201:
#             #     # Company created successfully
#             #     return redirect('company_list', {'form': form})
#             # else:
#             #     form = CompanyForm()
#             return render(request, 'home.html', {'form': form})

# class AddCompany(FormView):
#     template_name = 'home.html'
#     form_class = CompanyForm
#     # success_url = '/companies/'
#
#     def post(self, request, **kwargs):
#         form = SurveyForm(request.POST)
#         if form.is_valid():
#             data = {
#                 'name': form.cleaned_data.get('name'),
#                 'location': form.cleaned_data.get('location'),
#                 'description': form.cleaned_data.get('description'),
#                 # Add other fields
#             }
#             response = requests.post(
#                 'http://127.0.0.1:8001/api/v1/companies/', data=data,
#                 auth=basic)
#             # if response.status_code == 201:
#             #     # Company created successfully
#             #     return redirect('company_list', {'form': form})
#             # else:
#             #     form = CompanyForm()
#             # return render(request, 'home.html', {'form': form})
#         return super().post(request)


@login_required(login_url='loginPage')
def company_details(request, company_id):
    """Show all company details with button to create survey"""
    specific_company = Company.objects.get(id=company_id)
    context = {
        'company': specific_company,
        'surveys': Survey.objects.filter(company_id=specific_company.id)
    }
    return render(request, 'company_details.html', context)


class SurveyCreationView(FormView):
    template_name = 'create_survey.html'
    form_class = SurveyForm
    success_url = '/companies/'

    def post(self, request, **kwargs):
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
        return super().post(request)


@login_required(login_url='loginPage')
def test_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        new_company = Company(name=name,
                              location=location,
                              description=description)
        new_company.save()
        data = {'name': name, 'location': location, 'description': description}
        print(data)
        return JsonResponse(data, safe=False)

    else:
        return render(request, 'test_form.html', {})


def get_surveys_by_company(request, company_id):
    company = Company.objects.get(id=company_id)
    surveys = Survey.objects.filter(company=company, is_active=True)
    return render(request, 'surveys.html', {'surveys': surveys,
                                            'company': company})

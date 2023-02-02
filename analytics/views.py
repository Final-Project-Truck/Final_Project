import base64
import io
import urllib.parse

import matplotlib
import matplotlib.pyplot as plt
from django.db.models import Count
from django.shortcuts import render, redirect

from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Submission


def generate_report_surveys(request):
    if request.user.is_authenticated:
        matplotlib.use('Agg')
        ''' Number of surveys made per company'''
        surveys = Survey.objects.all().values('company_id').annotate(
            count=Count('id')).order_by('company_id')
        companies = Company.objects.all()
        x = []
        y = []
        for i in range(0, len(companies)):
            x.append(companies[i].name)
        for i in range(0, len(surveys)):
            # x.append(surveys[i]['company_id'])
            y.append(surveys[i]['count'])
            ''' convert the image to byte array, encode it to base64 and embed
                    into template'''
        if request.method == 'GET':
            plt.bar(x, y)
            plt.title('Number of surveys per company')
            plt.xticks(rotation=90)
            plt.xlabel('Company')
            plt.ylabel('Number of surveys')
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True, dpi=200)
            buf.seek(0)
            imsrc = base64.b64encode(buf.read())
            imuri = 'data:image/png;base64,{}'.format(
                urllib.parse.quote(imsrc))
            context = {'chart': imuri}
            buf.flush()
            buf.close()
        return render(request, 'chart.html', context)
    else:
        return redirect('/api/v1/')

def generate_report_submissions(request):
    if request.user.is_authenticated:
        matplotlib.use('Agg')
        ''' Number of submissions made per user'''
        submissions = Submission.objects.values('submitter_id').annotate(
            count=Count('submitter_id'))

        users = BaseUsers.objects.all()
        x = []
        y = []

        for i in range(0, len(users)):
            for j in range(0, len(submissions)):
                if users[i].id == submissions[j]['submitter_id']:
                    x.append(users[i].username)
                    y.append(submissions[j]['count'])
                else:
                    x.append(users[i].username)
                    y.append(0)

            ''' convert the image to byte array, encode it to base64 and embed
                    into template'''
        if request.method == 'GET':
            plt.bar(x, y)
            plt.title('Number of submissions per user')
            plt.xticks(rotation=90)
            plt.xlabel('Users')
            plt.ylabel('Number of submissions')
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True, dpi=200)
            buf.seek(0)
            imsrc = base64.b64encode(buf.read())
            imuri = 'data:image/png;base64,{}'.format(
                urllib.parse.quote(imsrc))
            context = {'chart_submission': imuri}
            buf.flush()
            buf.close()
        return render(request, 'submission.html', context)
    else:
        return redirect('/api/v1/')
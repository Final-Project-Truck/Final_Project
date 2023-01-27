import base64
import io
import urllib.parse

import matplotlib
import matplotlib.pyplot as plt
from django.db.models import Count
from django.shortcuts import render, redirect

from company.models import Company
from survey.models import Survey


def generate_report(request):
    if request.user.is_authenticated:
        matplotlib.use('Agg')
        ''' Number of surveys made per company'''
        surveys = Survey.objects.all().values('company_id').annotate(
            count=Count('id')).order_by('company_id')
        companies = Company.objects.all()
        x = []
        y = []
        for i in range(0, len(companies) -1):
             x.append(companies[i].name)
        for i in range(0, len(surveys) - 1):
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

        return render(request, 'chart.html', context)
    else:
        return redirect('/api/v1/')

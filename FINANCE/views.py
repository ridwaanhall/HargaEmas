from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
import requests

class DjangoProjectView(View):
    def get(self, request):
        try:
            local_time = timezone.localtime()
            project_time_zone = settings.TIME_ZONE
            
            response = requests.get('https://v2.jokeapi.dev/joke/Programming,Dark?blacklistFlags=religious&type=twopart')
            joke_data = response.json()
            
            if joke_data['error']:
                joke_setup = joke_data['setup']
                joke_delivery = joke_data['delivery']
            else:
                joke_setup = joke_data['setup']
                joke_delivery = joke_data['delivery']
            
            context = {
                'local_time': local_time,
                'project_time_zone': project_time_zone,
                'joke_setup': joke_setup,
                'joke_delivery': joke_delivery
            }
            return render(request, 'django-project.html', context)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
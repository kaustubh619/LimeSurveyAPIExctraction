from django.shortcuts import render
from django.http import HttpResponse
from limesurveyrc2api import LimeSurveyRemoteControl2API as LimeSurvey
import base64
import json
import PyPDF2
import slate3k as slate
from tablib import Dataset
from rest_framework.views import APIView
from rest_framework.response import Response

def survey(request):
    return render(request, 'survey.html')


class GetData(APIView):

    def get(self, request):
        url = "http://106.51.37.192:8000/ME_Survey/index.php/admin/remotecontrol"
        username = "admin"
        password = "admin123"

        api = LimeSurvey(url=url)

        session_key = api.sessions.get_session_key(username=username, password=password)

        result = api.surveys.list_surveys(session_key=session_key['result'], username=username)

        export_responses = api.respond.list_res(session_key=session_key['result'], survey_id="953879", document_type="json")
        stats = api.statistics.list_stats(session_key=session_key['result'], survey_id="953879", document_type="xls")

        decoded_export_responses = base64.b64decode(export_responses['result'])
        decoded_stats = base64.b64decode(stats['result'])

        # encoding = 'utf-8-sig'
        # string_data = decoded_export_responses.decode(encoding)

        f = open('filessss.xls', 'wb')
        f.write(decoded_stats)
        f.close()

        dataset = Dataset()
        g = open('filessss.xls', 'rb')
        any_data = g.read()
        g.close()
        imported_data = dataset.load(any_data)

        data = []
        for i in imported_data:
            data.append(list(i))
        
        return Response(data)

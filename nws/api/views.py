from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .utils import (get_url, api_response,)
from django.core.cache import cache
import requests, logging

_logger = logging.getLogger(__name__)

class NSWPing(APIView):
    
    def get(self, request):        
        url = get_url('A302', '.TXT')
        res = requests.get(url)
        resp = api_response(res.status_code, res.reason, 'pong')
        return JsonResponse(resp)    

class NSWInfo(APIView):
    def get(self, request):
        params = request.GET
        if not params.get('scode'):
            return redirect('home')
        
        scode = params.get('scode').upper()
        nocache = params.get('nocache')
        
        def metar_details(scode):
            from metar_taf_parser.parser.parser import MetarParser        
            url = get_url(scode, '.TXT')
            try:
                response = requests.get(url)
                _list = response.text.split()        
                date = _list.pop(0)
                time =_list.pop(0)
                code = ' '.join(_list)
                md = MetarParser().parse(code)
            except Exception as exc:
                _logger.error({'message':'Unable to parse meter codes','error':exc})
                resp = api_response(response.status_code, response.reason, '')                
                return JsonResponse(resp)
            qty = {
                'BKN': 'broken',
                'FEW': 'few',
                'NSC': 'no significant clouds.',
                'OVC': 'overcast',
                'SCT': 'scattered',
                'SKC': 'sky clear'
            }
            def parse_datetime(date,time):
                from datetime import datetime, timezone, timedelta
                input_string = date+' '+time
                format_string = "%Y/%m/%d %H:%M"
                
                parsed_datetime = datetime.strptime(input_string, format_string)
                # Set the timezone to GMT (UTC)
                parsed_datetime = parsed_datetime.replace(tzinfo=timezone.utc)
                return str(parsed_datetime)
            
            def cloud_status(c):
                if c.height:
                    return f"{qty[c.quantity.name]} at height {c.height} feet."
                else:
                    return f"{qty[c.quantity.name]}"
            values = {
                'Station': md.station,
                'Last_observation': parse_datetime(date,time),
                'Wind': f"{md.wind.direction} ({md.wind.degrees} degrees) at {md.wind.speed} {md.wind.unit}, gust '{md.wind.gust}'" if md.wind else '',
                'Visibility': f"{md.visibility.distance}",
                'Clouds': [cloud_status(i) for i in md.clouds],
                'Temperature': f"{md.temperature } \u00b0C",
                'Dew Point': f"{md.dew_point} \u00b0C",
                'Altimeter': md.altimeter,
                'Remark': md.remark,
                'Metar code': md.message
            }     
            
            resp = api_response(response.status_code, response.reason, values)                    
            return resp
        
        if not cache.has_key(scode+'.TXT') or nocache:            
            data = metar_details(scode)
            # set cache
            cache.set(scode + '.TXT', data, 300)
            return JsonResponse(data)
        else:
            data = cache.get(scode+'.TXT') 
            return JsonResponse(data)           
            
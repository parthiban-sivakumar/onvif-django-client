from django.shortcuts import render
from django.views.generic.base import View
from onvif import ONVIFCamera
from django.shortcuts import redirect
from django.shortcuts import render
import os
from django.template import RequestContext
from onvifApp.settings import BASE_DIR
from camera.models import Camera
from onvif import ONVIFService
import onvif
import json

from django.http import JsonResponse
# import zeep
# from zeep.wsse.username import UsernameToken


# Create your views here.
class CameraView(View):

    def get(self, request, *args, **kwargs):
        
        #Check WSDL path
        WSDL_PATH = os.path.join(os.path.dirname(onvif.__file__), 'wsdl')
        # Get Hostname
        cam_obj = Camera.objects.get(id=kwargs['id'])
        mycam = None
        try:
            mycam = ONVIFCamera(cam_obj.ip, int(cam_obj.port), cam_obj.username, cam_obj.password)
        except Exception as e:
            print('Exception message : ' , str(e))
            cam_obj.delete()
            return render( request,
			        'camera_login.html', {'success': 'False'})
        
        # Getdevice information

        resp = mycam.devicemgmt.GetHostname()
        hostname = str(resp.Name)
        resp = mycam.devicemgmt.GetDeviceInformation()
        Manufacturer = str(resp.Manufacturer)
        Model = str(resp.Model)
        FirmwareVersion = str(resp.FirmwareVersion)
        SerialNumber = str(resp.SerialNumber)
        HardwareId = str(resp.HardwareId)

        ############

        # Get System log

        syslog_obj = mycam.devicemgmt.create_type('GetSystemLog')
        #print('#######' , syslog_obj)
        syslog_obj['LogType'] = 'Access'
        syslog_resp_list = None
        try:
            syslog_resp = mycam.devicemgmt.GetSystemLog({'LogType' : syslog_obj.LogType})
            syslog_resp_list = str(syslog_resp.String).split('\n')
            #print(syslog_resp_list)
        except Exception as e:
            print('System log error: ', str(e))

        #############

        # Get date time 

        Sysdt_dt = mycam.devicemgmt.GetSystemDateAndTime()
        Sysdt_tz = Sysdt_dt.TimeZone
        Sysdt_year = Sysdt_dt.UTCDateTime.Date
        Sysdt_hour = Sysdt_dt.DaylightSavings
        
        #############


        return render( request,
			'camera_detail.html', {'hostname': hostname,
                'Manufacturer' : Manufacturer,'Model' : Model, 
                'FirmwareVersion': FirmwareVersion,
                'SerialNumber' : SerialNumber, 'HardwareId':HardwareId,
                'syslog_resp_list' : syslog_resp_list,
                'Sysdt_dt':Sysdt_dt, 'Sysdt_year' : Sysdt_year,
                'Sysdt_hour' : Sysdt_hour, 'Sysdt_tz' : Sysdt_tz
                 })

    def post(self, request, *args, **kwargs):
        print('nothing')

class CameraLoginView(View):

    def get(self, request, *args, **kwargs):     
        return render( request,
			'camera_login.html')

    def post(self, request, *args, **kwargs):
        ip = request.POST.get('ip-add','') 
        port = request.POST.get('port', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # cameras_list = list(Camera.objects.all().values())
        

        # return JsonResponse(cameras_list,safe=False)        # Check if camera is valid
        obj = Camera.objects.create(ip=ip, port=port,
            username=username, password=password)

        return redirect(
			'camera_detail', obj.id)
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import timezone
from hachi.common import *
from hachi.models import *
from hachi.forms import CalendarEventForm
import json, datetime
from time_bill import TimeBill

# Create your views here.
def fullCalendar(request):
    calendarEventForm = CalendarEventForm()
    return render_to_response('fullCalendar.html',
        {'calendarEventForm':calendarEventForm},
    )

def create_event(request):
    """读取HTTP请求, 创建Event
    """
    if request.method == 'GET':
        try:
            calendarEventForm = CalendarEventForm(request.GET)
            if calendarEventForm.is_valid():
                calendarEvent = calendarEventForm.save(commit=False)
                calendarEvent.start_time = str(calendarEvent.start_time).split('+')[0]
                calendarEvent.end_time = str(calendarEvent.end_time).split('+')[0]
                calendarEvent.save()
                return HttpResponse(returnJson(True))
            else:
                raise Exception(calendarEventForm.errors)
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in createEvent" % (e)))
    else:
        return HttpResponse(returnJson(False, "Request's method is not GET in getEventDescription"))


def getEvents(request):
    if request.method == 'GET':
        start_time = request.GET['start']
        end_time = request.GET['end']
        try :
            calendarEvents = CalendarEvent.objects.get_events_by_time(start_time, end_time)
            return HttpResponse(json.dumps(calendarEvents))
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in getEvents" % (e)))

def getEventDescription(request):
    if request.method == 'GET':
        try:
            id = int(request.GET['id'])
            calendarEvent = CalendarEvent.objects.get(id=id)
            return HttpResponse(returnJson(True, '', {
                'eventDescription' : calendarEvent.description,
            }))
        except Exception as e :
            return HttpResponse(returnJson(False, "%s in getEventDescription" % (e)))
    else : 
        return HttpResponse(returnJson(False, "Request's method is not GET in getEventDescription"))

def timeBill(request):
    if request.method == 'GET':
        try:
            return render_to_response('timeBill.html')
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in timeBill" % (e)))
    else : 
        return HttpResponse(returnJson(False, "Request's method is not GET in getEventDescription"))

def test(request):
    time_bill = TimeBill('2015-07-21', 10)
    return HttpResponse(json.dumps(time_bill.get_product_time_bill(1)))


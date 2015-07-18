from django.forms import ModelForm
from hachi.models import CalendarEvent

class CalendarEventForm(ModelForm):
    class Meta:
        model = CalendarEvent
        fields = "__all__"

     

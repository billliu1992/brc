from django.contrib import admin
from readings.models import *

admin.site.register(ReadingEntry)
admin.site.register(ReadingSchedule)
admin.site.register(ReadingScheduleEntry)

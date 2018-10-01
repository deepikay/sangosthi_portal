import os
import django
import csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sangoshti.settings")
django.setup()
from WebPortal.models import *
q=Show.objects.all()
shownames=[]
for i in q:
	if(i.STAT):
		shownames.append(i.showID)
fulldir=[]
for s in shownames:
    fulldir.append('/home/sangoshthi/sangoshthi_new/recordings/'+s+"/ZIP/")
ff=Content.objects.all()
rows=[]
rows.append('Phone')
rows.append('Name')
for i in ff:
    if(i.category=='HBPNC'):
        rows.append(i.name)
print(rows)
print(len(rows))

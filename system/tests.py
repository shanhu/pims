#from django.test import TestCase
from datetime import datetime
import calendar
from pprint import pprint

# Create your tests here.
nowstr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print( nowstr )  

dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")


print( dt.strftime("%A, %d. %B %Y %I:%M%p") ) 



cal = calendar.monthrange(2014, 2)

pprint(cal)

import datetime
import pytz


nzlocaltime= pytz.timezone('Pacific/Auckland')

#chose 13:45 new years day 2015, New Zealand at this time has
#daylight savings time active so it's time is 13hrs ahead of UTC
d = datetime.datetime(2014,1,1,13,45,tzinfo=nzlocaltime)

print "In New Zealand the time is:", d.ctime()
print "The same time in UTC is:",d.astimezone(pytz.utc).ctime()
print "Oops something is not right here, NZ is 13 hours ahead of"
print "UTC in the (southern) summer"

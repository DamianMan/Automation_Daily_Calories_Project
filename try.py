from datetime import datetime
from datetime import timedelta
from datetime import date


# taking input as the date
Begindatestring = "19-03-2023"

# carry out conversion between string
# to datetime object
Begindate = datetime.strptime(Begindatestring, "%d-%m-%Y")

# print begin date
print("Beginning date")
print(Begindate)

# calculating end date by adding 10 days
Enddate = (Begindate + timedelta(days=30))
# printing end date
print("Ending date")
Enddate_format = Enddate.strftime("%d-%m-%Y")
print(Enddate)

#comparing today
today = date.today().strftime("%d-%m-%Y")
print(f'today: {today}')
if today == Enddate_format:
    print('today')
    Enddate = (Enddate + timedelta(days=30))
    Enddate_format = Enddate.strftime("%d-%m-%Y")

    print('New Ending Date')
    print(Enddate_format)
else:
    Enddate = (Enddate + timedelta(days=10))

    print('New ending date')
    print(Enddate.strftime('%d-%m-%Y'))

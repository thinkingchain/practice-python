
from datetime import datetime 
         #Oct-20-2021 03:19:43 PM +UTC
myDate = 'Oct-20-2021 03:19:43 PM'

dt = datetime.strptime(myDate, '%b-%d-%Y %I:%M:%S %p')
dt_to_string = dt.strftime('%Y-%m-%d %H:%M:%S')
print(dt_to_string)


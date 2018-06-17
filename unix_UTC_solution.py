from datetime import datetime
import tzlocal

unix_timestamp = float("1331105102000")/1000.0
local_timezone = tzlocal.get_localzone()
local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)

month = local_time.strftime("%B")
date = local_time.strftime("%d")
if (len(date) == 1):
    date = "0" + date

print(local_time.strftime(month[0:3] + " " + date + ", %Y"))

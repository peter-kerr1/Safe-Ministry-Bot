from extensions.modules.constants import Roles
print(Roles.LEADER.value == "Leaders")


from datetime import datetime
import pytz
print(datetime.now(pytz.timezone('Australia/Sydney')).strftime("%H:%M:%S"))

print(type(5))
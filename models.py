from endpoints_proto_datastore.ndb.model import EndpointsModel
from google.appengine.ext import ndb

class Expense(EndpointsModel):
    _message_fields_schema = ("entityKey", "expense", "when", "category", "comment", "last_touch_date_time")
    expense = ndb.FloatProperty()
    when = ndb.DateProperty()
    category = ndb.StringProperty()
    comment = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)

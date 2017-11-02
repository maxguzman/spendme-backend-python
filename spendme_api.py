import endpoints
from protorpc import remote
from models import Expense
import main

ALLOWED_CLIENT_IDS = ['917298149160-2o259o9f76v62m17rvmnd7oqss3gjltq.apps.googleusercontent.com',
                      endpoints.API_EXPLORER_CLIENT_ID]

# deployed version
@endpoints.api(name='spendme', 
               version='v1', 
               description='SpendMe API', 
               hostname='maxgae-spendme.appspot.com', 
               allowed_client_ids=ALLOWED_CLIENT_IDS)
# local version
# @endpoints.api(name='spendme', 
#                  version='v1', 
#                  description='SpendMe API', 
#                  hostname='localhost:9080')
class SpendMeApi(remote.Service):

    @Expense.method(name='expense.insert',
                    path='expense')
    def insert_expense(self, request):
        if request.from_datastore:
            my_expense = request
        else:
            my_expense = Expense(parent=main.PARENT_KEY, 
                                 expense=request.expense, 
                                 when=request.when, 
                                 category=request.category, 
                                 comment= request.comment)
        my_expense.put()
        return my_expense
    
    @Expense.query_method(name='expense.list',
                          path='expenses',                             
                          query_fields=('limit', 'order', 'pageToken'))
    def list_expenses(self, query):
        return query
    
    @Expense.method(request_fields=('entityKey',), 
                    name='expense.delete',
                    path='expense/delete/{entityKey}',
                    http_method='DELETE')
    def expense_delete(self, request):
        if not request.from_datastore:
            raise endpoints.NotFoundException('expense not found')
        request.key.delete()
        return Expense(expense=0.00)
    
app = endpoints.api_server([SpendMeApi], restricted=False)

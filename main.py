import os
import webapp2
import jinja2
from models import Expense
from google.appengine.ext import ndb

# for debugging:
import logging
from datetime import datetime

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Generic key to serve as the parent (strong consistency)
PARENT_KEY = ndb.Key('Entity', 'expense_root')

class SpendMeWebApp(webapp2.RequestHandler):
    def get(self):
    	expenses_query = Expense.query(ancestor=PARENT_KEY).order(-Expense.last_touch_date_time)
    	logging.info({'expenses_query':expenses_query})
    	template = jinja_env.get_template('templates/spendme.html')
        self.response.write(template.render({'expenses_query':expenses_query}))

class InsertExpenseAction(webapp2.RequestHandler):
	def post(self):
		if self.request.get('entity_key'):
			expense_key = ndb.Key(urlsafe=self.request.get('entity_key'))
			# logging.info("String rep of REAL key = " + str(expense_key))
			expense = expense_key.get()
			expense.expense = float(self.request.get('expense_number'))
			expense.when = datetime.strptime(self.request.get('when'),  '%Y-%m-%d')
			expense.category = self.request.get('category')
			expense.comment = self.request.get('comment')
			expense.put()
		else:			
			new_expense = Expense(parent = PARENT_KEY,
								  expense = float(self.request.get('expense_number')),
								  when = datetime.strptime(self.request.get('when'),  '%Y-%m-%d'),
								  category = self.request.get('category'),
								  comment = self.request.get('comment'))
			new_expense.put()
		self.redirect(self.request.referer)

class DeleteExpenseAction(webapp2.RequestHandler):
	def post(self):
		expense_key = ndb.Key(urlsafe=self.request.get('entity_key'))
		expense_key.delete()
		self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
    ('/', SpendMeWebApp),
    ('/insertexpense', InsertExpenseAction),
    ('/deleteexpense', DeleteExpenseAction)
], debug=True)

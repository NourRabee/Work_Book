from django.core.exceptions import BadRequest
from datetime import *


class SearchQueryParameters:
    def __init__(self, query_params):
        self.query_params = query_params
        self.search_by = query_params.get('search_by')
        self.search_value = query_params.get('search_value')
        self.order_by = query_params.get('order_by', 'full_name')
        self.order_type = query_params.get('order_type', 'asc')
        self.filter_by = query_params.get('filter_by')
        self.filter_value = query_params.get('filter_value')
        self.limit = int(query_params.get('limit', 5))
        self.offset = int(query_params.get('offset', 0))

    def validate_mandatory_params(self):
        if self.search_by not in ['first_name', 'last_name', 'skill_id', 'full_name']:
            raise BadRequest('Please enter a valid search parameter; first_name, last_name, skill_id, full_name')
        if self.search_value is None:
            raise BadRequest('Please enter a search value')

        self.search_value = self.search_value.lower()

    def validate_params(self):

        if self.order_type:
            self.order_type = self.order_type.lower()
        if self.order_by:
            self.order_by = self.order_by.lower()

        if self.filter_by == 'slot_period':
            try:
                self.filter_value = datetime.strptime(self.filter_value, "%H:%M:%S").time()
                self.filter_by = self.filter_by.lower()
            except ValueError:
                raise BadRequest('Invalid time format for filtering. Please use HH:MM:SS format.')
        else:
            raise BadRequest('Filtering can only be done on slot_period.')


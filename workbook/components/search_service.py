from workbook.components.search_query_builder import SearchQueryBuilder


class SearchService:
    def __init__(self):
        self.search_builder = SearchQueryBuilder()

    def search(self, params):
        return (self.search_builder
                .set_params(params)
                .build_search_by()
                .build_order_by()
                .build_filter()
                .paginate()
                .execute())

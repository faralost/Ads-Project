from django.db.models import Q
from django.views.generic import ListView

from webapp.forms import SimpleSearchForm


class SearchListView(ListView):
    search_form_class = SimpleSearchForm
    search_form_field = "search"
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form_class()
        if self.search_value:
            context['form'] = self.search_form_class(initial={self.search_form_field: self.search_value})
            context[self.search_form_field] = self.search_value
        return context

    def get_form(self):
        return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get(self.search_form_field)

    def get_query(self):
        query = Q()
        for field in self.search_fields:
            kwargs = {field: self.search_value}
            query = query | Q(**kwargs)
        return query

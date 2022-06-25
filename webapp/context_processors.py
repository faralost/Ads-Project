from webapp.forms import SimpleSearchForm


def search_processor(request):
    form = SimpleSearchForm(request.GET)
    return {"search_form": form}

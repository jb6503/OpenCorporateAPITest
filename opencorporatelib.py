OCapiKey = ""

def lookup_url_(path):
    return 'https://api.opencorporates.com/v0.4/' + path


def reconcile_url_(path):
    return 'https://opencorporates.com/reconcile/' + path


def search(term):
    search_for = term.replace(' ', '+')
    return lookup_url_(('companies/search?q=' + search_for))


def lookup_sparse(id):
    return lookup_url_(id + '?api_token=' + OCapiKey + '&sparse=true')


def lookup(id):
    return lookup_url_(id + '?api_token=' + OCapiKey)


def reconcile(jurisdiction):
    return reconcile_url_(('us_' + jurisdiction))
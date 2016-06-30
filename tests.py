import requests
import pprint
import opencorporatelib as ocl

pprint.pprint(ocl.lookup(""))
pprint.pprint(ocl.reconcile("us_nv", "james brown"))
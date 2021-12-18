import json
import pickle

# with open - open with try..finally Link: https://www.programiz.com/python-programming/file-operation
with open('projects.json', 'r') as jsonFile:
  # returns JSON object as a dictionary
  jsonData = json.load(jsonFile)

# a dict többszörösen létrehozta a projects-et azért mélyebb szintől indítottam
with open('projects.pickle', 'wb') as pickleFile:
  tmp = list(jsonData.values())
  pickle.dump(tmp, pickleFile)
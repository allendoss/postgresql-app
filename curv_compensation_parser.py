from compensation_models import CompensationDatabaseModel
import json

class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )

def getJsonFileFromPath(json_path):
    try:
        with open(json_path, 'r') as f:
            compensation_data = json.load(f)
        return compensation_data
    except:
        print('json file does not exist')
        return None

def parseCurvModel(compensation_data):
    
    print(compensation_data)

def main():
    compensation_data = getJsonFileFromPath('/home/allen/postgresql-app/output/compensations.json')
    if compensation_data is not None:
        parseCurvModel(compensation_data)

main()
import MTGJson
import MTGDatabase

the_json = MTGJson.MtgJson()
database = MTGDatabase.MTGDatabase()

the_json.get_latest_json_url()

# the_json.open_json()

for i in the_json.open_json():
    print(i)
    database.record_changes(i[0], i[1], i[2])

# database.record_changes(the_json.open_json()[0], the_json.open_json()[1], the_json.open_json()[2])
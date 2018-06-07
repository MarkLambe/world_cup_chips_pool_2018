import json
import os

filename = 'data.json'

with open('backup_data.json', 'r') as backupjsonfile:
    backup_json_file = json.load(backupjsonfile)

with open(filename, 'r') as realjsonfile:
    real_json_file = json.load(realjsonfile)


for team in range(len(real_json_file['Teams'])):
    real_json_file['Teams'][team]['winning_odds'] = backup_json_file['Teams'][team]['winning_odds']

os.remove(filename)
with open(filename, 'w') as new_json_file:
    json.dump(real_json_file, new_json_file, indent=4, ensure_ascii=False)

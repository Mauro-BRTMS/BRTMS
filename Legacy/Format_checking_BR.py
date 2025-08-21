import pandas as pd
import re

def flag_row(row):
    flags = []
    if pd.notnull(row['destinationCode']) and len(str(row['destinationCode'])) < 4:
        flags.append('short_code')
    time_pattern = re.compile(r'^(1[0-2]|0?[1-9]):[0-5]\d:[0-5]\d\s?(AM|PM)$', re.IGNORECASE)
    if not pd.isna(row['pickupTime']) and not time_pattern.match(str(row['pickupTime'])):
        flags.append('bad_time_format')
    valid_days = {'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'}
    if str(row['pickupDay']) not in valid_days:
        flags.append('invalid_day')
    if str(row['deliveryDay']) not in valid_days:
        flags.append('invalid_day')
    time_window_pattern = re.compile(r'^\d{2}:\d{2}[AP]M\s*-\s*\d{2}:\d{2}[AP]M$')
    if not pd.isna(row['deliveryWindow']) and not time_window_pattern.match(str(row['deliveryWindow'])):
        flags.append('bad_time_window')
    return ', '.join(flags) if flags else ''

file = pd.read_csv("business_rules.csv", sep=';', dtype={'destinationCode': str, 'pickupTime': str})
print(file)
#file['flag'] = file['destinationCode'].apply(lambda x: 'flag' if pd.notnull(x) and len(str(x)) < 4 else '')
file['flag'] = file.apply(flag_row, axis=1)
file['code_padded'] = file['destinationCode'].astype(str).str.zfill(4)
file['destinationCode'] = file['code_padded']
file = file.drop(columns='code_padded')
file.to_csv("BR_format_checking.csv",index=False, sep =';')
print (file)

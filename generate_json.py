#!/usr/bin/env python3

import re
import json

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring

# remove these endings from metro names
CHOP_ENDINGS = (
    'MSA',
    'HMFA',
    'HNMFA',
    'Statutory Exception Area',
    '(part)',
)

with open('data-pdf.txt') as f:
    lines = f.readlines()

data = {}
metro_name = None
metro_data = {}
for i, l in enumerate(lines):
    if 'FY 2019 MFI:' in l:
        metro_name = lines[i - 1].strip()
        for ending in CHOP_ENDINGS:
            metro_name = rchop(metro_name, ending).strip()

    m = re.search(r'EXTR LOW INCOME (.*)', l)
    if m is not None:
        metro_data['extremely_low_income'] = list(map(int, m.group(1).strip().split()))

    m = re.search(r'VERY LOW INCOME (.*)', l)
    if m is not None:
        metro_data['very_low_income'] = list(map(int, m.group(1).strip().split()))

    m = re.search(r'LOW-INCOME (.*)', l)
    if m is not None:
        metro_data['low_income'] = list(map(int, m.group(1).strip().split()))
        data[metro_name] = metro_data
        metro_name = None
        metro_data = {}

print('\n'.join(sorted(data.keys())))
print(len(data.keys()))
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

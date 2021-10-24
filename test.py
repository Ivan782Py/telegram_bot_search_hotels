import re

i = '34  - f5 4.8 7,9  5.68787 0.47'
new_elem = re.findall(r"[0-9]*[.]?[0-9]+", i)
print(new_elem)

new_elem = re.findall(r'\d+(\.\d{1,2})?', i)
print(new_elem)
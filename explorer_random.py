import random
from prettytable import PrettyTable
import re
# ========================================================================================
## age vars =====
# clusters = "clusters-age"
# freq = "freq-age"
# pairs = "pairs-age"
# op_1 = "Under25"
# op_2 = "Over30"

## gender vars ====
clusters = "clusters-gender"
freq = "freq-gender"
pairs = "pairs-gender"
op_1 = "Male"
op_2 = "Female"

## class vars ====
# clusters = "clusters-class"
# freq = "freq-class"
# pairs = "pairs-class"
# op_1 = "High"
# op_2 = "Low"
"""
Age Clusters examples from the data
"""
with open(clusters, 'r', encoding="utf8") as f:
    user_input = f.readlines()
header = user_input[0].strip().split('\t')
t = PrettyTable(header)
chosen = [random.choice(user_input).strip().split('\t')][0][0]
print("The chosen word is: "+chosen)
r = re.compile(str(chosen))
newlist = list(filter(r.match, user_input))
cleaned = [i.strip().split('\t') for i in newlist]
result = [t.add_row(cleaned[i]) for i in range(0, len(cleaned))]
t.align = "l"
print(t)
f.close()
# ========================================================================================
"""
Age Pairs Examples from the data
"""
with open(pairs, 'r', encoding="utf8") as f:
    user_input = f.readlines()
header = user_input[0].strip().split('\t')
t = PrettyTable(header)
r = re.compile(str(chosen))
newlist = list(filter(r.match, user_input))
cleaned = [i.strip().split('\t') for i in newlist]
result = [t.add_row(cleaned[i]) for i in range(0, len(cleaned))]
t.align = "l"
print(t)
f.close()
# ========================================================================================
"""
Age Frequency Examples from the data
"""
with open(freq, 'r', encoding="utf8") as f:
    user_input = f.readlines()
header = user_input[0].strip().split(' ')
header.append("Winner")
t = PrettyTable(header)
r = re.compile(str(chosen))
newlist = list(filter(r.match, user_input))
cleaned = [i.strip().split(' ') for i in newlist]
for index, item in enumerate(cleaned):
    if cleaned[index][1] > cleaned[index][2]:
        cleaned[index].append(op_1)
    else:
        cleaned[index].append(op_2)
result = [t.add_row(cleaned[i]) for i in range(0, len(cleaned))]
t.align = "l"
print(t)
f.close()
# ========================================================================================

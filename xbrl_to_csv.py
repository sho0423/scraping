# -*- coding: utf-8 -*-
# xbrlからdbへ流し込む形にデータを整形する

import re

fname = 'jpcrp030000-asr-001_E03217-000_2019-08-31_01_2019-11-29'
fp = './out/'+fname+'.xbrl'
with open(fp) as f:
  lines = [i for i in f.readlines() if "jpdei" in i or "jppfs" in i or "jpcrp" in i]


for i in lines:
  if "jpdei_cor:NumberOfSubmissionDEI" in i:
    start = lines.index(i)
  elif "jpcrp_cor:BusinessResultsOfGroupTextBlock" in i or "BusinessResultsOfReportingCompanyTextBlock" in i:
    end = lines.index(i)
    break
info = lines[start:end]


pat = [r'/>', r'</.+', r'<', r'>']
pat_c = list(map(re.compile, pat))

parsed = []
for i in info:
  w = i
  for j in range(3):
    w = re.sub(pat_c[j], '', w)
  n = re.sub(r'>',' ',w)
  l = n.split()
  if l == []:
    continue
  
  if l[1]=='xsi:nil="true"':
    l.pop(1)
    l.append('null')
  
  if 'contextRef' not in l[1]:
    l.pop(1)

  t = ['Instant', 'Duration']
  st = ['i', 'd']
  y = ['Current', 'Prior1', 'Prior2', 'Prior3', 'Prior4']
  for j in range(len(y)):
    for k in range(len(t)):
      if y[j] + 'Year' + t[k] in l[1]:
        l[1] = l[1].replace(y[j] + 'Year' + t[k], str(j)+'_'+st[k])
        break
    else:
      continue
    break
  
  if 'NonConsolidatedMember' in l[1]:
    l[1] = l[1].replace('NonConsolidatedMember', 'nc')
  if len(l) > 3:
    if 'decimals' in l[3]:
      l.pop(3)

    if 'unitRef' in l[2]:
      l.pop(2)
  
  parsed.append(l)

print(len(parsed))

print(parsed)
cols = []

for i in parsed:
  if i[0] not in cols:
    cols.append(i[0])

  if i[0]=='jpdei_cor:FilerNameInJapaneseDEI':
    print(i[2])
  
  elif i[0]=='jpdei_cor:SecurityCodeDEI':
    print(i[2])
  
  elif i[0]=='jpdei_cor:TypeOfCurrentPeriodDEI':
    print(i[2])
  
  elif i[0]=='jpdei_cor:AccountingStandardsDEI':
    print(i[2])

print(cols)

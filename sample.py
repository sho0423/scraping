# -*- coding: utf-8 -*-

import requests
import json
import zipfile
import time
import os
import shutil
import re

def download_file(fname, path='./'):
  """URL を指定してファイルをダウンロードする
  """
  url = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/'+fname+'?type=1'
  r = requests.get(url, stream=True)
  with open(path+fname+'.zip', 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush()
    return fname

  # ファイルが開けなかった場合は False を返す
  return False

# apiから取得したzipの中から必要なxbrlだけを解凍
# inputpathを入力としてoutputpathへ結果を出力
def unzip_xbrl(fname, inputpath='./', outputpath='./'):
  with zipfile.ZipFile(inputpath+fname+'.zip') as zip_e:
    for j in zip_e.namelist():
      p = re.search(r'XBRL/PublicDoc/(.+)\.xbrl', j)
      if p:
        fp = p.group(0)
        zip_e.extract(fp, outputpath)
        shutil.move(outputpath+fp,outputpath)
        shutil.rmtree(outputpath+'XBRL/')
        os.remove(inputpath+fname+'.zip')
        break
      # time.sleep(1)  # 1秒スリープ



ymd = [2019, 11, 29]  # 一括ダウンロードする日付
date_embeded = str(ymd[0])+'-'+str(ymd[1])+'-'+str(ymd[2])

url = u'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date='+date_embeded+'&type=2'

headers = {"content-type": "application/json"}
r = requests.get(url, headers=headers)
data = r.json()

# 一般企業の四半期報告書と有報だけを選んで,ダウンロードするファイル名を取り出す
dl_fnames = [i['docID'] for i in data['results'] if i['formCode']=='043000' or i['formCode']=='030000']
print(len(dl_fnames))

for i in dl_fnames:
  download_file(i, './DL/')
  print('file: '+i+" is downloaded!")
  unzip_xbrl(i, './DL/', './out/')
  print('file: '+i+" is processed!({}/{})".format(dl_fnames.index(i)+1, len(dl_fnames)))

# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import re
import zipfile
import os
import time
import shutil
from pathlib import Path
from kab.items import KabItem
import glob

direc = Path(__file__).parent  # 現在のディレクトリ
dl_path = direc / 'DL/'
out_path = direc / 'out/'


dl_path = str(dl_path) + '/'
out_path = str(out_path) + '/'
print('頬おっほおっほお')
print(dl_path)
print(glob.glob(dl_path+'*'))

def download_file (fname, path='./'):
  """URL を指定してファイルをダウンロードする
  """
  url = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/'+fname+'?type=1'
  r = requests.get(url, stream=True)
  with open(path+'/'+fname+'.zip', 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush()
    return fname

  # ファイルが開けなかった場合は False を返す
  return False

# apiから取得したzipの中から必要なxbrlだけを解凍
# inputpathを入力としてoutputpathへ結果を出力
def unzip_xbrl (fname, inputpath, outputpath, formCode, docDescription, edinetCode, periodStart, periodEnd):
  fp = inputpath + fname + '.zip'
  with zipfile.ZipFile(fp) as zip_e:
    file_name = get_fname(formCode, docDescription, edinetCode, periodStart, periodEnd)
    tar = 'XBRL/PublicDoc/' + file_name + '.xbrl'
    n_l = zip_e.infolist()
    print('tar = ' + tar)
    for i in n_l:
      print(i.filename)
      if i.filename == tar:
        print('name matched!')
        j = n_l.index(i)
        zip_e.extract(zip_e.infolist()[j], outputpath)
    print('unzipped!')
    """
    XBRL/PublicDoc/jpcrp030000-asr-001_E05042-000_2019-08-31_01_2019-11-29.xbrl
    XBRL/PublicDoc/jpcrp030000-asr-001_E05042-000_2018-09-01_01_2019-08-31.xbrl
    shutil.move(tar, outputpath)
    print('moved!')
    shutil.rmtree(outputpath+'XBRL/')
    os.remove(inputpath+fname+'.zip')
    for j in zip_e.namelist():
      p = re.search(outputpath + r'/XBRL/PublicDoc/(.+)\.xbrl', j)
      if p:
        fp = p.group(0)
        zip_e.extract(fp, outputpath)
        print('unzipped!')
        shutil.move(outputpath+fp,outputpath)
        print('moved!')
        shutil.rmtree(outputpath+'XBRL/')
        os.remove(inputpath+fname+'.zip')
        break
      """
    time.sleep(1)  # 1秒スリープ

# 解凍するzipの名前を適切に判断するための関数
def get_fname (formCode, docDescription, edinetCode, periodStart, periodEnd):
  pattern = re.compile(r'第[0-9]四半期')
  s = re.search(pattern, docDescription)
  if s:
    quarter = 'q' + s.group()[1] + 'r'
  
  else:
    quarter = 'asr'
  return 'jpcrp' + formCode + '-' + quarter + '-' + '001_' + edinetCode + '-000_' + periodStart + '_01_' + periodEnd

def move_file (inputpath, outputpath):
  pass

class ScrapyEdinetSpiderSpider(scrapy.Spider):
  name = 'scrapy_edinet_spider'
  allowed_domains = ['disclosure.edinet-fsa.go.jp']
  start_urls = ['https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2019-11-29&type=2']

  def parse(self, response):
    """
    レスポンスに対するパース処理
    """
    # jsonにする
    res_json = json.loads(response.body_as_unicode())['results']
    print('ぼえええええええ')
    print(len(res_json))

    dl_docs = []
    dl_docs_formCode = []
    dl_docs_docDescription = []
    dl_docs_edinetCode = []
    dl_docs_periodStart = []
    dl_docs_periodEnd = []

    for doc in res_json:
      if doc['ordinanceCode'] == '010':
        if doc['formCode'] == '043000' or doc['formCode'] == '030000':
          # 雑多なデータを無視して有報と四半期報告書のみをダウンロード対象にする。
          dl_docs.append(doc['docID'])
          dl_docs_docDescription.append(doc['docDescription'])
          dl_docs_formCode.append(doc['formCode'])
          dl_docs_edinetCode.append(doc['edinetCode'])
          dl_docs_periodStart.append(doc['periodStart'])
          dl_docs_periodEnd.append(doc['periodEnd'])

          yield KabItem(
            name = doc['filerName'],
            ticker = doc['secCode'],
            periodStart = doc['periodStart'],
            periodEnd = doc['periodEnd'],
          )
    
    n = len(dl_docs)
    for i in range(3):
      download_file(dl_docs[i], dl_path)
      print('file: '+ dl_docs[i] +" has been downloaded!")
      unzip_xbrl(dl_docs[i], dl_path, out_path, dl_docs_formCode[i], dl_docs_docDescription[i], dl_docs_edinetCode[i], dl_docs_periodStart[i], dl_docs_periodEnd[i])
      print('file: '+ dl_docs[i] +" is processed!({}/{})".format(i + 1, len(dl_docs)))

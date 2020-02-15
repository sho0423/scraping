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
def unzip_xbrl_returns_file_name (fname, inputpath, outputpath):
  fp = inputpath + fname + '.zip'
  with zipfile.ZipFile(fp) as zip_e:
    file_name_pattern = re.compile(r'XBRL/PublicDoc/jpcrp[0-9]{6}-.{3}-[0-9]{3}_E[0-9]{5}-[0-9]{3}_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}_[0-9]{4}-[0-9]{2}-[0-9]{2}.xbrl')
    n_l = zip_e.infolist()
    for i in n_l:
      match_obj = file_name_pattern.match(i.filename)
      if match_obj:
        print('file found!')
        zip_e.extract(i, outputpath)
        print('unzipped!')
        return match_obj.group()
    print('file name match error!')


# 解凍したファイルのディレクトリ構造を取り除く
def move_file (fname, outputpath):
  shutil.move(outputpath + fname, outputpath)
  shutil.rmtree(outputpath+'XBRL/')

# dlして解凍してディレクトリ整理する一連の流れを関数化
def from_api_to_xbrl (docTitleList, dlDir, outDir):
  n = len(docTitleList)
  for i in range(n):
    download_file(docTitleList[i], dlDir)
    print('file: '+ docTitleList[i] +" has been downloaded!")
    fname = unzip_xbrl_returns_file_name(docTitleList[i], dlDir, outDir)
    move_file(fname, outDir)
    os.remove(dlDir + docTitleList[i] +'.zip')
    print('file: '+ docTitleList[i] +" is processed!({}/{})".format(i + 1, len(docTitleList)))
    time.sleep(1)

def extract_from_xbrl (filepath):
  # return xbrl_infos[]
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

    print('レスポンス受け取り成功、処理開始')
    print(len(res_json))

    # ダウンロードするzipを決めるリスト
    docIDs = []

    # xbrlを参照しなくても得られる情報
    meta_infos = []

    # xbrlを解析しないとわからない情報
    xbrl_infos = []
    

    for doc in res_json:
      # 雑多なデータを無視して有報と四半期報告書のみをダウンロード対象にする。
      if doc['ordinanceCode'] == '010':
        if doc['formCode'] == '043000' or doc['formCode'] == '030000':
          if doc['secCode']:
            
            docIDs.append(doc['docID'])

            meta_infos.append((doc['secCode'], doc['filerName'], doc['docDescription'], doc['periodStart'], doc['periodEnd']))
          


    
    from_api_to_xbrl(docIDs, dl_path, out_path)

    for i in range(len(docIDs)):
      yield KabItem(
        secCode = meta_infos[i][0],
        filerName = meta_infos[i][1],
        docDescription = meta_infos[i][2],
        periodStart = meta_infos[i][3],
        periodEnd = meta_infos[i][4],
      )
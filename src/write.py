from pathlib import Path
import re

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def openFile(name='out'):
  return open(f'{_dir}/' + name, 'w', buffering=1024*1024)

def saveStr(text, name='out'):
  file = openFile(name)
  file.write(str(text))
  file.close()

def saveCsv(rows, name='out.csv', sep=','):
  file = openFile(name)
  for row in rows:
    for i in range(0, len(row)):
      if i > 0:
        file.write(sep)
      file.write(str(row[i]))
    file.write('\n')
  file.close()

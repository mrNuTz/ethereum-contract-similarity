from pathlib import Path
import re

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def openFile(filename='out'):
  return open(f'{_dir}/' + filename, 'w', buffering=1024*1024)

def saveStr(text, filename='out'):
  file = openFile(filename)
  file.write(str(text))
  file.close()

def saveCsv(rows, filename='out.csv', sep=','):
  file = openFile(filename)
  for row in rows:
    for i in range(0, len(row)):
      if i > 0:
        file.write(sep)
      file.write(str(row[i]))
    file.write('\n')
  file.close()

from pathlib import Path
import re

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def open_out(name='out'):
  return open(f'{_dir}/' + name, 'w', buffering=1024*1024)

def write_out(text='', name='out'):
  file = open_out(name)
  file.write(str(text))
  file.close()


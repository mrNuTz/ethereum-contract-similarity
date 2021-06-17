from pathlib import Path
import re
from typing import Dict, List

from pandas.core.frame import DataFrame
from common import IdCodeT

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

def saveGml(
  groupToCodes: Dict[str, List[IdCodeT]],
  df: DataFrame,
  filename="similarityGraph.gml"
):
  file = openFile(filename=filename)
  file.write(
    f"""graph [
      directed 0
      label "{filename}"
    """)
  for (group, codes) in groupToCodes.items():
    for (id, code) in codes:
      file.write(
        f"""node [
          id "{id}"
          label "{id}"
          group "{group}"
        ]
        """)

  cols = tuple(df.columns)
  for index, row in df.iterrows():
    file.write("edge [\n")
    for col in cols:
      attr = 'source' if col == 'id1' else 'target' if col == 'id2' else col
      val = row[col]
      if isinstance(val, str):
        file.write(f'{attr} "{val}"\n')
      else:
        file.write(f"{attr} {val}\n")
    file.write("]\n")

  file.write("]\n")

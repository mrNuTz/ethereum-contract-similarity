import re
import matplotlib.pyplot as plt
from pathlib import Path

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def scatter(df, x, y, newFigure=False, name='scatter', colorBy=None, dotSize=1):
  if newFigure: plt.figure()
  if colorBy is not None:
    plt.scatter(df[x], df[y], s=dotSize, c=df[colorBy].rank())
  else:
    plt.scatter(df[x], df[y], s=dotSize)
  plt.title('scatter')
  plt.xlabel(x)
  plt.ylabel(y)
  plt.savefig(f'{_dir}/{name}_{x}_{y}.png')

def qq(df, x, y, newFigure=False, name='qq'):
  if newFigure: plt.figure()
  plt.scatter(df[x].rank().div(c := df[x].count()), df[y].rank().div(c), s=1)
  plt.title('qq')
  plt.xlabel(x)
  plt.ylabel(y)
  plt.savefig(f'{_dir}/{name}_{x}_{y}.png')

import matplotlib.pyplot as plt
from pathlib import Path

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = d.replace(r'/$', '')
  Path(_dir).mkdir(parents=True, exist_ok=True)

def scatter(df, x, y, newFigure=False):
  if newFigure: plt.figure()
  plt.scatter(df[x], df[y], s=1)
  plt.title('scatter')
  plt.xlabel(x)
  plt.ylabel(y)
  plt.savefig(f'{_dir}/scatter_{x}_{y}.png')

def qq(df, x, y, newFigure=False):
  if newFigure: plt.figure()
  plt.scatter(df[x].rank().div(c := df[x].count()), df[y].rank().div(c), s=1)
  plt.title('qq')
  plt.xlabel(x)
  plt.ylabel(y)
  plt.savefig(f'{_dir}/qq_{x}_{y}.png')

import re, os
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def saveScatter(
  df, x: str, y: str, title='scatter', filename=None, colorBy:str=None, dotSize=4,
  cmap='Paired', alpha=0.4
):
  plt.figure(figsize=(7,7))
  scatter(df, x, y, title, colorBy, dotSize, cmap, alpha)
  plt.savefig(f'{_dir}/{title} {x} {y}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()

def scatter(df, x, y, title='scatter', colorBy=None, dotSize=1, cmap='Paired', alpha=1):
  if colorBy is not None:
    plt.scatter(
      df[x], df[y], s=dotSize, c=df[colorBy].rank(),
      cmap=plt.get_cmap(cmap), alpha=alpha)
  else:
    plt.scatter(df[x], df[y], s=dotSize)
  plt.title(title)
  plt.xlabel(x)
  plt.ylabel(y)

def qq(df, x, y, title='qq'):
  plt.scatter(df[x].rank().div(c := df[x].count()), df[y].rank().div(c), s=1)
  plt.title(title)
  plt.xlabel(x)
  plt.ylabel(y)

def saveHistogram(
  series, title='hist', label=None, xlabel=None, ylabel=None, filename=None, **kwargs):
  plt.figure(figsize=(4, 5))
  hist(series, title, label, xlabel, ylabel, **kwargs)
  plt.savefig(f'{_dir}/{title}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()

def hist(series, title='hist', label=None, xlabel=None, ylabel=None, **kwargs):
  plt.hist(series, label=label, **kwargs)
  plt.title(title)
  if label is not None:
    plt.legend()
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel != None:
    plt.ylabel(ylabel)

def listPngFiles() -> List[str]:
  global _dir
  return sorted(f for f in os.listdir(_dir) if f[-4:] == '.png')

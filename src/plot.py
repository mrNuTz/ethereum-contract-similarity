import re
import matplotlib.pyplot as plt
from pathlib import Path

_dir = '.'

def setDir(d: str):
  global _dir
  _dir = re.sub(r'/$', '', d)
  Path(_dir).mkdir(parents=True, exist_ok=True)

def saveScatter(df, x: str, y: str, title='scatter', filename=None, colorBy:str=None, dotSize=1, cmap='Paired'):
  plt.figure(figsize=(7,7))
  scatter(df, x, y, title, colorBy, dotSize, cmap)
  plt.savefig(f'{_dir}/{title} {x} {y}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()

def scatter(df, x, y, title='scatter', colorBy=None, dotSize=1, cmap='Paired'):
  if colorBy is not None:
    plt.scatter(df[x], df[y], s=dotSize, c=df[colorBy].rank(), cmap=plt.get_cmap(cmap))
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

def saveHistogram(series, title='hist', xlabel=None, ylabel=None, filename=None, bins=10):
  plt.figure(figsize=(7,7))
  plt.hist(series, bins=bins)
  plt.title(title)
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel != None:
    plt.ylabel(ylabel)
  plt.savefig(f'{_dir}/{title}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()

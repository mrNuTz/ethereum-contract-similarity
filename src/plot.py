import re, os
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List
import numpy as np

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

def saveViolin(df, column, title=None, filename=None):
  title = f'{title} violin {column}' if title is not None else f'violin {column}'
  plt.figure(figsize=(4, 3))
  ax = plt.axes()
  series = (df[column][df['isInner'] == False], df[column][df['isInner'] == True])
  vp = ax.violinplot(series, vert=False, widths=1, showextrema=False)
  cBody, sBody = vp['bodies']
  sBody.set_facecolor('#ff7f0e')
  sBody.set_alpha(1)
  cBody.set_facecolor('#1f77b4')
  cBody.set_alpha(0.7)
  ax.boxplot(series, vert=False, widths=.5, showfliers=False, medianprops={'color': 'black'},)
  ax.set_yticks((1, 2), labels=('cross', 'same'))
  ax.set_title(title, { 'fontsize': 10 })
  plt.savefig(f'{_dir}/{title}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()

def listPngFiles() -> List[str]:
  global _dir
  return sorted(f for f in os.listdir(_dir) if f[-4:] == '.png')

def saveCDF(df, column, title=None, filename=None, **kwargs):
  title = f'{title} cdf {column}' if title is not None else f'cdf {column}'
  plt.figure(figsize=(4, 4))

  kwargs = {
    'bins': 30,
    'range': (0, 1),
    'alpha': 0.7,
    'density': True,
    'histtype': 'stepfilled',
    **kwargs
  }
  cross, *_ = plt.hist(
    df[column][df['isInner'] == False],
    label='cross group',
    cumulative=-1,
    **kwargs)
  same, *_ = plt.hist(
    df[column][df['isInner'] == True],
    label='same group',
    cumulative=True,
    **kwargs)
  overlap = np.array([cross, same]).min(axis=0).sum()

  plt.title(title, { 'fontsize': 10 })
  plt.legend()
  plt.savefig(f'{_dir}/{title}.png' if filename is None else f'{_dir}/{filename}.png')
  plt.close()
  return overlap

import matplotlib.pyplot as plt
import util

def scatter(df, x, y, newFigure=False):
  if newFigure: plt.figure()
  plt.scatter(df[x], df[y], s=1)
  plt.title('scatter')
  plt.xlabel(x)
  plt.ylabel(y)
  ts = util.timestamp()
  plt.savefig(f'out/{ts}_scatter_{x}_{y}.png')

def qq(df, x, y, newFigure=False):
  if newFigure: plt.figure()
  plt.scatter(df[x].rank().div(c := df[x].count()), df[y].rank().div(c), s=1)
  plt.title('qq')
  plt.xlabel(x)
  plt.ylabel(y)
  ts = util.timestamp()
  plt.savefig(f'out/{ts}_qq_{x}_{y}.png')

import util

def open_out(name='out'):
  ts = util.timestamp()
  name = f'{ts}_{name}'
  return open('out/' + name, 'w', buffering=1024*1024)

def write_out(text='', name='out'):
  file = open_out(name)
  file.write(str(text))
  file.close()

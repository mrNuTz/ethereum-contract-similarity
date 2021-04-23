from datetime import datetime

def open_out(name='out'):
  ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  name = f'{ts}_{name}'
  return open('out/' + name, 'w', buffering=1024*1024)

def write_out(text='', name='out'):
  file = open_out(name)
  file.write(str(text))
  file.close()

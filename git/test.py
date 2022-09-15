import select
import subprocess
import time

x = subprocess.Popen(['/bin/bash', '-c', "while true; do sleep 5; echo yes; done"], stdout=subprocess.PIPE)

y = select.poll()
y.register(x.stdout, select.POLLIN)

i = 0
while x.poll() is None:
    if y.poll(1):
        i += 1
        print(x.stdout.readline(), i)
        if i >= 2:
            x.kill()
    else:
        print("nothing here")
        time.sleep(1)

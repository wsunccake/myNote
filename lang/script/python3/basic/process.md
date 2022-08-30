# process

## subprocess

```python
import subprocess

subprocess.call(['ls', '-l'])

c1 = subprocess.Popen(['grep', '^root', '/etc/passwd'], stdout = subprocess.PIPE)
c2 = subprocess.Popen(["cut", "-d:", "-f1"], stdin = c1.stdout)
c2.communicate()
```

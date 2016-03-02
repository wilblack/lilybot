import subprocess

res = subprocess.check_output(['/etc/init.d/lilybotd', 'status'])

if res.find("Process dead") >= 0:
    subprocess.call(['/etc/init.d/lilybotd', 'start'])

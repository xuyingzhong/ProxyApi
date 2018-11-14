cat > adsl.py <<EOF 
#!/usr/bin/env python3
import subprocess
import time
while True:
    subprocess.call("pppoe-start", shell=True)
    subprocess.call("echo nameserver 8.8.8.8 >> /etc/resolv.conf",shell=True)
    subprocess.call("echo nameserver 223.5.5.5 >> /etc/resolv.conf",shell=True)
    subprocess.call("echo nameserver 223.6.6.6 >> /etc/resolv.conf",shell=True)
    subprocess.call(["curl","http://ip:port/?baship=云主机的名称&addr=云主机的城市"])
    time.sleep(180)
    subprocess.call("pppoe-stop", shell=True)
EOF

将地址放google浏览器转化一遍，复制进去，打开一下，然后复制出来，最终填入的地址是这样的。
http://ip:port/?baship=%E4%BA%91test136&addr=%E5%8D%81%E5%A0%B0%E7%94%B5%E4%BF%A1"

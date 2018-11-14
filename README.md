# ProxyApi
用于大数据采集用的代理池
在数据采集的过程中，最需要的就是一直变化的代理ip。
自建adsl为问题是只有一个区域的IP。
买的代理存在的问题是不稳定，影响采集效率。
本项目的作用是将目前的云vps，安装代理软件，然后使用脚本每隔3分钟拨号一次，返回当前可用的ip给代理池，代理池记录后，提供给API接口给采集程序调用。
1、安装软件：
我们使用的云立方的云vps，每季度打折后200元不到。推荐系统用centos，它自动将adsl的账号密码弄好。

yum -y install squid
yum install -y httpd-tools
yum install -y openssl

2、设置代理的账号和密码:
touch /etc/squid/squid_passwd
chown squid /etc/squid/squid_passwd
htpasswd /etc/squid/squid_passwd proxy #会提示输入两次密码

3、写入配置文件：
cat > /etc/squid/squid.conf <<EOF 
#http_access allow all
http_port 65500
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/squid_passwd
auth_param basic children 50
auth_param basic realm Squid proxy-caching web server
auth_param basic credentialsttl 2 hours
auth_param basic casesensitive off
acl ncsa_users proxy_auth REQUIRED
http_access allow ncsa_users
http_access deny all
forwarded_for off
request_header_access Allow allow all
request_header_access Authorization allow all
request_header_access WWW-Authenticate allow all
request_header_access Proxy-Authorization allow all
request_header_access Proxy-Authenticate allow all
request_header_access Cache-Control allow all
request_header_access Content-Encoding allow all
request_header_access Content-Length allow all
request_header_access Content-Type allow all
request_header_access Date allow all
request_header_access Expires allow all
request_header_access Host allow all
request_header_access If-Modified-Since allow all
request_header_access Last-Modified allow all
request_header_access Location allow all
request_header_access Pragma allow all
request_header_access Accept allow all
request_header_access Accept-Charset allow all
request_header_access Accept-Encoding allow all
request_header_access Accept-Language allow all
request_header_access Content-Language allow all
request_header_access Mime-Version allow all
request_header_access Retry-After allow all
request_header_access Title allow all
request_header_access Connection allow all
request_header_access Proxy-Connection allow all
request_header_access User-Agent allow all
request_header_access Cookie allow all
request_header_access All deny all
visible_hostname mybogusproxyhostname.local
httpd_suppress_version_string on
EOF

4、设置开机启动和重启squid：
systemctl enable squid && systemctl restart squid

5、写入拨号脚本：
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

6、启动拨号脚本：
#也可以写到/etc/rc.d/rc.local，记得把/etc/rc.d/rc.local设置可执行权限，不然不起作用。
nohup python adsl.py

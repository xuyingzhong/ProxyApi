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
/etc/squid/squid.conf 

4、设置开机启动和重启squid：
systemctl enable squid && systemctl restart squid

5、写入拨号脚本：
adsl.py 

6、启动拨号脚本：
#也可以写到/etc/rc.d/rc.local，记得把/etc/rc.d/rc.local设置可执行权限，不然不起作用。
nohup python adsl.py

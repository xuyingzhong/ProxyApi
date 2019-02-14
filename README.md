# ProxyApi
用于大数据采集用的代理池
在数据采集的过程中，最需要的就是一直变化的代理ip。
自建adsl为问题是只有一个区域的IP。
买的代理存在的问题是不稳定，影响采集效率。
云vps不允许安装花生壳等，即使有花生壳，它的解析也不及时，跟不上3分钟变一次。
本项目的作用是将目前的云vps，安装代理软件，然后使用脚本每隔3分钟拨号一次，返回当前可用的ip给代理池，代理池记录后，提供给API接口给采集程序调用。

一共有几个板块：代理主机拨号返回ip，代理池接受ip并记录然后提供给采集程序，统计代理主机的数量、每台提供的ip数量等，检查代理ip是否异常并展示到网页，简单的认证，网页执行命令管理云主机。

项目有个巧妙的地方分享给大家，就是对于后端的采集程序对于api的调用的频率是极高的，每秒可达几百上千次。因为数据量不大，所以全放内存运行，数据库只是接收到新ip地址后在改变了内存里面的变量的同时写到数据作为备份，如果程序出错，启动的时候先加载数据库的数据到内存。

代理池的程序在ProxyApi.tar中，使用的django框架，当时急用没有写注释，供大家参考。

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

7、查询方式，API的接口：
因为公司有几种语言，使用的代理格式不一样，所以这里只返回一个ip地址，代理的端口、用户名、密码是固定的，采集程序自己写。

http://ip:port/getip    所有随机

http://ip:port/getip?ip=云主机名称  按云主机名称查询

http://ip:port/getip?addr=重庆移动,重庆电信&tof=f    按地区随机，addr可以是单值，也可以使多值，多值用小写的,分割，tof （true or false），不写默认为t，传值f表示非

8、管理：
http://ip:port/checkip ，状态查询，可以只看故障的主机，可以看单个主机最近提供的ip，和总的提供的ip及不重复的ip。


http://ip:port/shell ，程序会自动把云主机的名字写到主机管理里面，但是管理ip、账号、密码需要手动添加，配置后才能网页执行命令。

9、新增一个/opt/ProxyApi/shell/timeout.py 用于自动处理掉线机器，和4小时发一次邮件报告状态，如果有连续掉线的机器，就可以告知运营商处理。不用盯着去处理故障了。

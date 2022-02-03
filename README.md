# eduroam-test-web-based


注意：

之前的 eduroam-test.cgi 是shell脚本，存在安全问题。

这里用C重写了，下载代码后，修改 eduroam-test.c 最上面的raidus 服务器IP和密码，然后执行 make 生成 eduroam-test.cgi，功能与之前的完全一样，放在/var/www/cgi-bin目录下即可。

感谢：

使用了 https://github.com/ndevilla/dict https://github.com/ndevilla/tcgi

# eduroam.ustc.edu.cn 安装过程

```
yum install openssl-devel  libnl-devel perl-libwww-perl.noarch

cd /usr/src
wget https://w1.fi/releases/wpa_supplicant-2.6.tar.gz
tar zxf wpa_supplicant-2.6.tar.gz
cd wpa_supplicant-2.6/wpa_supplicant
cp defconfig .config

vi .config
找到
#CONFIG_EAPOL_TEST=y
修改为
CONFIG_EAPOL_TEST=y

make eapol_test

cp eapol_test /usr/local/bin
```


Code for eduroam test via web based service

It is a service which emulates user connecting to the access point connected to the eduroam (http://eduroam.org) infrastructure. You can use your test accounts to test wheter your users will be able to authenticate with eduroam outside your institution.

## Requirement

* You have to your local RADIUS server connected to the eduroam.

## Instalation

* Store the script to /usr/lib/cgi-bin/
* Enable CGI scripts in Apache web server
* Configure apache to poin to the eduroam-test.cgi script, e.g.:

```
   ScriptAlias /eduroam-test/ /usr/lib/cgi-bin/
   <Directory /usr/lib/cgi-bin/>
	Options -Indexes -FollowSymLinks +ExecCGI
	Order allow,deny
	Allow from all

	SetHandler cgi-script
   </Directory>
```

* Or if you would like to have nice UI, then store index.html in /var/www/eduroam-test and  point Apache to it:

```
    Alias /eduroam-test/ /var/www/eduroam-test/
    <Directory /var/www/eduroam-test/>
	Options -Indexes -FollowSymLinks
        Order allow,deny
	Allow from all

	DirectoryIndex index.html
    </Directory>
```
* Configure RADIUS server IP and shared secret in the script

## Usage

* Just go to https://<your machine>/eduroam-test/eduroam-test.cgi

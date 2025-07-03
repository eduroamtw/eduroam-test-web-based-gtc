# eduroam-test-web-based (Python Version)

A Python Flask web application for testing eduroam RADIUS configurations. This service emulates a user connecting to an access point connected to the eduroam infrastructure. You can use test accounts to verify whether your users will be able to authenticate with eduroam outside your institution.

## Requirements

* Python 3.8 or higher
* Flask web framework
* `eapol_test` utility (from wpa_supplicant)
* A local RADIUS server connected to eduroam

```
flask run --host=0.0.0.0 --port 8080
```

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

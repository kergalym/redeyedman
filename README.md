# My blog
## Achtung! Pet project! Use it at own risk!

redeyedman blog source repo

# Screenshoots
## front:
<img src="https://i.imgur.com/YcqxqK9.png" />
<img src="https://i.imgur.com/2zU0VOS.png" />
<img src="https://i.imgur.com/YgnqLWu.png" />
<img src="https://i.imgur.com/MvXMZOB.jpg" />
<img src="https://i.imgur.com/N4zAs9J.png" />

#adminboard:
<img src="https://i.imgur.com/1QjnZmp.png" />
<img src="https://i.imgur.com/VJaygL2.jpg" />
<img src="https://i.imgur.com/sEzNwUG.png" />
<img src="https://i.imgur.com/ZUNl5HS.png" />
<img src="https://i.imgur.com/QJQqVpm.png" />

# Features
* CRUD 
* Assigning posts to category
* Basic User access management
* File management (includes graphic image converter)

# Working Apache virtualhost configuration file for Gentoo

cat /etc/apache2/vhosts.d/01_redeyedman-flask.kz.conf

 &lt;VirtualHost *:80&gt;
    
    ServerName redeyedman-flask.kz
    ServerAlias www.redeyedman-flask.kz
    DocumentRoot /var/www/redeyedman-flask.kz/htdocs/redeyedman-flask.kz

     WSGIDaemonProcess redeyedman-flask.kz user=apache group=apache threads=5
     WSGIScriptAlias / /var/www/redeyedman-flask.kz/htdocs/redeyedman-flask.kz/redeyedman.wsgi

    <Directory /var/www/redeyedman-flask.kz>
        WSGIProcessGroup redeyedman-flask.kz
        WSGIScriptReloading On
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
 &lt;/VirtualHost&gt;


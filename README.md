# My blog
redeyedman blog source repo


# Working Apache virtualhost configuration file for Gentoo

cat /etc/apache2/vhosts.d/01_redeyedman-flask.ru.conf

 &lt;VirtualHost *:80&gt;
    
    ServerName redeyedman-flask.ru
    ServerAlias www.redeyedman-flask.ru
    DocumentRoot /var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru

     WSGIDaemonProcess redeyedman-flask.ru user=apache group=apache threads=5
     WSGIScriptAlias / /var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru/redeyedman.wsgi

    <Directory /var/www/redeyedman-flask.ru>
        WSGIProcessGroup redeyedman-flask.ru
        WSGIScriptReloading On
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
 &lt;/VirtualHost&gt;


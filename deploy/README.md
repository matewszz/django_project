# Deploy

### Chaves SSH

Para criar chaves ssh no seu computador, utilize o comando ssh-keygen. Se você
já tem chaves SSH no computador e por algum motivo queira usar outra, use o
comando:

```
ssh-keygen -t rsa -b 4096 -f CAMINHO+NOME_DA_CHAVE
```

Lembre-se que a pasta .ssh deve existir dentro da pasta do seu usuário para que
seja possível criar a chave SSH. Muito comum ocorrer erros no Windows por falta
dessa pasta.

Para conectar-se ao servidor usando uma chave SSH com caminho personalizado,
utilize:

```
ssh IP_OU_HOST -i CAMINHO+NOME_DA_CHAVE
```

### Ao entrar no servidor

A primeira coisa será atualizar tudo:

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git

```


## Instalando o PostgreSQL

```
# Nós fizemos isso acima
sudo apt install postgresql postgresql-contrib -y
```

Caso queira mais detalhes: https://youtu.be/VLpPLaGVJhI  
Mais avançado: https://youtu.be/FZaEukN_raA

### Configurações

```
sudo -u postgres psql

# Criando um super usuário
CREATE ROLE usuario WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'senha';

# Criando a base de dados
CREATE DATABASE basededados WITH OWNER usuario;

# Dando permissões
GRANT ALL PRIVILEGES ON DATABASE basededados TO usuario;

# Saindo
\q

sudo systemctl restart postgresql
```

Caso queira mais detalhes: https://youtu.be/VLpPLaGVJhI  
Mais avançado: https://youtu.be/FZaEukN_raA

## Configurando o git

```
git config --global user.name 'matewszz'
git config --global user.email 'mferreira.nox@gmail.com'
git config --global init.defaultBranch main
```

## Criando um repositório no servidor

git clone hhtps_repo

## instalar o pyenv
```
sudo apt install git curl build-essential dkms perl wget -y

sudo apt install gcc make default-libmysqlclient-dev libssl-dev -y

sudo apt install -y zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm \
  libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git

curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

sudo apt-get install libssl-dev


-=-=-= COLOCAR TXT ABAIXO DENTRO DO nano server: nano ~/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

Depois Ctrl + O para salvar, Ctrl + x para sair. Recarrega o CMD = ➜ source ~/.zshrc    

Depois ir no cmd e instalar a versão do python desejada: pyenv install 3.10.11
Para escolher a versão do python: ➜ pyenv global 3.10.11
```

## Criando o ambiente virtual

```
python -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2  #conectar do postgress + python
pip install gunicorn  #conector do django com ngix
```

```
cp .env-example .env
nano .env
nano .env
```

# Criando o arquivo socket

```
sudo nano /etc/systemd/system/gunicorn_blog.socket

# Cole
[Unit]
Description=gunicorn blog socket

[Socket]
ListenStream=/run/gunicorn_blog.sock

[Install]
WantedBy=sockets.target

# Criando o arquivo gunicorn_blog.service
sudo nano /etc/systemd/system/gunicorn_blog.service

# Cole e edite
[Unit]
Description=gunicorn daemon
Requires=gunicorn_blog.socket
After=network.target

[Service]
User=__USUARIO__
Group=www-data
WorkingDirectory=/home/__USUARIO__/__PASTA_DO_PROJETO__
ExecStart=/home/__USUARIO__/__PASTA_DO_PROJETO__/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_blog.sock \
          __PASTA_DO_ARQUIVO_WSGI__.wsgi:application

[Install]
WantedBy=multi-user.target

# Ativando
sudo systemctl start gunicorn_blog.socket
sudo systemctl enable gunicorn_blog.socket

# Checando
sudo systemctl status gunicorn_blog.socket
curl --unix-socket /run/gunicorn_blog.sock localhost
sudo systemctl status gunicorn_blog

```

# Gere o arquivo dhparam.pem
```
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

# Instale o certbot
sudo apt install certbot

# Crie um certificado para seu domínio
sudo certbot certonly --standalone -d dominio.com.br
```

## Configurando o nginx
```
# Instale o nginx
sudo apt install nginx -y

# NESTE ARQUIVO, MODIFIQUE TODAS AS OCORRÊNCIAS DE temp.otaviomiranda.com.br
# PARA SEU DOMÍNIO

# Crie um server
sudo nano /etc/nginx/sites-enabled/temp.otaviomiranda.com.br

# PARA HTTP (:80)
# (Se já configurou o certbot no seu domínio, use a opção abaixo desta)
server {
	listen 80;
	listen [::]:80;

	index index.html index.htm index.nginx-debian.html index.php;

	server_name temp.otaviomiranda.com.br;

	location /static/ {
		root /home/luizotavio/blog;
	}

	location /media {
		alias /home/luizotavio/blog/media/;
	}

	location / {
		include proxy_params;
		proxy_pass http://unix:/run/gunicorn_blog.sock;
	}

	location ~ /\.ht {
		deny all;
	}

	location ~ /\. {
		access_log off;
		log_not_found off;
		deny all;
	}

	gzip on;
	gzip_disable "msie6";

	gzip_comp_level 6;
	gzip_min_length 1100;
	gzip_buffers 4 32k;
	gzip_proxied any;
	gzip_types
		text/plain
		text/css
		text/js
		text/xml
		text/javascript
		application/javascript
		application/x-javascript
		application/json
		application/xml
		application/rss+xml
		image/svg+xml;

	access_log off;
	#access_log  /var/log/nginx/temp.otaviomiranda.com.br-access.log;
	error_log   /var/log/nginx/temp.otaviomiranda.com.br-error.log;
}

# PARA HTTPS (:443)
# (APENAS SE VOCÊ CONFIGUROU O CERTBOT NO SEU DOMÍNIO)
server {
	listen 80;
	listen [::]:80;

	listen 443 ssl http2;
	listen [::]:443 ssl http2;
	ssl_certificate /etc/letsencrypt/live/temp.otaviomiranda.com.br/fullchain.pem; # managed by Certbot
	ssl_certificate_key /etc/letsencrypt/live/temp.otaviomiranda.com.br/privkey.pem; # managed by Certbot
	ssl_trusted_certificate /etc/letsencrypt/live/temp.otaviomiranda.com.br/chain.pem;

	# Improve HTTPS performance with session resumption
	ssl_session_cache shared:SSL:10m;
	ssl_session_timeout 5m;

	# Enable server-side protection against BEAST attacks
	ssl_prefer_server_ciphers on;
	ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

	# Disable SSLv3
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

	# Diffie-Hellman parameter for DHE ciphersuites
	# $ sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096
	ssl_dhparam /etc/ssl/certs/dhparam.pem;

	# Enable HSTS (https://developer.mozilla.org/en-US/docs/Security/HTTP_Strict_Transport_Security)
	add_header Strict-Transport-Security "max-age=63072000; includeSubdomains";

	# Enable OCSP stapling (http://blog.mozilla.org/security/2013/07/29/ocsp-stapling-in-firefox)
	ssl_stapling on;
	ssl_stapling_verify on;
	resolver 8.8.8.8 8.8.4.4 valid=300s;
	resolver_timeout 5s;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html index.php;

	server_name temp.otaviomiranda.com.br;

	location = /favicon.ico { access_log off; log_not_found off; }
	location /static/ {
		root /home/luizotavio/blog;
	}

	location /media {
		alias /home/luizotavio/blog/media/;
	}

	location / {
		include proxy_params;
		proxy_pass http://unix:/run/gunicorn_blog.sock;
	}

	# deny access to .htaccess files, if Apache's document root
	# concurs with nginx's one
	#
	location ~ /\.ht {
		deny all;
	}

	location ~ /\. {
		access_log off;
		log_not_found off;
		deny all;
	}

	gzip on;
	gzip_disable "msie6";

	gzip_comp_level 6;
	gzip_min_length 1100;
	gzip_buffers 4 32k;
	gzip_proxied any;
	gzip_types
		text/plain
		text/css
		text/js
		text/xml
		text/javascript
		application/javascript
		application/x-javascript
		application/json
		application/xml
		application/rss+xml
		image/svg+xml;

	  access_log off;
	#access_log  /var/log/nginx/temp.otaviomiranda.com.br-access.log;
	error_log   /var/log/nginx/temp.otaviomiranda.com.br-error.log;
}
```
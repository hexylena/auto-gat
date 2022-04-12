echo 'password' > ~/.vault-password.txt;

cat > ~/.hosts <<-EOF
[galaxyservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
[pulsarservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
EOF

cat > ~/.ansible.cfg <<-EOF
[defaults]
interpreter_python = /usr/bin/python3
inventory = ~/.hosts
retry_files_enabled = false
vault_password_file = ~/.vault-password.txt
EOF

cat > ~/.extra.yml <<-EOF
nginx_ssl_role: galaxyproject.self_signed_certs
openssl_self_sign: true
openssl_domains: "{{ certbot_domains }}"

# These need to be re-defined for some reason?
openssl_certificate_path: "/etc/ssl/certs/{{ openssl_domains[0] }}.crt"
openssl_private_key_path: "/etc/ssl/private/{{ openssl_domains[0] }}.pem"

nginx_conf_ssl_certificate: "{{openssl_certificate_path}}"
nginx_conf_ssl_certificate_key: "{{ openssl_private_key_path }}"
EOF

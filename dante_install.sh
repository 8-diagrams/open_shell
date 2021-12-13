# 本脚本适合 centos7 系统直接用dante建立socks5
# 同时适合 5.10.75-79.358.amzn2.x86_64 
# curl https://cdn.jsdelivr.net/gh/8-diagrams/open_shell/dante_install.sh
# bash <(curl -s -L https://cdn.jsdelivr.net/gh/8-diagrams/open_shell/dante_install.sh)

if [ $# -lt 3 ] ; then

   echo "用法 " $0 [端口] [用户名] [密码]

   exit 1;
fi

echo "begin to install..."

SS_PORT=$1
SS_U=$2
SS_P=$3

echo Socks5 端口 $SS_PORT
echo Socks5 用户名 $SS_U
echo Socks5 密码 $SS_P


rpm -ivh http://mirror.ghettoforge.org/distributions/gf/el/7/plus/x86_64/dante-1.4.1-176.9.x86_64.rpm
rpm -ivh http://mirror.ghettoforge.org/distributions/gf/el/7/plus/x86_64/dante-server-1.4.1-176.9.x86_64.rpm  



mkdir  /var/run/sockd/

cat - > /etc/sockd-${SS_PORT}.conf <<EOF

logoutput: stderr

# logoutput: /var/log/sockd.log

# 使用本地所有可用网络接口的 SS_PORT 端口
internal: eth0 port = ${SS_PORT}
external: eth0

# socks的验证方法，设置为 pam.username，本例中，是使用系统用户验证，即使用adduser添加用户
socksmethod: pam.username

user.privileged: root

user.unprivileged: nobody

# user.libwrap: nobody

# 访问规则
client pass {
        from: 0.0.0.0/0  to: 0.0.0.0/0
}

socks pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        protocol: tcp udp
        socksmethod: pam.username
        log: connect disconnect
}

socks block {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: connect error
}
EOF

cat - > /etc/pam.d/sockd<<EOF

#%PAM-1.0
#auth      required     pam_sepermit.so
auth       include      system-auth
account    required     pam_nologin.so
account    include      system-auth
password   include      system-auth
# pam_selinux.so close should be the first session rule
session    required     pam_selinux.so close
session    required     pam_loginuid.so
# pam_selinux.so open should only be followed by sessions to be
executed in the 
user context
session    required     pam_selinux.so open env_params
session    optional     pam_keyinit.so force revoke
session    include      system-auth
session    required     pam_limits.so

EOF

useradd ${SS_U} ; echo ${SS_P}| passwd --stdin ${SS_U}


nohup sockd -f /etc/sockd-${SS_PORT}.conf >/tmp/dante.run.log 2>&1 &

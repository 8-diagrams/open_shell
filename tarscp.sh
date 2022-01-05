#!/bin/bash

myip=`curl http://httpbin.org/ip  | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'`

if [ -z "${myip}" ] ; then

  echo "can't get VPS ip"
  exit 3

fi

echo "VPS IP" ${myip}

DIR=$1
if [ -z "${DIR}" ] ; then
   echo usage $0 "<file>" "login_name@host:path" "passwd_of_login"
   exit 2
fi

if [ $# -lt 3 ]; then
   echo usage $0 "<file>" "login_name@host:path" "passwd_of_login"
   exit 127
fi

SSH_LOGIN_PATH=$2
SSH_LOGIN_PWD=$3


echo tar this file/dir ${DIR} ...

fn=`echo ${DIR}| sed "s:/:++:g"`

isroot=`expr substr $DIR 1 1 == '/'`

#not from root
if [ $isroot -eq 1 ] ; then

   echo cd /
   cd /
   DIR=`echo $DIR | awk '{ print substr($1, 2,  length($1)-1) }' `

fi

TMPFN=/tmp/${fn}.tgz

echo tar -zcvf $TMPFN $DIR
dt=`date +%y%m%d%H%M`

tar -zcvf $TMPFN $DIR
if [ $? -eq 0 ] ; then
  echo scp $TMPFN $LOGIN_PATH/${myip}.${dt}.$fn.tgz

/usr/bin/expect <<EOF
set time 30
  spawn scp $TMPFN ${SSH_LOGIN_PATH}/${myip}.${dt}.$fn.tgz
  expect {
    "*yes/no" { send "yes\r"; exp_continue}
    "*password:" {send "${SSH_LOGIN_PWD}\r"}
  }
  expect eof
EOF
  
  rm -rf $TMPFN
  
else
   echo file not exists
fi

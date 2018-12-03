HOST=172.16.0.111
USER=developer
PASS=smart123
ls > FILES

ftp -inv $HOST << EOF
user $USER $PASS
cd /ftp/test
put $FILES 

bye

EOF

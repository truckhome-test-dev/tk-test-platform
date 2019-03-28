
sed -i "s/127.0.0.1/192.168.2.92/g" `grep 127.0.0.1 -rl ./`

sed -i "s/debug=True,host=/host=/g" `grep debug=True,host= -rl ./`


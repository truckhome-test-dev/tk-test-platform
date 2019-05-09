git fetch --all && git reset --hard origin/master && git pull

sed -i "s/127.0.0.1/192.168.2.92/g" `grep 127.0.0.1 -rl ./`
sed -i "s/5001/5000/g" `grep 5001 -rl ./`
sed -i "s/192.168.2.92:5001/192.168.2.92:5000/g" `grep 192.168.2.92:5001 -rl ./`
sed -i "s/debug=True,host=/host=/g" `grep debug=True,host= -rl ./`
sed -i "s?/home/jinyue/test?/home/tk-test-platform?g" `grep '/home/jinyue/test' -rl ./`

chmod +x shell.sh

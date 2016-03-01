## Set up

### Start Hub on boot

Copy `/hub/ardyh_hubd` to `/etc/init.d`


    sudo cp hub/ardyh_hubd /etc/init.d/.
    sudo update-rc.d ardyh_hubd defaults


To remove this or disable this

    sudo update-rc.d -f ardyh_clientd remove


You may need to do a `chmod 775` to make these executable. You can then start and stop the deamon with 

`sudo /etc/init.d/ardyh_hub start`
`sudo /etc/init.d/ardyh_hub stop`


Once the deamon starts it ties up the port. You can see what ports are currently being used with

```
sudo netstat -lptu
sudo netstat -tulpn
```


To view the current running ardyh_hubd use 
```
ps aux | grep ardyh_hubd
```

To view all threads where <PID> is gotten from the above command.
```
ps -e -T | grep <PID>
```
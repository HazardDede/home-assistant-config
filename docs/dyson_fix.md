```bash
pi@stack02:~/home-assistant-config $ docker exec -it hass bash
bash-5.0# cd /usr/local/lib/python3.8/site-packages/libpurecool/
bash-5.0# rm dyson.py
bash-5.0# curl -O https://raw.githubusercontent.com/bfayers/libpurecool/auth_customdeps/libpurecool/dyson.py
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4638  100  4638    0     0   5337      0 --:--:-- --:--:-- --:--:--  5337
bash-5.0# exit
```
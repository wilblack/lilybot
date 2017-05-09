## Sat. May 6, 2017

rpi4 is on ip 192.168.0.117, going to do  a router reboot.

The hub is running on rpi6. It needs ssh keys

I have rpi2 reporting on new client  
```
{"channel1": 477, "channel0": 843, "temp": 16.0, "lux": 4, "timestamp": "2017-05-06T15:47:56Z", "gain_m": 16, "timing_ms": 402, "humidity": 51.9}

```


I have rpi1 reporting on old client 
```
{"light": 334, "timestamp": "2017-05-06T15:47:59Z", "temp": 19.9, "humidity": 55.8}

```

    
    | rpi   | verison  | role      | status              |
    |-------|----------|-----------|---------------------|
    | rpi1  | A        |  grovebot | down, running old version |
    | rpi2  | A        |  grovebot | running new client  |
    | rpi3  | A        |           | unknown             |
    | rpi4  | A        |           | can't connect       |
    | rpi5  | A        |           | unknown             |
    | rpi6  | A        | hub       | running             |
    | rpi7  | A        |           | unknown             |



## May 5, 2017.
I want to build a Kubi clone. Mini me. 

So I need to pan 300 degrees and tilt +- 40 degrees

I need to set the hub up on Digital Ocean. The repo is not even their.




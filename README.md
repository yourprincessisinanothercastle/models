# worldmap generator

generate a worldmap which lives in in ram while the worldmap process is running.

has also some image output which should be nice if you are human.



## howto (tl;dr)


```
    > python world_test.py --help
    usage: world_test.py [-h] [--savetiles] name seed x y
    
    positional arguments:
      name
      seed
      x
      y
    
    optional arguments:
      -h, --help   show this help message and exit
      --savetiles
```


generating a world means creating a height- and a temperaturemap.
out of this we create a biome map (see constants.py for modifying)


![biomes](samples/test_0_0.pgm)
![height](samples/test_height_0_0.pgm)
![temperature](samples/test_temp_0_0.pgm)


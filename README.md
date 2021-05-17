# morfeusz2-polem-generator

```
gzip -dk resources/sgjp-20141120.tab.gz
```

```
python2 morfeusz2_unfolded/dict_unfold.py resources/sgjp-20141120
```

```
tar -xzf resources/morfeusz-src-20141120.tar.gz
```

```
cp morfeusz2_unfolded/trunk/CMakeLists.txt trunk
cp morfeusz2_unfolded/trunk/input/segmenty.dat trunk/input
```

```
mkdir bin
cd bin

cmake -D INPUT_DICTIONARIES=../../resources/sgjp-20141120.new.tab \
-D DEFAULT_DICT_NAME=unfolded -D INPUT_TAGSET=../../resources/sgjp-20141120.new.tagset ../trunk


make

make install
```


Requirements:

* swig
* libcppunit-dev

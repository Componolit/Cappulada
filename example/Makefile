all: add

number.o: number.cc number.h
	g++ -c -I. number.cc

add: number.o example.ads add.adb
	gnatmake add.adb -largs number.o

clean:
	rm -rvf number.o add.ali add.o example.ali example.o add

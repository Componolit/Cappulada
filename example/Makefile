all: add

number.o:
	g++ -c -I. number.cc

add: number.o example.ads example-number.ads
	gnatmake add.adb -largs number.o

clean:
	rm -rvf number.o add.ali add.o example.ali example.o example-number.ali example-number.o add

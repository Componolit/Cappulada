all: add

number.o: number.h
	g++ -c -I. number.cc

add: number.o example.ads example-number_t_int.ads
	gnatmake add.adb -largs number.o

clean:
	rm -rvf number.o add.ali add.o example.ali example.o example-number_t_int.ali example-number_t_int.o add

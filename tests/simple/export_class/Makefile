
all: add

number.o: number.ads number.adb
	gnatmake -c number.adb

main.o: main.cc number.h
	$(CC) -c main.cc -I.

add: main.o number.o
	$(CC) -o add main.o number.o -lgnat

clean:
	$(RM) main.o number.o number.ali add

CC=gcc
CFLAGS=-O3 -funroll-loops -c -Wall
LDFLAGS=-lm

SOURCES=$(wildcard *.c)
OBJECTS=$(notdir $(SOURCES:.c=.o))

EXECUTABLE=MyBot

#Comment/Uncomment the following to enable debugging
ifdef LOGFILENAME
CFLAGS+=-g -DDEBUG -DLOGFILENAME=\"$(LOGFILENAME)\"
else
CFLAGS+=-g -DDEBUG
endif

all: clean $(OBJECTS) $(MAINOBJECTS) $(EXECUTABLE) $(ALLEXECUTABLES)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

%.o: %.cpp
	$(CC) $(CFLAGS) $(LDFLAGS) -c -o $@ $^

clean: 
	-rm -f *.o $(EXECUTABLE) *.d debug.txt

.PHONY: all clean


####################################################################################
# Name: Makefile
# Description: A makefile I found online mixed with
#			   info from Kostas and stuff I remember.
#
#Author					Date		Version
#-------------------	--------	-------
#Bob Myers(FSU Prof)	Unknown		0.1: Base code
#Kostas Alexis			Unknown		0.2: Adds Variables for multi-use
#Hugo Mazariego			09/08/21	1.0: Merged file to make database project
#####################################################################################
CC = g++
CFLAGS = -std=c++11 -Wall
PROG = hugojrh_pa1	#Program name
DEPS = Database.h #Header files
OBJ = Database.o hugojrh_pa1.o #Object files (The implementation and main files)

%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

&(PROG): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm *.o $(PROG)
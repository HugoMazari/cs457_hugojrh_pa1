/*-----------------------------------------------------------
Name: Table.h
Summary: Declaration file for Table class.
Notes:

     Name         Date      Version
--------------  --------    -------
Hugo Mazariego  09/08/21    1.0: Made File
-----------------------------------------------------------*/
#ifndef TABLE_H
#define TABLE_H
#include <iostream>
#include <string>
#include <list>
using namespace std;

class Table
{
    private:
        const string extension = ".htb";
        string name;
        list<string> attributes;

    public:
        Table();
        Table(string);
        Table(string, list<string>);
        ~Table();

};

#endif // TABLE_H
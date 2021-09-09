/*-----------------------------------------------------------
Name: Database.h
Summary: Declaration file for Database class.
Notes:

     Name         Date      Version
--------------  --------    -------
Hugo Mazariego  09/08/21    1.0: Made File
-----------------------------------------------------------*/
#ifndef DATABASE_H
#define DATABASE_H
#include "Table.h"

class Database
{
    private:
        const string extension = ".hdb";
        string name;
        list<Table> tables;

    public: 
    Database();
    Database(string);
    ~Database();
};

#endif //DATABASE_H
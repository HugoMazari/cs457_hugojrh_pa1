# Name: Types.py
# Description: Types enum for future manipulation
#Author: Hugo
from enum import Enum
class Type(Enum):
    CHAR = "Char({amount})"
    VARCHAR = "Char({amount})"
    TEXT = "Text"
    INT = "^[\d]*$"
    BIGINT = "^[\d]*$"
    SMALLINT = "^[\d]*$"
    FLOAT = "^[\d]*\.[\d]*$"
    MONEY = 1
    DATETIME = 2

class Keywords:
    Keyword = ["create", "drop", "use", \
        "database", "table", "alter", \
            "add", "select", "from", \
                "insert", "into", "values", \
                    "update", "set", "where", "delete", \
                        "char", "varchar", "text", "int", \
                            "bigint", "smallint", "float", \
                                "money", "datetime", "left outer join", "inner join", \
                                    "on"]
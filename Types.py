# Name: Types.py
# Description: Types enum for future manipulation
#Author: Hugo
from enum import Enum
class Type(Enum):
    CHAR = "Char(20)"
    VARCHAR = "Char(50)"
    TEXT = "Text"
    INT = 5
    BIGINT = 10
    SMALLINT = 15
    FLOAT = 20
    MONEY = 1
    DATETIME = 2
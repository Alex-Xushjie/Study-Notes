# String formatting
There are many methods to format the string in Python.\
The best way is to use .format method.\
Example:\
`str = 'There are {} {} students'.format (2, "smart")`\
`str = 'There are {0} {1} students'.format (2, "smart")`\
`str = 'There are {qty} {adj} students'.format (qty=2,adj="smart")`

There are three placeholders in above example:
1) If there is nothing inside the { }, it means that items are filled in sequence. That is, the parameters following the format function will be inserted into the preceding { } in order.
2) When numbers are added inside the { }, they indicate the corresponding positions (0th position, 1st position, etc.). The parameters following the format function are assigned as the 0, 1, 2... positions sequentially.
* Although the positions marked by {number} can be in any order, the order of the parameters in the format function remains unchanged.
3) When strings are added inside the { }, these strings act as names for those positions. Values can then be assigned to these named positions through the format function, and both the positions and format arguments can be freely arranged.
## Formatting types
:<		Left aligns the result (within the available space)
:>		Right aligns the result (within the available space)
:^		Center aligns the result (within the available space)
:=		Places the sign to the left most position
:+		Use a plus sign to indicate if the result is positive or negative
:-		Use a minus sign for negative values only
: 		Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers)
:,		Use a comma as a thousand separator
:_		Use a underscore as a thousand separator
:b		Binary format
:c		Converts the value into the corresponding unicode character
:d		Decimal format
:e		Scientific format, with a lower case e
:E		Scientific format, with an upper case E
:f		Fix point number format
:F		Fix point number format, in uppercase format (show inf and nan as INF and NAN)
:g		General format
:G		General format (using a upper case E for scientific notations)
:o		Octal format
:x		Hex format, lower case
:X		Hex format, upper case
:n		Number format
:%		Percentage format


# 正则表达式
正则表达式是通过一些特殊的字符，在一段文字中匹配特定的字符。
在编程中，正则表达式是比较复杂的内容，但是对于网络运维而言，需要用到的正则表达式还算比较简单。因为大多数的网络设备都是使用标准的ASCI码，所以不需要去考虑特殊或复杂字符的情况。
在网络运维中，网络设备存在很多回显的内容，我们需要使用正则表达式去提取回显内容中的关键词，整理成新的内容进一步分析处理。

Example：
`import re   //导入re模块，内置模块，不需要安装`
`re.match(r'正则表达式内容', '需要匹配的字符串内容')   //r表示原始字符串(raw)抑制转义`
需要匹配的字符串内容可以填变量名：
`import re`
`str = '需要匹配的字符串内容'`
`re.match(r'正则表达式', str)`

## Metacharacters
[]	    A set of characters	                                                            "[a-m]"	
\	    Signals a special sequence (can also be used to escape special characters)	    "\d"	
.	    Any character (except newline character)	                                    "he..o"	
^	    Starts with	                                                                    "^hello"	
$	    Ends with	                                                                    "planet$"	
*	    Zero or more occurrences	                                                    "he.*o"	
+	    One or more occurrences	                                                        "he.+o"	
?	    Zero or one occurrences	                                                        "he.?o"	
{}	    Exactly the specified number of occurrences	                                    "he.{2}o"	
|	    Either or	                                                                    "falls|stays"	
()	    Capture and group

## Special Sequences
\A	    Returns a match if the specified characters are at the beginning of the string	              	
\b	    Returns a match where the specified characters are at the beginning or at the end of a word
        (the "r" in the beginning is making sure that the string is being treated as a "raw string")	   
\B	    Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word
        (the "r" in the beginning is making sure that the string is being treated as a "raw string")	   
\d	    Returns a match where the string contains digits (numbers from 0-9)	                         	
\D	    Returns a match where the string DOES NOT contain digits
\s	    Returns a match where the string contains a white space character
\S	    Returns a match where the string DOES NOT contain a white space character
\w	    Returns a match where the string contains any word characters 
        (characters from a to Z, digits from 0-9, and the underscore _ character)	
\W	    Returns a match where the string DOES NOT contain any word characters	
\Z	    Returns a match if the specified characters are at the end of the string	

## Sets
[arn]	    Returns a match where one of the specified characters (a, r, or n) is present	
[a-n]	    Returns a match for any lower case character, alphabetically between a and n	
[^arn]	    Returns a match for any character EXCEPT a, r, and n	
[0123]	    Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
[0-9]	    Returns a match for any digit between 0 and 9	
[0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
[a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
[+]	        In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string










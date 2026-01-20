# String formatting
There are many methods to format the string in Python.\
The best way is to use .format method.\
## Example:
`str = 'There are {} {} students'.format (2, "smart")`\
`str = 'There are {0} {1} students'.format (2, "smart")`\
`str = 'There are {qty} {adj} students'.format (qty=2,adj="smart")`

There are three placeholders in above example:
1) If there is nothing inside the { }, it means that items are filled in sequence. That is, the parameters following the format function will be inserted into the preceding { } in order.
2) When numbers are added inside the { }, they indicate the corresponding positions (0th position, 1st position, etc.). The parameters following the format function are assigned as the 0, 1, 2... positions sequentially.
* Although the positions marked by {number} can be in any order, the order of the parameters in the format function remains unchanged.
3) When strings are added inside the { }, these strings act as names for those positions. Values can then be assigned to these named positions through the format function, and both the positions and format arguments can be freely arranged.

## Formatting types
</pre>
:<     Left aligns the result (within the available space)
:>     Right aligns the result (within the available space)
:^     Center aligns the result (within the available space)
:=     Places the sign to the left most position
:+     Use a plus sign to indicate if the result is positive or negative
:-     Use a minus sign for negative values only
:      Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers)
:,     Use a comma as a thousand separator
:_     Use a underscore as a thousand separator
:b     Binary format
:c     Converts the value into the corresponding unicode character
:d     Decimal format
:e     Scientific format, with a lower case e
:E     Scientific format, with an upper case E
:f     Fix point number format
:F     Fix point number format, in uppercase format (show inf and nan as INF and NAN)
:g     General format
:G     General format (using a upper case E for scientific notations)
:o     Octal format
:x     Hex format, lower case
:X     Hex format, upper case
:n     Number format
:%     Percentage format
</pre>

# 正则表达式
正则表达式是通过一些特殊的字符，在一段文字中匹配特定的字符。\
在编程中，正则表达式是比较复杂的内容，但是对于网络运维而言，需要用到的正则表达式还算比较简单。因为大多数的网络设备都是使用标准的ASCI码，所以不需要去考虑特殊或复杂字符的情况。\
在网络运维中，网络设备存在很多回显的内容，我们需要使用正则表达式去提取回显内容中的关键词，整理成新的内容进一步分析处理。

## Example：
`import re`   //导入re模块，内置模块，不需要安装\
`re.match(r'正则表达式内容', '需要匹配的字符串内容')`   //r表示原始字符串(raw)抑制转义\
需要匹配的字符串内容可以填变量名：\
`import re`\
`str = '需要匹配的字符串内容'`\
`re.match(r'正则表达式', str)`

## Metacharacters
<pre>
[]     A set of characters	                                                           
\      Signals a special sequence (can also be used to escape special characters)	      
.      Any character (except newline character)	                                   	
^      Starts with	                                                                     	
$      Ends with	                                                                  	
*      Zero or more occurrences	                                                  	    
+      One or more occurrences	                                                       
?      Zero or one occurrences	                                                        
{}     Exactly the specified number of occurrences	                                     
|      Either or	                                                                 	
()     Capture and group
</pre>
        
## Special Sequences
<pre>
\A     Returns a match if the specified characters are at the beginning of the string	              
\b     Returns a match where the specified characters are at the beginning or at the end of a word
        (the "r" in the beginning is making sure that the string is being treated as a "raw string")	   
\B     Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word
        (the "r" in the beginning is making sure that the string is being treated as a "raw string")	   
\d     Returns a match where the string contains digits (numbers from 0-9)	                         	
\D     Returns a match where the string DOES NOT contain digits
\s     Returns a match where the string contains a white space character
\S     Returns a match where the string DOES NOT contain a white space character
\w     Returns a match where the string contains any word characters 
        (characters from a to Z, digits from 0-9, and the underscore _ character)	
\W     Returns a match where the string DOES NOT contain any word characters	
\Z     Returns a match if the specified characters are at the end of the string	
</pre>

## Sets
<pre>
[arn]              Returns a match where one of the specified characters (a, r, or n) is present	
[a-n]              Returns a match for any lower case character, alphabetically between a and n	
[^arn]             Returns a match for any character EXCEPT a, r, and n	
[0123]             Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
[0-9]              Returns a match for any digit between 0 and 9	
[0-5][0-9]         Returns a match for any two-digit numbers from 00 and 59	
[a-zA-Z]           Returns a match for any character alphabetically between a and z, lower case OR upper case	
[+]                In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string
</pre>

# 列表
列表的主要属性：
1) 任意对象的有序集合。 //意思就是列表里面的元素可以是任意的python对象
2) 通过偏移读取。   //偏移就是指列表的位置，0号位、1号位等等，通过偏移提取列表中的数据（元素）
3) 可变长度，异构以及任意嵌套。 （长度不是固定；异构指列表中可以存放任何元素；任意嵌套指列表里面嵌套列表、元组等都可以）
4) 属于可变序列的分类
5) 对象引用数组   //列表中的某个位置存储的并不是真实的数据内容，而是一个指向内存某个位置的指针，通过该指针引用存放在内存该位置中的具体的数据内容

## Example：
`L = []` //一个空列表\
`L = [123, 'router', 1.23, {}, ['switch', 'list_2', 1.23]]`  //支持任意类型（异构）、嵌套\
`L = list('spam')`  //可迭代对象转换为列表\
`L[i]`   //支持索引\
`L[i][j]`  //索引嵌套\
`L[i:j]`  //切片\
`len(L)`  //计算长度\
`L1 + L2`   //支持连接，重复\
`L1 * 7`    //支持运算

## 方法
append()    //在列表的队尾添加**一个元素**\
`L1 = [1, 2, 3, 4]`\
`L2 = [11, 22, 33, 44]`\
`L1.append(L2)`     //将L2作为一整个元素添加进L1的队尾，会直接修改原列表内容\
`>>>print(L1)`    //查看原列表L1\
`[1, 2, 3, 4, [11, 22, 33, 44]]`\
*注意，L1.append()这个操作没有返回结果，如果使用L1 = L1.append(5)这种语句的话，会使得L1变成None，因为这条语句是将一个空（没有返回结果）赋值给L1。

extend()   //对原列表进行扩展
`L1 = [1, 2, 3, 4]`\
`L2 = [11, 22, 33, 44]`\
`L1.append(L2)`     //在列表的队尾增加数字5，会直接修改原列表内容\
`>>>print(L1)`    //查看原列表L1\
`[1, 2, 3, 4, 11, 22, 33, 44]`\
*该方法同样没有返回值，或理解为返回值为空

insert()   //在列表的某一个位置插入一个元素\
`L2 = [1, 2, 3, 4]`\
`L2.insert(1, 'router')`     //在列表的1号位插入一个字符串‘router’，会直接修改原列表内容\
`>>>print(L2)`    //查看原列表L2\
`[1, 'router', 2, 3, 4]`\
*该方法同样没有返回值，或理解为返回值为空

pop()    //将列表最后一个元素弹出，作为返回结果，会改变原列表\
`L1 = [1, 2, 3, 4]`\
`pop_result = L1.pop()`     //在列表的队尾增加数字5，会直接修改原列表内容\
`>>>print(L1)`    //查看原列表L1\
`[1, 2, 3]`\
`>>>print(pop_result)`    //查看返回结果\
`4`

sort()       //对列表进行排序，从小到大
reverse()    //对列表进行反向排序，从大到小
*这两个方法都是对列表进行排序，但是会改变原始列表，不推荐。推荐使用内置函数sorted()--正向排序  sorted(L1, reverse = True)--反向排序

copy()      //复制列表，浅层复制

import copy
copy.deepcopy  //复制列表，深层复制
*在python中，列表只是一个指向内存的指针，如果只是简单的L2 = L1，不能达到复制L1的效果，没有意义
*如果想复制列表，需要使用copy方式，但是该方法是浅层复制，意思是如果列表存在嵌套的话，嵌套的列表依旧是一个指针，无法复制
*使用copy.deepcopy函数的话，无论列表嵌套多少层，都是完全复制。
`L1 = [1, 2, 3, [11, 22, 33]]`\
`L2 = L1`     //引用，不能达到复制的效果
`L3 = L1.copy()`   //浅层复制
`import copy`
`L4 = copy.deepcopy(L1)`   //深层复制
`L1[3].append(44)`       //在L1嵌套的列表中添加一个元素44
`print(L1)`
`[1, 2, 3, [11, 22, 33, 44]]`
`print(L2)`
`[1, 2, 3, [11, 22, 33, 44]]`
`print(L3)`
`[1, 2, 3, [11, 22, 33, 44]]`   //浅层复制依旧会被改变
`print(L4)`
`[1, 2, 3, [11, 22, 33]]`      //深层复制就不会改变



# 字典
字典是python对象的一种，是一种可变的对象。
主要属性：
1) 通过键而不是偏移量来读取数据
2) 任意对象的无序集合（python 3.6之后是有顺序的，通过循环语句可以看出来）
3) 可变长，异构，任意嵌套（字典中的“值”可以是任意对象，“键”只能是不可变对象）
4) 属于可变映射类型
5) 对象引用表(散列表)


# 元组
主要属性：
1) 任意对象的有序集合
2) 通过偏移读取数据
3) 属于不可变序列类型
4) 固定长度，异构，任何嵌套
5) 对象引用的数组



# 文件


# 语句
程序由模块组成
模块包含语句
语句包含表达式
表达式建立并处理对象

## 赋值语句
赋值语句建立对象引用
变量名在首次赋值时会被创建
变量名在引用前必须先赋值
隐式赋值（例如：导入模块，函数和类）


## 打印语句


## 条件语句


## 循环语句


# 函数
一个函数就是将一些语句集合在一起的部件，他们能够不止一次的在程序中运行。函数还能够计算出一个返回值，并能够改变作为函数输入的参数，而这些参数在代码运行时也许每次都不相同。
以函数的形式去编写一个操作可以使它成为一个能够广泛应用的工具，让我们在不同的情况下能够使用它。
1) 最大化的代码重用和最小化的代码冗余
2) 流程的分解
熟练的使用模块和函数，有利于优化代码。

## 函数格式
`def name(arg1, arg2, ... argN):`     //定义一个函数，name是函数名
`       ...`                          //执行一系列语句
`       return xxx`                   //停止并返回某个结果，作为函数的输出。
*我们通常使用return语句返回结果，而不是print语句去打印，print只是将函数运行的结果打印出来，而函数本身的输出仍然是None
*return是停止并返回，因此在此语句之后的语句将不会被执行

## 全局变量与函数本地变量
简单来说，在函数外定义的变量称为全局变量，函数内部定义的参数称为本地变量。本地变量如果与全局变量相同，函数优先查找使用本地变量。\
可以修改，新增全局变量，但是不建议这么做。

# 模块





# 类


# 内置模块


# 数据持久化


# 多进程多线程


# 异常处理









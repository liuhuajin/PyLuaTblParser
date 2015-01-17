from PyLuaTblParser import *

a1 = PyLuaTblParser()
a2 = PyLuaTblParser()
a3 = PyLuaTblParser()

test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
#a1.load(test_str)
#d1 = a1.dumpDict()

#a1.loadDict(d1)
#a2.dumpLuaTable("1.txt")
#a3.loadLuaTable("luaTable.txt")

#d3 = a3.dumpDict()

pyt = PyLuaTblParser()
test_str1 = r'{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
test_str2 = r"{1,nil,nil}"
test_str3 = r"{[1]=1, nil, nil}"
test_str4 = r"{nil, nil, [3]=3.14, nil, nil, key = 183}"
test_str5 = r"{a={a={'12\/3','1231'}}}"
test_str6 = r"{[1]=2}"
test_str7 = r"""
	{
		1,
		2,
		3,
		nil,
		nil,
	}
	"""
test_str8 = r"{[1]=nil}"
test_str9 = r"{[1]=1,3,4,5,7,nil,nil,nil,1,3,4,5}"
test_str10 = r"""
	{
		--a
		['1']--a
		= 1--a
		,
		a =3--a
		,
		nil --a
		,
		b = "fine"
		,
	}
	"""
test_str11 = r"{aa={nil,3,5,[4]=5}}"
test_str12 = r"{[1]=1,nil,nil,3}"
test_str13 = r"{1,3,4,5,7,nil,nil,nil,1,3,4,5}"
test_str14 = r"""{"abcd \uabed \u1234 \u1244",,} """
test_str15 = r"""
	{
	"a"--b
	--c
	,
	}
	"""
test_str16 = """
	{,,,,}
	"""
test_str17 = r"""
		{
	--b
	--c
	,
	--d
	   1--a   
	   --e
	  --f
	   ,
	   x--h
	   =2
	}
	"""
test_str18 = r"""
{
	[1] = -1e10,
	[2] = -12,
	nil,--dumpLuaTable
	--array
	--a2
	--c
}
"""
test_str19 = """{[1]="value", [2]=nil, [3]="value"}"""
test_str20 = """{1,2,3,nil,4}"""
test_str21 = r"""{
		3,  
		2,
		while_pass--a
		=1
       	}"""
test_str22 = "{}"
test_str23 = "{['1'] = nil, 'hello', 123, nil, [':['] = nil, 'world'}"
test_str24 = r"""{[1]="i am \n
ok"}
"""
test_str25 = "{true1=1}"
test_str26 = r"""{["\"s\""]=2}"""
test_str27 = r"""{[1]={[2]={a="3",b="4",c='\"s\"'}}}"""
test_str28 = r"""{a={b="\uabcd\n\r\t'"}}"""
test_str29 = r"""{a='\"c'}"""
test_str30 = r"""{['/\\"\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?'] = "test"}"""
test_str31 = r"""{1,2 --df
,"dfdf"}"""
test_str32 = "{nil,nil,nil}"
test_str33 = "{a={a={'12\/3','1231'}}}"
test_str34 = r"""{["1"]=nil,"hello",123,nil,"world"}"""
test_str35 = "{'c',[1]=2}"
test_str36 = r"""{["array with nil"] = {nil,nil,[3] = 3.14,nil,nil,key = 183}}"""
test_str37 = "{1,2,nil,4}"
test_str38 = "{[1]=1,nil,a=3}"
pyt.load(test_str38)
#pyt.loadDict(d)	
#pyt.loadDict(d2)
#print d2
res = pyt.dumpDict()
print res

#pyt.loadLuaTable("luaTable.txt")
#d = pyt.dumpDict()
#print d
pyt.dumpLuaTable("dumpLuaTable.txt")
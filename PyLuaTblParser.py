import string
class PyLuaTblParser(object):
	
	def __init__(self):
		pass

	def load(self, s):
		print s
		index = self.__ignore_space(s, 0)		
		if s[index] != '{':
			raise TypeError("input type is not table!")
		self.__var, index = self.__parser_table(s, index+1)

	def dump(self):
		lua_str = self.__dump_var(self.__var)
		return lua_str

	def loadLuaTable(self, f):
		f = open(f, 'r')
		text = f.read()
		print text
		self.load(text)
		f.close()

	def dumpLuaTable(self, f):
		f = open(f, 'w')
		lua_str = self.__dump_var(self.__var)
		f.write(lua_str)
		f.close()

	def loadDict(self, d):
		self.__var = {}
		for key in d:
			if isinstance(key, long) or isinstance(key, int) or isinstance(key, basestring) and d[key] != None:
				self.__var[key] = d[key]
		
	def dumpDict(self):
		d = {}
		if isinstance(self.__var, list):
			l = []
			for v in self.__var:
				l.append(v)
			return l
		for key in self.__var :
			if isinstance(key, float):
				key = int(key)
			d[key] = self.__var[key]
		return d

	def __translate(self, s):		
		s=s.replace("\\", "\\\\")
		s=s.replace("'", "\\'")
		s=s.replace('"', '\\"')
		s=s.replace("\b", "\\b")
		s=s.replace("\f", "\\f")
		s=s.replace("\n", "\\n")
		s=s.replace("\r", "\\r")
		s=s.replace("\t", "\\t")
		return s
	def __dump_var(self, var):
		result_str = ""
		if isinstance(var, list):
			for value in var :
				if isinstance(value, list) or isinstance(value, dict) :
					result_str = result_str + self.__dump_var(value) + ","
				elif isinstance(value, basestring):
					result_str = self.__translate(result_str)
					result_str = result_str + "'" + value + "',"
				elif isinstance(value, bool) and value == True :
					result_str = result_str + "true,"
				elif isinstance(value, bool) and value == False:
					result_str = result_str + "false,"
				elif value == None :
					result_str = result_str + "nil,"
				else:
					result_str = result_str + str(value) + ','
			result_str = '{' + result_str + '}'
		else:
			for key in var:
				value = var[key]
				if isinstance(key, float) or isinstance(key, int) or isinstance(key, long):
					result_str = result_str + '[' + str(key) + ']='
				else:
					key_str = key
					key_str = self.__translate(key_str)
					result_str = result_str + '["' + key_str + '"]='
				if isinstance(value, list) or isinstance(value, dict) :
					result_str = result_str + self.__dump_var(value) + ","
				elif isinstance(value, basestring):
					value = self.__translate(value)
					result_str = result_str + "'" + value + "',"
				elif isinstance(value, bool) and value == True :
					result_str = result_str + "true,"
				elif isinstance(value, bool) and value == False:
					result_str = result_str + "false,"
				elif value == None :
					result_str = result_str + "nil,"
				else:
					result_str = result_str + str(value) + ','
			result_str = '{' + result_str + '}'
		return result_str

	def __parser_table(self, s, index):
		index = self.__ignore_space(s, index)
		number_str = "0123456789+-.eE"
		number_begin = "+-.0123456789"
		key_index = 0
		key_flag = False
		d = {}
		l =[]
		while True :
			key = None
			index = self.__ignore_space(s, index)
			if '}' == s[index]:
				index = index+1
				break
			elif '[' == s[index]:
				key, index = self.__parser_key(s, index+1)
				index = self.__ignore_space(s, index)
				#have key
				key_flag = True
				if ']' != s[index]:
					raise TypeError("input [ ] not match")
				else:
					index = index + 1
				index = self.__ignore_space(s, index)
				if '=' != s[index]:
					raise TypeError("input = not match []")
				else:
					index = index + 1
					index = self.__ignore_space(s, index)
					value, index = self.__parser_value(s, index)

			elif ',' == s[index] or ';' == s[index]:
				index = self.__ignore_space(s, index+1)
				continue
			else :
				index = self.__ignore_space(s, index)
				if '{' == s[index] :
					# table
					value, index = self.__parser_table(s, index+1)
				elif '"' == s[index] or "'" == s[index] :
					# string
					value, index = self.__parser_string(s, index)
				elif number_begin.find(s[index]) != -1 :
					# number
					value, index = self.__parser_number(s, index)
				else :
					result_str, flag, index = self.__pre_parser(s, index)
					if True == flag :
						if "true" == result_str:
							value = True
						if "false" == result_str:
							value = False
						if "nil" == result_str:
							value = None
					else:
						key = result_str
						index = self.__ignore_space(s, index)
						#have key
						key_flag = True
						while index < len(s) and s[index] != '=':
							index = index + 1
						if index == len(s):
							raise BaseException()
						if '=' != s[index] :
							raise BaseException()
						index = index+1
						index = self.__ignore_space(s, index)
						value, index = self.__parser_value(s, index)
			if None == key :
				key = key_index+1
				d[key] = value
				key_index = key_index + 1
			else :
				if isinstance(key, int):
					if key > key_index:
						d[key] = value
				else:
					d[key] = value
		if any(d) == False:
			return d, index
		elif False == key_flag:
			#have no key
			for key in d :
				l.append(d[key])
			return l, index
		else:
			#del None value
			r = {}
			for key in d :
				if None != d[key]:
					r[key] = d[key]
			return r, index

	def __parser_value(self, s, index):
		number_str = "0123456789+-."
		if '{' == s[index]:
			# table
			value, index = self.__parser_table(s, index+1)
		elif '"' == s[index] or "'" == s[index] :
			# '' "" string
			value, index = self.__parser_string(s, index)
		elif number_str.find(s[index]) != -1 :
			#number
			value, index = self.__parser_number(s, index)
		else :
			# nil  true false
			value, index = self.__parser_content(s, index)
		return value, index

	def __pre_parser(self, s, index):
		start = index
		end = start
		#while  s[end] not in ' \n\r\t=,}-' :
		while s[end] in '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
			end = end + 1
		result_str = s[start:end]
		if "true" == result_str or "false" == result_str or "nil" == result_str:
			# value
			return result_str, True, end
		else:
			#key
			return result_str, False, end

	def __parser_content(self, s, index):
		
		result_str = s[index:index+3]
		if result_str == 'nil' :
			return None, index+3
		result_str = s[index:index+4]
		if result_str == 'true' :
			return True, index+4
		result_str = s[index:index+5]
		if result_str == 'false' :
			return False, index+5
		else :
			if s[index] in "={\"\';":
				raise BaseException()
			raise TypeError("content is not nil true false")

	def __parser_key(self, s, index):
		#[]
		index = self.__ignore_space(s, index)
		number_str = "0123456789+-.eE"
		if '"' == s[index] or "'" == s[index]:
			#string
			result, index = self.__parser_string(s, index)
			return result, index
		else:
			#number
			result, index = self.__parser_number(s, index)
			return result, index

	def __parser_string(self, s, index):
		begin = s[index]
		end_pos = index+1
		ignore_flag = False
		end_flag = False
		while True:			
			if True == end_flag :
				break
			if True == ignore_flag :
				ignore_flag = False
			else:
				if "\\" == s[end_pos] :
					ignore_flag = True
				else :
					end_flag = (begin == s[end_pos])
			end_pos = end_pos + 1
		result_str = s[index+1:end_pos-1]

		result_str = result_str.replace("\\/", '/')
		result_str = result_str.replace('\\"', '"')
		result_str = result_str.replace("\\'", "'")
		result_str = result_str.replace('\\n', '\n')
		result_str = result_str.replace('\\a', '\a')
		result_str = result_str.replace('\\v', '\v')
		result_str = result_str.replace('\\t', '\t')
		result_str = result_str.replace('\\r', '\r')
		result_str = result_str.replace('\\b', '\b')
		result_str = result_str.replace('\\f', '\f')
		result_str = result_str.replace('\\\\', '\\')
		result_str = result_str.replace('\\u', 'u')
		result_str = result_str.replace('\\x', 'x')

		return (result_str, end_pos)

	def __parser_number(self, s, index):
		index = self.__ignore_space(s, index)
		number_str = "0123456789+-.eE"
		start = index
		str_len = len(s)
		while index < str_len and number_str.find(s[index]) != -1 :
			if s[index] == '-' and s[index+1] == '-':
				break
			index = index + 1
		result = s[start:index]
		number = float(result)
		if float(int(number)) == number:
			number = int(number)
		return (number, index)

	def __ignore_space(self, s, index):
		str_len = len(s)
		ignore_str = " \n\t\r"

		while True:
			orgin = index
			while ignore_str.find(s[index]) != -1 and index < str_len :
				index += 1
			if index+1 < str_len and '-' == s[index] and '-' == s[index+1]:
				index = index+2
				# ????????????  \n   \r      ????
				while '\n' != s[index] and '\r' != s[index] and index < str_len:
					index = index+1
			if orgin == index:
				break
		return index

def main():
	pass
if __name__ == "__main__":
	main()
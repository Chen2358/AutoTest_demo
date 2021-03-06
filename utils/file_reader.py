# -*-* coding: utf-8 -*-

import os
import yaml
from xlrd import open_workbook


#读取yaml文件
class YamlReader(object):

	def __init__(self, yamlf):
		if os.path.exists(yamlf):
			self.yamlf = yamlf
		else:
			raise FileNotFoundError('文件不存在！')
		self._data = None

	@property
	def data(self):
		#如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
		if not self._data:
			with open(self.yamlf, 'rb') as f:
				self._data = list(yaml.safe_load_all(f))	#load返回generator，yonglist组织列表
		return self._data


class ExcelReader(object):

	#读取Excel文件
	def __init__(self, excel, sheet=0, title_line=True):
		if os.path.exists(excel):
			self.excel = excel
		else:
			raise FileNotFoundError('文件不存在!')
		self.sheet = sheet
		self.title_line = title_line
		self._data = list()

	@property
	def data(self):
		if not self._data:
			workbook = open_workbook(self.excel)
			if type(self.sheet) not in [int, str]:
				raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
			elif type(self.sheet) == int:
				s = workbook.sheet_by_index(self.sheet)
			else:
				s = workbook.sheet_by_name(self.sheet)

			if self.title_line:
				title = s.row_values(0)		#首行为title
				for col in range(1, s.nrows):
					#依次遍历剩余行，与首行组成dict，拼到self._data中
					self._data.append(dict(zip(title, s.row_values(col))))
			else:
				for col in range(0, s.nrows):	#遍历所有行
					self._data.append(s.row_values(col))
		return self._data

if __name__ == '__main__':
	y = 'E:\\Python37\\projects\\testvenv\\Test_framework\\config\\config.yml'
	yam_reader = YamlReader(y)
	print(yam_reader.data)

	e = 'E:\\Python37\\projects\\testvenv\\Test_framework\\data\\test.xlsx'
	exc_reader = ExcelReader(e, title_line=True)
	print(exc_reader.data)




















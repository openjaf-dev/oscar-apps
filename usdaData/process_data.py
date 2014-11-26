import urllib
import csv
from bs4 import BeautifulSoup
import time
from oscar.apps.dashboard.reports.csv_utils import CsvUnicodeReader

class ProcessData(object):
	
	
		
	def __init__ ( self,ext,base_url,types,repFrec,proxies=None, parent = None ):
		self.base_url = base_url
		self.ext = ext
		self.types = types
		self.repFrec = repFrec
		self.proxies = proxies
		day = int(time.strftime("%d"))-1
		self.repDate =  str(time.strftime("%m"))+"%2F"+str(day)+"%2F"+str(time.strftime("%Y"))
		self.endDate =  str(time.strftime("%m"))+"%2F"+str(time.strftime("%d"))+"%2F"+str(time.strftime("%Y"))
		self.filename = '../../pricing/Archives/USDA-Data{0}.csv'.format(str(time.strftime("%m-%d-%Y")))
		self.comm = self.getcommodity('apps/usdaData/file/commodities.csv')
		

	def getcommodity(self,file_path):
		comm = {}
		for row in CsvUnicodeReader(open(file_path, 'rb'),
                                    delimiter=',', quotechar='"',
                                    escapechar='\\'):
			comm[row[1]] = row[0] 
		return comm	
			
	def downloadData(self,full_url):
		#page = urllib.urlopen(full_url)
		page = urllib.urlopen(full_url,proxies=self.proxies)
		data = page.read()
		return data

	def getLocations(self,tp):
		locations= {}
		url_form = str('http://www.marketnews.usda.gov/portal/fv?paf_dm=full&dr=1&paf_gear_id=1200002&repType=wiz&type={0}&locChoose={1}&commodityclass=allcommodity&step2=true&run=Update').format(tp,self.locChoose)
		form_page = self.downloadData(url_form)
		soup = BeautifulSoup(form_page)
		name_select = "locAbr"
		if tp == "movement":
			name_select = "locAbrfrom"
		select = soup.find('select',{'name':name_select})
		option_tags = select.find_all('option')
		for option in option_tags:
			locations[option['value']] = option.text
		return locations

	def createFullUrl(self,tp,locAbr):
		repTypeChanger = tp+self.repFrec
		step2 = "true&type={0}&rowDisplayMax=25&startIndex=1&organic=&locAbr={1}&paf_gear_id=1200002&commodityclass=allcommodity&locAbrPass=ALL%7C%7C&locName=&locChoose={2}&dr=1&repDate={3}&endDate={4}".format(tp,locAbr,self.locChoose,self.repDate,self.endDate)
		step3 = "date=true&Run=Run&locAbrlength=1&environment=&blech=&Run.y=5&Run.x=26&lastCommodity=&previousVal=&lastLocation=&{0}=true".format(self.ext) 
		full_url = self.base_url+"&repType={0}&paf_dm=full&repTypeChanger={1}&{2}step2={3}&step3{4}".format(repTypeChanger,repTypeChanger,'',step2,step3)
		print full_url
		return full_url	
	
	def createCsvFile(self):
		fieldnames = ['marketType', 'commodityName', 'cityName', 'typeCommodity', 'package', 'variety', 'subVariaty', 'grade', 'date', 'lowPrice', 'highPrice', 'average', 'mostlyLow', 'mostlyHigh', 'origin', 'originDistrict', 'itemSize', 'marketTone']
		self.test_file = open(self.filename,'wb')
		self.csvwriter = csv.DictWriter(self.test_file, delimiter="@", fieldnames=fieldnames)
		self.csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
	
	def closeCsvFile(self):
		self.test_file.close()	
	
	def readXml(self,data,tp):
		soup = BeautifulSoup(data)
		items = soup.report.find_all("item")
		items_array = []
		for item in items:
			if str(item.commodityname.string) in self.comm:
				row={}				
				low_price = float(item.lowpricemin.string) if item.lowpricemin.string != None else 0
				high_price = float(item.highpricemax.string) if item.highpricemax.string != None else 0
				average = (low_price + high_price)/2
				row['marketType'] = tp
				row['commodityName'] = str(item.commodityname.string)
				row['cityName'] = str(item.cityname.string).replace(',','-')
				row['typeCommodity'] = ""#item.typeName.string
				row['package'] = str(item.packagedesc.string) if item.packagedesc.string != None else "{}"
				row['variety'] = str(item.varietyname.string) if item.varietyname.string != None else "{}"
				row['subVariaty'] = str(item.subvarname.string)
				row['grade'] = str(item.gradedesc.string) if item.gradedesc.string != None else "{}"
				row['date'] = item.date.string
				row['lowPrice'] = low_price
				row['highPrice'] = high_price
				row['average'] = average
				row['mostlyLow'] = item.mostlylowmin.string if item.mostlylowmin.string != None else "{}"
				row['mostlyHigh'] = item.mostlyhighmax.string if item.mostlyhighmax.string != None else "{}"
				row['origin'] = str(item.originname.string) if item.originname.string != None else "{}"
				row['originDistrict'] = str(item.districtname.string) if item.districtname.string != None else "{}"
				row['itemSize'] = item.itemsize.string  if item.itemsize.string != None else "{}"
				row['marketTone']= str(item.markettone.string) if item.markettone.string != None else "{}"
				items_array.append(row)
		return items_array
	
	def addDataCsvFile(self,data,tp):
		if self.ext == 'xml':
			data_dict = self.readXml(data,tp)
		elif self.ext == 'xls':
			data_dict = self.readXls()
		for row in data_dict:
			self.csvwriter.writerow(row)
		
	def process_retail(self):
		data_url = str('http://www.marketnews.usda.gov/gear/usda/report_xml.jsp?&repType=wiz&paf_dm=full&portal=fv&step2=true&region=ALL&type=Retail&organic=ALL&paf_gear_id=1200002&commodityclass=allcommodity&reportConfig=true&class=ALL&run=Run&locChoose=location&dr=1&repDate=11%2F21%2F2014&commodity=ALL&compareLy=No&endDate=11%2F21%2F2014&format={0}&rebuild=false&reportId=26').format(self.ext)
		data = self.downloadData(data_url)
		return data

	def main(self):
		self.createCsvFile()
		for tp in self.types:
			if tp =='retail':
				data = self.process_retail()
			else:
				if  tp == 'shipPrice':
					self.locChoose = 'locState'	
				else: 
					self.locChoose = 'location'	
				locations = self.getLocations(tp)		
				for locAbr,location in locations.items():
					f_url = self.createFullUrl(tp,locAbr)
					data = self.downloadData(f_url)
					self.addDataCsvFile(data,tp)
		self.closeCsvFile()
		return self.filename

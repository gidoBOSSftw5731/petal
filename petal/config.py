from ruamel import yaml
from .grasslands import Peacock
from random import randint
from datetime import datetime
log = Peacock()



class Config(object):
	def __init__(self):
		try:
			with open('config.yaml', 'r') as fp:
				self.doc = yaml.load(fp, Loader=yaml.RoundTripLoader)
		except IOError as e:
			log.err("Could not open config.yaml: " + str(e))
			exit()
		except Exception as e:
			log.err("An unexcpected exception of type: "
				+ type(e).__name__
				+ "has occurred: " + str(e))
			exit()
		else:
			if "token" in self.doc:
				self.token = self.doc["token"]
				self.useToken = not self.doc["selfbot"]
			else:
				log.err("Token missing in config.yaml")
				exit(404)
		# Defining constants below
		try:
			self.prefix = self.doc["prefix"]
			self.owner = self.doc["owner"]
			self.pm = self.doc["acceptPMs"]
			self.l1 = self.doc["level"]["l1"]
			self.l2 = self.doc["level"]["l2"]
			self.l3 = self.doc["level"]["l3"]
			self.l4 = self.doc["level"]["l4"]
			self.aliases = self.doc["aliases"]
			self.permitNSFW = self.doc["permitNSFW"]
			self.blacklist = self.doc["blacklist"]
			self.commands = self.doc["commands"]
			self.useLog = "logChannel" in self.doc
			if self.useLog:
				self.logChannel = self.get("logChannel")
				self.modChannel = self.get("modChannel")
			self.wordFilter = self.get("wordFilter") 
			self.tc = self.get("trackChannel")
			if self.tc is None:
				log.warn("trackChannel object not found in config.yaml. That functionality is disabled")
			
			self.lockLog = False
			#self.imageIndex = self.doc["imageIndex"]
			self.hugDonors = self.doc["hugDonors"]
			self.stats = self.doc["stats"]
		except KeyError as e:
			log.err("Missing config item: " + str(e))
			exit(404)
		return
	
	def flip(self):
		self.lockLog = not self.lockLog
		
	def get(self, field):
		if field is None:
			return "<poof>"
		else:
			try:
				return self.doc[field]
			except KeyError:
				log.err(field + " is not found in config")
		return None

	def save(self, vb=False):
		try:
			with open('config.yaml', 'w') as fp:
				yaml.dump(self.doc, fp, Dumper=yaml.RoundTripDumper)
		except PermissionError:
			log.err("No write access to config.yaml")
		except IOError as e:
			log.err("Could not open config.yaml: " + str(e))
		except Exception as e:
			log.err("An unexcpected exception of type: "
				+ type(e).__name__
				+ "has occurred: " + str(e))
		else:
			if vb:
				log.info("Save complete")
		return
	
	def getVoid(self):
		v = self.get("void")
		if len(v) == 0 : 
			return "The void is empty"
		else: 
			return v[randint(0, len(v) - 1)]["content"]
	
	def saveVoid(self, content, name, id):
		v = self.get("void")
		for e in v:
			if e["content"] == content:
				return None

		v.append({"content":content, "author":name + " " + id, "number":len(v),"time":str(datetime.utcnow())} )
		return len(v)
			
				
		
		

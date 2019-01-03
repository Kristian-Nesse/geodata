# -*- coding: utf-8 -*-
#
# ../ELE610/py3/hafrs.py
#
# Karl Skretting, UiS, 2018

"""
 bruk:
   # (py35) C:\..\py3> python -i startup.py
   >>> import hafrs
   >>> t = hafrs.test01()


********* Historikk 
Fram til juni 2018 er det her bare noe gammel (ikke effektiv) kode fra Sindre Aas Græe: singleFile10x10()
og to enkle funksjoner som jeg laget som et alternativ for hans løsning: readAscToList() og writeTo10x10()
og en testfunksjon for disse funksjoner: test01()
Disse funksjonene fra mars 2018 er enkle. 

********* Plan
Plan kan være å ha flere funksjoner for Funn i Hafrsfjord prosjektet og tilhørende data.
Kanskje kan jeg (vi?) prøve å lage klasser/funksjoner i henhold til kommentarer nedenfor.
Nye og bedre funksjoner bør bruke numpy og cv2 og Qt5 eller plt pakkene.
Kan det bli et prosjekt i ELE630 høsten 2018??

********* Kommentarer lagt til av Karl Juni 2018.
Dette er noen ideer for videre arbeid med Funn i Hafrsfjord (FiH) prosjektet, etter at Sindre
har jobbet med masteroppgaven sin og ikke fått så mye til. Kanskje trenst tydeliger føringer for 
hva som bør gjøres helt konkret. Noen slike ideer nevnes nedenfor.
1) Noen dybdedata er i filer nnn.asc der nnn er et tall, totalt er det ca 887 millioner punkt fordelt
   over 71 filer, 23 GB, filene er fra 0.5 MB til ganske store, kanskje opp til 0.5 GB. 
2) Oppgaver for disse filene, funksjoner som gjøres for filnavn
2a Dele store filer i flere filer, nnn-01.asc, ... Hensikten er å ha filene små nok til å kunne
   behandles i minne til datamaskinen på en grei måte. Inndeling kan greit gjøres der to etterfølgende
   punkt er langt, mer enn 100-200 m, fra hverandre. Dette kan gjøres etter behov, da slipper en
   å lagre 23 GB ekstra i databasen. 
2b Lese ei fil og fine inndeling i linjer, to etterfølgende punkt der avstanden er liten, mindre en 10-20 cm,
   hører til samme linje. Deretter kan linjer samles i sveip, to linjer som er (nesten) parallelle og med
   liten avstand kan antas å høre til samme sveip, kanskje må linjene også komme etter hverandre. 
   mellom linjer kan det være enkle punkt, eller korte løsrevne linjer. 
   Ei (stor) fil med alle data om sveip bør genereres, fil og punkt som er med, grenser og hjørnepunkt,
2c To, eller flere, sveip som overlapper bør kunne sammlignes med tanke på å lokalisere 'offset' og tilpasse 
   disse til hverandre. Kanskje både med hensyn til posisjon og dybde.
2d Sortere data, helst etter justering som i punkt 2c, slik at alle (brukbare) data for ei lita rute
   samles i ei fil. Før ble 10m x 10m brukt, men jeg tror nå at kanskje 20x20, 25x25, eller kanskje 50x50
   er mer hensiktsmessig. En skal kanskje ikke heller være redd for om noen (løse) punkt utelates, i hvert
   fall bør en ha en gjennomtenkt forklaring for hvordan løse punkt, korte linjer skal tas med. En mulighet
   er at en i denne fila har med alle relevante punkt, og en (u)sikkerhet
2e Fra ei sortert rute lage et detaljert bilde av dybden med største oppløsning på kanskje 2 cm,
   før ble 1 cm brukt men dette er kanskje å strekke data lenger enn ønskelig. Dette bør en kunne gjøre
   med en fornuftig filtrering av resultat fra 2d. Disse 'bildene' bør gjerne lagres.
3) Visualisere både prosess og resultater på en god dynamisk måte, der både posisjon og oppløsning
   bør kunne endres (i passende steg). 
"""

import os
from math import hypot, atan2, pi
from tools import ls
# import numpy as np

# (north, east) in UTM 32V, hele Hafrsfjord er innenfor 10 km x 10 km rute med offset SW (nede til venstre)
offsetHafrs = (6530000,300000)   
dataSeparator = ' '  # in nnn.asc -filer, nnn er et tall
uxDataKatalog = '//nfs/prosjekt/Hafrsfjord/3D Terrain Data/Detaljert Punktsky/xyz punktdata/nhs-2014-s-t0711-1'
pcDataKatalog = 'C:\Karl\hafrsdata'

# made by Karl June 2018
class BAzh1:
	""" Compressed integers stored in bytearray
	BAzh1 is for bytearray as Zip (compressed) format, Hafrsfjord project, variant 1
	ex: b = hafrs.BAzh1()
	    nl = [0,5,23,-4,0,0,2354876,10,9,8,7,6,5,4,3,2,1,0,23<<10,23<<12,23<<14,23<<16,23<<6,23<<8]
	    for n in nl: b.writeVLI(n)
	    b.resetPos()
	    restored_nl = []
	    for i in range(len(nl)): restored_nl.append( b.readVLI() )
	"""
	def __init__(self, len=0):
		self.ba = bytearray(len)
		self.pos = 0
		return
	
	def __len__(self):
		return len(self.ba)
		
	def __str__(self):
		return "BAzh1: integers stored in bytearray, %i bytes" % len(self)
	
	def resetPos(self):
		self.pos = 0
		return
	
	def clear(self):
		self.pos = 0
		for i in range(len(self.ba)):
			self.ba[i] = 0
		return
	
	def writeBit(self,bit):
		""" Write bit (True, False, 1, or 0) to self.ba and increment pos.
		Note: Do not write 0, self.ba is initialized with zeros (or should be set to zeros first)
		"""
		if not (self.pos < (8*len(self))):
			self.ba.append(0)
		if (bit):
			byte = self.pos // 8
			bno = self.pos % 8
			self.ba[byte] = self.ba[byte] | (1 << bno)
		self.pos += 1
		return
	
	def readBit(self):
		""" Read a bit (return 0 or 1) and increment pos.
		"""
		if not (self.pos < (8*len(self))):
			pass  # if pos is to large:   IndexError: bytearray index out of range
		byte = self.pos // 8
		bno = self.pos % 8
		if (self.ba[byte] & (1 << bno)):
			bit = 1
		else:
			bit = 0
		self.pos += 1
		return bit
		
	def writeInt(self,n,nofbit):
		for i in range((nofbit-1),-1,-1): 
			self.writeBit(n & (1 << i))
		return
	
	def readInt(self,nofbit):
		n = 0
		for i in range((nofbit-1),-1,-1): 
			if self.readBit():
				n += (1 << i)
		return n
	
	def writeVLI(self,n):
		""" Write Variable Length Integer to self.ba and increment pos.
		Small numbers use few bits, large numbers use more bits
		Note: max size is now (1<<28)-1 = 268 435 455, which uses 40 bit
		"""
		if (n == 0):
			self.writeBit(0)
		else:
			self.writeBit(1)
			neg = (n < 0)
			n = abs(n)
			if (n <= 4):
				self.writeBit(0)
				self.writeBit(neg)
				self.writeBit((n-1) & 2)
				self.writeBit((n-1) & 1)
			elif (n <= 8):
				self.writeBit(1)
				self.writeBit(0)
				self.writeBit(neg)
				self.writeBit((n-5) & 2)
				self.writeBit((n-5) & 1)
			else: # n > 8
				self.writeBit(1)
				self.writeBit(1)
				self.writeBit(neg)  # now 4 bits are written
				if (n < 131): # and we have n > 8
					self.writeInt(n-3,7)
				elif (n < (1 << 12)):
					self.writeInt(0,7)
					self.writeInt(n,12)
				elif (n < (1 << 16)):
					self.writeInt(1,7)
					self.writeInt(n,16)
				elif (n < (1 << 20)):
					self.writeInt(2,7)
					self.writeInt(n,20)
				elif (n < (1 << 28)):
					self.writeInt(3,7)
					self.writeInt(n,28)
				else:
					self.writeInt(4,7)
				#end if
			#end if
		# end if
		return
	
	def readVLI(self):
		""" Read Variable Length Integer from self.ba and increment pos.
		"""
		n = 0
		if self.readBit():
			if not self.readBit():  # '10' lest |n| <= 4
				neg = self.readBit()
				n = 1 + self.readInt(2)
			else:
				if not self.readBit():  # '110' lest |n| <= 8
					neg = self.readBit()
					n = 5 + self.readInt(2)
				else: # '111' lest, |n| > 8
					neg = self.readBit()
					n7 = self.readInt(7)
					if (n7 > 4):
						n = n7 + 3
					elif (n7 == 0):
						n = self.readInt(12)
					elif (n7 == 1):
						n = self.readInt(16)
					elif (n7 == 2):
						n = self.readInt(20)
					elif (n7 == 3):
						n = self.readInt(28)
					else:
						n = (1 << 28)
					#end if
				#end if
			#end if
			if neg:
				n = -n
			#end if
		#end if
		return n
#end class BAzh1

# made by Karl June 2018
class PointNED:
	""" 3D Point (North, East, Depth) as in "Funn i Hafrsfjord" (FiH) project.
	PointNED is initialized by a string or three numbers (tuple or list)
	The string should be three numbers separated by spaces, as lines in asc-file, ex: "16.asc".
	North and East are UTM 32V coordinates [m], Depth is in [m], and may have two decimals after '.'.
	Examples, as from file "16.asc":
		p1 = hafrs.PointNED('6534927.09 305795.80 11.72')
		p2 = hafrs.PointNED((6534927.08, 305795.73, 11.73))
	"""
	def __init__(self, txt=None):
		if isinstance(txt, str):
			try:
				(nstr, estr, dstr) = txt.split()  # any whitespace string is a separator
				self.north = float(nstr)
				self.east =  float(estr)
				self.depth = float(dstr)
				self.ok = True
			except:
				self.ok = False
		elif isinstance(txt, (list, tuple)) and (len(txt) == 3):
			try:
				self.north = float(txt[0])
				self.east =  float(txt[1])
				self.depth = float(txt[2])
				self.ok = True
			except:
				self.ok = False
		else:
			print('PointNED(): Error creating point.')
			self.ok = False
		return
	
	def __str__(self):
		# ex: print(p1) # or str(p1)
		if self.ok:
			t = ("PointNED: UTM 32V (N,E,D) = (%10.2f, %10.2f, %8.2f)" % self.asTuple())
		else:
			t = "PointNED: punkt med feil."
		return t
	
	def asTuple(self):
		# ex: p1.asTuple()
		if self.ok:
			t = (self.north, self.east, self.depth)
		else:
			t = ()
		return t
	
	def asList(self):
		# ex: p1.asList()
		if self.ok:
			t = [self.north, self.east, self.depth]
		else:
			t = []
		return t
	
	def __sub__(self, pkt):
		""" Returns hypotenuse distance between two points, excluding depth
		ex: dist = p1 - p2  # note p1 is self (first input argument) in function
		"""
		if isinstance(pkt, PointNED) and pkt.ok and self.ok:
			d = hypot(self.north - pkt.north, self.east - pkt.east)
		else: 
			d = -1.0  #  indicate error
		return d
	
	def midPoint(self, pkt, a=0.5):
		""" Returns point halfway (or 'a') from self towards pkt (middle point)
		i.e. pm = (1-a)*p1 + a*p2 = p1 + a*(p2-p1)
		ex: pm = p1.midPoint(p2)
		"""
		if isinstance(pkt, PointNED) and pkt.ok and self.ok:
			(y1,x1,z1) = self.asTuple()   # y: north, x: east
			(y2,x2,z2) = pkt.asTuple()
			(dy,dx,dz) = (y2-y1, x2-x1, z2-z1)
			pm = PointNED(( y1+a*dy, x1+a*dx, z1+a*dz ))
		else: 
			pm = PointNED()  #  empty (not ok) PointNED, indicate error
		return pm
		
	def direction(self, pkt):
		""" Direction from self towards pkt, 0 (or 360) is north, 90 is east, 180, south, and 270 west
		"""
		if isinstance(pkt, PointNED) and pkt.ok and self.ok:
			(y1,x1,_) = self.asTuple()   # y: north, x: east
			(y2,x2,_) = pkt.asTuple()
			(dy,dx) = (y2-y1, x2-x1)  
			d = (180.0/pi)*atan2(dx, dy)
			if (d<0):
				d = d+360.0
		else: 
			d = -1  #  indicate error
		return d
	
	def distLine(self, p0, p1):
		""" Distance from self to line between p0 and p1, 
		also returns 'a', such that point on line closest to self is p0.midPoint(p1,a)
		ex:  (pkt,p0,p1) = (hafrs.PointNED((2,9,0)), hafrs.PointNED((2,6,0)), hafrs.PointNED((6,9,0)))
		     (d,a) = pkt.distLine(p0,p1)
		     dist = pkt - p0.midPoint(p1,a)  # same as d
		"""
		if isinstance(p0, PointNED) and isinstance(p1, PointNED) and p0.ok and p1.ok and self.ok:
			(y,x,z) = self.asTuple()
			(y0,x0,z0) = p0.asTuple()
			(y1,x1,z1) = p1.asTuple()
			(dy,dx) = (y1-y0, x1-x0)  
			a = (dy*(y-y0)+dx*(x-x0)) / (dy*dy+dx*dx)
			d = hypot( (1.0-a)*y0+a*y1-y, (1.0-a)*x0+a*x1-x )
		else: 
			d = -1  #  indicate error
			a = 0
		return (d,a)
#end class PointNED

class PunktListe:
	""" En klasse for liste av PointNED, data er en list (av PointNED)
	ex: pL = PunktListe()  # oppretter ei tom liste
	    pL = PunktListe(p)  # oppretter liste med der p er et eller flere PointNED
	    pL = PunktListe(fn)  # oppretter liste med innhold fra filnavn fn
	    pL = hafrs.PunktListe('16.asc')
	    ba = pL.toBAzh1()
	    pLlist = hafrs.lesAscFil('16.asc')
	    ba4 = pLlist[4].toBAzh1()
	    pL4 = hafrs.PunktListe.fromBAzh1(ba4)
	"""
	def __init__(self, p=None):
		self.data = []
		if not (p == None):
			if isinstance(p, str):
				# leser hele fila som ei punktliste
				fileName = p
				with open(fileName, 'r') as file:
					for line in file:
						self.append( PointNED(line) )
				file.close()
			else:
				self.append(p)
		return
	
	def __str__(self):
		t = ("PunktListe: %i PointNED" % len(self.data))
		return t
	
	def __len__(self):
		return len(self.data)
		
	def __getitem__(self, key):
		return self.data[key]
	
	def append(self, p=None):
		""" Append ok point(s), a single point or points in a list (or tuple)
		"""
		if isinstance(p, PointNED) and p.ok:
			self.data.append(p)
		if isinstance(p, (list, tuple)):
			for item in p:
				if isinstance(item, PointNED) and item.ok: 
					self.data.append(item)
		return
	
	def toBAzh1(self):
		bazh1 = BAzh1()
		bazh1.writeVLI(len(self))
		if len(self):
			(n0,e0,d0) = (int(100*offsetHafrs[0]), int(100*offsetHafrs[1]), 0)
			for i in range(len(self)):
				(n,e,d) = self[i].asTuple()
				(n,e,d) = (int(100*n+0.01), int(100*e+0.01), int(100*d+0.01))
				bazh1.writeVLI( n - n0 )
				bazh1.writeVLI( e - e0 )
				bazh1.writeVLI( d - d0 )
				(n0,e0,d0) = (n,e,d)
		return bazh1
	
	def fromBAzh1(bazh1):
		pL = PunktListe()
		bazh1.resetPos()
		antP = bazh1.readVLI()
		(n0,e0,d0) = (int(100*offsetHafrs[0]), int(100*offsetHafrs[1]), 0)
		for i in range(antP):
			n = bazh1.readVLI() + n0
			e = bazh1.readVLI() + e0
			d = bazh1.readVLI() + d0
			pL.append( PointNED([n/100, e/100, d/100]) )
			(n0,e0,d0) = (n,e,d)
		return pL
	
	def text(self, ant=4):
		# ex: print(pL.text(2))
		if len(self) == 0:
			t = "PunktListe is empty."
		elif len(self) <= (2*ant):
			t = ("PunktListe of %i PointNED (in UTM 32V):" % len(self.data))
			for i in range(len(self.data)):
				t = t + ("\n  pkt %4i: " % i) + ("(N,E) = (%10.2f, %10.2f), depth = %6.2f" % self[i].asTuple()) 
		else:
			t = ("PunktListe of %i PointNED (in UTM 32V):" % len(self.data))
			for i in range(ant):
				t = t + ("\n  %9i: " % i) + ("(N,E) = (%10.2f, %10.2f), depth = %6.2f" % self[i].asTuple()) 
			t = t + "\n          ..."
			for i in range(len(self.data)-ant,len(self.data)):
				t = t + ("\n  %9i: " % i) + ("(N,E) = (%10.2f, %10.2f), depth = %6.2f" % self[i].asTuple()) 
		#
		return t
	
	def eightProp(self):
		""" return (len(self),len1,len2,dxy_min,dxy_max,direction,z_min,z_max)
		ex: (len0,len1,len2,dxy_min,dxy_max,direction,z_min,z_max) = self.eightProp()
		"""
		if len(self) == 0:
			return (0,-1,-1,0,0,-1,-1,0)
		else:
			len1 = (self[-1] - self[0])  # avstand fra start til slutt
			direction = self[0].direction(self[-1])
			(len2,dxy_min, dxy_max) = (0.0, 200000.0, 0.0)
			(z_min, z_max) = (self[0].depth, self[0].depth)
			for i in range(1,len(self)):
				delta_xy = (self[i] - self[i-1]) # PointNED.__sub__()
				len2 += delta_xy
				dxy_min = min(dxy_min, delta_xy)
				dxy_max = max(dxy_max, delta_xy)
				z_min = min(z_min, self[i].depth)
				z_max = max(z_max, self[i].depth)
			#end for
		return (len(self),len1,len2,dxy_min,dxy_max,direction,z_min,z_max)
	
	def info(self,allPoints=False):
		""" ex:   print(pL.info()), print( pLlist[1].info() )
		Finner og returnerer, tekst med mange linjer, noen egenskaper for ei punktliste,
		"""
		if len(self) == 0:
			t = "PunktListe er tom."
		else:
			t = ("PunktListe med %i PointNED (UTM 32V):" % len(self.data))
			if allPoints:
				for i in range(len(self)):
					t = t + ('\n   %4i: %s' % (i,str(self[i])))
			(len0,len1,len2,dxy_min,dxy_max,direction,z_min,z_max) = self.eightProp()
			t = t + ("\n  Avstand fra første til siste punkt er              %7.2f [m]" % len1)
			t = t + ("\n  Total avstand langs punkt i liste er               %7.2f [m]" % len2)
			t = t + ("\n  Minimum avstand mellom etterfølgende punkt er      %7.2f [m]" % dxy_max)
			if (len0 > 1):
				t = t + ("\n  Gjennomsnitt avstand mellom etterfølgende punkt er %7.2f [m]" % (len2/(len0-1)))
			t = t + ("\n  Maksimum avstand mellom etterfølgende punkt er     %7.2f [m]" % dxy_max)
			t = t + ("\n  Retning for linje fra første til siste punkt er    %7.2f [deg]" % direction)
			(d,_) = self.distLine(self[0],self[-1])
			t = t + ("\n  Gjennomsnitt avstand fra punkt til linje er        %9.4f [m]" % (sum(d)/len(d)))
			t = t + ("\n  Maksimum avstand fra punkt til linje er            %9.4f [m]" % (max(d)))
		#
		return t
	
	def infoLinje(self, head='PunktListe: '):
		""" Finner og returnerer tekst på ei linje med noen egenskaper for ei punktliste
		ex: print( pLlist[2].infoLinje() )
		    for i in range(len(pLlist)): print( pLlist[i].infoLinje('pLlist[%4i]: ' % i) )
		"""
		fmt = '%s%3i Pkt, len %5.2f-%5.2f [m], dxy %4.2f-%4.2f [m], dir %6.2f [deg], z %5.2f-%5.2f [m]'
		fmt2 = ' (%7.2f N, %7.2f E)'
		if len(self) == 0:
			t = head + "  0 Pkt, tom"
		else:
			t = (fmt % ((head,) + self.eightProp())) + (fmt2 % (self[0].north-offsetHafrs[0],self[0].east-offsetHafrs[1]))
		return t
		
	def distLine(self, p0, p1):
		""" Distance from all points in self to line between p0 and p1, 
		also returns aL, such that point on line closest to self[i] is p0.midPoint(p1,aL[i])
		both dL and aL are list, len(dL) == len(aL)
		ex:  pLlist = hafrs.lesAscFil('16.asc')
		     pL = pLlist[4]
		     (d,a) = pL.distLine(pL[0],pL[-1])
		     (d,a) = pLlist[5].distLine(pLlist[4][0],pLlist[4][-1])
		"""
		if isinstance(p0, PointNED) and isinstance(p1, PointNED) and p0.ok and p1.ok and (len(self) > 0):
			(y0,x0,z0) = p0.asTuple()
			(y1,x1,z1) = p1.asTuple()
			(dx,dy) = (x1-x0, y1-y0)  
			temp = (dx*dx+dy*dy)
			aL = []
			dL = []
			for i in range(len(self)):
				(y,x,z) = self[i].asTuple()
				a = (dx*(x-x0)+dy*(y-y0)) / temp
				aL.append( a )
				dL.append( hypot( (1.0-a)*x0+a*x1-x, (1.0-a)*y0+a*y1-y ) )
		else: 
			dL = []  #  indicate error
			aL = []
		return (dL,aL)
	
	def diffHist(self, dH):
		""" add values for this PunktListe to difference histogram in dH
		dh is a list of 24 numbers, the first 12 for dxdy and the last 12 for dz
		ex: dH = [ 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0]
		    pLlist = hafrs.lesAscFil('16.asc')
		    for i in range(len(pLlist)): pLlist[i].diffHist(dH)
		ex: 
		"""
		if (len(self) >= 1):
			for i in range(1,len(self)):
				delta_x = 100*abs(self[i].east - self[i-1].east) 
				delta_y = 100*abs(self[i].north - self[i-1].north)
				delta_z = 100*abs(self[i].depth - self[i-1].depth)
				for hi in (int(delta_x+0.01), int(delta_y+0.01)):
					if (hi > 11):
						hi = 11
					dH[hi] += 1
				hi = int(delta_z) + 12
				if (hi > 23):
					hi = 23
				dH[hi] += 1
			#end for
		#end if 
		return
#end class PunktListe


def lesAscFil(fileName, d1=0.5):
	""" Funksjonen leser fila gitt med inn argument 'fileName'. 
	Fila skal være ei enkel tekstfil, asc-fil (ex: 16.asc)
	Hver linje fra tekstfila er en tekststreng (string) som kan tolkes av "class PointNED"
	NED er forkortelse for: North-East-Depth. 
	Funksjonen returnerer ei liste med PunktListe objekt. 
	Hver PunktListe inneholde punkt som er nærmere en d1 [m] fra foregående punkt
	Merk at  pL = PunktListe('16.asc')  leser fila til bare ei punktliste, og virker nesten som
	lesAscFil('16.asc', d1 = 200000) (som returnerer array med ett element; ei punktliste)
	
	ex:  pLlist = hafrs.lesAscFil('16.asc')  
	"""
	pLlist = [PunktListe()]
	p0 = None  # last Point
	with open(fileName, 'r') as file:
		for line in file:
			p = PointNED(line)
			if p.ok:
				if ((p-p0) < d1):
					pLlist[-1].append(p)
				else:
					pLlist.append( PunktListe(p) ) 
				p0 = p
		#end for
	file.close()
	return pLlist

# OBSOLETE June 14, 2018  (Karl S)
def lesAscFil_0(fileName, d1=0.0):
	""" Funksjonen leser fila gitt med inn argument 'fileName'. 
	Fila skal være ei enkel tekstfil, asc-fil (ex: 16.asc)
	Hver linje fra tekstfila er en tekststreng (string) som kan tolkes av "class PointNED"
	Funksjonen returnerer ei liste (list) der hvert element er 
	 1) et enkelt punkt  (hvis d1=0.0)
	 2) ei liste med punkt som er nærmere enn d1 fra forrige punkt
	OBS! store filer (flere millioner punkt) vil gjerne bruke mye minne
	hvert punkt (som tuple) tar kanskje 72 byte. I tillegg tar listene med pekere plass,
	numpy pakken lagrer array (of float) med ned mot 8 byte per tall, 24 byte per punkt
	tuple tar kanskje 48 byte overhead + 8 byte per tall.
	
	ex:  pktList = hafrs.lesAscFil_0('16.asc')  # kanskje 20021*72 + sys.getsizeof(pktList) = 1.62 MB
	     X = np.array(pktList)  # X.shape = (20021, 3)  sys.getsizeof(X) = 480616
	"""
	pointList = []
	p0 = None
	file = open(fileName, 'r')
	for line in file:
		p = PointNED(line)
		if (p0 == None):
			dist = 20000.0  # et stort tall
		else:
			dist = p - p0
		# lagrer i pointList
		# tilsynelatende tar tuple litt mindre plass enn list, men minst som p1 (klasse PointNED):
		# (sys.getsizeof(p1.asTuple()), sys.getsizeof(p1.asList()), sys.getsizeof(p1)) = (72, 88, 56)
		if (d1 == 0.0):
			pointList.append( p.asTuple() )
		else:
			if (dist < d1):
				pointList[-1].append( p.asTuple() )
			else:
				pointList.append( [] ) 
				pointList[-1].append( p.asTuple() )
		p0 = p
	#end for
	file.close()
	return pointList


# ********* Det nedenfor er fra Sindre, mars 2018
#    directory1_in_str = 'E:\\Master2018\\xyz_punktdata\\nhs-2014-s-t0711-1'
#    directory2_in_str = 'E:\\Master2018\\xyz_punktdata\\nhs-2015-s-t0711-2'    
#    directory1 = os.fsencode(directory1_in_str)
#    directory2 = os.fsencode(directory2_in_str)
#    
#    for file in os.listdir(directory1):
#        filename = os.fsdecode(file)
#        dir = directory1_in_str+'\\'+filename
#        singleFile10x10(dir)
#         
def singleFile10x10(fileName):
	# (dette er mest slik som Sindre ville løse problemet)
	# Mappen filene skrives til
	#writeDir = 'E:\\Master2018\\10x10_data\\'
		
	columnSeparator = '\n'
	
	north = []
	east = []
	depth = []
	
	# Største og minste koordinater som finnes i datasettet
	limits = {'MaxEast': 309144.99, 'MaxNorth': 6538290.27, 'MinEast': 305335.27, 'MinNorth': 6533568.56}
	
	   
	# Går gjennom filen og deler inn koordinater og dybde i hver sin liste
	with open(fileName,'r') as f:       
		
		for line in f.readlines():
			columns = line.split(columnSeparator)
			
			for column in columns:
				if not column: continue
				
				# Omgjør til cm, og dermed heltall, og trekker fra minste øst-/nordkoordinat     
				# som nå er origo.
				nrth = int(float(column.split(dataSeparator)[0])*100)- int(limits['MinNorth']*100)
				est = int(float(column.split(dataSeparator)[1])*100)- int(limits['MinEast']*100)
				dpth = int(float(column.split(dataSeparator)[2])*100)
				
				north.append(nrth)
				east.append(est)
				depth.append(dpth)
								  
	# Sjekker koordinatlistene for hvilken 10x10-rute (meter) punktene hører til 
	# og bestemmer filnavn ut ifra det.         
	for i in range(len(north)):
		
		if north[i]>=1000 and east[i]>=1000:
			
			file_n = int(north[i]//1000)*1000
			file_e = int(east[i]//1000)*1000
			
		elif north[i]<1000 and east[i]>=1000:
			
			file_n = 0
			file_e = int(east[i]//1000)*1000
			
		elif north[i]>=1000 and east[i]<1000:
			
			file_n = int(north[i]//1000)*1000
			file_e = 0
			
		else:
			print('Noe er galt')        
		
		fileName = 'N{}E{}.asc'.format(file_n,file_e)    
		
		#writeDirFull = writeDir+fileName
		writeDirFull = fileName
		
		# Åpner filen med riktig navn og skriver koordinater og dybde til filen.
		# Hvis filen ikke eksisterer lages den.
		with open(writeDirFull,'a') as f:                                                    
			f.write('{} {} {}\n'.format(north[i],east[i],depth[i]))
		#
	#
	
	return
# ************* Det ovenfor er fra Sindre


# laget av Karl mars 2018
def readAscToList(fileName):
	def lesLinje(linje):
		# return (nnn, eee, n, e, d) as integers 
		# nnn and eee identify the 10x10 square where point belong
		# n,e is offset in cm from lower left corner (SW) for this point, d is depth in cm
		(nstr, estr, dstr) = linje.split(dataSeparator)
		# add 1 mm below to make sure 'floor' is ok
		(nfloat, efloat) = (float(nstr) - offsetHafrs[0] + 0.001, float(estr) - offsetHafrs[1] + 0.001)
		nnn = int( (nfloat/10) % 1000 )
		eee = int( (efloat/10) % 1000 )
		n = int( (nfloat*100) % 1000 )
		e = int( (efloat*100) % 1000 )
		d = int( (float(dstr)*100)+0.001 )
		return (nnn, eee, n, e, d)
	
	pointList = []
	file = open(fileName, 'r')
	for line in file:
		pointList.append( lesLinje(line) )
	#end for
	file.close()
	return pointList

# laget av Karl mars 2018
def writeTo10x10(t):
	# t is here the list, pointList', as made by readAscToList(..)
	seksBytes = bytearray(b'\x00\x00\x00\x00\x00\x00')
	t.sort()   # sorterer etter nnn og eee, og n
	lastFn = 'N%03iE%03i.dat' % (0,0)         # fil som ikke finnes/brukes
	isFileOpen = False
	for (nnn, eee, n, e, d) in t:
		seksBytes[0:2] = n.to_bytes(2,'big')
		seksBytes[2:4] = e.to_bytes(2,'big')
		seksBytes[4:6] = d.to_bytes(2,'big')
		fn = 'N%03iE%03i.dat' % (nnn,eee)
		if (fn != lastFn):
			if isFileOpen: 
				file.close()
			file = open(fn,'ba')
			lastFn = fn
			isFileOpen = True
		#end if
		file.write(seksBytes)
	#end for
	if isFileOpen: 
		file.close()
	return

# laget av Karl mars 2018
def test01():
	# Filen 16.asc er liten og grei å teste med
	singleFile10x10('16.asc')
	
	# mitt forslag
	t = readAscToList('16.asc')
	writeTo10x10(t)
	return t

# laget av Karl juni 2018 
def test02(cat='', fn='*.asc'):
	""" leser ei fil fra katalog, eventulet lister filer
	ex: fl = hafrs.test02('pc')
	    pLlist = hafrs.lesAscFil(fl[1], d1=0.6)  # leser ei stor fil, ca 95 [s]
	    for i in range(10): print( pLlist[i].infoLinje('pLlist[%4i]: ' % i) )
	    pLlen = []
	    for i in range(len(pLlist)): pLlen.append( len(pLlist[i]) )
	    pLdist = []
	    for i in range(1,len(pLlist)): pLdist.append( pLlist[i][0] - pLlist[i-1][-1] )
	"""
	if cat == 'ux':
		cat = uxDataKatalog
	if cat == 'pc':
		cat = pcDataKatalog
	if (len(cat) > 0) and (not cat[-1] == os.path.sep):
		cat = cat + os.path.sep
	fl = ls(cat + fn)
	if len(fl) == 0:
		print('Ingen filer ble lest fra "%s"' % (cat+fn))
	else:
		for f in fl:
			print(f)
	return fl


if __name__ == '__main__':
	test02()
	
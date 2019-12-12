#Beispiele fuer die Verwendung von TLorentzVector fuer Vierervektor-Operationen. Mehr Informationen unter https://root.cern.ch/doc/master/classTLorentzVector.html
#3er-Vektoren sind aehnlich zu verwenden, Dokumentation findet man hier: https://root.cern.ch/doc/master/classTVector3.html

from ROOT import TLorentzVector, TVector3 

import math


def main():
	
	# initialisiere TLorentzVector-Objekt und setze Pt, eta, phi und M. Damit ist der Vierervektor vollstaendig bestimmt
	c_ = TLorentzVector()
	c_.SetPtEtaPhiM(99.83,0.332,-2.45,0)
	
	s = TLorentzVector()
	s.SetPtEtaPhiM(22.08,0.137,2.215,0)
	
	ny = TLorentzVector()
	ny.SetPtEtaPhiM(44.73, 0, -2.472, 0)
	
	mu = TLorentzVector()
	mu.SetPtEtaPhiM(65.58, 1.08, -0.851, 0)
	
	wp = ny + mu
	
	# Addiere zwei Vierervektoren
	wm = c_+s
	
	b = TLorentzVector()
	b_ = TLorentzVector()
	
	b_.SetPtEtaPhiM(74.01, 1.379, 0.494, 0)
	

	b.SetPtEtaPhiM(65.34, -0.228, 1.340, 0)
	
	
	t_ = wm + b_
	t = wp + b
	
	# Ausgabe der invarianten Masse eines Vierervektors
	print("Masse Anti-Top: " + str(t_.M()))
	print("Masse Top: " + str(t.M()))
	print(t_)
	
main()

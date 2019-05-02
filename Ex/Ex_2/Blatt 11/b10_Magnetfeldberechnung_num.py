#!/bin/env python
#
# (c) SS2018, Dr. Markus Merschmeyer, III. Physikalisches Institut A, RWTH Aachen University
# (c)(R) SS2018.     Lennart Wilde & Samuel Mahler                  , RWTH Aachen University
#
# Hilfe:  Python:       https://www.python.org
#         numpy/scipy:  https://docs.scipy.org/doc/
#         anaconda:     https://www.continuum.io/why-anaconda

##---------------------------------------------------------------------------------------------
## externe Pakete
##---------------------------------------------------------------------------------------------
import numpy as np              # numpy-Paket fuer Array-Funktionen, sqrt() usw. importieren
import scipy.constants as scc   # scipy-Paket fuer Konstanten importieren
from matplotlib import colors, ticker, cm
import matplotlib.pyplot as plt


##---------------------------------------------------------------------------------------------
## Konstanten
##---------------------------------------------------------------------------------------------
c_pi    = scc.pi                # pi
c_mu0   = scc.mu_0              # mu_0


##---------------------------------------------------------------------------------------------
## Magnetfeldfunktionen
##---------------------------------------------------------------------------------------------

def Bz_LS(R=0.01, I=1.0, z=0.05):
    """ Funktion zur analytischen Berechnung des Magnetfelds einer einzelnen Leiterschleife,
        siehe Vorlesung ExII, SS 2018, Kapitel 4.2.3, Gleichung 27 (Seite 13)
        Parameter:
        R : Leiterschleifenradius (in m)
        I : Leiterschleifenstrom  (in A)
        z : senkr. Entfernung zum Zentrum der Leiterschleife (in m)
    """
    return c_mu0/2.*I*(R**2/(np.sqrt(z**2+R**2))**3) # B-Feld in Tesla

def Bz_EC(n_w=1.0, I=1.0):
    """ Funktion zur analytischen Berechnung des Magnetfelds im Innern einer (unendlich langen) Zylinderspule,
        siehe Vorlesung ExII, SS 2018, Kapitel 4.2.3, Gleichung 24 (Seite 12)
        Parameter:
        n_w : Windungsdichte (in Windungen/cm)
        I   : Leiterschleifenstrom  (in A)
    """
    return c_mu0*I*n_w # B-Feld in Tesla

def v_coil(R=1.0, n_w=1.0, t=0.0):
    """ Funktion zur vektoriellen Beschreibung einer Spule (Helix)
        Parameter:
        R   : Spulenradius (in cm)
        n_w : Windungsdichte (in Windungen/cm)
        t   : aktueller Wert des Kurven-/Windungsparameters (keine Einheit)
    """
    v_tmp = np.array([R*np.cos(2*c_pi*t),
                     -R*np.sin(2*c_pi*t),
                       1/n_w*t])
    # Hinweis: Cosinus/Sinus-Funktionen: np.cos(), np.sin()                   
    return v_tmp # 3er-Vektor mit Einheiten in cm

def biot_savart(R=1.0, n_w=1.0, t_min=0., t_max=1.0, n_step=10, I=1.0, x=0.0, y=0.0, z=0.0):
    """ Funktion zur Berechnung des Magnetfelds einer Leiterschleife/Spule an einem Punkt im Raum
        nach dem Gesetz von Biot-Savart
        Parameter:
        R      : Spulenradius (in cm)
        n_w    : Windungsdichte (in Windungen/cm)
        t_min  : minimaler Wert des Windungsparameters (keine Einheit)
        t_max  : maximaler Wert des Windungsparameters (keine Einheit)
        n_step : Anzahl der Berechnungen pro Windung (keine Einheit)
        I      : Spulenstrom (in A)
        x      : x-Koordinate des Punktes, an dem die Feldstaerke berechnet werden soll (in cm)
        y      : y-Koordinate...
        z      : z-Koordinate...
    """
    # Vorbereitungen
    v_B    = np.array([x, y, z])  # Ortsvektor fuer die Feldberechnung initialisieren
    v_Btot = np.array([0.,0.,0.]) # initialisiere den Summenvektor des B-Feldes
    d_t    =  1/n_step
    
    # berechne Liste mit den Wegelementen d\vec{s} entlang der Spule
    v_ds = []
    for t in np.arange(t_min, t_max, d_t):
        v_ds.append(v_coil(R, n_w, t) - v_coil(R, n_w, t+d_t))
    
    # berechne Liste mit Abstandsvektoren vom jeweiligen Ort (v_coil()) auf der Spule zum Ort (v_B),
    # an dem das B-Feld bestimmt werden soll: \vec{r} = v_B - v_coil()
    v_r = []
    for t in np.arange(t_min, t_max, d_t):
        v_r.append(v_B - v_coil(R, n_w, t))
        # Liste der Abstandsvektoren mit Laenge^3 normieren
    v_rN = []
    for vr in v_r:
        v_rN.append(vr/((np.linalg.norm(vr))**3))
    
    # berechne Liste der Kreuzprodukte \vec{r}xd\vec{s}*(1/r^3)
    v_xrNds = np.cross(v_ds, v_rN)
    
    # multipliziere mit Vorfaktoren -> Liste der einzelnen Beitraege zum B-Feld
    v_xrNds = v_xrNds * c_mu0*I/(4*c_pi)
    
    # bilde Summe ueber alle Vektoren -> Vektor des B-Felds am Ort \vec{r}
    v_Btot = np.sum(v_xrNds, axis = 0)
    
    #return v_Btot     # ganzen B-Feldvektor zurueckgeben
    #return v_Btot[2]  # z-Komponente des B-Feldvektors zurueckgeben
    #return abs(v_Btot[2])  # Betrag der z-Komponente des B-Feldvektors zurueckgeben
    return np.linalg.norm(v_Btot) # Laenge des B-Feldvektors zurueckgeben


##---------------------------------------------------------------------------------------------
## Visualisierungsfunktionen
##---------------------------------------------------------------------------------------------

def visloop():
    """ Funktion zur Berechnung und Darstellung der Ergebnisse fuer den Aufgabenteil b):
          Feldverlauf entlang der z-Achse (Symmetrieachse) einer einzelnen Leiterschleife
        Hinweise:
          - ueberlegen Sie sich geeignete Startwerte fuer die Parameter
          - nutzen Sie 'print'-Ausgaben zur Funktionskontrolle und zum Debugging
          - starten Sie zuerst mit kleinen Werten fuer 'n_step' sowie die Schrittweiten in
            z-Richtung bzw. n_step um schnell erste Ergebnisse zu erhalten; wenn Sie sicher
            sind, dass alles gut funktioniert nehmen Sie detailliertere Berechnungen vor
    """
    ### Vergleich von analytischer und numerischer Berechnung des Bz-Feldes als Funktion des z-Abstands
    
    # Parameterwerte festlegen
    R     =       2     # Radius der Leiterschleife (in cm)
    n_w   =       1000     # Windungszahldichte (in Windungen/cm)
    t_min =       0     # Startpunkt der Leiterschleife
    t_max =       1     # Endpunkt der Leiterschleife
    n_step=       100   # Anzahl der Rechenschritte pro Leiterschleife (bzw. Windung)
    I     =       5     # Stromstaerke in der Leiterschleife (in A)
    z_min =       0     # Startpunkt auf der z-Achse
    z_max =       10     # Endpunkt auf der z-Achse
    z_st1 =       0.05   # z-Schrittweite fuer die numerische Berechnung
    z_st2 =       0.05   # z-Schrittweite fuer die analytische Berechnung
    
    # z-Wertelisten berechnen (mit 'numpy.arange')
    z1 = np.arange(z_min, z_max, z_st1)
    z2 = np.arange(z_min, z_max, z_st2)
    # weiter oben definierte Funktionen fuer numpy "aufbereiten" (mit 'numpy.frompyfunc')
    f_num = np.frompyfunc(biot_savart, 9, 1) # biot_savart : 9 Eingabewerte, 1 Ausgabewert
    f_ana = np.frompyfunc(Bz_LS, 3, 1)       # Bz_LS : 3 Eingabewerte, 1 Ausgabewert
    # B-Feld-Wertelisten der numerischen bzw. analytischen Funktion berechnen
    B_num = f_num(R, n_w, t_min, t_max, n_step, I, 0., 0., z1) # ... numerisch
    B_ana = f_ana(R, I, z2)                                    # ... analytisch
    # Werteliste der relativen Abweichung berechnen (z-Werteliste #1) und den Maximalwert ausgeben
    relabw = abs(B_ana - B_num)/B_ana
    # 3-fach Diagramm (uebereinander) mit gemeinsamer x-Achse erzeugen
    fig, axarr = plt.subplots(3, sharex=True)
    fig.set_size_inches(8., 10.) # Groesse der exportierten Bilddatei in Zoll (Breite, Hoehe)
    # oberstes Diagramm: lineare Darstellung des Bz-Feldes als Funktion des z-Abstands
    #   numerisch: ausgefuellte blaue Kreise ('bo') mit z-Werteliste #1
    #   analytisch: durchgezogene schwarze Linie ('k') mit z-Werteliste #2
    l1, l2 = axarr[0].plot(z1, B_num, 'bo', z2, B_ana, 'k')
    axarr[0].set_title('Analytische und numerische Loesung (lin)') # ... Diagrammtitel
    axarr[0].set_ylabel('B_z-Feldstaerke in T')                    # ... Beschriftung y-Achse
    axarr[0].axis([z_min, z_max, 0., 0.7E-4])                      # ... Bereich x-Achse (z-Werte), y-Achse (Bz-Feldstaerke)
    # mittleres Diagramm: semilogarithmische Darstellung des Bz-Feldes als Funktion des z-Abstands
    #   sonst wie oben
    axarr[1].semilogy(z1, B_num, 'bo', z2, B_ana, 'k')
    axarr[1].set_title('Analytische und numerische Loesung (log)') # ... Diagrammtitel
    axarr[1].set_ylabel('B_z-Feldstaerke in T')                    # ... Beschriftung y-Achse
    axarr[1].axis([z_min, z_max, 1.E-8, 1.E-4])                    # ... Bereich x-Achse (z-Werte), y-Achse (log(Bz-Feldstaerke))
    # unteres Diagramm: Betrag der relativen Abweichung von analytischer und numerischer Berechnung
    #   rote, gestrichelte Linie ('r--'), z-Werteliste (#1)
    axarr[2].semilogy(z1, relabw, 'r--')
    axarr[2].set_title('relative Abweichung, n_step = ' + str(n_step)) # ... Diagrammtitel
    axarr[2].set_xlabel('z-Abstand / cm')                              # ... Beschriftung x-Achse
    axarr[2].set_ylabel('(B_z,ana-B_z,num)/B_z,ana')                   # ... Beschriftung y-Achse
    axarr[2].axis([z_min, z_max, 5.e-4, 1])                         # ... Bereich x-Achse (z-Werte), y-Achse (rel. Abw.)
    # Legende fuer das oberste Diagramm einzeichnen (Datenobjekte l1, l2; Bezeichnungen; relative Position)
    #   relative Position: x -> 65% (von links), y -> 80% (von unten)
    fig.legend((l1, l2), ('numerisch', 'analytisch'), (0.65, 0.80))
    # Diagramm speichern mit 300 dpi Aufloesung
    fig.savefig('visloop_1.png', dpi=300)
    #plt.show()
    del axarr, fig
    
    plt.show()
    
    ### (maximale) relative Abweichung als Funktion der Anzahl der Rechenschritte pro Leiterschleife bestimmen
    
    # Parameterwerte festlegen
    n_min = 1   # Startwert fuer die Anzahl der Rechenschritte pro Leiterschleife
    n_max = 100   # Endwert ...
    n_stp = 1   # Schrittweite ...
    # restliche Parameter wie oben

    # Werteliste der Anzahl der Rechenschritte pro Leiterschleife berechnen
    ns = np.arange(n_min, n_max, n_stp)
    # fuer jedes Element der n_step-Werteliste den Betrag der maximalen relativen Abweichung berechnen
    re = [] # leere Liste fuer Max.-Werte der rel. Abw. erzeugen
    for n in ns:
        B_num = f_num(R, n_w, t_min, t_max, n, I, 0., 0., z1) # ... numerisch
        B_ana = f_ana(R, I, z2)                                    # ... analytisch
        # Werteliste der relativen Abweichung berechnen (z-Werteliste #1) und den Maximalwert ausgeben
        relabw = abs(B_num - B_ana)/B_ana
        re.append(max(relabw)) # neuen Maximalwert zur Liste hinzufuegen
    
    # Diagramm erzeugen
    fig = plt.figure()
    fig.set_size_inches(8., 4.5) # Groesse der exportierten Bilddatei in Zoll (Breite, Hoehe)
    ax = fig.add_subplot(111)
    # semilogarithmische Darstellung der relativen Abweichung von analytischer und numerischer Berechnung
    #   als Funktion der Anzahl der Rechenschritte pro Leiterschleife (n_step)
    ax.semilogy(ns, re, 'bo')
    ax.set_xlabel('Anzahl n der Schritte / Windung') # ... Beschriftung x-Achse
    ax.set_ylabel('Relative Abweichung')             # ... Beschriftung y-Achse
    ax.axis([n_min, n_max, 5.e-4, 1.e0])             # ... Bereich x-Achse (n_step-Werte), y-Achse (max. rel. Abw.)
    # zusaetzliche Linie von 'n_min' nach 'n_max' bei y=1.0*10^-3 einzeichnen
    ax.plot([n_min, n_max], [1.e-3, 1.e-3], 'r-', lw=2)
    # Diagramm speichern mit 300 dpi Aufloesung
    fig.savefig('visloop_2.png', dpi=300)
    plt.show()
    
    for i in range(len(re)):
        if re[i] < 1.e-3:
            print("Nach {} Schritten ist der relative Fehler kleiner als 1%.".format(i))
            break


def viscoil():
    """ Funktion zur Berechnung und Darstellung der Ergebnisse fuer den Aufgabenteil c):
          numerische Berechnung des B-Feldes im Zentrum einer langen Zylinderspule,
          Vergleich mit der analytischen Berechnung
        Hinweise:
          - ueberlegen Sie sich geeignete Startwerte fuer die Parameter
          - nutzen Sie 'print'-Ausgaben zur Funktionskontrolle und zum Debugging
          - starten Sie zuerst mit kleinen Werten fuer 'n_step' sowie die Schrittweite fuer
            die Spulenlaenge um schnell erste Ergebnisse zu erhalten; wenn Sie sicher
            sind, dass alles gut funktioniert nehmen Sie detailliertere Berechnungen vor
    """

    # Parameterwerte festlegen
    R      =  1.8  # Spulenradius (in cm)
    n_w    =  25   # Windungszahldichte (in Windungen/cm)
    n_step =  50   # Anzahl der Rechenschritte pro Windung
    I      =  1  # Spulenstrom (in A)
    L_min  =  1  # minimale Laenge der Spule (in cm)
    L_max  =  50  # maximale Laenge der Spule (in cm)
    L_step =  1  # Schrittweite bei der Vergroesserung der Spulenlaenge (in cm)

    # Werteliste der Spulenlaengen erzeugen.
    L = np.arange(L_min, L_max, L_step)
    # weiter oben definierte Funktionen fuer numpy "aufbereiten" (mit 'numpy.frompyfunc')
    f_num = np.frompyfunc(biot_savart, 9, 1)
    f_ana = np.frompyfunc(Bz_EC, 2, 1)
    # Wertebereich fuer den Windungsparameter 't' festlegen
    t_min = 0.
    t_max = L*n_w
    # B-Feld-Wertelisten der numerischen bzw. analytischen Funktion berechnen    
    B_num = f_num(R, n_w, t_min, t_max, n_step, I, 0., 0., L/2) # ... numerisch
    B_ana = f_ana(n_w, I)                                    # ... analytisch
    # Werteliste der relativen Abweichung berechnen
    relabw = abs(B_num - B_ana)/B_ana
    
    # Diagramm erzeugen
    fig = plt.figure()
    fig.set_size_inches(8., 4.5) # Groesse der exportierten Bilddatei in Zoll (Breite, Hoehe)
    # semilogarithmische Darstellung der relativen Abweichung von analytischer und numerischer Berechnung
    #   als Funktion der Spulenlaenge
    ax = fig.add_subplot(111)
    ax.semilogy(L, relabw, 'bo')
    ax.set_xlabel('Spulenlaenge / cm')   #... Beschriftung x-Achse
    ax.set_ylabel('Relative Abweichung') #... Beschriftung y-Achse
    ax.axis([L_min, L_max, 1.e-3, 1.e0]) # ... Bereich x-Achse (Spulenlaenge), y-Achse (max. rel. Abw.)
    # zusaetzliche Linie von 'L_min' nach 'L_max' bei y=1.0*10^-2 einzeichnen
    ax.plot([L_min, L_max], [1.e-2, 1.e-2], 'r-', lw=2)
    # Diagramm speichern mit 300 dpi Aufloesung
    fig.savefig('viscoil.png', dpi=300)
    plt.show()
    
    for i in range(len(relabw)):
        if relabw[i] < 1.e-2:
            print("Mit {} cm kann die Spule durch eine Unendlich lange Spule angenähert werden.".format(i))
            break


##---------------------------------------------------------------------------------------------
## Hauptprogramm
##---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import  b10_Magnetfeldberechnung_num as b10
    biot_savart()
    b10.visloop()
    b10.viscoil()

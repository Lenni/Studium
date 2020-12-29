#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:52:37 2018

@author: AFigueroa
"""

import numpy as np
from matplotlib import pyplot as plt

def FuelDep(P,Time, Enrichment, Deltat, FuelMass):   
    """Calculate the fuel depletion in a nuclear reactor.
    
    Using cumulative fission yields and cross sections estimated with a
    thermal neutron spectrum the fission processes of relevant nuclides
    are calculated. Relevant decay constants are used to take nuclear 
    decay into account. The fuel is depleted for a specified period of 
    time.
    
    Parameters
    ----------
    P:          thermal power [MW]
    Time:       total time period [days]
    Enrichment: fraction of U235 in the fuel [%/100]
    Deltat:     length of the time steps in the integration [s]
                should be < 60 s
    FuelMass:   Mass of the Uranium fuel [g]

    Output
    ------
    Return a dictionary containing the time steps and relevant isotopes of
    the spent fuel.
    time:   time steps [s]
    U235:   mass of U235 [kg]
    U238:   mass of U238 [kg]
    Np239:  mass of Np239 [kg]
    Pu239:  mass of Pu239 [kg]
    Pu240:  mass of Pu240 [kg]
    """
    
    # Cross-sections:
    sf238U = 16.83e-30
    sc238U = 2.690e-24

    sf235U = 582.6e-24
    sc235U = 98.8e-24

    sf239Pu = 748.1e-24
    sc239Pu = 269.3e-24

    sf240Pu = 37.84e-27
    sc240Pu = 289.5e-24

    sf239Np = 29.06e-27
    sc239Np = 68e-24
    
    sa83Kr = 201.2e-24
    sa113Cd = 26.93e-21
    sa133Xe = 190e-24
    sa135Xe = 3.219e-18    
    sa143Nd = 323.9e-24
    sa148Pm = 2.002e-21
    sa149Sm = 68.35e-21
    sa151Sm = 14.07e-21
    sa152Eu = 11.80e-21
    sa153Ga = 16.45e-21
    sa154Ga = 84.49e-24
    sa155Ga = 50.69e-21
    sa157Ga = 215.2e-21
    
    
    
    # Cumulative Fission Yields: Thermal Spectrum
    Y235to83Kr = 5.395910e-03
    Y238to83Kr = 3.968990e-03
    Y239to83Kr = 2.967380e-03
    
    Y235to113Cd = 1.395600e-04 + 2.269010e-06
    Y238to113Cd = 4.539230e-04 + 7.380690e-06
    Y239to113Cd = 8.034630e-04 + 1.306410e-05
    
    Y235to133Xe = 6.689360e-02
    Y238to133Xe = 6.760790e-02
    Y239to133Xe = 7.015560e-02
    
    Y235to135Xe = 6.523010e-02
    Y238to135Xe = 6.922760e-02
    Y239to135Xe = 7.604770e-02
    
    Y235to143Nd = 5.947859e-02
    Y238to143Nd = 4.632000e-02
    Y239to143Nd = 4.412790e-02
        
    Y235to148Pm = 4.150530e-11 + 8.783570e-11
    Y238to148Pm = 6.859560e-12 + 1.664460e-11
    Y239to148Pm = 1.907670e-08 + 4.037120e-08
    
    Y235to149Sm = 1.079850e-02
    Y238to149Sm = 1.623790e-02
    Y239to149Sm = 1.216310e-02
    
    Y235to151Sm = 4.181090e-03
    Y238to151Sm = 7.987540e-03
    Y239to151Sm = 7.382980e-03
    
    Y235to152Eu = 2.563600e-12 + 1.520780e-13
    Y238to152Eu = 4.180080e-14 + 1.971740e-15
    Y239to152Eu = 1.281750e-09 + 7.603600e-11 
    
    Y235to153Ga = 4.325930e-10
    Y238to153Ga = 7.558230e-14
    Y239to153Ga = 2.169650e-12
    
    Y235to154Ga = 1.936640e-09
    Y238to154Ga = 8.251430e-11 
    Y239to154Ga = 2.799920e-07
    
    Y235to155Ga = 3.207940e-04
    Y238to155Ga = 1.412620e-03
    Y239to155Ga = 1.656840e-03
    
    Y235to157Ga = 6.141520e-05
    Y238to157Ga = 4.139020e-04
    Y239to157Ga = 7.413960e-04
    
    # Decay Constants in seconds:
    Lambda133Xe = np.log(2)/(5.243*86400) #[days^{-1}]
    Lambda135Xe = np.log(2)/(9.14*3600) #[days^{-1}]
    Lambda148Pm = np.log(2)/(5.368*3600) #[days^{-1}]
    Lambda151Sm = np.log(2)/(90*365*3600) #[days^{-1}]
    Lambda152Eu = np.log(2)/(13.537*365*3600) #[days^{-1}]
    Lambda153Ga = np.log(2)/(240*86400) #[days^{-1}]
    Lambda239Np = np.log(2)/(2.365*86400) #[days^{-1}]
    
    E = 200 #[MeV] on average
    
    # Internal Variables:
    N235U0 = ((FuelMass * Enrichment)/235.044)*6.022e23
    SF235U0 = N235U0 * sf235U
    N238U0 = ((FuelMass * (1-Enrichment))/238.029)*6.022e23
    SF238U0 = N238U0 * sf238U
    N239Np0 = 0
    N239Pu0 = 0
    N240Pu0 = 0
    N83Kr0 =  0
    N113Cd0 = 0
    N133Xe0 = 0
    N135Xe0 = 0
    N143Nd0 = 0
    N148Pm0 = 0
    N149Sm0 = 0
    N151Sm0 = 0
    N152Eu0 = 0
    N153Ga0 = 0
    N154Ga0 = 0
    N155Ga0 = 0
    N157Ga0 = 0
    
    Power = (P*1e6*6.25e12) #[MeV]
    N83Kr  = []
    N113Cd = []
    N133Xe = []
    N135Xe = []
    N143Nd = []
    N148Pm = []
    N149Sm = []
    N151Sm = []
    N152Eu = []
    N153Ga = []
    N154Ga = []
    N155Ga = []
    N157Ga = []
    N235U = []
    N238U =[]
    N239Np = []
    N239Pu = []
    N240Pu = []
    Phi = []
    t = []
    
    N83Krt  = N83Kr0
    N113Cdt = N113Cd0
    N133Xet = N133Xe0
    N135Xet = N135Xe0
    N143Ndt = N143Nd0
    N148Pmt = N148Pm0
    N149Smt = N149Sm0
    N151Smt = N151Sm0
    N152Eut = N152Eu0
    N153Gat = N153Ga0
    N154Gat = N154Ga0
    N155Gat = N155Ga0
    N157Gat = N157Ga0
    N235Ut = N235U0
    N238Ut = N238U0
    N239Npt = N239Np0
    N239Put = N239Pu0
    N240Put = N240Pu0
   
    
    Phi0 = Power /(E*(SF235U0 + SF238U0))
    Phit = Phi0
    time = 0
    print('Starting Calculation...')
    for a in range(int((Time*86400)/Deltat)): #Integrate every 10 min for 1 year
        N235Ut_t = N235Ut*(1-((sf235U+sc235U)*Phit*Deltat))
        N235U.append(N235Ut_t)
        
    
        N238Ut_t = N238Ut*(1-(sf238U+sc238U)*Phit*Deltat)
        N238U.append(N238Ut_t)
        
    
        N239Npt_t = (N239Npt*(1-(((sf239Np+sc239Np)*Phit) + Lambda239Np)*Deltat)) + (N238Ut*sc238U*Phit*Deltat)
        N239Np.append(N239Npt_t)
   
    
        N239Put_t = (N239Put*(1-(sf239Pu+sc239Pu)*Phit*Deltat)) + (Lambda239Np*N239Npt*Deltat)
        N239Pu.append(N239Put_t)
    
    
        N240Put_t = (N240Put*(1-(sf240Pu+sc240Pu)*Phit*Deltat)) + (N239Put*sc239Pu*Phit*Deltat)
        N240Pu.append(N240Put_t)
        
        N83Krt_t = (N83Krt*(1-(sa83Kr*Phit*Deltat))) + (N235Ut*sf235U*Y235to83Kr*Phit*Deltat)+(N238Ut*sf238U*Y238to83Kr*Phit*Deltat)+(N239Put*sf239Pu*Y239to83Kr*Phit*Deltat)
        N83Kr.append(N83Krt_t)
        
        N113Cdt_t = (N113Cdt*(1-(sa149Sm*Phit*Deltat))) + (N235Ut*sf235U*Y235to113Cd*Phit*Deltat)+(N238Ut*sf238U*Y238to113Cd*Phit*Deltat)+(N239Put*sf239Pu*Y239to113Cd*Phit*Deltat)
        N113Cd.append(N113Cdt_t)
        
        N133Xet_t = (N133Xet*(1-(sa133Xe*Phit*Deltat))) + (N235Ut*sf235U*Y235to133Xe*Phit*Deltat)+(N238Ut*sf238U*Y238to133Xe*Phit*Deltat)+(N239Put*sf239Pu*Y239to133Xe*Phit*Deltat) - (Lambda133Xe*N133Xet*Deltat)
        N133Xe.append(N133Xet_t)
        
        N135Xet_t = (N135Xet*(1-(sa135Xe*Phit*Deltat))) + (N235Ut*sf235U*Y235to135Xe*Phit*Deltat)+(N238Ut*sf238U*Y238to135Xe*Phit*Deltat)+(N239Put*sf239Pu*Y239to135Xe*Phit*Deltat) - (Lambda135Xe*N135Xet*Deltat)
        N135Xe.append(N135Xet_t)
        
        N143Ndt_t = (N143Ndt*(1-(sa143Nd*Phit*Deltat))) + (N235Ut*sf235U*Y235to143Nd*Phit*Deltat)+(N238Ut*sf238U*Y238to143Nd*Phit*Deltat)+(N239Put*sf239Pu*Y239to143Nd*Phit*Deltat)
        N143Nd.append(N143Ndt_t)
        
        N148Pmt_t = (N148Pmt*(1-(sa148Pm*Phit*Deltat))) + (N235Ut*sf235U*Y235to148Pm*Phit*Deltat)+(N238Ut*sf238U*Y238to148Pm*Phit*Deltat)+(N239Put*sf239Pu*Y239to148Pm*Phit*Deltat) - (Lambda148Pm*N148Pmt*Deltat)
        N148Pm.append(N148Pmt_t)
        
        N149Smt_t = (N149Smt*(1-(sa149Sm*Phit*Deltat))) + (N235Ut*sf235U*Y235to149Sm*Phit*Deltat)+(N238Ut*sf238U*Y238to149Sm*Phit*Deltat)+(N239Put*sf239Pu*Y239to149Sm*Phit*Deltat)
        N149Sm.append(N149Smt_t)
        
        N151Smt_t = (N151Smt*(1-(sa151Sm*Phit*Deltat))) + (N235Ut*sf235U*Y235to151Sm*Phit*Deltat)+(N238Ut*sf238U*Y238to151Sm*Phit*Deltat)+(N239Put*sf239Pu*Y239to151Sm*Phit*Deltat) - (Lambda151Sm*N151Smt*Deltat)
        N151Sm.append(N151Smt_t)
        
        N152Eut_t = (N152Eut*(1-(sa152Eu*Phit*Deltat))) + (N235Ut*sf235U*Y235to152Eu*Phit*Deltat)+(N238Ut*sf238U*Y238to152Eu*Phit*Deltat)+(N239Put*sf239Pu*Y239to152Eu*Phit*Deltat) - (Lambda152Eu*N152Eut*Deltat)
        N152Eu.append(N152Eut_t)
        
        N153Gat_t = (N153Gat*(1-(sa153Ga*Phit*Deltat))) + (N235Ut*sf235U*Y235to153Ga*Phit*Deltat)+(N238Ut*sf238U*Y238to153Ga*Phit*Deltat)+(N239Put*sf239Pu*Y239to153Ga*Phit*Deltat) - (Lambda153Ga*N153Gat*Deltat)
        N153Ga.append(N153Gat_t)
        
        N154Gat_t = (N154Gat*(1-(sa154Ga*Phit*Deltat))) + (N235Ut*sf235U*Y235to154Ga*Phit*Deltat)+(N238Ut*sf238U*Y238to154Ga*Phit*Deltat)+(N239Put*sf239Pu*Y239to154Ga*Phit*Deltat)
        N154Ga.append(N154Gat_t)
        
        N155Gat_t = (N155Gat*(1-(sa155Ga*Phit*Deltat))) + (N235Ut*sf235U*Y235to155Ga*Phit*Deltat)+(N238Ut*sf238U*Y238to155Ga*Phit*Deltat)+(N239Put*sf239Pu*Y239to155Ga*Phit*Deltat)
        N155Ga.append(N155Gat_t)
        
        N157Gat_t = (N157Gat*(1-(sa157Ga*Phit*Deltat))) + (N235Ut*sf235U*Y235to157Ga*Phit*Deltat)+(N238Ut*sf238U*Y238to157Ga*Phit*Deltat)+(N239Put*sf239Pu*Y239to157Ga*Phit*Deltat)
        N157Ga.append(N157Gat_t)
        
        N83Krt  = N83Krt_t
        N113Cdt = N113Cdt_t
        N133Xet = N133Xet_t
        N135Xet = N135Xet_t
        N143Ndt = N143Ndt_t
        N148Pmt = N148Pmt_t
        N149Smt = N149Smt_t
        N151Smt = N151Smt_t
        N152Eut = N152Eut_t
        N153Gat = N153Gat_t
        N154Gat = N154Gat_t
        N155Gat = N155Gat_t
        N157Gat = N157Gat_t
        N235Ut = N235Ut_t
        N238Ut = N238Ut_t
        N239Npt = N239Npt_t
        N239Put = N239Put_t
        N240Put = N240Put_t
        
        Phit = (P*1e6*6.25e12) / (200*((N235Ut_t*sf235U)+(N238Ut_t*sf238U)+(N239Npt_t*sf239Np)+(N239Put_t*sf239Pu)+(N240Put_t*sf240Pu)
        -(N83Krt_t*sa83Kr)-(N113Cdt_t*sa113Cd)-(N133Xet_t*sa133Xe)-(N135Xet_t*sa135Xe)-(N143Ndt_t*sa143Nd)-(N148Pmt_t*sa148Pm)-(N149Smt_t*sa149Sm)-(N151Smt_t*sa151Sm)-(N152Eut_t*sa152Eu)-(N153Gat_t*sa153Ga)-(N154Gat_t*sa154Ga)-(N155Gat_t*sa155Ga)-(N157Gat_t*sa157Ga)))
        Phi.append(Phit)
        
    
        t.append(time)
        time = time + Deltat
        if a == int(((Time*86400)/Deltat)/4):
            print('25% Completed...')
        if a == int(2*((Time*86400)/Deltat)/4):
            print('50% Completed...')
        if a == int(3*((Time*86400)/Deltat)/4):
            print('75% Completed...')
    
    print('100% Completed.')       
    m235U = np.array(N235U)
    m238U = np.array(N238U)
    m239Np = np.array(N239Np)
    m239Pu = np.array(N239Pu)
    m240Pu = np.array(N240Pu)
    
    M235U = ((m235U*235.044) /(6.022e23*1000))
    M238U = ((m238U*238.029) /(6.022e23*1000))
    M239Np = ((m239Np*239.053) /(6.022e23*1000))
    M239Pu = ((m239Pu*239.052) /(6.022e23*1000))
    M240Pu = ((m240Pu*240.054) /(6.022e23*1000))

    Phiplot = np.array(Phi)
    Ratio240239 = M240Pu/M239Pu 
    tplot = np.array(t)/86400 #[t in days]

    
    return {'time': tplot,
            'U235': M235U,
            'U238': M238U,
            'Np239': M239Np,
            'Pu239': M239Pu,
            'Pu240': M240Pu,
           }
    

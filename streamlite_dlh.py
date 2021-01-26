# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 18:12:30 2021

@author: peter.r
"""

import streamlit as st
import numpy as np
import pandas as pd
import math

st.title('Dostala by firma úver?')

# nacitaj data a vyber firmu
@st.cache
def load_data():
    data = pd.read_excel("ds_nc1.xlsx")
    return data

data = load_data()

firma = st.selectbox(
    'Vyber firmu',
    data['nazov'].unique())

df = data[data["nazov"] == firma]
df.reset_index(inplace = True)
# vypocet na

PVK = df.loc[0, 'SVK']
DEBTtoEBITDA = df.loc[0, 'DTE']
DSCR = df.loc[0, 'DS']
EquityRatio = df.loc[0, 'ER']
maxUver = df.loc[0, 'maxUV']
# min(df.loc[0,'maxUverDtE'], df.loc[0,'maxUverDSCR'], df.loc[0,'maxUverEquity'])

# what if one variable is nan?
if math.isnan(DSCR):
    DSCR = 0
if math.isnan(DEBTtoEBITDA):
    DEBTtoEBITDA = 0
if math.isnan(EquityRatio):
    EquityRatio = 0

k = [df.loc[0,"maxUverDtE"], df.loc[0,'maxUverDSCR'], df.loc[0,'maxUverEquity']]
k = k.index(min(k)) # hlavne krit

test = [DEBTtoEBITDA < 5, DSCR < 1.2, EquityRatio < 0.08]


if (PVK < 0.08) | (maxUver < 0) | all(test):
    #kr
    "NIE - spoločnosť " + firma + " by nedostala úver."
    "Niečo vo vašom účtovníctve je potrebné zmeniť."
    
    if st.button('Zisti prečo'):
        if (PVK < 0.08):
            "Spoločnosť "+ firma +" má podľa výsledkov za rok 2019 pomer vlastného imania ku záväzkom menej ako 8% a nachádza sa v kríze (v zmysle zákona č. 513/1991 Zb. Obchodného zákonníka § 67a až 67i )."

            "Aby sa spoločnosť dostala z krízy, potrebuje buď zvýšiť svoje vlastné imanie alebo znížiť svoje záväzky. Ak máte záujem o konzultáciu v tejto oblasti, sme Vám k dispozícii"
        else:
            if k == 0:
                "Podľa účtovných výkazov za rok 2019 je pomer dlhu k EBITDA spoločnosti vyšší ako 5. Banky nebudú chcieť spoločnosti požičať, buď z dôvodu už vysokého zadĺženia, alebo z dôvodu nízkej ziskovosti. Ak spoločnosť chce získať úver, musí zvýšiť EBITDA, teda zisk pred zdanením, odpismi a úrokmi."
                "Ak  máte záujem o konzultáciu v tejto oblasti, sme Vám k dispozícii"
            elif k == 1:
                "Podľa účtovných výkazov za rok 2019 je ukazovateľ DSCR (Debt Service Coverage Ratio) spoločnosti na úrovni menší ako 1,2. Banky nebudú chcieť spoločnosti požičať, keďže výška splátok existujúcich úverov a lízingov spoločnosti v pomere k EBITDA nedovoľuje spoločnosti splácať ešte vyššie splátky ako doposiaľ. Ak spoločnosť chce získať financovanie musí zvýšiť EBITDA, teda zisk pred zdanením, odpismi a úrokmi alebo znížiť dlhovú službu, teda sumu splátok úverov a lízingov."
                "Ak  máte záujem o konzultáciu v tejto oblasti, sme Vám k dispozícii"
    
            elif k == 2:
                "Podľa účtovných výkazov za rok 2019 je pomer vlastného imania k aktívam spoločnosti na úrovni " + str(EquityRatio) + " Tento ukazovateľ nie je kritický, no je ďaleko o ideálu. Banky neradi požičiavajú firmám s ukazovateľom nižším ako 0,2. S dobre napísaným busines plánom však firma pri žiadosti o úver môže uspieť."
                "Ak  máte záujem o konzultáciu v tejto oblasti, sme Vám k dispozícii"
            else:
                "Toto by nemalo nastať."
        "Ponuka telefonickej konzultácie 39,90€+DPH alebo poradenstva pri napísaní business plánu pre banku a získaní úveru"
    
else:
    "ANO - spoločnosť " + firma + " by dostala úver."
    "Maximálne celkové úverové zadĺženie s 5-ročnou splatnosťou môže byť " + str(maxUver) + " euro"
    if st.button('Zisti viac o možnosti získať úver.'):
        if (~np.isnan(df.loc[0,"zv115"]) | (~np.isnan(df.loc[0,"zv135"]))):
            # existuje hodnota
             pass # co srpavit s hodnotami
        else:
            "Zadaj doplňujúce údaje o firme:"
            x = st.text_input(label="Suma lízingov")
            y = st.text_input(label="Suma mesačných lízingových plátok")
    
            "Maximálne celkové úverové zadĺženie s 5-ročnou splatnosťou môže byť " + str(maxUver) + " Kde najdem vypocet?"

        if k == 0:
            "Podľa účtovných výkazov za rok 2019 je pomer dlhu k EBITDA spoločnosti na úrovni " + str(DEBTtoEBITDA) + "-násobku. Tento ukazovateľ je hraničným pre určenie maximálnej zadženosti. Ak chcete väčší úver ako " + str(maxUver) + " eur, musíte zvýšiť EBITDA, teda zisk pred zdanením, odpismi a úrokmi.\n"
            
            "Ak  máte záujem o konzultáciu v tejto oblasti, sme Vám k dispozícii"
        elif k == 1:
            "Podľa účtovných výkazov za rok 2019 je ukazovateľ DSCR* (miera pokrytia dlhovej služby) spoločnosti na úrovni " + str(DSCR) + " Tento ukazovateľ je hraničným pre určenie maximálnej zadĺženosti. Ak chcete väčší úver ako " + str(maxUver) + " musíte zvýšiť EBITDA, teda zisk pred zdanením, odpismi a úrokmi alebo znížiť dlhovú službu, teda sumu splátok úverov a lízingov."

        elif k == 2:
            "Podľa účtovných výkazov za rok 2019 je pomer vlastného imania k aktívam spoločnosti na úrovni " + str(EquityRatio) + ". Tento ukazovateľ je hraničným pre určenie maximálnej zadženosti. Ak chcete väčší úver ako " + str(maxUver) + " mali by ste zvýšiť vlastné imanie alebo znížiť celkové aktíva."

        else:
            "Ani jedna podmienka"
            
        "Ponuka telefonickej konzultácie 39,90€+DPH alebo poradenstva pri napísaní business plánu pre banku a získaní úveru"
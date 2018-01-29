from load_postbank_umsätze import Load as LoadPostbank
from load_dkb_giro_umsätze import Load as LoadDKBGiro
from load_dkb_umsätze import Load as LoadDKB
from load_init import Load as LoadInit

loadInit = LoadInit()
loadInit.load_data()

loadPostbank = LoadPostbank()
loadPostbank.load_data()

loadDKBGiro = LoadDKBGiro()
loadDKBGiro.load_data()

loadDKB = LoadDKB()
loadDKB.load_data()
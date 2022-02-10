# Yapay sinir ağları
import math

girdiler = (10,30,20)
ciktilar = (1, 0)


Output_Adet = len(ciktilar)
Input_Adet = len(girdiler)
Hidden_Adet = 2


w = {
    'I1-H1':0.2,
    'I1-H2':0.7,
    'I2-H1':-0.1,
    'I2-H2':-1.2,
    'I3-H1':0.4,
    'I3-H2':1.2,
    'H1-O1':1.1,
    'H1-O2':3.1,
    'H2-O1':0.1,
    'H2-O2':1.17
    }
	

class HiddenNode():
    def __init__(self, no, girdi, w):
        self.girdi = girdi
        self.w = w
        self.no = no
        self.isim = 'H%s' % (self.no+1,)
        
    def fNet(self):
        """top = 0
        for i in range(len(self.girdi)):
            top = top + self.girdi[i] * self.w[i]
        self.toplam = top"""
        
        self.toplam = sum(x*y for x,y in zip(self.girdi, self.w))
        
    def sigmoid(self):
        self.fNet()
        self.cikti = 1/(1 + math.e ** (-self.toplam))

    def HataDegeriBul(self):
        toplam = 0
        for ou in O:
            key = self.isim + '-' + ou.isim
            toplam = toplam + w[key] * ou.hata
            #print('*'*20)
            #print('key:',key, 'w:', w[key], 'Hata:',ou.hata, 'toplam:',toplam)
                  
        
        self.hata = self.cikti * (1 - self.cikti) * toplam
        #print('HOPDEDİK:', self.cikti, self.hata, toplam)

class OutputNode(HiddenNode):
    def __init__(self, no, girdi, w, target):
        HiddenNode.__init__(self, no, girdi, w)
        
        self.target = target
        self.isim = self.isim.replace('H','O')
        

    def HataDegeriBul(self):
        self.hata = self.cikti * (1 - self.cikti) * (self.target - self.cikti)
        

def HiddenNodeHataBul(goster = False):
    for hd in H:
        hd.HataDegeriBul()

        if goster:
            print(hd.isim,': Hata=',hd.hata)

def InputHiddenAgirlikGuncelleme(goster = False):
    n_sabit = 0.1
    
    for i in range(len(girdiler)):
        for hd in H:
            key = 'I'+str(i+1)+'-'+hd.isim
            agirlik = w[key]
            delta = girdiler[i] * hd.hata * n_sabit
            agirlik = agirlik + delta
            w[key] = agirlik

            if goster:
                print('Key:',key, 'delta:',delta, 'Yeni Ağırlık:',agirlik)

def HiddenOutputAgirlikGuncelleme(goster = False):
    n_sabit = 0.1
    
    for hd in H:
        for ou in O:
            key = hd.isim + '-' + ou.isim
            agirlik = w[key]
            delta = hd.cikti * ou.hata * n_sabit
            agirlik = agirlik + delta
            w[key] = agirlik

            if goster:
                print('Key:',key, 'delta:',delta, 'Yeni Ağırlık:',agirlik)



    
H = []
for hd in range(Hidden_Adet):
    agirlik = []
    for i in range(Input_Adet):
        key = 'I%s-H%s' % (i+1, hd+1)
        #print('key:',key,w[key])
        agirlik.append(w[key])
        
    yeninode = HiddenNode(hd, girdiler, tuple(agirlik))
    yeninode.sigmoid()
    print('Cikti:',yeninode.cikti)
    H.append(yeninode)

O = []
for ou in range(Output_Adet):

    girdi = []
    for hd in H:
        girdi.append(hd.cikti)
        
    agirlik = []
    for hd in range(Hidden_Adet):
        key = 'H%s-O%s' % (hd+1, ou+1)
        agirlik.append(w[key])
        
    yeninode = OutputNode(ou, tuple(girdi), tuple(agirlik), ciktilar[ou])
    yeninode.sigmoid()
    yeninode.HataDegeriBul()
    print('Cikti:',yeninode.cikti)
    print('Hata Degeri:', yeninode.hata)
    O.append(yeninode)


HiddenNodeHataBul(True)
InputHiddenAgirlikGuncelleme(True)
HiddenOutputAgirlikGuncelleme(True)
print(w)

# Yapay sinir ağları
import math
import random
random.seed(111)

def wYap(input_node_adedi, hidden_node_adedi, output_node_adedi, goster=False):
    w = {}
    for i in range(input_node_adedi):
        for h in range(hidden_node_adedi):
            key = 'I%s-H%s' % (i+1, h+1)
            value = random.randrange(1,600)/10000
            w[key] = value

    for h in range(hidden_node_adedi):
        for o in range(output_node_adedi):
            key = 'H%s-O%s' % (h+1, o+1)
            value = random.randrange(1,600)/10000
            w[key] = value

    if goster:
        print()
        print('Ağırlık Tablosu:')
        l = sorted(w.keys())
        for i in l:
            print(i, w[i])
        
    return w
            
    
class HiddenNode():
    def __init__(self, no, girdi, w):
        self.girdi = girdi
        self.w = w
        self.no = no
        self.isim = 'H%s' % (self.no+1,)
        
    def sigmoid(self):
        self.fNet()
        self.cikti = 1/(1 + math.e ** (-self.toplam))


    def fNet(self):
        """top = 0
        for i in range(len(self.girdi)):
            top = top + self.girdi[i] * self.w[i]
        self.toplam = top"""
        
        self.toplam = sum(x*y for x,y in zip(self.girdi, self.w))
        

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
        

def HiddenNodelariYap():
    H = []
    for hd in range(Hidden_Adet):

        # Bu node için ağırlık değerlerini bul
        agirlik = []
        for i in range(Input_Adet):
            key = 'I%s-H%s' % (i+1, hd+1)
            #print('key:',key,w[key])
            agirlik.append(w[key])
            
        # HiddenNode sınıfından girdiler ve ağırlıklarla bir node oluştur
        yeninode = HiddenNode(hd, girdiler, tuple(agirlik))
        H.append(yeninode)

    return H

def OutputNodelariYap():
    O = []
    for ou in range(Output_Adet):

        # Hidden node cikti alanları Output'ların girdileridir.
        girdi = []
        for hd in H:
            girdi.append(hd.cikti)
            
        # Ağırlıkları bulalım
        agirlik = []
        for hd in range(Hidden_Adet):
            key = 'H%s-O%s' % (hd+1, ou+1)
            agirlik.append(w[key])
            
        target = ciktilar[ou]
        yeninode = OutputNode(ou, tuple(girdi), tuple(agirlik), target)
        
        O.append(yeninode)

    return O

def kes(sayi):
    s = '%10.6f' % sayi
    return s

def InputHiddenAgirlikGuncelleme(goster = False):
    n_sabit = 0.1
    
    for i in range(len(girdiler)):
        for hd in H:
            key = 'I'+str(i+1)+'-'+hd.isim
            agirlik = w[key]

            delta = girdiler[i] * hd.hata * n_sabit

            yeni_agirlik = agirlik + delta

            w[key] = yeni_agirlik

            if goster:
                print(key, 'delta:', kes(delta),' Ağırlık: Eski',kes(agirlik),'\tYeni:', kes(yeni_agirlik))
                
                
def HiddenOutputAgirlikGuncelleme(goster = False):
    n_sabit = 0.1
    
    for hd in H:
        for ou in O:
            key = hd.isim + '-' + ou.isim
            agirlik = w[key]

            delta = hd.cikti * ou.hata * n_sabit

            yeni_agirlik = agirlik + delta
            
            w[key] = yeni_agirlik

            if goster:
                print(key, 'delta:', kes(delta),' Ağırlık: Eski',kes(agirlik),'\tYeni:', kes(yeni_agirlik))
                


def w_Degisim_Guncelleme():
    for k,v in w.items():
        val_list = w_Degisim[k]
        val_list.append(v)
        w_Degisim[k] = val_list
        
def w_Degisim_Bas(d,mesaj=' '):
    print()
    print(mesaj)
    sira_list = sorted(d)
    for k in sira_list:
        #value_list = ['%8.4f' %(x,) for x in d[k]]
        value_list = ['%5.0f' %(x*1000,) for x in d[k]]
        print(k, '=>',','.join(value_list))
    
# Program başlangıcı
test = 2                # 1: 3 girdili test, 2:7 girdili test


if test == 1:

    # Girdi ve çıktı
    iterasyonlar = (
                    ((10,30,20),(1,0)),

                    )
    sorgular = (
                ((10,30,20),('?','?')),
                )
    
    girdi_adedi = len(iterasyonlar[0][0])
    cikti_adedi=  len(iterasyonlar[0][1])

    # Hidden Node sayısı
    Hidden_Adet = 2

    # Ağırlık tablosu
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
    
else:
    # Girdi ve çıktılar
    iterasyonlar = (
                    ((1,1,1,1,1,1,0),(0,0,0)),
                    ((0,1,1,0,0,0,0),(0,0,1)),
                    ((1,1,0,1,1,0,1),(0,1,0)),
                    ((1,1,1,1,0,0,1),(0,1,1)),
                    ((0,1,1,0,0,1,1),(1,0,0)),
                    ((1,0,1,1,0,1,1),(1,0,1)),
                    ((1,0,1,1,1,1,1),(1,1,0)),
                    ((1,1,1,0,0,0,0),(1,1,1)),
                    )

    sorgular = (
                    ((1,1,1,1,1,1,0),(0,0,0)),
                    ((0,1,1,0,0,0,0),(0,0,1)),
                    )



    girdi_adedi = len(iterasyonlar[0][0])
    cikti_adedi=  len(iterasyonlar[0][1])

    # Hidden Node sayısı
    Hidden_Adet = 4

    # Ağırlık taplosu
    w = wYap(girdi_adedi, Hidden_Adet, cikti_adedi, True)
    


# Ağırlık tablosu değişimleri bu sözlükte tutulacak
w_Degisim = {key:[val] for key,val in w.items()}

for i in iterasyonlar:
    girdiler = i[0]
    ciktilar = i[1]
    
    
    Output_Adet = len(ciktilar)
    Input_Adet = len(girdiler)
    

    # Hidden node'ları oluştur ve çıktılarını bul
    H = HiddenNodelariYap()
    # çıktılarılarını bul
    for hd in H:
        hd.sigmoid()
        #print(hd.isim,'--> cikti:',kes(hd.cikti))

    # Output node'ları oluştur
    O = OutputNodelariYap()
    # Output Node'larının çıktıları bul
    for ou in O:
        ou.sigmoid()
        #print(ou.isim,'--> cikti:',kes(ou.cikti))

    # Output Node'larının hatalarını bul
    for ou in O:
        ou.HataDegeriBul()
        #print(ou.isim,'--> hata :',kes(ou.hata))
        
    # Hidden node'larının hatalarını bul
    for hd in H:
        hd.HataDegeriBul()
        #print(hd.isim,'--> hata :',kes(hd.hata))

    
    InputHiddenAgirlikGuncelleme(False)
    HiddenOutputAgirlikGuncelleme(False)
    w_Degisim_Guncelleme()

w_Degisim_Bas(w_Degisim,'w_Değişim Tablosu( x 1000)')

for ou in O:
    print(ou.isim,'--> cikti:',kes(ou.cikti))

# Sorgu işlemleri

for i in sorgular:
    girdiler = i[0]
    ciktilar = i[1]
    
    
    Output_Adet = len(ciktilar)
    Input_Adet = len(girdiler)
    

    # Hidden node'ları oluştur ve çıktılarını bul
    H = HiddenNodelariYap()
    # çıktılarılarını bul
    for hd in H:
        hd.sigmoid()
        #print(hd.isim,'--> cikti:',kes(hd.cikti))

    # Output node'ları oluştur
    O = OutputNodelariYap()
    # Output Node'larının çıktıları bul

    print()
    print('SORGU SONUÇLARI:')
    for ou in O:
        ou.sigmoid()
        print(ou.isim,'--> cikti:',kes(ou.cikti))


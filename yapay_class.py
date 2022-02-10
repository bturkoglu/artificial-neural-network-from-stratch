# Yapay sinir ağları
import math
import random

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
        
class Yapay():
    def __init__(self,input_node_adedi, hidden_node_adedi, output_node_adedi):
        
        self.input_node_adedi  = input_node_adedi
        self.hidden_node_adedi = hidden_node_adedi
        self.output_node_adedi = output_node_adedi

        self.girdiler = tuple()
        self.ciktilar = tuple()
        
        self.w = {}
        self.H = []
        self.O = []
        
        self.n_sabit = 0.1
        

    def HiddenNodelariYap(self):
        H = []
        for hd in range(self.hidden_node_adedi):

            # Bu node için ağırlık değerlerini bul
            agirlik = []
            for i in range(self.input_node_adedi):
                key = 'I%s-H%s' % (i+1, hd+1)
                #print('key:',key,w[key])
                agirlik.append(w[key])
                
            # HiddenNode sınıfından girdiler ve ağırlıklarla bir node oluştur
            yeninode = HiddenNode(hd, self.girdiler, tuple(agirlik))
            H.append(yeninode)

        self.H = H

    def OutputNodelariYap(self):
        O = []
        for ou in range(self.output_node_adedi):

            # Hidden node cikti alanları Output'ların girdileridir.
            girdi = []
            for hd in H:
                girdi.append(hd.cikti)
                
            # Ağırlıkları bulalım
            agirlik = []
            for hd in range(self.hidden_node_adedi):
                key = 'H%s-O%s' % (hd+1, ou+1)
                agirlik.append(w[key])
                
            target = self.ciktilar[ou]
            yeninode = OutputNode(ou, tuple(girdi), tuple(agirlik), target)
            
            O.append(yeninode)

        self.O = O

    def kes(self, sayi):
        s = '%10.6f' % sayi
        return s                    

    def InputHiddenAgirlikGuncelleme(self, goster = False):
                
        for i in range(self.input_node_adedi):
            for hd in self.H:
                key = 'I'+str(i+1)+'-'+hd.isim
                agirlik = self.w[key]

                delta = self.girdiler[i] * hd.hata * self.n_sabit

                yeni_agirlik = agirlik + delta

                self.w[key] = yeni_agirlik

                if goster:
                    print(key, 'delta:', kes(delta),' Ağırlık: Eski',
                          kes(agirlik),'\tYeni:', kes(yeni_agirlik))
                    
                    
    def HiddenOutputAgirlikGuncelleme(self, goster = False):
        
        for hd in self.H:
            for ou in self.O:
                key = hd.isim + '-' + ou.isim
                agirlik = self.w[key]

                delta = hd.cikti * ou.hata * self.n_sabit

                yeni_agirlik = agirlik + delta
                
                self.w[key] = yeni_agirlik

                if goster:
                    print(key, 'delta:', kes(delta),' Ağırlık: Eski',
                          kes(agirlik),'\tYeni:', kes(yeni_agirlik))
                    

if __name__ == '__main__':

    random.seed(111)
        
    def randomUret():
        return random.randrange(1,600)/10000
    
    def wYap(input_node_adedi, hidden_node_adedi, output_node_adedi, goster=False):
        w = {}
        for i in range(input_node_adedi):
            for h in range(hidden_node_adedi):
                key = 'I%s-H%s' % (i+1, h+1)
                value = randomUret()
                w[key] = value

        for h in range(hidden_node_adedi):
            for o in range(output_node_adedi):
                key = 'H%s-O%s' % (h+1, o+1)
                value = randomUret()
                w[key] = value

        if goster:
            print()
            print('Ağırlık Tablosu:')
            l = sorted(w.keys())
            for i in l:
                print(i, w[i])
            
        return w



    def testDatasi(testNo):
        if testNo == 1:
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

            elif testNo == 2:
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
                
           return iterasyonlar, sorgular, girdi_adedi, cikti_adedi, Hidden_Adet, w

        
    iterasyonlar, sorgular, girdi_adedi, cikti_adedi, Hidden_Adet, w = testDatasi(2)


    

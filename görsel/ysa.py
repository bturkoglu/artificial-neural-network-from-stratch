# Yapay sinir ağları
import math
import random
random.seed(111)
import os.path
import sys

class HNode():
    def __init__(self, no):
        self.no = no
        self.isim = 'H%s' % (self.no+1,)

        self.toplam = 0
        self.cikti  = 0
        self.hata   = 0
        
    def sigmoid(self, girdiler, wtablo):
        self.fNet(girdiler, wtablo)
        self.cikti = 1/(1 + math.e ** (-self.toplam))
        
    def fNet(self, girdiler, wtablo):
        top = 0
        for i in range(len(girdiler)):
            key = 'I%s-%s' % (i+1, self.isim)
            top = top + girdiler[i] * wtablo[key]
        self.toplam = top

    def hataDegeriBul(self, outputnodlar, wtablo):
        toplam = 0
        for ou in outputnodlar:
            key = self.isim + '-' + ou.isim
            toplam = toplam + wtablo[key] * ou.hata
            #print('*'*20)
            #print('key:',key, 'w:', wtablo[key], 'Hata:',ou.hata, 'toplam:',toplam)

        self.hata = self.cikti * (1 - self.cikti) * toplam
        #print('HOPDEDİK:', self.cikti, self.hata, toplam)



class ONode():
    def __init__(self, no):
        self.no = no
        self.isim = 'O%s' % (self.no+1,)

        self.toplam = 0
        self.cikti  = 0
        self.hata   = 0
        
    def sigmoid(self, hiddennodlar, wtablo):
        self.fNet(hiddennodlar, wtablo)
        self.cikti = 1/(1 + math.e ** (-self.toplam))
        
    def fNet(self, hiddennodlar, wtablo):
        top = 0
        for hd in hiddennodlar:
            key = '%s-%s' % (hd.isim, self.isim)
            top = top + hd.cikti * wtablo[key]
        self.toplam = top

    def hataDegeriBul(self, ciktilar):
        target = ciktilar[self.no]
        self.hata = self.cikti * (1 - self.cikti) * (target - self.cikti)
        



class Yapay:
    def __init__(self, Input_Adet=7, Output_Adet=3, Hidden_Adet=4):
        self.Input_Adet  = Input_Adet
        self.Output_Adet = Output_Adet
        self.Hidden_Adet = Hidden_Adet

        self.w = {}
        self.w_min = 1
        self.w_max = 600
        self.w_bolen = 10000
        self.w_degisim = {}
        
        self.n_sabit = 0.1

        self.hazir_agirlik_tablosu = ''
        
        self.Hidden = []
        self.Output = []
        
        self.girdiler = ()
        self.ciktilar = ()
        
        self.nodelariYap()

    def nodelariYap(self):
        for h in range(self.Hidden_Adet):
            node = HNode(h)
            self.Hidden.append(node)
        for o in range(self.Output_Adet):
            node = ONode(o)
            self.Output.append(node)

    def ogren(self, girdiler, ciktilar):
        self.girdiler = girdiler
        self.ciktilar = ciktilar
        
        # Hidden node çıktılarını bul
        for hd in self.Hidden:
            hd.sigmoid(girdiler, self.w)
            #print(hd.isim,'--> cikti:',kes(hd.cikti))

        # Output node çıktılarını bul
        for ou in self.Output:
            ou.sigmoid(self.Hidden, self.w)
            #print(ou.isim,'--> cikti:',kes(ou.cikti))

        # Output Node'larının hatalarını bul
        for ou in self.Output:
            ou.hataDegeriBul(ciktilar)
            #print(ou.isim,'--> hata :',kes(ou.hata))

        # Hidden node'larının hatalarını bul
        for hd in self.Hidden:
            hd.hataDegeriBul(self.Output, self.w)
            #print(hd.isim,'--> hata :',kes(hd.hata))

        # Ağırlık tablosunu güncelle
        self.agirlik_Guncelle_I_H()
        self.agirlik_Guncelle_H_O()

    def sorgula(self, girdiler):
        # Hidden node çıktılarını bul
        for hd in self.Hidden:
            hd.sigmoid(girdiler, self.w)
            #print(hd.isim,'--> cikti:',kes(hd.cikti))

        # Output node çıktılarını bul
        st=''
        mesaj = ''
        for ou in self.Output:
            ou.sigmoid(self.Hidden, self.w)
            mesaj = mesaj + '%s --> çıktı:%s \n' % (ou.isim, ou.cikti)
            print(ou.isim,'--> cikti:',ou.cikti)
            st = st + str(int(round(ou.cikti,0)))

        goruntu = hex(int(st,2))[-1]
        goruntu = goruntu.upper()
        if goruntu in ('BD'):
            goruntu = goruntu.lower()
        mesaj += 'Sonuç: (%s) : %s --> %s\n\n' % (st, int(st,2),goruntu)
        print(mesaj)
        return mesaj
                    
    def agirlik_Guncelle_I_H(self, goster = False):
               
        for i in range(len(self.girdiler)):
            for hd in self.Hidden:
                key = 'I%s-%s' % (i+1, hd.isim)
                agirlik = self.w[key]

                delta = self.girdiler[i] * hd.hata * self.n_sabit

                yeni_agirlik = agirlik + delta

                self.w[key] = yeni_agirlik

                if goster:
                    print(key, 'delta:', kes(delta),' Ağırlık: Eski',
                          kes(agirlik),'\tYeni:', kes(yeni_agirlik))
                        
    def agirlik_Guncelle_H_O(self, goster = False):
        for hd in self.Hidden:
            for ou in self.Output:
                key = hd.isim + '-' + ou.isim
                agirlik = self.w[key]

                delta = hd.cikti * ou.hata * self.n_sabit

                yeni_agirlik = agirlik + delta
                
                self.w[key] = yeni_agirlik

                if goster:
                    print(key, 'delta:', kes(delta),' Ağırlık: Eski',
                          kes(agirlik),'\tYeni:', kes(yeni_agirlik))
            

    def agirlikTablosuUret(self, goster=False):
        w = {}
        for i in range(self.Input_Adet):
            for h in self.Hidden:
                key = 'I%s-%s' % (i+1, h.isim)
                value = random.randrange(self.w_min, self.w_max)/self.w_bolen
                w[key] = value
                
        for h in self.Hidden:
            for o in self.Output:
                key = '%s-%s' % (h.isim, o.isim)
                value = random.randrange(self.w_min, self.w_max)/self.w_bolen
                w[key] = value
                
        if goster:
            print()
            print('Ağırlık Tablosu:')
            l = sorted(w.keys())
            for i in l:
                print(i, w[i])
            
        return w

    def agirlikTablosuOku(self, goster = False):
        w= {}
        isim = self.hazir_agirlik_tablosu
        
        with open(isim, 'r') as f:
            for line in f:
                st = line.strip().partition('\t')
                key = st[0].strip()
                value = float(st[2])
                w[key] = value

        if goster:
            print()
            print('Ağırlık Tablosu:')
            l = sorted(w.keys())
            for i in l:
                print(i, w[i])

        # Okunan tablodan node sayılarını bulalım.
        input_adet  = len(set([k.partition('-')[0] for k in w if k.startswith('I')]))
        hidden_adet = len(set([k.partition('-')[0] for k in w if k.startswith('H')]))
        output_adet = len(set([k.partition('-')[2] for k in w if k.startswith('H')]))
        print('I:',input_adet, 'H:',hidden_adet,'O:',output_adet)
        self.__init__(input_adet, output_adet, hidden_adet)
        self.w = w

##class W_Degisim:
##    def __init__(self, isim, w):
##        self.isim = isim
##        self.w_Degisim = {key:[val] for key,val in w.items()}
##
##    def Guncelle(self, w):
##        for k,v in w.items():
##            val_list = self.w_Degisim[k]
##            val_list.append(v)
##            self.w_Degisim[k] = val_list
##            
##    def Bas(self,mesaj=' '):
##        print()
##        print(mesaj)
##        sira_list = sorted(self.w_Degisim)
##        for k in sira_list:
##            #value_list = ['%8.4f' %(x,) for x in self.w_Degisim[k]]
##            value_list = ['%5.0f' %(x*1000,) for x in self.w_Degisim[k]]
##            print(k, '=>',','.join(value_list))
##
##    def Sakla(self):
##        sira_list = sorted(self.w_Degisim)
##        with open(self.isim, 'w') as f:
##            
##            for k in sira_list:
##                #value_list = ['%8.4f' %(x,) for x in self.w_Degisim[k]]
##                value_list = ['%5.0f' %(x*1000,) for x in self.w_Degisim[k]]
##                line = '%s => %s \n' % (k, '\t'.join(value_list))
##                f.write(line)
##
##    def agirlik_Degisim_Sakla(self, isim_ek, wTablo):
##
##        isim = 'w_Degis'+isim_ek
##        
##        sira_list = sorted(wTablo)
##        if os.path.isfile(isim) == False:
##            # Dosya yok. Başlıkları yazarak oluşturalım.
##            with open(isim,'w') as f:
##                st = ''
##                for k in sira_list:
##                    st = st + '%s \t' % k
##                st = st + '\n'
##                f.write(st)
##        
##        
##        with open(isim, 'a') as f:
##            st = ''
##            for k in sira_list:
##                st = st + '%5.0f\t' % (wTablo[k]*1000)
##            st = st + '\n'
##            f.write(st)
##
##
##
##    def agirlik_Tablosu_Sakla(self, isim_ek, wTablo):
##
##        isim = 'Agirlik' + isim_ek
##        
##        sira_list = sorted(wTablo)
##        with open(isim, 'w') as f:
##            
##            for k in sira_list:
##                line = '%s \t %s \n' % (k, wTablo[k])
##                f.write(line)
##        
##    def agirlik_Degisim_incele(self, isim_ek):
##        isim_kaynak = 'w_Degis'+isim_ek
##        isim_hedef = 'w_Degis_oran' + isim_ek
##
##        #Başlık satırını ve ilk satırı okuyup, hedefe aynen yazalım.
##        hedef = open(isim_hedef,'w')
##        
##        with open(isim_kaynak,'r') as f:
##            baslik   = f.readline()
##            ilksatir = f.readline()
##
##            ilksatir_liste = ilksatir.strip().split('\t')
##            onceki_value = [int(i) for i in ilksatir_liste]
##            adet = len(onceki_value)
##            
##            hedef.write(baslik)
##            hedef.write(ilksatir)
##            for line in f:
##                satir = [int(i) for i in line.strip().split('\t')]
##                degisim = [x[0]-x[1] for x in zip(satir, onceki_value)]
##                yenisatir = ''.join(['%5s\t'% x for x in degisim])+'\n'
##
##                hedef.write(yenisatir)
##                onceki_value = satir

class Destek:
    def egitimKumesiOku(self, dosyaismi, goster=False):
        tamami = []
        with open(dosyaismi,'r') as f:
            for line in f:
                l=line.strip().partition('\t')
                girdi = tuple(l[0].split(','))
                cikti = tuple(l[2].split(','))
                tamami.append((girdi,cikti))
        tamami = tuple(tamami)

        inputNodeAdedi  = len(tamami[0][0])
        outputNodeAdedi = len(tamami[0][1])
        
        if goster:
            print('Eğitim Kümesi:')
            print('input Node:%s, output Node:%s' % (inputNodeAdedi, outputNodeAdedi))
            for i in tamami:
                print('\t',i)
            print()

        return inputNodeAdedi, outputNodeAdedi, tamami
            
    def agirlik_Degisim_Sakla(self, isim_ek, wTablo):

        isim = 'w_Degis'+isim_ek
        
        sira_list = sorted(wTablo)
        if os.path.isfile(isim) == False:
            # Dosya yok. Başlıkları yazarak oluşturalım.
            with open(isim,'w') as f:
                st = ''
                for k in sira_list:
                    st = st + '%s \t' % k
                st = st + '\n'
                f.write(st)
        
        
        with open(isim, 'a') as f:
            st = ''
            for k in sira_list:
                st = st + '%5.0f\t' % (wTablo[k]*1000)
            st = st + '\n'
            f.write(st)



    def agirlik_Tablosu_Sakla(self, isim_ek, wTablo):

        isim = 'Agirlik' + isim_ek
        
        sira_list = sorted(wTablo)
        with open(isim, 'w') as f:
            
            for k in sira_list:
                line = '%s \t %s \n' % (k, wTablo[k])
                f.write(line)
        
    def agirlik_Degisim_incele(self, isim_ek):
        isim_kaynak = 'w_Degis'+isim_ek
        isim_hedef = 'w_Degis_oran' + isim_ek

        #Başlık satırını ve ilk satırı okuyup, hedefe aynen yazalım.
        hedef = open(isim_hedef,'w')
        
        with open(isim_kaynak,'r') as f:
            baslik   = f.readline()
            ilksatir = f.readline()

            ilksatir_liste = ilksatir.strip().split('\t')
            onceki_value = [int(i) for i in ilksatir_liste]
            adet = len(onceki_value)
            
            hedef.write(baslik)
            hedef.write(ilksatir)
            for line in f:
                satir = [int(i) for i in line.strip().split('\t')]
                degisim = [x[0]-x[1] for x in zip(satir, onceki_value)]
                yenisatir = ''.join(['%5s\t'% x for x in degisim])+'\n'

                hedef.write(yenisatir)
                onceki_value = satir                
                
            
            
if __name__ == '__main__':
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
                    ((1,1,0,1,1,0,1),(0,1,0)),
                    ((1,1,1,1,0,0,1),(0,1,1)),
                    ((0,1,1,0,0,1,1),(1,0,0)),
                    ((1,0,1,1,0,1,1),(1,0,1)),
                    ((1,0,1,1,1,1,1),(1,1,0)),
                    ((1,1,1,0,0,0,0),(1,1,1)),
                     )



    

    input_adedi = len(iterasyonlar[0][0])
    output_adedi=  len(iterasyonlar[0][1])

    # Hidden Node sayısı
    Hidden_Adet = 4

    yp = Yapay(input_adedi, output_adedi, Hidden_Adet)

    #yp.hazir_agirlik_tablosu = ''
    yp.hazir_agirlik_tablosu = 'Agirlik_08.txt'
    
    if yp.hazir_agirlik_tablosu:
        # Ağırlık tablosu oku
        yp.agirlikTablosuOku(goster=False)

    else:
        
        # Ağırlık tablosu
        yp.w = yp.agirlikTablosuUret(goster=True)


    # Ağırlık değişim tablosu yap
    destek = Destek()


    state = 2       #state=1 öğren, state=2 sorgu, state=3 ağırlık değişim incele

    if state == 3:
        destek.agirlik_Degisim_incele('_08.txt')
        sys.exit('Degişim inceleme tablosu oluşturuldu.')

    if state == 1:
        import time
        start = time.time()
        
        grupdis = 100
        grupic  = 10000

        isim_ek = '_09.txt'
        
        for dis in range(grupdis):
            for ic in range(grupic):
                
                for i in iterasyonlar:
                    girdiler = i[0]
                    ciktilar = i[1]
                    yp.ogren(girdiler, ciktilar)

            destek.agirlik_Degisim_Sakla(isim_ek,yp.w)
            print('[',dis,'.dış:', int((time.time() - start)),'.sn]', end=' ')
            
        
        destek.agirlik_Tablosu_Sakla(isim_ek,yp.w)

        print()
        print('Bitis:(dis:%s ic:%s) %s sn.' % (dis,ic, (time.time() - start)))
        sys.exit('öğrenme tamamlandı.')

    if state == 2:
        for i in sorgular:
            girdiler = i[0]
            yp.sorgula(girdiler)
        sys.exit('Sorula tamamlandı.')

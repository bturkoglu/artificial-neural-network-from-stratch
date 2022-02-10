from tkinter import *
from ysa2 import Yapay

class Cizim(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.canvas_width = 720
        self.canvas_height = 620
        
        self.hesap = Yapay()
        self.agirlik_dosya_adi = 'Agirlik_04_03.txt'
        self.giris_bilgi = (('Ağırlık Dosya adı','agirlik_dosya_adi'),
                           )
        self.renk0 = '#f4f4f4'
        self.renk1 = '#80ff00'
        
        self.girisler = {}

        self.tuslar = {}
        
        self.tuslari_yap()


    def alanlari_oku(self):
        #Deneme başarılı
        for text, degisken in self.giris_bilgi:
            deger = self.girisler[text].get()
            deger = deger.strip()
            liste = degisken.split('.')
            if len(liste) > 1:
                v='self.'+'.'.join(liste[:-1])
            else:
                v = 'self'

            object.__setattr__(eval(v), liste[-1], deger)
      
    def tuslari_yap(self):
        #Ekranın soluna tuşlar için bir frame yapalım
        f = Frame(self, width=250,height = self.canvas_height, bd=8, relief=RAISED)
        f.pack(side=LEFT, fill=Y)
        
        # Entry'ler
        frmEntry = Frame(f, bd=3, relief=RAISED)
        frmEntry.pack(side=TOP)

        for text, data in self.giris_bilgi:
            lab = Label(frmEntry, text= text)
            ent = Entry(frmEntry, justify=CENTER, bd=3)
            ent.insert(0, eval('self.'+data))
            lab2 = Label(frmEntry, text= ' ')
            
            lab.pack(side=TOP)
            ent.pack(side=TOP,padx=5)
            lab2.pack(side=TOP)
            self.girisler[text] = ent


        #Butonlar
        frmButton = Frame(f, bd=3)
        frmButton.pack(side=TOP,pady= 10,fill=X)

        tus_bilgi = (('Tabloyu Oku', self.tabloOku,'normal'),
                      ('Temizle', self.temizlik, 'normal'),
                      ('Çıkış', self.quit,'normal'),
                      )

        self.tuslar = {}
        for text, metot, durum in tus_bilgi:
            b = Button(frmButton, text = text, command = metot, state=durum)
            b.pack(side=TOP, expand=YES, fill=X, pady=5)
            self.tuslar[text] = b
            
        # Ledler için ayrı bir frame tanımla

        frmLed = Frame(self, width=60, height = self.canvas_height, padx=10)
        frmLed.pack(side=LEFT, fill=Y)

        en = 1
        en2= 2
        boy = 10

        f = Frame(frmLed)
        f.pack(side=TOP)
        ort = dict(bg = self.renk0, relief=GROOVE)
        L1 = Button(f,text='L1', command = lambda:self.renkDegis('L1'), width=boy, height=en, **ort)
        L2 = Button(f,text='L2', command = lambda:self.renkDegis('L2'), width=en2, height=boy, **ort)
        L6 = Button(f,text='L6', command = lambda:self.renkDegis('L6'), width=en2, height=boy, **ort)
        L7 = Button(f,text='L7', command = lambda:self.renkDegis('L7'), width=boy, height=en, **ort)
        L3 = Button(f,text='L3', command = lambda:self.renkDegis('L3'), width=en2, height=boy, **ort)
        L5 = Button(f,text='L5', command = lambda:self.renkDegis('L5'), width=en2, height=boy, **ort)
        L4 = Button(f,text='L4', command = lambda:self.renkDegis('L4'), width=boy, height=en, **ort)

        L1.grid(row=0,column=0,columnspan=7)
        L6.grid(row=1,rowspan=6,column=0)
        L2.grid(row=1,rowspan=6,column=6)
        L7.grid(row=7,column=0,columnspan=7)
        L5.grid(row=8,rowspan=6,column=0)
        L3.grid(row=8,rowspan=6,column=6)
        L4.grid(row=14,column=0,columnspan=7)
        
        for i in (L1,L2,L3,L4,L5,L6,L7):
            self.tuslar[i['text']] = i
            i['fg'] = self.renk0
            i['text'] = ''
            
        # Sorgu tuşu frame'i
        frmSorgu = Frame(self, width=60, height = self.canvas_height, padx=10)
        frmSorgu.pack(side=LEFT, fill=Y)
        sorgu = Button(frmSorgu, text='Sorgula', command = self.sorgula, width = 10)
        sorgu.pack(expand=YES)

        #Sonuc göstermek için Text koyalım

        
        frmText = Frame(self, width=60, height = 30, padx=10)
        frmText.pack(side=LEFT, fill=Y)

        S = Scrollbar(frmText)
        
        t = Text(frmText, height=25, width= 40)
        S.pack(side=RIGHT, fill=Y)
        
        t.pack(side=LEFT, fill=Y)
        S.config(command=t.yview)
        t.config(yscrollcommand=S.set)
        
        self.tuslar['t'] = t
        

    def renkDegis(self, tus):

        b = self.tuslar[tus]
        if b['bg'] == self.renk0:
            b['fg'] = self.renk1
            b['bg'] = self.renk1
            
        else:
            b['fg'] = self.renk0
            b['bg'] = self.renk0
            
    def sorgula(self):
        sorgu = []
        for i in ('L1','L2','L3','L4','L5','L6','L7'):
            if self.tuslar[i]['bg'] == self.renk0:
                n = 0
            else:
                n = 1
            sorgu.append(n)
        print('sorgu:',sorgu)
        mesaj = self.hesap.sorgula(sorgu)
        t = self.tuslar['t']
        t.insert(END, mesaj)
    
    def tabloOku(self):
        self.alanlari_oku()
        self.hesap.hazir_agirlik_tablosu = self.agirlik_dosya_adi
        self.hesap.agirlikTablosuOku()
        
    
    def temizlik(self):
        t = self.tuslar['t']
        t.delete(1.0,END)
        for i in ('L1','L2','L3','L4','L5','L6','L7'):
            self.tuslar[i]['bg'] = self.renk0
            self.tuslar[i]['fg'] = self.renk0
            
if __name__ == '__main__':
    Cizim().mainloop()

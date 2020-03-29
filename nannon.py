from teningur import Teningur

import sys
h="hvítur"
s="svartur"

class Leikbord:

    def __init__(self):
        self.teningur=Teningur()
        self.stigh=0
        self.stigs=0
        self.bord=[1,1,1,0,0,-1,-1,-1]



    def prentun_a_lista(self):

        for i in range(len(self.bord)):
            if self.bord[i]==0:
                print(" _ ",end=" ")
            elif self.bord[i]==-1:
                print(" S ",end=" ")
            elif self.bord[i]==-2:
                print(" (SS) ",end=" ")
            elif self.bord[i]==-3:
                print(" (SSS) ",end=" ")
            elif self.bord[i]==1:
                print(" H ",end=" ")
            elif self.bord[i]==2:
                print(" (HH) ",end=" ")
            elif self.bord[i]==3:
                print(" (HHH) ",end=" ")
        print("\n")
        print(" 1   2   3   4   5   6   7   8")
    def ga_hvor_vann(self):
        if 1 not in self.bord and 2 not in self.bord and 3 not in self.bord:
            self.stigh=self.stigh+1
            print("\n")
            print("Hvítur vann þessa umferð. Hvítur er með",self.stigh,"stig\n")
            print("\n")
            self.bord=[1,1,1,0,0,-1,-1,-1]
            self.prentun_a_lista()
            return True
        elif -1 not in self.bord and -2 not in self.bord and -3 not in self.bord:
            self.stigs=self.stigs+1
            print("\n")
            print("Svartur vann þessa umferð. Svartur er með",self.stigs,"stig\n")
            print("\n")
            self.bord=[1,1,1,0,0,-1,-1,-1]
            self.prentun_a_lista()
            return True
        else:
            return False
    def leyfilegur_leikur_hvitur(self,faersla,kast):
        try:
            if self.bord[faersla-1]==-1 or self.bord[faersla-1]==0 or self.bord[faersla-1]==self.bord[faersla+kast-1]:
                return False
            else:
                return True

        except IndexError:
            self.bord[faersla-1]=0
            return True

    def leyfilegur_leikur_svartur(self,faersla2,kast2):
        if self.bord[faersla2-1]==1 or self.bord[faersla2-1]==0:
            return False
        if faersla2-kast2-1<0:
            self.bord[faersla2-1]=0
            return True
        elif self.bord[faersla2-1]==self.bord[faersla2-kast2-1]:
            return False

        elif self.bord[faersla2-1]==-2 and self.bord[faersla2-kast2-1]==-1:
            return False
        elif self.bord[faersla2-1]==-3 and self.bord[faersla2-kast2-1]==-1:
            return False
        else:
            return True

    def block_hvitur(self,faersla,kast):
        try:
            if faersla+kast-1==7:
                return False
            #tékkar ef 2 eru hlið við hlið
            elif (self.bord[faersla+kast-1]==-1 and self.bord[faersla+kast]==-1) or (self.bord[faersla+kast-1]==-1 and self.bord[faersla+kast-2]==-1):
                if faersla+kast-1==6 and self.bord[faersla+kast-2]!=-1:


                    return False

                else:
                    return True
            #tékkar ef 3 eru hlið við hlið
            elif (self.bord[faersla+kast-1]==-1 and self.bord[faersla+kast]==-1 and self.bord[faersla+kast+1]==-1) or (self.bord[faersla+kast-1]==-1 and self.bord[faersla+kast-2]==-1 and self.bord[faersla+kast+1]==-1) or (self.bord[faersla+kast-1]==-1 and self.bord[faersla+kast+1]==-1 and self.bord[faersla+kast+2]==-1):

                return True



            else:
                return False

        except IndexError:
            return False

    def block_svartur(self,faersla2,kast2):
        if faersla2-kast2-1==0:
            self.bord[faersla2-1]=0
            return False


        #tékkar ef 2 eru hlið við hlið
        elif (self.bord[faersla2-kast2-1]==1 and self.bord[faersla2-kast2]==1) or (self.bord[faersla2-kast2-1]==1 and self.bord[faersla2-kast2-2]==1):
            if faersla2-kast2-1==1 and self.bord[faersla2-kast2]!=1:

                return False
            else:
                return True
        #tékkar ef 3 eru hlið við hlið
        elif (self.bord[faersla2-kast2-1]==1 and self.bord[faersla2-kast2-2]==1 and self.bord[faersla2-kast2-3]==1) or (self.bord[faersla2-kast2-1]==1 and self.bord[faersla2-kast2-2]==1 and self.bord[faersla2-kast2]==1) or (self.bord[faersla2-kast2-1]==1 and self.bord[faersla2-kast2]==1 and self.bord[faersla2-kast2-2]==1):
            return True


        else:
            return False


    def hreyfing_a_hvitum(self,faersla,kast):
        leyfilegt=self.leyfilegur_leikur_hvitur(faersla,kast)
        blokk=self.block_hvitur(faersla,kast)
        if leyfilegt==False:
            print("veldu annan leikmann")
            self.hreyfing_a_hvitum(int(input()),kast)
        elif blokk==True:
            print("þú varst blokkaður")

            return self.bord
        else:
            try:
                if self.bord[faersla-1]==1:
                    if faersla+kast-1==7:
                        self.bord[faersla-1]=0

                    elif self.bord[faersla+kast-1]==0:
                        self.bord[faersla-1]=0
                        self.bord[faersla+kast-1]=1
                    elif self.bord[faersla+kast-1]==-1:
                        self.bord[faersla-1]=0
                        self.bord[faersla+kast-1]=1
                        if self.bord[len(self.bord)-1]==0:
                            self.bord[len(self.bord)-1]=-1
                        elif self.bord[len(self.bord)-1]==-1:
                            self.bord[len(self.bord)-1]=-2
                        elif self.bord[len(self.bord)-1]==-2:
                            self.bord[len(self.bord)-1]=-3

                elif self.bord[faersla-1]==2:#þegar 2 leikmenn eru á saman á heimareit
                    if self.bord[faersla+kast-1]==0:
                        self.bord[faersla-1]=1
                        self.bord[faersla+kast-1]=1
                    elif self.bord[faersla+kast-1]==-1:
                        self.bord[faersla-1]=1
                        self.bord[faersla+kast-1]=1
                        if self.bord[len(self.bord)-1]==0:
                            self.bord[len(self.bord)-1]=-1
                        elif self.bord[len(self.bord)-1]==-1:
                            self.bord[len(self.bord)-1]=-2
                        elif self.bord[len(self.bord)-1]==-2:
                            self.bord[len(self.bord)-1]=-3


                elif self.bord[faersla-1]==3:#þegar 3 leikmenn eru á saman á heimareit
                    if self.bord[faersla+kast-1]==0:
                        self.bord[faersla-1]=2
                        self.bord[faersla+kast-1]=1
                    elif self.bord[faersla+kast-1]==-1:
                        self.bord[faersla-1]=2
                        self.bord[faersla+kast-1]=1
                        if self.bord[len(self.bord)-1]==0:
                            self.bord[len(self.bord)-1]=-1
                        elif self.bord[len(self.bord)-1]==-1:
                            self.bord[len(self.bord)-1]=-2
                        elif self.bord[len(self.bord)-1]==-2:
                            self.bord[len(self.bord)-1]=-3


            except IndexError:
                self.bord[faersla-1]=0
        return self.bord

    def hreyfing_a_svortum(self,faersla2,kast2):
        leyfilegt=self.leyfilegur_leikur_svartur(faersla2,kast2)
        blokk=self.block_svartur(faersla2,kast2)
        if leyfilegt==False:
            print("veldu annan leikmann")
            self.hreyfing_a_svortum(int(input()),kast2)
        elif blokk==True:
            print("þú varst blokkaður")
            return self.bord
        else:
            if faersla2-kast2-1<0:
                self.bord[faersla2-1]=0
            elif self.bord[faersla2-1]==-1:
                if faersla2-kast2-1==0:
                    self.bord[faersla2-1]=0
                elif self.bord[faersla2-kast2-1]==0:
                    self.bord[faersla2-1]=0
                    self.bord[faersla2-kast2-1]=-1
                elif self.bord[faersla2-kast2-1]==1:
                    self.bord[faersla2-1]=0
                    self.bord[faersla2-kast2-1]=-1
                    if self.bord[0]==0:
                        self.bord[0]=1
                    elif self.bord[0]==1:
                        self.bord[0]=2
                    elif self.bord[0]==2:
                        self.bord[0]=3

            elif self.bord[faersla2-1]==-2:#þegar 2 leikmenn eru á saman á heimareit
                if self.bord[faersla2-kast2-1]==0:
                    self.bord[faersla2-1]=-1
                    self.bord[faersla2-kast2-1]=-1
                elif self.bord[faersla2-kast2-1]==1:
                    self.bord[faersla2-1]=-1
                    self.bord[faersla2-kast2-1]=-1
                    if self.bord[0]==0:
                        self.bord[0]=1
                    elif self.bord[0]==1:
                        self.bord[0]=2
                    elif self.bord[0]==2:
                        self.bord[0]=3


            elif self.bord[faersla2-1]==-3:#þegar 3 leikmenn eru á saman á heimareit
                if self.bord[faersla2-kast2-1]==0:
                    self.bord[faersla2-1]=-2
                    self.bord[faersla2-kast2-1]=-1
                elif self.bord[faersla2-kast2-1]==1:
                    self.bord[faersla2-1]=-2
                    self.bord[faersla-kast2-1]=-1
                    if self.bord[0]==0:
                        self.bord[0]=1
                    elif self.bord[0]==1:
                        self.bord[0]=2
                    elif self.bord[0]==2:
                        self.bord[0]=3

            if self.bord[0]==-1:
                self.bord[0]=0

        return self.bord





    def spila(self): #pragma: no cover
        while self.stigh<11 and self.stigs<11:
            #sjá hvernig leikborðið ser stillt upp í byrjun


            while self.ga_hvor_vann()==False:
                self.prentun_a_lista()
                #hérna  á hvítur leik
                print("\n")
                print(h, "á leik. Veldu aðgerð:(K)asta")
                k=input()

                if k=="k":
                    kast=self.teningur.roll()
                    print("\n")
                    print(h,"kastar og fær",kast,"Hvaða leikmann á að færa?")
                #hvítur
                faersla=input()

                if faersla.isdigit():#skoðar hvort inputið er tala
                    umferd=self.hreyfing_a_hvitum(int(faersla),kast)
                    self.prentun_a_lista()

                self.ga_hvor_vann()
                #svartur
                print("\n")
                print(s, "á leik. Veldu aðgerð:(K)asta")
                k=input()


                if k=="k":
                    kast2=self.teningur.roll()
                    print("\n")
                    print(s,"kastar og fær",kast2,"Hvaða leikmann á að færa?")

                faersla2=input()
                if faersla2.isdigit():#skoðar hvort inputið er tala
                    umferd2=self.hreyfing_a_svortum(int(faersla2),kast2)

                self.ga_hvor_vann()


if __name__ == '__main__':
    l=Leikbord()
    l.spila()

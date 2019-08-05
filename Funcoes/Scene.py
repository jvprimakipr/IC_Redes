import pandas as pd
class Scene:
    
    def __init__(self,directory):
        d={'Min_i':[0],'Seg_i':[0],'Min_f':[''],'Seg_f':['']}
        self.DF=pd.DataFrame(d,columns=['Min_i','Seg_i','Min_f','Seg_f'],index=['Cena1'])
        self.DF.index.name="Scene"
        self.DF_ID = 0
        self.actual_line=1
        self.actual_col=0
        self.directory = directory
        
    def data(self):
        return self.DF
    
    def new(self,name):
        Id=self.conv(name)
        if Id is not False:
            if self.proc(Id):
                print('Id repetido na cena')
            else:
                self.actual_col+=1
                if self.actual_col > self.DF.shape[1]-4:
                    self.DF[self.character()]=['']*self.DF.shape[0]
                self.DF.loc[self.scene(),self.character()]=ID
            
    def news(self,lista):
        for i in range(len(lista)):
            self.novo(lista[i])
    
    def timei(self,L,extra=0):
        if L[0]>=0 and L[1]>=0 and L[1]<60:
            if self.DF.shape[0]==1:
                self.DF.iloc[-1,0]=L[0]
                self.DF.iloc[-1,1]=L[1]
            elif self.sec(L[0],L[1])>=self.sec(self.DF.iloc[-2,2],self.DF.iloc[-2,3]):
                self.DF.iloc[-1,0]=L[0]
                self.DF.iloc[-1,1]=L[1]
            elif extra==1:
                self.DF.iloc[-1,0]=L[0]
                self.DF.iloc[-1,1]=L[1]
            else:
                print('Tempo Inicial <= Tempo Final da cena anterior')
        else:
            print('Tempo errado')
        
    def timef(self,L):
        if L[0]>=0 and L[1]>=0 and L[1]<60:
            var=self.sec(L[0],L[1])-self.sec(self.DF.iloc[-1,0],self.DF.iloc[-1,1])
            if var>0 and var <60:
                self.DF.iloc[-1,2]=L[0]
                self.DF.iloc[-1,3]=L[1]
                self.actual_line+=1
                self.actual_col=0
                self.DF.loc[self.scene()]=['']*self.DF.shape[1]
                if L[1]==59:
                    self.DF.iloc[-1,0]=L[0]+1
                    self.DF.iloc[-1,1]=0
                else:
                    self.DF.iloc[-1,0]=L[0]
                    self.DF.iloc[-1,1]=L[1]+1
            elif var<=0:
                print('Tempo Final <= Tempo Inicial')
            else:
                print(self.scene()+' possui mais de 1 minuto')
                
    def scene(self):
        return 'Scene'+str(self.actual_scene)
    
    def character(self):
        return 'P'+str(self.actual_col)
    
    def sec(self,m,s):
        return 60*m+s
    
    def find(self,Id):
        DF1=self.DF.iloc[[self.actual_line-1],4:self.actual_col+4]==Id
        v1=sum(DF1.sum())
        if v1!=0:
            return True
        else:
            return False
           
    def conv(self,name):
        if type(personagem)==str:
            L=list(self.DF_ID.index[self.DF_ID["Nick"] == "name"])
            if len(L)==1:
                return L[0]
            if len(L)==0:
                print('Personagem não encontrado')
                return False
        elif type(personagem)==int:
            return personagem
        else:
            print('ID incorreto')
            
    def importing_id(self):
        self.DF_ID=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.DF_ID=self.DF_ID.set_index("ID")
        
    def importing(self):
        self.DF=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.DF=self.DF.set_index("Scene")
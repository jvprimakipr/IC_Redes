import pandas as pd
class Scene:
    
    def __init__(self,directory):
        d={'Min_i':[0],'Seg_i':[0],'Min_f':[''],'Seg_f':['']}
        self.DF=pd.DataFrame(d,columns=['Min_i','Seg_i','Min_f','Seg_f'],index=['Scene1'])
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
            if self.find(Id):
                print('Id repetido na cena')
            else:
                self.actual_col+=1
                if self.actual_col > self.DF.shape[1]-4:
                    self.DF[self.character()]=['']*self.DF.shape[0]
                self.DF.loc[self.scene(),self.character()]=Id
            
    def news(self,L):
        for i in range(len(L)):
            self.new(L[i])
    
    def timei(self,m,s,extra=0):
        if m>=0 and s>=0 and s<60:
            if self.DF.shape[0]==1:
                self.DF.iloc[-1,0]=m
                self.DF.iloc[-1,1]=s
            elif self.sec(m,s)>=self.sec(self.DF.iloc[-2,2],self.DF.iloc[-2,3]):
                self.DF.iloc[-1,0]=m
                self.DF.iloc[-1,1]=s
            elif extra==1:
                self.DF.iloc[-1,0]=m
                self.DF.iloc[-1,1]=s
            else:
                print('Tempo Inicial <= Tempo Final da cena anterior')
        else:
            print('Tempo errado')
        
    def timef(self,m,s):
        if m>=0 and s>=0 and s<60:
            var=self.sec(m,s)-self.sec(self.DF.iloc[-1,0],self.DF.iloc[-1,1])
            if var>0 and var <60:
                self.DF.iloc[-1,2]=m
                self.DF.iloc[-1,3]=s
                self.actual_line+=1
                self.actual_col=0
                self.DF.loc[self.scene()]=['']*self.DF.shape[1]
                if s==59:
                    self.timei(m+1,0)
                else:
                    self.timei(m,s+1)
            elif var<=0:
                print('Tempo Final <= Tempo Inicial')
            else:
                print(self.scene()+' possui mais de 1 minuto')
    
    def end(self):
        pass
    
    
    def scene(self):
        return 'Scene'+str(self.actual_line)
    
    def character(self):
        return 'P'+str(self.actual_col)
    
    def sec(self,m,s):
        return 60*m+s
    
    def ind(self,num):
        a='00'+str(num)
        b=a[-3:-1]+a[-1]
        return b
    
    def find(self,Id):
        DF1=self.DF.iloc[[self.actual_line-1],4:self.actual_col+4]==Id
        v1=sum(DF1.sum())
        if v1!=0:
            return True
        else:
            return False
           
    def conv(self,name):
        if type(name)==int:
            return self.ind(name)
        elif type(name)==str:
            if name.isnumeric():
                return self.ind(name)
            name=name.lower()
            L1=list(self.DF_ID.index[self.DF_ID["Label"] == name])
            L2=list(self.DF_ID.index[self.DF_ID["Nick"] == name])
            if len(L1)==1:
                return L1[0]
            elif len(L2)==1:
                return L2[0]
            elif len(L1)==0 and len(L2)==0:
                print('Personagem não encontrado')
                return False
        else:
            print('ID incorreto')
            return False
            
    def inputing(self):
        n=input('Name: ')
        while n.lower()!='stop'and n.lower()!='pare':
            if n.lower()=='timei':
                ti=input('timei(')
                print(')')
                ti=ti.split(',')
                if len(ti)==2:
                    self.timei(int(tf[0]),int(tf[1]))
                elif len(ti)==3:
                    self.timei(int(tf[0]),int(tf[1]),int(ti[2]))
            elif n.lower()=='timef':
                tf=input('timef(')
                print(')')
                tf=tf.split(',')
                if len(tf)==2:
                    self.timef(int(tf[0]),int(tf[1]))
            else:
                self.new(n)
            print('')
            n=input('Name: ')
        
    def importing_id(self):
        self.DF_ID=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.DF_ID=self.DF_ID.set_index("ID")
        self.DF_ID.fillna('',inplace=True)
        self.DF_ID=self.DF_ID.applymap(lambda x: x.lower())
        
    def importing(self):
        self.DF=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.DF=self.DF.set_index("Scene")
        self.DF.fillna('',inplace=True)
        for i in self.DF.columns[0:4]:
            self.DF[i] = pd.to_numeric(self.DF[i])
        m=self.DF.iloc[-1,2]
        s=self.DF.iloc[-1,3]
        self.actual_line=self.DF.shape[0]+1
        self.actual_col=0
        self.DF.loc[self.scene()]=['']*self.DF.shape[1]
        if s==59:
            self.timei(m+1,0)
        else:
            self.timei(m,s+1)
            
        
    def csv(self):
        if self.DF.loc[self.scene(),'P1']=='':
            aux=self.DF.drop([self.scene()])
            aux.to_csv(self.directory+"/Scene.csv")
        else:
            print('Digite o tempo final da ultima cena')
        
    def excel(self):
        if self.DF.loc[self.scene(),'P1']=='':
            aux=self.DF.drop([self.scene()])
            aux.to_csv(self.directory+"/Scene.xls")
        else:
            print('Digite o tempo final da ultima cena')
    
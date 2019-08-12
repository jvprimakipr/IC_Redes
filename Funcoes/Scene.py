import pandas as pd
class Scene:
    
    def __init__(self,directory):
        self.directory = directory
        d={'Min_i':[0],'Seg_i':[0],'Min_f':[''],'Seg_f':[''],'Number':['']}
        self.scene=pd.DataFrame(d,columns=['Min_i','Seg_i','Min_f','Seg_f','Number'],index=['Scene1'])
        self.scene.index.name='Scene'
        self.id = 0
        self.importing_id()
        self.actual_line=1
        self.actual_col=0
        
    def data(self):
        return self.scene
    
    def new(self,name):
        Id=self.convert(name)
        if Id is not False:
            if self.find(Id):
                print('Id repetido na cena')
            else:
                self.actual_col+=1
                if self.actual_col > self.scene.shape[1]-5:
                    self.scene[self.ch()]=['']*self.scene.shape[0]
                self.scene.loc[self.sc(),self.ch()]=Id
            
    def news(self,L):
        for i in range(len(L)):
            self.new(L[i])
    
    def timei(self,m,s,extra=0):
        if m>=0 and s>=0 and s<60:
            if self.scene.shape[0]==1:
                self.scene.iloc[-1,0]=m
                self.scene.iloc[-1,1]=s
            elif self.sec(m,s)>=self.sec(self.scene.iloc[-2,2],self.scene.iloc[-2,3]):
                self.scene.iloc[-1,0]=m
                self.scene.iloc[-1,1]=s
            elif extra==1:
                self.scene.iloc[-1,0]=m
                self.scene.iloc[-1,1]=s
            else:
                print('Tempo Inicial <= Tempo Final da cena anterior')
        else:
            print('Tempo errado')
        
    def timef(self,m,s):
        if m>=0 and s>=0 and s<60:
            var=self.sec(m,s)-self.sec(self.scene.iloc[-1,0],self.scene.iloc[-1,1])
            if var>0 and var <60:
                self.scene.loc[self.sc(),'P1':self.ch()]=sorted(self.scene.loc[self.sc(),'P1':self.ch()])
                self.scene.iloc[-1,2]=m
                self.scene.iloc[-1,3]=s
                self.scene.loc[self.sc(),'Number']=self.actual_col
                self.actual_line+=1
                self.actual_col=0
                self.scene.loc[self.sc()]=['']*self.scene.shape[1]
                if s==59:
                    self.timei(m+1,0)
                else:
                    self.timei(m,s+1)
            elif var<=0:
                print('Tempo Final <= Tempo Inicial')
            else:
                print(self.sc()+' possui mais de 1 minuto')
    
    def sc(self):
        return 'Scene'+str(self.actual_line)
    
    def ch(self):
        return 'P'+str(self.actual_col)
    
    def sec(self,m,s):
        return 60*m+s
    
    def ind(self,num):
        a='00'+str(num)
        b=a[-3:-1]+a[-1]
        return b
    
    def find(self,Id):
        DF1=self.scene.iloc[[self.actual_line-1],5:self.actual_col+5]==Id
        v1=sum(DF1.sum())
        if v1!=0:
            return True
        else:
            return False
           
    def convert(self,name):
        if type(name)==int:
            return self.ind(name)
        elif type(name)==str:
            if name.isnumeric():
                return self.ind(name)
            name=name.lower()
            L1=list(self.id.index[self.id['Label'] == name])
            L2=list(self.id.index[self.id['Nick'] == name])
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
    
    def reconvert(self,num):
        if type(num)==int:
            num=self.ind(num)
        return self.id.loc[num,'Label']
    
    def review(self):
        for i in range(1,self.scene.shape[0]):
            n=self.scene.iloc[i-1,4]
            aux=pd.DataFrame(columns=self.scene.columns[0:5+n],index=[self.scene.index[i-1]])
            aux.loc['Names',:]=['']*aux.shape[1]
            a=list(self.scene.iloc[i-1,0:5+n])
            b=a[0:5]+[self.reconvert(x) for x in a[5:len(a)]]
            aux.iloc[0,:]=a
            aux.iloc[1,:]=b
            print(aux)
            e=input('Está correto?')
            print('')
    
    def inputing(self):
        n=input('Name: ')
        while n.lower()!='stop'and n.lower()!='pare':
            if n.lower()=='timei':
                ti=input('timei(')
                print(')')
                ti=ti.split(',')
                if len(ti)==2:
                    self.timei(int(ti[0]),int(ti[1]))
                elif len(ti)==3:
                    self.timei(int(ti[0]),int(ti[1]),int(ti[2]))
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
        self.id=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.id=self.id.set_index('ID')
        self.id.fillna('',inplace=True)
        self.id=self.id.applymap(lambda x: x.lower())
        
    def importing(self):
        self.scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.scene=self.scene.set_index('Scene')
        self.scene.fillna('',inplace=True)
        for i in self.scene.columns[0:5]:
            self.scene[i] = pd.to_numeric(self.scene[i])
        m=self.scene.iloc[-1,2]
        s=self.scene.iloc[-1,3]
        self.actual_line=self.scene.shape[0]+1
        self.actual_col=0
        self.scene.loc[self.sc()]=['']*self.scene.shape[1]
        if s==59:
            self.timei(m+1,0)
        else:
            self.timei(m,s+1)
            
        
    def csv(self):
        if self.scene.loc[self.sc(),'P1']=='':
            arq=self.scene.drop([self.sc()])
            arq.to_csv(self.directory+'/Scene.csv')
        else:
            print('Digite o tempo final da ultima cena')
        
    def excel(self):
        if self.scene.loc[self.sc(),'P1']=='':
            arq=self.scene.drop([self.sc()])
            arq.to_csv(self.directory+'/Scene.xls')
        else:
            print('Digite o tempo final da ultima cena')
    
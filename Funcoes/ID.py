import pandas as pd
class ID:
    
    def __init__(self,directory):
        self.id=pd.DataFrame(columns=['Label','Nick'],dtype=str)
        self.id.index.name='ID'
        self.folders = []
        self.directory = directory
        
    def data(self):
        return self.id
        
    def new(self,label,nick=''):
        if (self.find(label)==False and nick=='') or (self.find(label)==False and self.find(nick)==False):
            self.id.loc[self.ind(self.id.shape[0]+1)]=[label,nick]         
        else:
            print('Esse personagem já está na lista')
            
    def news(self,L):
        for i in L:
            if type(i)==str:
                self.new(i)
            elif len(i)==2:
                self.new(i[0],i[1])
    
    def ind(self,num):
        a='00'+str(num)
        b=a[-3:-1]+a[-1]
        return b
    
    def find(self,word):
        DF1=self.id.Label==word
        v1=DF1.sum()
        DF2=self.id.Nick==word
        v2=DF2.sum()
        if v1+v2==0:
            return False
        else:
            return True
    
    def correct(self,line=0):
        line=int(line)-1
        a=input('Trocar '+self.id.iloc[line,0]+' por: ')
        b=input('Trocar '+self.id.iloc[line,1]+' por: ')
        if a!='':
            self.id.iloc[line,0]=a
        if b!='':
            self.id.iloc[line,1]=b
        
    def delete(self,line=0):
        line=int(line)-1
        if line==-1:
            print(self.id.iloc[line,:])
            d=input('Você realmente deseja deletar?')
            if d.lower()=='sim' or d.lower()=='s' or d.lower()=='yes':
                self.id = self.id.drop([self.ind(self.id.shape[0])])
                print('Deletado')
        else:
            print(self.id.iloc[line,:])
            d=input('Você realmente deseja deletar?')
            if d.lower()=='sim' or d.lower()=='s' or d.lower()=='yes':
                for i in range(line,self.id.shape[0]):
                    self.id.iloc[i,0:2]=self.id.iloc[i+1,0:2]
                self.id = self.id.drop([self.ind(self.id.shape[0])])
                print('Deletado')
                
    def change(self,line1,line2):
        line1=int(line1)-1
        line2=int(line2)-1
        aux1=self.id.iloc[line1,0]
        aux2=self.id.iloc[line1,1]
        self.id.iloc[line1,0:2]=self.id.iloc[line2,0:2]
        self.id.iloc[line2,0:2]=[aux1,aux2]
        
    def review(self):
        for i in range(1,self.id.shape[0]+1):
            print(self.id.iloc[i-1,:])
            c=input('Corrigir:')
            print('')
            if c.lower()=='del' or c.lower()=='delete':
                self.delete(i)
            elif c.lower()=='change':
                ch=input('Trocar linha '+self.id.index[i-1]+' pela linha: ')
                ch=int(ch)
                if ch>=1 and ch<=self.id.shape[0]:
                    self.change(i,ch)
            elif c!='':
                self.correct(i)
        return self.id
    
    def inputing(self):
        l=input('Label: ')
        n=input('Nick: ')
        while l.lower()!='stop'and n.lower()!='stop':
            self.new(l,n)
            print('')
            l=input('Label: ')
            n=input('Nick: ')
    
    def saving(self,folders):
        self.folders = folders
        self.directory=''
        for i in self.folders:
            self.directory+='/'
            self.directory+=i
        
    def importing(self):
        self.id=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.id = self.id.set_index('ID')
        self.id.fillna('',inplace=True)
                
    def csv(self):
        self.id.to_csv(self.directory+'/ID.csv')
        
    def excel(self):
        self.id.to_excel(self.directory+'/ID.xls')
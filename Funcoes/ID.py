import pandas as pd
class ID:
    
    def __init__(self,directory):
        self.DF=pd.DataFrame(columns=['Label','Nick'],dtype=str)
        self.DF.index.name="ID"
        self.folders = []
        self.directory = directory
        
    def data(self):
        return self.DF
        
    def new(self,label,nick=''):
        if (self.find(label)==False and nick=='') or (self.find(label)==False and self.find(nick)==False):
            self.DF.loc[self.ind(self.DF.shape[0]+1)]=[label,nick]         
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
        DF1=self.DF.Label==word
        v1=DF1.sum()
        DF2=self.DF.Nick==word
        v2=DF2.sum()
        if v1+v2==0:
            return False
        else:
            return True
    
    def correct(self,line=0):
        line=int(line)-1
        a=input('Trocar '+self.DF.iloc[line,0]+' por: ')
        b=input('Trocar '+self.DF.iloc[line,1]+' por: ')
        if a!='':
            self.DF.iloc[line,0]=a
        if b!='':
            self.DF.iloc[line,1]=b
        
    def delete(self,line=0):
        line=int(line)
        if line==0:
            print(self.DF.iloc[line-1,:])
            d=input('Você realmente deseja deletar?')
            if d.lower()=='sim' or d.lower()=='s' or d.lower()=='yes':
                self.DF = self.DF.drop([self.ind(self.DF.shape[0])])
                print('Deletado')
        else:
            print(self.DF.iloc[line-1,:])
            d=input('Você realmente deseja deletar?')
            if d.lower()=='sim' or d.lower()=='s' or d.lower()=='yes':
                for i in range(line,self.DF.shape[0]):
                    self.DF.iloc[i-1,0:2]=self.DF.iloc[i,0:2]
                self.DF = self.DF.drop([self.ind(self.DF.shape[0])])
                print('Deletado')
                
    def change(self,line1,line2):
        line1=int(line1)-1
        line2=int(line2)-1
        aux1=self.DF.iloc[line1,0]
        aux2=self.DF.iloc[line1,1]
        self.DF.iloc[line1,0:2]=self.DF.iloc[line2,0:2]
        self.DF.iloc[line2,0:2]=[aux1,aux2]
        
    def review(self):
        for i in range(1,self.DF.shape[0]+1):
            print(self.DF.iloc[i-1,:])
            c=input('Corrigir:')
            print('')
            if c.lower()=='del' or c.lower()=='delete':
                self.delete(i)
            elif c.lower()=='change':
                ch=input('Trocar linha '+self.DF.index[i-1]+' pela linha: ')
                ch=int(ch)
                if ch>=1 and ch<=self.DF.shape[0]:
                    self.change(i,ch)
            elif c!='':
                self.correct(i)
        return self.DF
    
    def inputing(self):
        l=input('Label: ')
        n=input('Nick: ')
        while l.lower()!='stop'and n.lower()!='stop':
            print('')
            self.new(l,n)
            l=input('Label: ')
            n=input('Nick: ')
    
    def saving(self,folders):
        self.folders = folders
        self.directory=""
        for i in self.folders:
            self.directory+="/"
            self.directory+=i
        
    def importing(self):
        self.DF=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.DF = self.DF.set_index("ID")
        self.DF.fillna('',inplace=True)
                
    def csv(self):
        self.DF.to_csv(self.directory+"/ID.csv")
        
    def excel(self):
        self.DF.to_excel(self.directory+"/ID.xls")
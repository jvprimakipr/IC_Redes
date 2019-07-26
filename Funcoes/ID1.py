import pandas as pd
class ID:
    def __init__(self):
        self.DF=pd.DataFrame(columns=['Label','Nick'])
        self.DF.index.name='ID'
        
    def data(self):
        return self.DF
        
    def new(self,label,nick=''):
        if (self.find(label)==False and nick=='') or (self.find(label)==False and self.find(nick)==False):
            self.DF.loc[self.ind(self.DF.shape[0]+1)]=[label,nick]
            
        else:
            print('Esse personagem já está na lista')
            
    def news(self,L):
        for i in L:
            if len(i)==1:
                self.new(i[0])
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
        else:
            print(self.DF.iloc[line-1,:])
            d=input('Você realmente deseja deletar?')
            if d.lower()=='sim' or d.lower()=='s' or d.lower()=='yes':
                for i in range(line,self.DF.shape[0]):
                    self.DF.iloc[i-1,0:2]=self.DF.iloc[i,0:2]
                self.DF = self.DF.drop([self.ind(self.DF.shape[0])])
                
    def change(self,line1,line2):
        line1=int(line1)
        line2=int(line2)
        aux1=self.DF.iloc[line1-1,0]
        aux2=self.DF.iloc[line1-1,1]
        self.DF.iloc[line1-1,0:2]=self.DF.iloc[line2-1,0:2]
        self.DF.iloc[line2-1,0:2]=[aux1,aux2]
        
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
                
    def csv(self,name):
        self.DF.to_csv("/dados/home/joaoviniciuspr/IC_Redes/Trabalhos/"+name+"/"+"ID.csv")
        
    def excel(self,name):
        self.DF.to_excel("/dados/home/joaoviniciuspr/IC_Redes/Trabalhos/"+name+"/"+"ID.xls")
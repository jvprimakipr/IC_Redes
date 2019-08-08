class Relation:
    def __init__(self,directory):
        self.directory=directory
        self.DF_scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.DF_scene=self.DF_scene.set_index("Scene")
        self.DF_scene.fillna('',inplace=True) #Printar mensagem de erro
        d={'Peso':['']}
        self.DF=pd.DataFrame(d,columns=['Peso'],index=[0])
        d1={'Origem':[''],'Destino':[''],'Peso':['']}
        self.relacao=pd.DataFrame(d1,columns=['Origem','Destino','Peso'],index=['0'])
        self.peso_atual=0
        self.executado=0
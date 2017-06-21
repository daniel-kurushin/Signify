import re
import subprocess
import urllib
from pymystem3 import Mystem
from bs4 import BeautifulSoup
from urllib.parse import quote
from pymystem3 import Mystem
import pymorphy2
import sys
import graphviz as gv



def main(argv):			
		with open(argv[1], encoding='utf-8') as f:
		    s = re.sub(r'\s+', ' ', f.read(), flags=re.M)
		f=re.split(r'(?<=[.!?…]) ',s)
		sentens=[]
		for i,t in enumerate(f):
		    sentens.append(t)
		    print(str(i)," ",t)




		morph = pymorphy2.MorphAnalyzer() 

		ZnakiP=[",","!","/n",".",":",";",'"',"'","\n","...","?","!","(",")","-"," ","  "]
		t = Mystem()
		PARS=[]
		for sent in sentens:
		    input_file=open("input.txt","w",encoding="utf-8")
		    input_file.write(sent)
		    input_file.close()
		    
		    # Делаем синтаксический анализ текста, находим граматические основы
		    process = subprocess.Popen('tomitaparser.exe config.proto', stdout=subprocess.PIPE,shell=True) 
		    process.communicate()
		    process.wait()
		    
		    predicate=[]
		    Nouns=[]
		    DOP=[]
		    DOP.append({})
		    OPR=[]
		    with open("pretty.html",encoding='utf8') as fp:
		            soup = BeautifulSoup(fp,"html.parser")    
		    par_f=soup.find_all('table')
		    for table in par_f:
		        th=table.find('th')    
		        if(th.text=="Noun1"):
		            slovo=th.find_parent("table").find('a').text
		            Nouns.append(slovo)
		        if(th.text=="Verb1"):
		            slovo=th.find_parent("table").find('a').text
		            predicate.append(slovo)
		        if(th.text=="OPR1"):
		            sl=th.find_parent("table").find_all('a')
		            for slovo in sl:
		                OPR.append(slovo.text)
		        if(th.text=="DOP1"):
		            sl=th.find_parent("table").find_all('a')
		            for slovo in sl:
		                DOP[0][slovo.text.lower()]=slovo.next_element.next_element.next_element.next_element
		    TREE={}
		    TREE[Nouns[0]]={} 

		    

		    for v in predicate:
		        TREE[Nouns[0]][v]={}
		    if(OPR!=[]):
		            for temp in OPR:
		                for noun in TREE:
		                    if(len(re.split(r"[,' ']",temp))==1):
		                        TREE[Nouns[0]][temp]=t.analyze(temp)[0]['analysis'][0]['gr']
		                    else:
		                            m2=[]
		                            for f in re.split(r"[,' ']",temp):
		                                if(f!=''):
		                                    m2.append(f)
		                            if(noun in m2):
		                                mk=t.analyze(temp)
		                                wsp=[]
		                                for tr in mk:
		                                    if(not tr['text'] in ZnakiP):
		                                        if(not 'CONJ' in tr['analysis'][0]['gr']):
		                                            wsp.append(tr['text'])
		                                for tl in wsp:
		                                    if(tl!=noun):
		                                        TREE[Nouns[0]][tl]=t.analyze(tl)[0]['analysis'][0]['gr']



		    for temp in TREE[Nouns[0]]:
		        if(temp in DOP[0].values()):
		            for sp in DOP[0]:
		                if(DOP[0][sp]==temp):
		                    m2=[]
		                    for f in re.split(r"[,' ']",sp):
		                        if(f!=''):
		                            m2.append(f)                         
		                    for rg in m2:                    
		                        TREE[Nouns[0]][temp][rg]={}
		                        for _opr in OPR:
		                            reg=re.split(r"[,' ']",temp)                        
		                            if(noun in reg):
		                                mk=t.analyze(_opr)
		                                wsp=[]
		                                for tr in mk:
		                                    if(not tr['text'] in ZnakiP):
		                                        if(not 'CONJ' in tr['analysis'][0]['gr']):
		                                            wsp.append(tr['text'])
		                                for tl in wsp:
		                                    if(tl!=rg):                                
		                                        TREE[Nouns[0]][temp][rg][tl]=t.analyze(tl)[0]['analysis'][0]['gr']


		  
		    
		    for noun in TREE:
		        d1=[noun]
		        for verb in TREE[noun]:
		            if(morph.parse(verb)[0].tag.POS=='ADJF'):            
		                d2=[noun,'быть']
		                d2.append(verb)
		                if(not d2 in PARS):
		                    PARS.append(d2.copy()) 
		                d2.pop()
		            else:
		                d4=[verb,"может быть"]
		                d1.append(verb)            
		                for temp in TREE[noun][verb]:            
		                            if(morph.parse(temp)[0].tag.POS=='NOUN'):
		                                d1.append(morph.parse(temp)[0].normal_form)
		                                if(not d1 in PARS):
		                                        PARS.append(d1.copy())
		                                d1.pop()
		                                d3=[temp,'быть']    
		                                
		                                for temp2 in TREE[noun][verb][temp]:
		                                        d3.append(temp2)
		                                        PARS.append(d3.copy())
		                                        d3.pop()
		                            else:
		                                d4.append(temp)
		                                if(not d4 in PARS):
		                                    PARS.append(d4.copy())
		                                d4.pop()


		    
		obj = PARS.copy()

		g1=gv.Digraph(format='png')

		for temp in obj:
		    a=morph.parse(temp[0])[0].tag.POS
		    if(a=='VERB' or a=='INFN'):
		            for t in obj:
		                if(t[1]==temp[0]):
		                    g1.node(t[0],shape='rect',style='filled',fillcolor='#cccccc')
		                    g1.node(temp[0])
		                    g1.node(temp[2],shape='rect',style='filled',fillcolor='#cccccc')
		                    g1.edge(t[0],temp[0])                    
		                    g1.edge(temp[0],temp[2],label=temp[1])
		                    g1.edge(temp[0],t[2])
		                    
		    else:
		        g1.node(temp[0],shape='rect',style='filled',fillcolor='#cccccc')
		        g1.node(temp[2],shape='rect',style='filled',fillcolor='#cccccc')
		        g1.edge(temp[0],temp[2],label=temp[1])

		print(g1.source)
		g1.render('img/'+argv[2])


if __name__ == '__main__':	
	main(sys.argv)

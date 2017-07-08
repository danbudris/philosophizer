# -*- coding: utf-8 -*-
import wptools

class philosopher:
    """
    A Philosopher, whose information is pulled from the wikipedia API, and their chain of influence as mapped on Wikipedia
    """
    influences    = []
    influenced    = []
    rawinfluenced = []
    
    def __init__(self,name):
        self.name           = name    
        self.influences     += get_philo(self.name)[0]
        self.influenced     += get_philo(self.name)[1]
        self.rawinfluenced  += get_philo(self.name)[2]
        
    def addInfluence(self,influence):
        self.influences.append(influence)
        
    def addInfluenced(self,influenced):
        self.influenced.append(influenced)
       

def process_influence(influence):    
    """
    removes []{} from influenced/ed string, then splits along commas, then pipes, then semicolon; 
    needs to remove the references (ref)
    needs to account for some templates using [] as seperators
    encoding (see Ronald Barthes influcned) can be an issue, with the . showing up as strange Unicode sometimes; learna bout encoding
    """
    influence = influence.translate(None,'[]{}')    
    commasplit = influence.split(',') 
    pipesplit = []
    for entry in commasplit:
        pipesplit += entry.split('|')
    semicolonsplit = []
    for entry in pipesplit:
        semicolonsplit += entry.split(';')
    
    return semicolonsplit
        
def get_philo(philo_name):  
    """
    Uses WpTools to reach out to the wikipedia API and return the influences and influenced for a given philosopher.  
    Processes the retrun value as much as possible, so that it is in a somewhat standardized format
    """
    philo = wptools.page(philo_name).get_parse()
    try:
        influences = ((philo.infobox['influences']).encode('UTF8'))
    except:
        influenceslist = 'no influences'
    try:
        influenced = ((philo.infobox['influenced']).encode('UTF8'))
    except:
        influencedlist = 'none influened'
    try:
        influencedlist = process_influence(influenced)
    except:
        influencedlist = 'none influenced'
    try:
        influenceslist = process_influence(influences)
    except:
        influences = 'no influences'
    return (influenceslist,influencedlist,influenced)
    

def build_influence_tree(philo, influence):
    """
    gets the influnced of the influenced, and creates objects from them
    """
    if (influence == 'influenced'):
        influence = philo.influenced
    
    if (influence == 'influences'):
        influence = philo.influences
    
    philodict = {}
    x = 0
    for thinker in influence:
        try:
            philoclass = philosopher(thinker)
            philodict[thinker] = philoclass
            x += 1
            if x > 10:
                return philodict
        except:
            print 'busted'
    return philodict
    
Lacan = philosopher("Jaques Lacan")
Jakobson = philosopher("Roman Jakobson")
Barthes = philosopher("Roland Barthes")
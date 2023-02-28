# -*- coding: utf-8 -*-
"""
Created on Wed May 19 02:57:14 2021

@author: zhang
"""


import tkinter.ttk
from tkinter import *
import datetime as dt #module de gestion des dates, fonctionne sous forme de classe
import matplotlib.pyplot as plt; plt.rcdefaults() #utile pour les traitements
import numpy as np #utile pour les traitements 
import matplotlib.pyplot as plt #utile pour les traitements 
import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
import tkinter.filedialog as TKFD 



"""_______________________CLASSES_______________________"""

class Personnel(): #classe mère Personnel dont les classes filles sont Internes et Externes
    def __init__(self, lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance):
        self._nom= str(lenom) #chaine de caractère, exemple: Lemaitre 
        self._prenom = str (leprenom) #même chose
        self._sexe = str(lesexe) #homme, femme, autre 
        
        if type(ledate_de_naissance) is tuple or type(ledate_de_naissance) is str: #traite les dates au format 'AAAA/MM/JJ'
            self._date_de_naissance=dt.date(int(ledate_de_naissance[:4]), int(ledate_de_naissance[5:7]), int(ledate_de_naissance[8:10]))
        else:
            self._date_de_naissance = 'None'
       
        self._pays_de_naissance = str(lepays_de_naissance) #exemple : France
        
    #méthodes de la classe
    def get_nom(self):
        return self._nom
    def get_prenom(self):
        return self._prenom
    def get_sexe(self):
        return self._sexe
    def get_date_de_naissance(self):
        return self._date_de_naissance
    def get_pays_de_naissance(self):
        return self._pays_de_naissance
    
    def __repr__(self):
        return "{} {}".format(self.nom, self.prenom)



    #passage en propriété pour simplifier l'accès ensuite 
    nom = property(get_nom)
    prenom = property(get_prenom)
    sexe = property(get_sexe)
    date_de_naissance = property(get_date_de_naissance)
    pays_de_naissance = property(get_pays_de_naissance)


class Internes(Personnel): #classe fille de Personnel
    def __init__(self, lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance, lebureau_occupe,lehistorique_carriere, letaux_appartenance):
        super().__init__(lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance) #appel des méthodes de la classe mère
        self._bureau_occupe = str(lebureau_occupe)#chaine de caractère car les bureaux peuvent avoir des noms, exemple : Labo SI
        self._historique_carriere = list(lehistorique_carriere) #sous forme d'une liste de liste avec les infos imbriquées 
        self._taux_appartenance = dict(letaux_appartenance) #exemple : {'Conception':0.9,'Fabrication':0.1}
        self._postes_actuels = []  #un interne peut occuper 2 postes au seins de l'établissement 
        
        
    #Assesseurs
    def get_bureau_occupe(self):
        return self._bureau_occupe
    def get_historique_carriere(self):
        return self._historique_carriere
    def get_taux_appartenance(self):
        return self._taux_appartenance
    
    # méthodes dela classe 
    def get_postes_actuels(self):
        """permet de récupérer la liste des postes encore d'actualité de l'interne"""
        self._postes_actuels=[] #réinitialisation. Sinon la méthode ajoute le même poste plusieurs fois
        for chaqueposte in self._historique_carriere:
           if chaqueposte.date_fin == None :
               self._postes_actuels.append(chaqueposte.intitule)
        return self._postes_actuels
    
    #passage en propriété pour simplifier l'accès ensuite 
    bureau_occupe= property(get_bureau_occupe)
    postes_actuels = property(get_postes_actuels)
    historique_carriere =  property(get_historique_carriere)
    taux_appartenance = property(get_taux_appartenance)
    postes_actuels = property(get_postes_actuels)
    
    def __repr__(self):
        return "{} {}".format(self.nom, self.prenom)
    
    
class Externes(Personnel): #classe fille de Personnel
    def __init__(self, lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance, leposte_occupe, leetablissement_actuel, leinvitations):
        super().__init__(lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance) #appel des méthodes de la classe mère
        self._poste_occupe = str(leposte_occupe) #par exemple : technicien de surface  
        self._etablissement_actuel = str(leetablissement_actuel) #lieu d'origine de l'externe
        self._invitations = list(leinvitations) #liste des précédentes invitations au labo [date de début, date de fin]
    
    #Assesseurs
    def get_poste_occupe(self):
        return self._poste_occupe
    def get_etablissement_actuel(self):
        return self._etablissement_actuel
    def get_invitations(self):
        return self._invitations
    
    def addPoste_occupe(self, unposte):
        """Permet d'ajouter un poste occupé à l'externe (type str)"""
        if isinstance(unposte, str):
            self._poste_occupe = unposte
    
    #passage en propriété pour simplifier l'accès ensuite 
    poste_occupe= property(get_poste_occupe,addPoste_occupe)
    # labo_actuel =  property(get_labo_actuel)
    etablissement_actuel = property(get_etablissement_actuel)
    invitations = property(get_invitations)
    
    def __repr__(self):
        return "{} {}".format(self.nom, self.prenom)

class Projet(): #classe mère de projet de recherche et projet de thèse
    def __init__(self, letitre, leetablissement_realisation):
        self._titre=str(letitre) #titre du projet
        self._etablissement = str(leetablissement_realisation) 
    
    #Assesseurs
    def get_titre(self):
        return self._titre
    def get_etablissement(self):
        return self._etablissement 
    
    #passage en propriété pour simplifier l'accès ensuite 
    titre = property(get_titre)
    etablissement= property(get_etablissement)
    
    def __repr__(self):
        return "{} {}".format(self.titre, self.etablissement)
    
class Projet_recherche(Projet): #classe fille de projet pour les projets de recherche 
    def __init__(self, letitre, leetablissement_realisation, leacronyme, lebudget, lepersonnes_impliquees, lepilote_projet_recherche):
        super().__init__(letitre, leetablissement_realisation) #appel des méthodes de la classe mère
        self._date_previsionnelle = None #On en ajoute une après instanciation du projet avec les méthodes addBLABLABLA
        self._date_debut = None #On en ajoute une après instanciation du projet avec les méthodes addBLABLABLA
        self._date_cloture = None #On en ajoute une après instanciation du projet avec les méthodes addBLABLABLA
        self._budget = float(lebudget) #le budget sera un flottant, ceci permet de chiffrer précisément au besoin
        self._personnes_impliquees = list(lepersonnes_impliquees) #sous forme d'une liste des personnes impliquées
        self._pilote_projet_recherche = str(lepilote_projet_recherche) #le pilote devra faire partie des personnes impliquées
        self._projets_these_associes = None #On en ajoute après instanciation du projet de recherche et des projets de thèse avec les méthodes addBLABLABLA
        self._etablissement_realisation = dict(leetablissement_realisation)
        self._acronyme = str(leacronyme)

        
    #assesseurs
    def get_date_previsionnelle(self):
        return self._date_previsionnelle
    def get_date_debut(self):
        return self._date_debut
    def get_date_cloture(self):
        return self._date_cloture
    def get_budget(self):
        return self._budget
    def get_personnes_impliquees(self):
        return self._personnes_impliquees
    def get_pilote_projet_recherche(self):
        return self._pilote_projet_recherche
    def get_projets_these_associes(self):
        return self._projets_these_associes
    def get_etablissement_realisation(self):
        return self._etablissement_realisation
    def get_acronyme(self):
        return self._acronyme
   
    
    
    #méthodes de la classe
    #ATTENTION : cette méthode ne fonctionne correctement qu'une fois que tous les projets du xml ont été instanciés
    def addProjet_these_associe(self,liste_projet_associe): #méthode pour ajouter une liste de projets associés
        if isinstance(liste_projet_associe, list):
            for nomprojet in liste_projet_associe:
                self._projets_these_associes.append(nomprojet)
                
    def addDateprevisionnelle(self,ledate_previsionnelle): #méthode pour ajouter une date prévisionnelle  
        if isinstance (ledate_previsionnelle,str):
            self._date_previsionnelle=dt.date(int(ledate_previsionnelle[:4]), int(ledate_previsionnelle[5:7]), int(ledate_previsionnelle[8:10]))
   
    def addDatededebut(self,ledate_debut): #méthode pour ajouter une date de début
        if isinstance (ledate_debut,str):
            self._date_debut=dt.date(int(ledate_debut[:4]), int(ledate_debut[5:7]), int(ledate_debut[8:10]))
            
    def addDatedecloture(self,ledate_cloture): #méthode pour ajouter une date de cloture
        if isinstance (ledate_cloture,str):
            self._date_cloture=dt.date(int(ledate_cloture[:4]), int(ledate_cloture[5:7]), int(ledate_cloture[8:10]))
            
    
    #passage en propriété pour simplifier l'accès ensuite 
    date_previsionnelle = property(get_date_previsionnelle, addDateprevisionnelle)
    date_debut = property(get_date_debut, addDatededebut)
    date_cloture = property(get_date_cloture, addDatedecloture)
    budget = property(get_budget)
    personnes_impliquees = property(get_personnes_impliquees)
    pilote_projet_recherche = property(get_pilote_projet_recherche)
    projets_associes = property(get_projets_these_associes, addProjet_these_associe)
    etablissement_realisation= property(get_etablissement_realisation)
    acronyme= property(get_acronyme)

    
    def __repr__(self):
        return "{} {}".format(self.titre, self.etablissement)

class Projet_these(Projet):
    def __init__(self, letitre, leetablissement_realisation,ledate_lancement, lejury_soutenance,ledoctorant,ledirecteur,leencadrant):
        super().__init__(letitre, leetablissement_realisation)
        self._date_lancement = dt.date(int(ledate_lancement[:4]), int(ledate_lancement[5:7]), int(ledate_lancement[8:10])) #date aau format 'AAAA/MM/JJ'
        self._date_soutenance = None #ajoutée ultérieurement
        self._jury_soutenance = dict(lejury_soutenance) #dictionnaire au format {'NOM':'Role'}
        self._doctorant = ledoctorant #objet de la classe Interne
        self._directeur = dict(ledirecteur) # au format {'directeur' : 'taux'}
        self._encadrant = dict(leencadrant) # au format {'encadrant' : 'taux'}
        self._ref_production = None #ajoutée ultérieurement
        self._projet_associe=[]
        
    
    #assesseurs
    def get_date_lancement(self):
        return self._date_lancement
    def get_date_soutenance(self):
        return self._date_soutenance
    def get_jury_soutenance(self):
        return self._jury_soutenance
    def get_doctorant (self):
        return self._doctorant
    def get_directeur(self):
        return self._directeur
    def get_encadrant(self):
        return self._encadrant
    def get_ref_production(self):
        return self._ref_production
    def get_list_projet_associe(self):
        return self._projet_associe
    

    
    #Méthodes
    def addDatedesoutenance(self,ledate_soutenance): #méthode pour ajouter une date de soutenance 
        if isinstance (ledate_soutenance,str):
            self._date_soutenance=dt.date(int(ledate_soutenance[:4]), int(ledate_soutenance[5:7]), int(ledate_soutenance[8:10]))
    
    def addRef_production(self, leref_production): #méthode pour ajouter une référence de production
        if isinstance(leref_production,str):
            self._ref_production = str(leref_production) #str() évite les partages de pointeur
    
    #ATTENTION : cette méthode ne fonctionne correctement qu'une fois que tous les projets du xml ont été instanciés
    def addProjet_associe(self,liste_projet_associe): #méthode pour ajouter une liste de projets associés
        if isinstance(liste_projet_associe, list):
            for nomprojet in liste_projet_associe:
                self._projet_associe.append(nomprojet)
    
    #passage en propriété pour simplifier l'accès ensuite 
    date_lancement = property(get_date_lancement)
    date_soutenance = property(get_date_soutenance,addDatedesoutenance) #property(get,set) s'utilise comme une variable
    jury_soutenance = property(get_jury_soutenance)
    doctorant = property(get_doctorant)
    directeur = property(get_directeur)
    encadrant = property(get_encadrant)
    reference = property(get_ref_production)
    projets_associes = property(get_list_projet_associe,addProjet_associe)
    
    
    
    def __repr__(self):
        return "{},{}.{}".format(self.doctorant, self.titre, self.etablissement )

class publications():  #Classe mère des articles et rapports techniques
    def __init__(self, ledate, leauteurs, letitre, lelien):
        self._date = dt.date(int(ledate[:4]), int(ledate[5:7]), int(ledate[8:10])) #au format (AAAA, M, J)
        self._auteurs = list(leauteurs)
        self._titre = str(letitre)
        self._lien = str(lelien)
        self._origine = None
        self._cadre_publication = None
    
    #assesseurs
    def get_auteurs(self):
        return self._auteurs
    def get_date(self) :
        return self._date
    def get_titre(self):
        return self._titre
    def get_lien(self):
        return self._lien
    def get_origine(self):
        return self._origine
    def get_cadre_publication(self):
        return  self.lecadre_publication
    
    #méthodes de la classe 
    def addOrigine(self,leorigine):
        if isinstance(leorigine,str):
            self._origine=leorigine
    
    def addCadre_Publication(self, lecadre):
        if isinstance(lecadre,str):
            self._cadre_publication=lecadre
    
    def addDatedePublication(self,ledate): #méthode pour ajouter une date de Publication 
        if isinstance (ledate,str):
            self._date=dt.date(int(ledate[:4]), int(ledate[5:7]), int(ledate[8:10]))
    
    #passage en propriété pour simplifier l'accès ensuite 
    auteurs=property(get_auteurs)
    date=property(get_date)
    titre=property(get_titre)
    lien=property(get_lien)
    origine=property(get_origine)
    cadre_publication=property(get_cadre_publication)
    
    def __repr__(self): #Respecte le format des bibliographies conseillé par le labo
        return "{},{},{},{}".format(self.auteurs, self.date, self.titre, self.lien)
    
class article_journal(publications):
    def __init__(self, ledate, leauteurs, letitre, lelien, lenom_revue):
        super().__init__(ledate, leauteurs, letitre, lelien)
        self._nom_revue = str(lenom_revue)
        self._renommee = None #on ira chercher l'info dans la classe revue 
        self._quartile = None #on ira chercher l'info dans la classe revue
    
    #assesseur
    def get_nom_revue(self):
        return self._nom_revue
    def get_renommee(self):
        return self._renommee
    def get_quartile(self):
        return self._quartile
    
    #méthodes de la classe 
    def addQuartile(self,unquartile):
        if isinstance(unquartile, dict):
            self._quartille= {**unquartile}
    
    def addFacteur_impact(self,unfacteur):
        if isinstance(unfacteur, dict):
            self._renommee= {**unfacteur}
    
    #passage en propriété pour simplifier l'accès ensuite 
    nom_revue= property(get_nom_revue)
    renommee = property(get_renommee)
    quartile = property(get_quartile)
    
    

class article_conference(publications):
    def __init__(self, ledate, leauteurs, letitre, lelien, lenom_conference, ledate_conference, lelieu_conference):
        super().__init__(ledate, leauteurs, letitre, lelien)
        self._nom_conference = str(lenom_conference)
        self._date_conference = str(ledate_conference)
        self._lieu_conference = str(lelieu_conference)
    
    # assesseurs
    def get_nom_conference(self):
        return self._nom_conference
    def get_date_conference(self):
        return self._date_conference
    def get_lieu_conference(self):
        return self._lieu_conference
    
    #passage en propriété pour simplifier l'accès ensuite 
    nom_conference = property(get_nom_conference)
    date_conference = property(get_date_conference)
    lieu_conference = property(get_lieu_conference)

class rapport_technique(publications):
    def __init__(self, ledate, leauteurs, letitre, lelien):
        super().__init__(ledate, leauteurs, letitre, lelien)
        self._date = dt.date(int(ledate[:4]), int(ledate[5:7]), int(ledate[8:10])) #au format (AAAA, M, J)
        self._titre = str(letitre)
        self._lien = str(lelien)
    
    #assesseurs
    def get_date(self):
        return self._date
    def get_titre(self):
        return self._titre
    def get_lien(self):
        return self._lien
    
    #propriétés
    date = property(get_date)
    titre = property(get_titre)
    lien = property(get_lien)

class etablissement():
    def __init__(self,lenom_etablissement):
        self._nom_etablissement = str(lenom_etablissement)
        self._employes = [] #liste des externes connus du labo qui travaillent dans l'établissement 
        self._budget_projets_communs=0 #comptabilise le budget donné pour des projets communs avec le labo. Utile pour les traitements
        self._nombre_projets_communs=0 #comptabilise le nombre de projets communs avec le labo. Utile pour les traitements
    
    #assesseurs
    def get_nom_etablissement(self):
        return self._nom_etablissement
    def get_employes(self):
        return self._employes
    def get_budget_projets_communs(self):
        return self._budget_projets_communs
    def get_nombre_projets_communs(self):
        return self._nombre_projets_communs
    
    #méthodes de la classe 
    
    def addEmploye (self,unemploye):
        if isinstance(unemploye, Personnel):
            self._employes.append(unemploye)
    
    def addBudget_projets_communs(self,budget):
        self._budget_projets_communs+= int(budget)
    
    def addNombre_projets_communs(self):
        self._nombre_projets_communs+=1
        
    #passage en propriété pour simplifier l'accès ensuite 
    nom_etablissement = property(get_nom_etablissement)
    employes = property(get_employes)
    budget_projets_communs = property(get_budget_projets_communs)
    nombre_projets_communs = property(get_nombre_projets_communs)
    
    def __repr__(self):
        return "{}".format(self.nom_etablissement)

class revue(): 
    def __init__(self, lenom_revue, leacronyme, lequartile, lefacteur_impact):
        self._nom_revue = str(lenom_revue)
        self._facteur_impact= dict(lefacteur_impact) #au format {'annee':'Facteur Impact'}
        self._quartile = dict(lequartile) #au format {'annee':'Quartile'}
        self._acronyme = str(leacronyme)
        self._nombre_publications_labo= 0 #comptabilise le nombres de publications dans la revue faite par le labo
    
    #asseceurs
    def get_nom_revue(self):
        return self._nom_revue
    def get_facteur_impact(self):
        return self._facteur_impact
    def get_quartile(self):
        return self._quartile
    def get_acronyme(self):
        return self._acronyme
    def get_nombre_publications_labo(self):
        return self._nombre_publications_labo
    
    #méthodes de la classe
    
    def addFacteur_impact(self,facteur, annee): #méthode pour ajouter un facteur d'impact en fonction d'une année
        self._facteur_impact[int(annee)]=float(facteur) #int pour être sur que l'année est un nombre
    
    def addQuartile(self,quartile, annee): #méthode pour ajouter un quartile en fonction d'une année
        self._quartile[int(annee)]=float(quartile) #float pour être sur que l'année est un nombre et pas un str
    
    def addPublication(self):
        self._nombre_publications_labo+=1
        
    #passage en propriété pour simplifier l'accès ensuite 
    nom_revue = property(get_nom_revue)
    facteur_impact = property(get_facteur_impact, addFacteur_impact)
    quartile = property(get_quartile, addQuartile)
    acronyme = property(get_acronyme)
    nombre_publications_labo = property(get_nombre_publications_labo)
    
    def __repr__(self):
        return "{} d'acronyme {}".format(self.nom_revue, self.acronyme)


class Axe_recherche():
    def __init__(self,lenom_axe):
        self._responsable = None
        self._personnel = [] #liste des internes de l'axe 
        self._nom_axe = str(lenom_axe)
        
    #Assesseurs
    def get_responsable(self):
        return self._responsable
    def get_personnel(self):
        return self._personnel
    def get_nom_axe(self):
        return self._nom_axe
    
    #méthodes
    def addPersonnel(self, qqun):
        if isinstance(qqun,Internes):
            self._personnel.append(qqun)
    
    def addResponsable(self,qqun):
        if isinstance(qqun, Internes):
            self._responsable=qqun
    
    #passage en propriété pour simplifier l'accès ensuite 
    responsable = property(get_responsable)
    personnel = property(get_personnel,addPersonnel)
    nom_axe = property(get_nom_axe)
    
    def __repr__(self):
        return "{}".format(self.nom_axe)
      

class Poste():
    def __init__(self,leintitule,ledate_debut,ledate_fin, leetablissement):
        self._intitule = str(leintitule)
        self._date_debut = dt.date(int(ledate_debut[:4]), int(ledate_debut[5:7]), int(ledate_debut[8:10]))
        self._etablissement = str(leetablissement)
        
        #quand le poste est occupé actuellement, la date de fin n'existe pas  
        self._date_fin = None
        if isinstance(ledate_fin, str):
            self._date_fin = dt.date(int(ledate_fin[:4]), int(ledate_fin[5:7]), int(ledate_fin[8:10]))
        
    #Assesseur
    def get_intitule(self):
        return self._intitule
    def get_date_debut(self):
        return self._date_debut
    def get_date_fin(self):
        return self._date_fin
    def get_etablissement(self):
        return self._etablissement 
    
    #passage en propriété pour simplifier l'accès ensuite 
    intitule = property(get_intitule)
    date_debut = property(get_date_debut)
    date_fin = property (get_date_fin)
    etablissement = property (get_etablissement)
    
class Organisation(): #cette classe est uniquement utile pour l'enregistement du xml
    def __init__(self, ledirecteur):
        self._directeur = str(ledirecteur)
        self._universite = []
        self._axe_de_recherche = {}
        
    #Assesseurs
    def get_directeur(self):
        return self._directeur
    def get_universite(self):
        return self._universite
    def get_axe_de_recherche(self):
        return self._axe_de_recherche
    
    #méthodes
    
    def addUniversite(self,uneuniversite):
        if isinstance(uneuniversite, etablissement):
            self._universite.append(uneuniversite)
    
    def addAxe_de_recherche(self,unaxe,undirecteur):
        self._axe_de_recherche[unaxe]=undirecteur
    
    directeur = property(get_directeur)
    universite = property(get_universite, addUniversite)
    axe_de_recherche = property (get_axe_de_recherche,addAxe_de_recherche)

"""__________________instanciation des objets à partir du xml__________________"""


class Interface():
    def __init__(self):
        ## Création des dictionnaires 
        self.Dict_Internes={} ; self.Dict_Externes={}
        self.Dict_Etablissement={}
        self.Dict_Axes={}
        self.Dict_Projets_These={}
        self.Dict_Projets_Recherche={}
        self.Dict_Projets = {}
        self.Dict_Rate_Directeur={} #clé : Nom Objet : rate
        self.Dict_Rate_Encadrant={} #clé : Nom Objet : rate
        self.Dict_Role_Jury={}
        self.Dict_Poste = {}
        self.Dict_Budget_Etablissements_Realisation={}
        self.Dict_Revues={}
        self.Dict_Quartiles={}
        self.Dict_Facteur_Impact={}
        self.Dict_Article_Journal={}
        self.Dict_Article_Conference={}
        self.Dict_Article_Technique={}
        self.Dict_Quartiles={}
        self.Dict_Facteur_Impact={}
        self.Dict_Organisation={}
        
        # Création des listes pour enregistrement
        self.list_Internes =[]   #non utilisée finalement 
        
        # Réalisation de l'interface utilisateur et de la boucle principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Base de données Labo")
        tabControl = ttk.Notebook(self.fenetre)
        
        
        #Création des onglets
        tab1 = tk.Frame(tabControl,bg='#942811')
        tab2 = tk.Frame(tabControl,bg='#942811')
        tab3 = tk.Frame(tabControl,bg='#942811')
        tab4 = tk.Frame(tabControl,bg='#942811')
        tab5 = tk.Frame(tabControl,bg='#942811' )
        
        #Noms des onglets 
        tabControl.add(tab1, text ='Personnel')
        tabControl.add(tab2, text ='Publications')
        tabControl.add(tab3, text = 'Revues')
        tabControl.add(tab4, text = 'Projets')
        tabControl.add(tab5, text = 'Traitements')
        tabControl.pack(expand = 1, fill ="both")
        
        # Création et positionnement des boutons chargés de gérer la lecture/écriture des fichiers XML
        menuBar=tk.Menu(self.fenetre)
        menuFichier = tk.Menu(menuBar,tearoff=0) #1er menu déroulant
        menuBar.add_cascade(label= 'Fichier', menu=menuFichier)
        menuFichier.add_command(label = 'Ouvrir', command=self.chargementXML)
        menuFichier.add_command(label = 'Enregistrer sous', command = self.enregistrerXML)
        menuFichier.add_separator()
        menuFichier.add_command(label = 'Quitter', command=self.fenetre.destroy)
        
        menuEdit=tk.Menu(menuBar,tearoff=0) #2e menu déroulant
        menuBar.add_cascade(label= 'Help', menu=menuEdit)
        menuEdit.add_command(label= 'About')
        
        
        self.fenetre.config(menu=menuBar)
        
        
        
        #Création des Noms des données à saisir
        tk.Label(tab1,text = "Type de personnel", bg='#EB984E').grid(row=1, column=1, sticky = 'W', padx =5, pady=5)
        tk.Label(tab1, text = "Nom", bg='#EB984E').grid(row=2, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Prénom", bg='#EB984E').grid(row=2, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Sexe", bg='#EB984E').grid(row=3, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Pays de Naissance", bg='#EB984E').grid(row=3, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Informations sur l'interne", bg='#EB984E').grid(row=4, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Date de naissance (AAAA/MM/JJ)", bg='#EB984E').grid(row=5, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Bureau", bg='#EB984E').grid(row=5, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Axe de recherche", bg='#EB984E').grid(row=6, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Taux d'appartenance", bg='#EB984E').grid(row=6, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Historique de carrière: postes occupés", bg='#EB984E').grid(row=7, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Début", bg='#EB984E').grid(row=7, column=3, sticky = 'N',padx = 5, pady = 5)
        tk.Label(tab1, text = "Fin", bg='#EB984E').grid(row=7, column=5, sticky = 'N',padx = 5, pady = 5)

        tk.Label(tab1, text = "Informations sur l'externe", bg='#EB984E').grid(row=8, column = 1, sticky = 'W', padx = 5, pady = 5)
        tk.Label(tab1, text = "Université actuelle", bg='#EB984E').grid(row=8, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Invitations", bg='#EB984E').grid(row=9, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab1, text = "Début", bg='#EB984E').grid(row=9, column=2, sticky = 'N',padx = 5, pady = 5)
        tk.Label(tab1, text = "Fin", bg='#EB984E').grid(row=10, column=2, sticky = 'N',padx = 5, pady = 5)
        
        
        #Instanciation des variables pour la saisie des données 
        self.varType_personnel = tk.StringVar()
        self.varNom = tk.StringVar()
        self.varPrenom = tk.StringVar()
        self.varSexe = tk.StringVar()
        self.varDate_naissance = tk.StringVar()
        self.varPays_naissance = tk.StringVar()
        self.varBureau = tk.StringVar()
        self.varHistorique_carriere = tk.StringVar()
        self.varPoste_debut = tk.StringVar()
        self.varPoste_fin = tk.StringVar()
        self.varAxe_recherche = tk.StringVar()
        self.varTauxAppartenance = tk.StringVar()
        self.varEtabl = tk.StringVar()
        self.varInvit_debut = tk.StringVar()
        self.varInvit_fin = tk.StringVar()
        
        
        
        
        # Création des zones de texte pour la saisie des données 
        ttk.Combobox(tab1, textvariable = self.varType_personnel, values =["Interne", "Externe"], state = 'readonly').grid(row=1, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varNom).grid(row=2, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varPrenom).grid(row=2, column=4, sticky = 'W',padx = 5, pady = 5)
        ttk.Combobox(tab1, textvariable = self.varSexe, values =["F", "M"], state = 'readonly').grid(row=3, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varPays_naissance).grid(row=3, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varDate_naissance).grid(row=5, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varBureau).grid(row=5, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varAxe_recherche).grid(row=6, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varTauxAppartenance).grid(row=6, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varHistorique_carriere).grid(row=7, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varPoste_debut).grid(row=7, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varPoste_fin).grid(row=7, column=6, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varEtabl).grid(row=8, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varInvit_debut).grid(row=9, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab1, textvariable = self.varInvit_fin).grid(row=10, column=3, sticky = 'W',padx = 5, pady = 5)
        
        # Création et positionnement de la zone de liste de choix
        self.liste_Personnel = tk.Listbox(tab1, width = 40, height =25)
        self.liste_Personnel.grid(row = 1, column = 0, rowspan = 10, padx = 5, pady = 5) 
        self.liste_Personnel.bind("<Double-Button-1>", self.afficher_info_Membre_selectionne)
        
        ## Insertion du treeview dans le 1er onglet
        
        self.tv1=ttk.Treeview(tab1)
        columns1 = ('Nom', 'Prénom','Sexe', 'Pays','Poste occupé', 'v', ' ')
        self.tv1.grid(row=13, column=0, columnspan = 5, sticky = 'w e n s',padx = 5, pady = 5)
        self.tv1['columns'] = columns1
        self.tv1.column('#0',width=50, stretch=False)
        self.tv1.column('Nom', anchor=tk.CENTER, width=30)
        self.tv1.column('Prénom', anchor=tk.CENTER, width=30)
        self.tv1.column('Sexe', anchor=tk.CENTER, width=30)
        self.tv1.column('Pays', anchor=tk.CENTER, width=80)
        self.tv1.column('Poste occupé', anchor=tk.CENTER, width=40)
        self.tv1.column('v', anchor=tk.CENTER, width=40)
        self.tv1.column(' ', anchor=tk.CENTER, width=40)
        self.tv1.heading('#0', text='Internes', anchor=tk.CENTER)
        self.tv1.heading('Nom', text='Nom', anchor=tk.CENTER)
        self.tv1.heading('Prénom', text='Prénom', anchor=tk.CENTER)
        self.tv1.heading('Sexe', text='Sexe', anchor=tk.CENTER)
        self.tv1.heading('Pays', text='Pays', anchor=tk.CENTER)
        self.tv1.heading('Poste occupé', text='Poste occupé', anchor=tk.CENTER)
        self.tv1.heading('v', text='v', anchor=tk.CENTER)
        self.tv1.heading(' ', text=' ', anchor=tk.CENTER)
        
        #Insertion du déroulant 'Internes'
        self.tv1.insert('','end', 'internes', text = 'Internes', values = ('', '', '', '', '','Date de naissance', 'Bureau'))
       
        # Insertion déroulant 'Externes' 
        self.tv1.insert('','end', 'externes', text = 'Externes', values = ('', '', '', '','', 'Université', 'Invitations'))
        
        #Suite de la fonction classement des données de la colonne du Treeview
        for col in columns1:
            self.tv1.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column1(_col, False))
        

        # Création des boutons, puis association des bonnes procédures
       
        tk.Button(tab1, text = "Ajouter un personnel", command=self.ajouter_personnel, bg = '#5DADE2').grid(row=11, column=1, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab1, text = "Afficher la pyramide des âges", command=self.pyramide_des_ages, bg = '#5DADE2').grid(row=12, column=1, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab1, text = "Classer les membres par statut", command=self.membres_par_statut, bg = '#5DADE2').grid(row=11, column=2, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
       
        
       
        
        # Onglet Publications
        
        #Création des Titres des Zones de texte à saisir
        tk.Label(tab2, text = "Type", bg='#EB984E').grid(row=1, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Titre", bg='#EB984E').grid(row=2, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Date de publication", bg='#EB984E').grid(row=2, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Auteurs", bg='#EB984E').grid(row=3, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Lien de la publication", bg='#EB984E').grid(row=3, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Informations sur l'article de journal", bg='#EB984E').grid(row=4, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Article tiré du journal", bg='#EB984E').grid(row=5, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Informations sur la conférence", bg='#EB984E').grid(row=6, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Nom de la conférence", bg='#EB984E').grid(row=9, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Lieu de la conférence", bg='#EB984E').grid(row=9, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Intitulé de la conférence", bg='#EB984E').grid(row=10, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab2, text = "Date de la conférence", bg='#EB984E').grid(row=10, column=3, sticky = 'W',padx = 5, pady = 5)
        
        # Instanciation des variables pour la saisie des entrées 
        self.varType_publication = tk.StringVar()
        self.varTitre = tk.StringVar()
        self.varDate_publication=tk.StringVar()
        self.varAuteur = tk.StringVar()
        self.varLien_publication = tk.StringVar()
        self.varJournal_source = tk.StringVar()
        self.varNom_conf = tk.StringVar()
        self.varLieu_conf = tk.StringVar()
        self.varIntitule_conf = tk.StringVar()
        self.varDate_conf = tk.StringVar()
        
        
        
        # Création des zones de texte et positionnement
        ttk.Combobox(tab2, textvariable = self.varType_publication, values =["Article de Journal", "Article de conférence", "Rapport"], state = 'readonly').grid(row=1, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varTitre).grid(row=2, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varDate_publication).grid(row=2, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varAuteur).grid(row=3, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varLien_publication).grid(row=3, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varJournal_source).grid(row=5, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varNom_conf).grid(row=9, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varLieu_conf).grid(row=9, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varIntitule_conf).grid(row=10, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab2, textvariable = self.varDate_conf).grid(row=10, column=4, sticky = 'W',padx = 5, pady = 5)
        
        
        
        # Création et positionnement de la zone de listbox des publications
        self.liste_Publications = tk.Listbox(tab2, width = 40, height =25)
        self.liste_Publications.grid(row = 1, column = 0, rowspan = 10, padx = 5, pady = 5) 
        
        #Création du Treeview des Articles de journal
        self.tv21=ttk.Treeview(tab2)
        columns21 = ('Titre', 'Date de publication', 'Auteur', 'Renommee')
        self.tv21.grid(row=12, column=2, columnspan = 4, sticky = 'w e n s',padx = 5, pady = 5)
        self.tv21['columns'] = columns21
        self.tv21.column('#0', width=80, stretch=False)
        self.tv21.column('Titre', anchor=tk.CENTER, width=60)
        self.tv21.column('Date de publication', anchor=tk.CENTER, width=60)
        self.tv21.column('Auteur', anchor=tk.CENTER, width=60)
        self.tv21.column('Renommee', anchor=tk.CENTER, width=60)
        self.tv21.heading('#0', text='Articles de Journal', anchor=tk.CENTER)
        self.tv21.heading('Titre', text='Titre', anchor=tk.CENTER)
        self.tv21.heading('Date de publication', text='Date de Publication', anchor=tk.CENTER)
        self.tv21.heading('Auteur', text='Auteur', anchor=tk.CENTER)
        self.tv21.heading('Renommee', text='Renommee', anchor=tk.CENTER)
       
        
        #Suite de la fonction classement des données de la colonne du Treeview
        for col in columns21:
            self.tv21.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column21(_col, False))
        
        #Création du treeview des articles de conférences
        
        self.tv22=ttk.Treeview(tab2)
        columns22 = ('Titre', 'Date de publication', 'Auteur', 'Nom de la conférence')
        self.tv22.grid(row=7, column=9, columnspan = 4, sticky = 'w e n s',padx = 5, pady = 5)
        self.tv22['columns'] = columns22
        self.tv22.column('#0', width=80, stretch=False)
        self.tv22.column('Titre', anchor=tk.CENTER, width=60)
        self.tv22.column('Date de publication', anchor=tk.CENTER, width=60)
        self.tv22.column('Auteur', anchor=tk.CENTER, width=60)
        self.tv22.column('Nom de la conférence', anchor=tk.CENTER, width=60)
        self.tv22.heading('#0', text='Articles de conférence', anchor=tk.CENTER)
        self.tv22.heading('Titre', text='Titre', anchor=tk.CENTER)
        self.tv22.heading('Date de publication', text='Date de Publication', anchor=tk.CENTER)
        self.tv22.heading('Auteur', text='Auteur', anchor=tk.CENTER)
        self.tv22.heading('Nom de la conférence', text='Nom de la conférence', anchor=tk.CENTER)
       
        
        
        
        #Suite de la fonction classement des données de la colonne du Treeview
        for col in columns22:
            self.tv22.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column22(_col, False))
        
        # Création du Treeview des rapports techniques
        self.tv23=ttk.Treeview(tab2)
        columns23 = ('Titre', 'Date de publication', 'Auteur', 'Nom de la conférence')
        self.tv23.grid(row=7, column=9, columnspan = 4, sticky = 'w e n s',padx = 5, pady = 5)
        self.tv23['columns'] = columns23
        self.tv23.column('#0', width=80, stretch=False)
        self.tv23.column('Titre', anchor=tk.CENTER, width=60)
        self.tv23.column('Date de publication', anchor=tk.CENTER, width=60)
        self.tv23.column('Auteur', anchor=tk.CENTER, width=60)
        self.tv23.column('Nom de la conférence', anchor=tk.CENTER, width=60)
        self.tv23.heading('#0', text='Rapports Techniques', anchor=tk.CENTER)
        self.tv23.heading('Titre', text='Titre', anchor=tk.CENTER)
        self.tv23.heading('Date de publication', text='Date de Publication', anchor=tk.CENTER)
        self.tv23.heading('Auteur', text='Auteur', anchor=tk.CENTER)
        self.tv23.heading('Nom de la conférence', text='Nom de la conférence', anchor=tk.CENTER)
       
        
        #Suite de la fonction classement des données de la colonne du Treeview
        for col in columns23:
            self.tv23.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column23(_col, False))


        # Création du bouton ajouter une note, puis association la bonne procédure ajouter_note
        tk.Button(tab2, text = "Ajouter une publication", bg = '#5DADE2').grid(row=11, column=1, columnspan = 2, sticky = 'w e n s',padx = 5, pady = 5)
        
        ## Onglet REVUES
        #Instanciation des titres des zones de texte
        tk.Label(tab3, text = "Nom du Journal", bg='#EB984E').grid(row=1, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab3, text = "Acronyme de la revue", bg='#EB984E').grid(row=1, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab3, text = "Performances", bg='#EB984E').grid(row=3, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab3, text = "Facteur d'influence", bg='#EB984E').grid(row=4, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab3, text = "Quartile", bg='#EB984E').grid(row=4, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab3, text = "Année", bg='#EB984E').grid(row=5, column=1, sticky = 'W',padx = 5, pady = 5)
        
        #Instanciation des variables 
        self.varNom_Journal = tk.StringVar()
        self.varAcronyme_revue = tk.StringVar()
        self.varFI = tk.StringVar()
        self.varQuartile = tk.StringVar()
        self.varAnnee_revue = tk.StringVar()
        
       
        # Création et plcement des entrées
        
        tk.Entry(tab3, textvariable = self.varNom_Journal).grid(row=1, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab3, textvariable = self.varAcronyme_revue).grid(row=1, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab3, textvariable = self.varFI).grid(row=4, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab3, textvariable = self.varQuartile).grid(row=4, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab3, textvariable = self.varAnnee_revue).grid(row=5, column=2, sticky = 'W',padx = 5, pady = 5)
        
        # Création et positionnement de la zone de liste de choix
        self.liste_revue = tk.Listbox(tab3, width = 25, height =15)
        self.liste_revue.grid(row = 1, column = 0, rowspan = 5, padx = 5, pady = 5) 
        # self.liste_revue.bind("<Double-Button-1>", self.afficher_revue)
        
        
        self.tv3=ttk.Treeview(tab3)
        columns = ('Nom Journal', 'FI', 'Quartile')
        self.tv3.grid(row=8, column=2, columnspan = 4, sticky = 'w e n s',padx = 5, pady = 5)
        self.tv3['columns'] = columns
        self.tv3.column('#0', width=0, stretch=False)
        self.tv3.column('Nom Journal', anchor=tk.CENTER, width=80)
        self.tv3.column('FI', anchor=tk.CENTER, width=80)
        self.tv3.column('Quartile', anchor=tk.CENTER, width=80)
        self.tv3.heading('#0', text='', anchor=tk.CENTER)
        self.tv3.heading('Nom Journal', text='Id', anchor=tk.CENTER)
        self.tv3.heading('FI', text='Facteur influence', anchor=tk.CENTER)
        self.tv3.heading('Quartile', text='Quartile', anchor=tk.CENTER)
       
        #Suite de la fonction classement de la colonne
        for col in columns:
            self.tv3.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column3(_col, False))


        # Création du bouton ajouter une revue, puis association de la procédure
        tk.Button(tab3, text = "Ajouter une revue", bg = '#5DADE2').grid(row=6, column=1, columnspan = 2, sticky = 'w e n s',padx = 5, pady = 5)
        
        
        # Onglet Projets
        
        # Création des textes correspondant à chaque information à saisir par l'utilisateur
        tk.Label(tab4, text = "Type de projet", bg='#EB984E').grid(row=1, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Projet de Thèse", bg='#EB984E').grid(row=2, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Titre du projet de Thèse", bg='#EB984E').grid(row=3, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Date de soutenance", bg='#EB984E').grid(row=3, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Doctorant", bg='#EB984E').grid(row=4, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Lieu de soutenance", bg='#EB984E').grid(row=4, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Equipe de superviseurs", bg='#EB984E').grid(row=5, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Taux d'implication", bg='#EB984E').grid(row=5, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Jury", bg='#EB984E').grid(row=6, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Role du jury", bg='#EB984E').grid(row=6, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Lien du projet", bg='#EB984E').grid(row=7, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Projet de recherche", bg='#EB984E').grid(row=8, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Intitulé du projet de recherche", bg='#EB984E').grid(row=9, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Acronyme du projet de recherche", bg='#EB984E').grid(row=9, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Date prévisionnelle de fin", bg='#EB984E').grid(row=10, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Pilote du projet de recherche", bg='#EB984E').grid(row=10, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Equipe du projet de recherche", bg='#EB984E').grid(row=11, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Investisseurs", bg='#EB984E').grid(row=12, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Budget", bg='#EB984E').grid(row=12, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab4, text = "Rapport technique associé", bg='#EB984E').grid(row=13, column=1, sticky = 'W',padx = 5, pady = 5)
        
        
        # Création des variables pour la mise en place des saisies de données par l'utilisateur
        
        self.varType_projet = tk.StringVar()
        self.varTitre = tk.StringVar()
        self.varDate_soutenance = tk.StringVar()
        self.varCandidat = tk.StringVar()
        self.varLieu_soutenance = tk.StringVar()
        self.varEquipe_superviseurs = tk.StringVar()
        self.varTaux_implication = tk.StringVar()
        self.varJury = tk.StringVar()
        self.varRole_Jury = tk.StringVar()
        self.varLien_projet = tk.StringVar()
        self.varIntitule_recherche = tk.StringVar()
        self.varAcronyme_recherche = tk.StringVar()
        self.varDate_fin = tk.StringVar()
        self.varPilote_recherche = tk.StringVar()
        self.varEquipe_recherche = tk.StringVar()
        self.varInvestisseurs = tk.StringVar()
        self.varBudget = tk.StringVar()
        self.varRt_associe = tk.StringVar()
        
        
        # Création des zones de texte associées aux variables définies ci-dessus et les positionner dans la grille.
        ttk.Combobox(tab4, textvariable = self.varType_projet, values =["Projet de thèse", "Projet de recherche"], state = 'readonly').grid(row=1, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varTitre).grid(row=3, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varDate_soutenance).grid(row=3, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varCandidat).grid(row=4, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varLieu_soutenance).grid(row=4, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varEquipe_superviseurs).grid(row=5, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varTaux_implication).grid(row=5, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varJury).grid(row=6, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varRole_Jury).grid(row=6, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varLien_projet).grid(row=7, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varIntitule_recherche).grid(row=9, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varAcronyme_recherche).grid(row=9, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varDate_fin).grid(row=10, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varPilote_recherche).grid(row=10, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varEquipe_recherche).grid(row=11, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varInvestisseurs).grid(row=12, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varBudget).grid(row=12, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab4, textvariable = self.varRt_associe).grid(row=13, column=2, sticky = 'W',padx = 5, pady = 5)
        
        # Création et positionnement de la zone de liste de choix
        self.liste_projects = tk.Listbox(tab4, width = 40, height =25)
        self.liste_projects.grid(row = 1, column = 0, rowspan = 13, padx = 5, pady = 5) 
        # self.liste_Eleves.bind("<Double-Button-1>", self.afficher_info_projet)
        
        
        
        ## Création du Treeview des projets
        
        
        self.tv4=ttk.Treeview(tab4)
        columns4 = ('v', '',' ','  ','   ')
        self.tv4.grid(row=14, column=0, columnspan = 8, sticky = 'w e n s',padx = 10, pady = 10)
        self.tv4['columns'] = columns4
        #Création des colonnes
        self.tv4.column('#0',width=80, stretch=False)
        self.tv4.column('v', anchor=tk.CENTER, width=80)
        self.tv4.column('v', anchor=tk.CENTER, width=80)
        self.tv4.column(' ', anchor=tk.CENTER, width=80)
        self.tv4.column('   ', anchor=tk.CENTER, width=80)
        self.tv4.column('   ', anchor=tk.CENTER, width=80)
        #Définition des Titres des colonnes 
        self.tv4.heading('#0', text='Type de Projet', anchor=tk.CENTER)
        self.tv4.heading('v', text='v', anchor=tk.CENTER)
        self.tv4.heading('', text='', anchor=tk.CENTER)
        self.tv4.heading(' ', text='', anchor=tk.CENTER)
        self.tv4.heading('   ', text='V', anchor=tk.CENTER)
        self.tv4.heading('   ', text='V', anchor=tk.CENTER)
        
        #Insertion du déroulant 'Projet de recherche'
        self.tv4.insert('','end', 'projet_recherche', text = 'Projet de recherche', values = ('Titre projet recherche', 'Date de fin prévisonielle', 'Société et investissement', 'Pilote recherche', 'Equipe'))
       
        # Insertion déroulant 'Projet de thèse' 
        self.tv4.insert('','end', 'projet_these', text = 'Projet de thèse', values = ('Titre', 'Date de soutenance', 'Laboratoire', 'Doctorant', 'Directeur'))
        
        # Continuité de la fonction sort pour le treeview 4 
        for col in columns4:
            self.tv4.heading(col, text=col,command=lambda _col=col: self.treeview_sort_column4(_col, False))


        # Création du bouton ajouter un projet
        tk.Button(tab4, text = "Ajouter un projet", bg = '#5DADE2').grid(row=13, column=1, columnspan = 2, sticky = 'w e n s',padx = 5, pady = 5)
        
        
        
        #Création des Libellés des données
        
        tk.Label(tab5, text = "TRAITEMENTS", bg='#EB984E').grid(row=1, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab5, text = "Date 1", bg='#EB984E').grid(row=5, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab5, text = "Date 2", bg='#EB984E').grid(row=5, column=3, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab5, text = "Auteur", bg='#EB984E').grid(row=6, column=1, sticky = 'W',padx = 5, pady = 5)
        tk.Label(tab5, text = "Axe", bg='#EB984E').grid(row=6, column=3, sticky = 'W',padx = 5, pady = 5)
        
        #Instanciation des variables pour la saisie de donnée
        self.varDate1 = tk.StringVar()
        self.varDate2 = tk.StringVar()
        self.varAuteur_publications = tk.StringVar()
        self.varAxe_publications = tk.StringVar()
        
        #Création des zones de saisie de texte
        tk.Entry(tab5, textvariable = self.varDate1).grid(row=5, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab5, textvariable = self.varDate2).grid(row=5, column=4, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab5, textvariable = self.varAuteur_publications).grid(row=6, column=2, sticky = 'W',padx = 5, pady = 5)
        tk.Entry(tab5, textvariable = self.varAxe_publications).grid(row=6, column=4, sticky = 'W',padx = 5, pady = 5)
        
        #Création des boutons dans l'interface, associés aux traitements correspondants 
        tk.Button(tab5, text = "Revues utilisées par le labo", command=self.revues_utilisees, bg = '#5DADE2').grid(row=11, column=3, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Taux d'articles en colab externes", command=self.taux_articles_externes, bg = '#5DADE2').grid(row=11, column=4, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Taux de thèses en colab externes", command=self.taux_theses_externes, bg = '#5DADE2').grid(row=11, column=5, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Taux de publication doctorant", command=self.taux_publication_doctorant, bg = '#5DADE2').grid(row=12, column=5, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Listes des partenaires Projets", command=self.partenaires_projets, bg = '#5DADE2').grid(row=12, column=4, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Listes des projets multi-axiaux", command=self.projets_multi_axes, bg = '#5DADE2').grid(row=12, column=3, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Listes des publication multi-axiales", command=self.publications_multi_axes, bg = '#5DADE2').grid(row=12, column=2, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5) 
        tk.Button(tab5, text = "Publications de l'auteur sur la période", command =  self.publication_auteur, bg = '#5DADE2').grid(row=13, column=2, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Publications de l'axe sur la période", command =  self.publication_axe, bg = '#5DADE2').grid(row=13, column=4, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Publications du labo sur la période", command =  self.publication_laboratoire, bg = '#5DADE2').grid(row=14, column=4, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Nombre moyen publications par doctorant sur la période", command =  self.publication_moyenne_doctorant, bg = '#5DADE2').grid(row=15, column=4, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Durée moyenne des thèses sur la période en jours", command =  self.duree_these, bg = '#5DADE2').grid(row=13, column=3, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Liste des taux d'encadrements sur la période", command =  self.encadrement_cumule, bg = '#5DADE2').grid(row=14, column=3, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        tk.Button(tab5, text = "Montant projets conclus sur la période par axe de recherche", command =  self.montant_des_projets, bg = '#5DADE2').grid(row=15, column=3, columnspan = 1, sticky = 'w e n s',padx = 5, pady = 5)
        
        
        self.fenetre.mainloop()
        
        
    def chargementXML(self):
        """Charge un document XML organisé comme dataexample et instancie les objets dans les classes"""
        fichieracharger = TKFD.askopenfilename(title = 'Laboratory_data_example v1.4...', defaultextension = ".xml", filetypes = [("XML", "*.xml")], multiple = False)
        if fichieracharger != "":    
            arbrexml = ET.parse(fichieracharger)
            # Obtention du tronc de l'arbre XML
            tronc = arbrexml.getroot()
            
            for Axe in tronc[0].findall('Research_Team'):
                self.Dict_Axes[Axe.get('Name')]=Axe_recherche(Axe.get('Name'))
                
            """----------MEMBRES---------"""
            
            #(Internes)
            for member in tronc[1].findall('Member'):
                
                leliste_poste = [] #format [[intitulé, date début, date fin],[...],...]
                for mesposte in member.findall('Position'):
                    
                    #Instanciation des établissements :
                    if mesposte.get('Company') not in self.Dict_Etablissement.keys() and mesposte.get('Company') is not None:
                        self.Dict_Etablissement[mesposte.get('Company')]=etablissement(mesposte.get('Company'))
                        
                    leliste_poste.append(Poste(mesposte.get('Name'), mesposte.get('Start'), mesposte.get('End'), mesposte.get('Company')))
                    
                leDict_axe = {} #format {NomAxe;axerate}
                for axe in member.findall('Research_Team'):
                    leDict_axe [axe.get('Name')] = axe.get('Rate')
                
                
                self.Dict_Internes[member.get('Name')] = Internes(member.get('Name'),member.get('FirstName'),member.get('Gender'), member.get('BD'), member.get('Country'),member.get('Office'),leliste_poste, leDict_axe)
                    
                #implémentation du personnel dans la classe axes :
                for axe in member.findall('Research_Team'):
                    self.Dict_Axes[axe.get('Name')].addPersonnel(self.Dict_Internes[member.get('Name')])
                    
                    
                for mesposte in member.findall('Position'):
                    if mesposte.get('Company') is not None:
                        self.Dict_Etablissement[mesposte.get('Company')].addEmploye(self.Dict_Internes[member.get('Name')])
                
            #(Externes)
            
            for member in tronc[1].findall('External_Member'):
               
                leinvitations=[]
                
                for visite in member.findall('Stay'):
                    leinvitations.append([visite.get('Start'), visite.get('End')])
                #lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance, leposte_occupe, leetablissement_actuel, leinvitations
                self.Dict_Externes [member.get('Name')] = Externes(member.get('Name'),member.get('FirstName'),member.get('Gender'),member.get('BD'),member.get('Country'),member.get('Job'),member.get('Company'),leinvitations)
                
                #etablissement 
                if not member.get('Company') in self.Dict_Etablissement.keys():
                    self.Dict_Etablissement[member.get('Company')]=etablissement(member.get('Company'))
                
                self.Dict_Etablissement[member.get('Company')].addEmploye(self.Dict_Externes[member.get('Name')])
                
            # (Tous les Membres)
            self.Dict_Membres = {**self.Dict_Internes, **self.Dict_Externes} #concatène self.Dict_Internes et self.Dict_Externes
            for memberPOO in list(self.Dict_Membres.values()):
                self.liste_Personnel.insert("end",str(memberPOO))
            
            
            """-----------AXES 2-----------""" #implémentation des directeurs d'axe 
            
            for Axe in tronc[0].findall('Research_Team'):
                self.Dict_Axes[Axe.get('Name')].addResponsable(self.Dict_Internes[Axe.get('Head')])
                
            
            """-----------PROJETS----------"""
            Liste_Temporaire_Projets=[] #sert à instancier les projets associés
            
            
            #PhD (projet de thèse)
            
            
            for projet in tronc[2].findall('PhD'):
                
                #Pour la liste temporaire
                Liste_Temporaire_Projets.append(projet.get('Name'))
                
                #PhD_Director Name Rate
                
                for directeur_projet in projet.findall('PhD_Director'):
                     self.Dict_Rate_Directeur[directeur_projet.get('Name')]=directeur_projet.get('Rate')
            
                # les Supervisor Name et Rate
                
                for encadrant_projet in projet.findall('Supervisor'):
                     self.Dict_Rate_Encadrant[encadrant_projet.get('Name')]= encadrant_projet.get('Rate')
            
                # Production Ref 
                leref = None  #reinitialise leref pour éviter de concerver la référence du projet précédent du xml
                for ref in projet.findall('Production'): #la boucle for évite l'erreur due à  None.get('blabla') dans le cas où le projet n'a pas de production 
                     leref= ref.get('Ref')
                
                # Jury
                
                for jury in projet.findall('Jury_Members'):
                    for membrejury in jury.findall('Member'):
                        self.Dict_Role_Jury[membrejury.get('Name')]=(membrejury.get('Role'))
                
                #Instanciation des établissements :
                if projet.get('Place') not in self.Dict_Etablissement.keys() and projet.get('Place') != 'LCFC-Metz':
                        self.Dict_Etablissement[projet.get('Place')]=etablissement(projet.get('Place'))
                        self.Dict_Etablissement[projet.get('Place')].addNombre_projets_communs()
                
                #letitre, leetablissement_realisation,ledate_lancement, lejury_soutenance,ledoctorant,ledirecteur,leencadrant
                self.Dict_Projets_These[projet.get('Name')]= Projet_these(projet.get('Name'),projet.get('Place'),projet.get('Start'), self.Dict_Role_Jury, self.Dict_Internes[projet.get('Candidate')],self.Dict_Rate_Directeur,self.Dict_Rate_Encadrant)
                self.Dict_Projets_These[projet.get('Name')].date_soutenance=projet.get('Defense_Date')    #appel de la property          
                self.Dict_Projets_These[projet.get('Name')].addRef_production(leref)
                
            #PhD (projet de recherche)
            
            for Projet in tronc[2].findall('Project'):
                
                #Pour la liste temporaire
                Liste_Temporaire_Projets.append(Projet.get('Name'))
                
                #personnes_impliquees
                Liste_Personnes_Impliquees=[] #clé : Nom Objet : rate
                for membre_projet in Projet.findall('Member'):
                     Liste_Personnes_Impliquees.append(membre_projet.get('Name'))
                
                #etablissements_realisation
               
                for etablissement_projet in Projet.findall('Company_Involved'):
                    if not etablissement_projet.get('Name') in self.Dict_Etablissement.keys():
                        self.Dict_Etablissement[etablissement_projet.get('Name')]= etablissement(etablissement_projet.get('Name'))
                    self.Dict_Budget_Etablissements_Realisation[etablissement_projet.get('Name')]=float(etablissement_projet.get('Funding').replace(' ','')) #replace enleve les espaces des nombres
                    #budget de collaboration avec le laboratoire
                    self.Dict_Etablissement[etablissement_projet.get('Name')].addBudget_projets_communs(float(etablissement_projet.get('Funding').replace(' ','')))
                    self.Dict_Etablissement[etablissement_projet.get('Name')].addNombre_projets_communs()
                    
                #budget total du projet
                budget_total = 0
                for budget in self.Dict_Budget_Etablissements_Realisation.keys():
                    budget_total += self.Dict_Budget_Etablissements_Realisation[budget]
                
                #letitre, leetablissement_realisation, leacronyme,lebudget, lepersonnes_impliquees, lepilote_projet_recherche
                self.Dict_Projets_Recherche[Projet.get('Name')] = Projet_recherche(Projet.get('Name'),self.Dict_Budget_Etablissements_Realisation,Projet.get('Short'),budget_total,Liste_Personnes_Impliquees,Projet.get('Head'))
                self.Dict_Projets_Recherche[Projet.get('Name')].date_debut = Projet.get('Start')    #appel de la property
                self.Dict_Projets_Recherche[Projet.get('Name')].date_previsionnelle = Projet.get('Expected_End') 
                self.Dict_Projets_Recherche[Projet.get('Name')].date_fin = Projet.get('End') 
            
            #Projets associés 
            
                #pour les projets de thèse
            for projet in tronc[2].findall('PhD'):
                List_Projet_Associe=[]
                for projetassocie in projet.findall('Project_Link'):
                    if projetassocie.get('Name') in self.Dict_Projets.keys():
                        List_Projet_Associe.append(self.Dict_Projets[projetassocie.get('Name')])
                    else : 
                        List_Projet_Associe.append('Projet non référencé : ' + projetassocie.get('Name'))
                self.Dict_Projets_These[projet.get('Name')].projets_associes = List_Projet_Associe
                
                #pour les projets de recherche
            for Projet in tronc[2].findall('Project'):
                List_Projet_Associe=[]
                for projetassocie in Projet.findall('Project_Link'):
                    if projetassocie.get('Name') in self.Dict_Projets.keys():
                        List_Projet_Associe.append(self.Dict_Projets[projetassocie.get('Name')])
                    else : 
                        List_Projet_Associe.append('Projet non référencé : ' + projetassocie.get('Name'))
                self.Dict_Projets_Recherche[Projet.get('Name')].projets_associes = List_Projet_Associe
            
            
            """----------REVUES---------"""
            
            for desjournaux in tronc[3].findall('Journals'):
                for lejournal in desjournaux.findall('Journal'):
                    
                    
                    for lesannees in lejournal.findall('Performances'):
                        self.Dict_Quartiles[int(lesannees.get('Year'))]=float(lesannees.get('Quartile'))
                        self.Dict_Facteur_Impact[int(lesannees.get('Year'))]=float(lesannees.get('IF'))
                        
                    #lenom_revue, leacronyme, lequartile, lefacteur_impact
                    self.Dict_Revues[lejournal.get('Short')]=revue(lejournal.get('Name'),lejournal.get('Short'),self.Dict_Quartiles,self.Dict_Facteur_Impact)
                
            
            """----------PUBLICATIONS---------"""
            
            #Article de journal
            
            for article in tronc[3].findall('Journal_paper'):
            
                #auteurs_article
                Liste_Auteurs=[]
                for chaqueauteur in article.findall('Author'):
                    Liste_Auteurs.append(chaqueauteur.get('Name'))
                
                
                #ledate, leauteurs, letitre, lelien, lenom_revue
                self.Dict_Article_Journal[article.get('Title')]=article_journal(article.get('Available'), Liste_Auteurs, article.get('Title'), article.get('DOI'), article.get('Journal') )
                self.Dict_Revues[article.get('Journal')].addPublication()
            
                self.Dict_Article_Journal[article.get('Title')].addQuartile(self.Dict_Revues[article.get('Journal')].quartile)
                self.Dict_Article_Journal[article.get('Title')].addFacteur_impact(self.Dict_Revues[article.get('Journal')].facteur_impact)
            
            #Article de conférence
            
            for article in tronc[3].findall('Conference'):
                           
                #auteurs_article
                Liste_Auteurs=[]
                for chaqueauteur in article.findall('Author'):
                    Liste_Auteurs.append(chaqueauteur.get('Name'))
                
              
                #ledate, leauteurs, letitre, lelien, lenom_conference, ledate_conference, lelieu_conference
                self.Dict_Article_Conference[article.get('Title')]=article_conference(article.get('Available'), Liste_Auteurs,article.get('Title'),article.get('DOI'),article.get('Conference_Name'),article.get('Dates'),article.get('Place'))
            
            #Revue technique 
            
            for article in tronc[3].findall('Report'):
                
                #auteurs_article
                Liste_Auteurs=[]
                for chaqueauteur in article.findall('Author'):
                    Liste_Auteurs.append(chaqueauteur.get('Name'))
                
                #ledate, leauteurs, letitre, lelien
                self.Dict_Article_Technique[article.get('Title')]=rapport_technique(article.get('Available'), Liste_Auteurs,article.get('Title'),article.get('DOI'))
            
            """----------Organisation-----------"""
            
            
            for uneorga in tronc.findall('Organization'):
                self.Dict_Organisation[uneorga.get('Laboratory_Head_Name')]=Organisation(uneorga.get('Laboratory_Head_Name'))
                #universites
                for chaque_universite in uneorga.findall('University'):
                    self.Dict_Organisation[uneorga.get('Laboratory_Head_Name')].addUniversite(chaque_universite.get('Name'))
        
            
            
            #Insérer les personnels dans treeview
            for member in self.Dict_Externes.values():
                self.tv1.insert('externes', 'end', text='', values=(member.nom, member.prenom, member.sexe, member.pays_de_naissance, member.poste_occupe, member.etablissement_actuel, member.invitations))
            
            for member in self.Dict_Internes.keys():
                self.tv1.insert('internes', 'end', text='', values=(self.Dict_Internes[member].nom, self.Dict_Internes[member].prenom, self.Dict_Internes[member].sexe, self.Dict_Internes[member].pays_de_naissance, self.Dict_Internes[member].postes_actuels[0], self.Dict_Internes[member].date_de_naissance, self.Dict_Internes[member].bureau_occupe))
                        
            #Insérer les Revues dans la listbox revue
            for revuePOO in list(self.Dict_Revues.values()):
                self.liste_revue.insert("end",str(revuePOO))
                       
            self.Dict_Publication = {**self.Dict_Article_Conference, **self.Dict_Article_Journal, **self.Dict_Article_Technique}
            
            for artconf in list(self.Dict_Article_Conference.values()):
                self.liste_Publications.insert("end", str(artconf))
            for artjourn in list(self.Dict_Article_Journal.values()):
                self.liste_Publications.insert("end", str(artjourn))
            for artech in list(self.Dict_Article_Technique.values()):
                self.liste_Publications.insert("end", str(artech))
            
            #Insérer les Revues dans le treeview
            
            for revuePOO in list(self.Dict_Revues.values()):
                self.tv3.insert(parent='',index=0, text='',values=(revuePOO.nom_revue, revuePOO.facteur_impact, revuePOO._quartile))
                
            # Insérer les articles de Journaux dans le Treeview
            for articlePOO in list(self.Dict_Article_Journal.values()):
                self.tv21.insert(parent='',index = 0, text='',values=(articlePOO.titre, articlePOO.date, articlePOO.auteurs, articlePOO.renommee))
            
            #Insérer les projets
            
            self.Dict_Projets = {**self.Dict_Projets_Recherche, **self.Dict_Projets_These}
            
            for projetPOO in list(self.Dict_Projets.values()):
                self.liste_projects.insert("end", str(projetPOO))
            
            # Insertion projets recherche dans Treeview
            
            for projetPOO in list(self.Dict_Projets_Recherche.values()):
                self.tv4.insert('projet_recherche','end', text='',values=(projetPOO.titre, projetPOO.date_previsionnelle, projetPOO.etablissement, projetPOO.pilote_projet_recherche, projetPOO.personnes_impliquees ))
            
            # Insertion projets thèse dans Treeview
            for projetPOO in list(self.Dict_Projets_These.values()):
                self.tv4.insert('projet_these','end', text='',values=(projetPOO.titre, projetPOO.date_soutenance, projetPOO.etablissement, projetPOO.doctorant, projetPOO.directeur))
    
    ### TRAITEMENTS

    #Classer les valeurs des colonnes de Treeview (onglet Personnel) (Permet de classer les objets selon la donnée sélectionée en appuyant sur le titre de la colonne)
    def treeview_sort_column1(self, col, reverse):
        l = [(self.tv1.set(k, col), k) for k in self.tv1.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv1.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv1.heading(col, command=lambda _col=col: self.treeview_sort_column1(_col, not reverse))
        
    #Classer les valeurs des colonnes de Treeview sur les articles de journal
    def treeview_sort_column21(self, col, reverse):
        l = [(self.tv21.set(k, col), k) for k in self.tv21.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv21.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv21.heading(col, command=lambda _col=col: self.treeview_sort_column21(_col, not reverse))
    
    #Classer les valeurs des colonnes de Treeview sur les articles de conférence
    def treeview_sort_column22(self, col, reverse):
        l = [(self.tv22.set(k, col), k) for k in self.tv22.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv22.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv22.heading(col, command=lambda _col=col: self.treeview_sort_column22(_col, not reverse))
    
    #Classer les valeurs des colonnes de Treeview sur les rapports techniques
    def treeview_sort_column23(self, col, reverse):
        l = [(self.tv23.set(k, col), k) for k in self.tv23.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv23.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv23.heading(col, command=lambda _col=col: self.treeview_sort_column23(_col, not reverse))
    
    # Classer les valeurs des colonnes du treeview (pour l'onglet revues)
    def treeview_sort_column3(self, col, reverse):
        l = [(self.tv3.set(k, col), k) for k in self.tv3.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv3.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv3.heading(col, command=lambda _col=col: self.treeview_sort_column3(_col, not reverse))
    
    #Classer les valeurs des colonnes treeview onglet Projets 
    def treeview_sort_column4(self, col, reverse):
        l = [(self.tv4.set(k, col), k) for k in self.tv4.get_children('')]
        l.sort(reverse=reverse)
    
        # réarrangement des données en les classant
        for index, (val, k) in enumerate(l):
            self.tv4.move(k, '', index)
    
        # Classement inversé au prochain clic
        self.tv4.heading(col, command=lambda _col=col: self.treeview_sort_column4(_col, not reverse))
    
    def afficher (self):
        Dict_Membres = {**self.Dict_Internes, **self.Dict_Externes}
        for memberPOO in list(Dict_Membres.values()):
                self.liste_Personnel.insert("end",str(memberPOO))
    
    def afficher_info_Membre_selectionne(self, event):
        if self.liste_Personnel.curselection()[0] != None:
          
            if list(self.Dict_Internes)[self.liste_Personnel.curselection()[0]] in list(self.Dict_Internes.keys()):
                
                _Membre_selectionne = self.Dict_Internes[list(self.Dict_Internes)[self.liste_Personnel.curselection()[0]]]
                # On l'affiche également dans une fenetre de dialogue de type pop-up
                for poste in _Membre_selectionne.taux_appartenance:
                    
                    tk.messagebox.showinfo(title = "Information sur {}".format(str(_Membre_selectionne)), message = "Nom : {} \n Prénom : {} \n Sexe : {} \n Pays de naissance :{} \n Date de naissance : {} \n Bureau : {} \n Historique de carrière : {} de {} à {} \n Axes de recherche : {}"  .format(str(_Membre_selectionne.nom), str(_Membre_selectionne.prenom), str(_Membre_selectionne.sexe), str(_Membre_selectionne.pays_de_naissance), str(_Membre_selectionne.date_de_naissance), str(_Membre_selectionne.bureau_occupe),str(_Membre_selectionne.historique_carriere[0].intitule), str(_Membre_selectionne.historique_carriere[0].date_debut), str(_Membre_selectionne.historique_carriere[0].date_fin), str(_Membre_selectionne.taux_appartenance)))
            
            else:
                if list(self.Dict_Externes)[self.liste_Personnel.curselection()[0]] in list(self.Dict_Externes.keys()):
                    _Membre_selectionne = self.Dict_Externes[list(self.Dict_Externes)[self.liste_Personnel.curselection()[0]]]
                    
                    # On l'affiche également dans une fenetre de dialogue de type pop-up
                    
                    tk.messagebox.showinfo(title = "Information sur {}".format(str(_Membre_selectionne)), message = "Nom : {} \n Prénom : {} \n Sexe : {} \n Pays de naissance :{} \n Université : {} \n Invitations : {}"  .format(str(_Membre_selectionne.nom), str(_Membre_selectionne.prenom), str(_Membre_selectionne.sexe), str(_Membre_selectionne.pays_de_naissance), str(_Membre_selectionne.etablissement_actuel),str(_Membre_selectionne.invitations)))
    
    
    #Ajouter un personnel dans le xml
    def ajouter_personnel(self):
        def corriger_date(unedate):
            if isinstance(unedate, dt.date):
                Annee= str(unedate.year)
                
                if len(str(unedate.month))<2:
                    Mois='0'+str(unedate.month)
                else:
                    Mois= str(unedate.month)
                if len(str(unedate.day)) <2:
                    Jour = '0'+str(unedate.day)
                else:
                    Jour = str(unedate.day)
                return(Annee+'/'+Mois+'/'+Jour)
        self.Dict_axe_taux = {}
        if self.varType_personnel.get() == "Internes":
            if self.varPoste_debut.get() != '' and self.varHistorique_carriere.get() != '':
                if self.varNom.get()!='' and self.varPrenom.get()!='' and self.varSexe.get()!='' and self.varDate_naissance.get()!='' and self.varPays_naissance.get()!='' and self.varBureau.get()!='' and self.varHistorique_carriere.get()!='' and self.varTauxAppartenance.get()!='' and self.varAxe_recherche.get() != '':
                    self.Dict_axe_taux[self.varAxe_recherche.get()] = self.varTauxAppartenance.get()
                    internePOO = Internes(self.varNom.get(), self.varPrenom.get(), self.varSexe.get(), self.varDate_naissance.get(), self.varPays_naissance.get(), self.varBureau.get(), [Poste(self.varHistorique_carriere.get(), self.varPoste_debut.get(), self.varPoste_fin.get(), 'LCFC - EA4495')], self.Dict_axe_taux)
                    self.Dict_Internes[internePOO]=internePOO
                    self.liste_Personnel.insert('end', internePOO)
                    self.tv1.insert('internes','end',text='',values=(internePOO.nom, internePOO.prenom, internePOO.sexe, internePOO.pays_de_naissance, internePOO.historique_carriere, internePOO.date_de_naissance, internePOO.bureau_occupe))
        if self.varType_personnel.get() == "Externes":
            if self.varNom.get()!='' and self.varPrenom.get()!='' and self.varSexe.get()!='' and self.varPays_naissance.get()!='' and self.varEtabl.get() != '' and self.varInvit_debut.get() != '' :
                externePOO = Externes(self.varNom.get(), self.varPrenom.get(), self.varSexe.get(), self.varDate_naissance.get(), self.varPays_naissance.get(), self.varEtabl.get(), [self.varInvit_debut.get(), self.varInvit_fin.get()])
                self.Dict_Internes[externePOO]=externePOO
                self.liste_Personnel.insert('end', externePOO)
                self.tv1.insert('externes','end',text='',values=(externePOO.nom, externePOO.prenom, externePOO.sexe, externePOO.pays_de_naissance, externePOO.historique_carriere, externePOO.etablissement, externePOO.invitations))
        
    #Génerer la liste des membres internes du laboratoire par statut (et l'afficher en fenetre pop) 

    def membres_par_statut(self):
        Statut={}
        for qqun in self.Dict_Internes.keys():
            for intituleposte in self.Dict_Internes[qqun].postes_actuels :
                if intituleposte not in Statut.keys() :
                    Statut[str(intituleposte)]=[] #str pour être sur de donner comme clé le nom du poste ensuite 
            for intituleposte in self.Dict_Internes[qqun].postes_actuels :
                Statut[intituleposte].append(qqun)
        
        return tk.messagebox.showinfo(title = "Membres par statut", message = Statut)
     
    #Génerer la liste des membres internes du laboratoire par statut et la renvoyer. Utile pour les autres méthodes 
    def membres_par_statut2(self):
        Statut={}
        for qqun in self.Dict_Internes.keys():
            for intituleposte in self.Dict_Internes[qqun].postes_actuels :
                if intituleposte not in Statut.keys() :
                    Statut[str(intituleposte)]=[] #str pour être sur de donner comme clé le nom du poste ensuite 
            for intituleposte in self.Dict_Internes[qqun].postes_actuels :
                Statut[intituleposte].append(qqun)
        
        return Statut 

       
        
    #et générer la pyramide des âges (par pas de 5 ans). (Elle est plot dans spyder)
    #Nous conseillons de plot la figure sur une fenêtre séparée (option de spyder)
    
    def pyramide_des_ages(self):
        """ fonction sans variable en entrée qui renvoie la pyramide des ages du personnel interne"""
        
        hommes=np.zeros(21)
        femmes=np.zeros(21)
        
        for qqun in self.Dict_Internes.keys():
            sonage=(dt.date.today()-(self.Dict_Internes[qqun].date_de_naissance)).days//365
            
            for age in range (0,100,5):
                if self.Dict_Internes[qqun].sexe == 'M':
                    if sonage >= age and sonage < age+5 :
                        hommes[age//5]=hommes[age//5]+1
                if self.Dict_Internes[qqun].sexe == 'F':
                    if sonage >= age and sonage < age+5 :
                        femmes[age//5]=femmes[age//5]-1
        objects = ('0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85-89','90-94','95-100','100+')
        y_pos = np.arange(len(objects))
        
        fig, ax = plt.subplots(figsize=(8,8))
        ax.set_xlim([-max(hommes)-1, max(hommes)+1])
        plt.barh(y_pos, hommes, align='center')
        plt.yticks(y_pos, objects)
        plt.barh(y_pos, femmes, align='center')
        
        plt.xlabel('Personnel')
        plt.title('Pyramide des ages')
        plt.legend(('Hommes', 'Femmes'))
        
        plt.show()

    
    #Générer la bibliographie (l’ensemble des publications), sur une période donnée :
    #Pour la présentation d’une référence bibliographique, vous pouvez vous inspirer des conseils proposés par l’université de lorraine : Guide biblio ISO690 2020-2021.pdf (univ-lorraine.fr))
        
        #D’un personnel du laboratoire
   
    def publication_auteur(self):
        """Auteur au format str(SIADAT) renvoie les publications publiées entre les dates 1 et 2 (au format AAAA/MM/JJ)"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
            bibliographie=[]
            auteur=self.varAuteur_publications.get()
            for chaque_publication in self.Dict_Publication.keys():
                date_publi=self.Dict_Publication[chaque_publication].date
                if date_publi >= Date1 and date_publi<= Date2:
                    #ok
                    for nom_chaque_auteur in self.Dict_Publication[chaque_publication].auteurs:
                        if str(nom_chaque_auteur) == str(auteur):
                            bibliographie.append(self.Dict_Publication[chaque_publication])
            
            return tk.messagebox.showinfo(title = "Bibliographie sur la période {}:{}".format(self.varDate1.get(),self.varDate2.get()), message = bibliographie)
            
        
        #D’un axe de recherche du laboratoire
    def publication_axe(self):
        """renvoie les publications publiées entre les dates 1 et 2 (au format AAAA/MM/JJ). Si un auteur fait partie de l'axe la publication est ajoutée"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
            axe = self.varAxe_publications.get()
            bibliographie=[]
            
            for chaque_publication in self.Dict_Publication.keys():
                date_publi=self.Dict_Publication[chaque_publication].date
                if date_publi >= Date1 and date_publi<= Date2:
                    
                    for nom_chaque_auteur in self.Dict_Publication[chaque_publication].auteurs:
                        if self.Dict_Membres[nom_chaque_auteur] in self.Dict_Axes[axe].personnel:
                            if self.Dict_Publication[chaque_publication] not in bibliographie:
                                bibliographie.append(self.Dict_Publication[chaque_publication])
            return tk.messagebox.showinfo(title = "Bibliographie sur la période {}:{} de l'axe {}".format(self.varDate1.get(),self.varDate2.get(),axe), message = bibliographie)
            
        
        
        #Du laboratoire complet
    def publication_laboratoire(self):
        """renvoie les publications publiées entre les dates 1 et 2 (au format AAAA/MM/JJ)"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
        
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
                
            bibliographie=[]
            
            for chaque_publication in self.Dict_Publication.keys():
                date_publi=self.Dict_Publication[chaque_publication].date
                if date_publi >= Date1 and date_publi<= Date2:
                    bibliographie.append(self.Dict_Publication[chaque_publication])
            return tk.messagebox.showinfo(title = "Bibliographie sur la période {}:{} du labo".format(self.varDate1.get(),self.varDate2.get()), message = bibliographie)
            
    
    
    
    #Calculer le nombre de publication moyen par doctorant sur une période demandée
    def publication_moyenne_doctorant(self):
        """ATTENTION : ne comptabilise que les doctorants actuels!!! Renvoie lamoyenne de publication par doctorant sur la periode entre les dates 1 et 2 (au format AAAA/MM/JJ)"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
                  
            Nombre_Doctorant=0
            self.Dict_membres_statut=self.membres_par_statut2()
            for doctorant in self.Dict_membres_statut['Doctorant']:
                Nombre_Doctorant+=1
                
            # les publications écrites par plusieurs doctorants sont comptées une seule fois 
            Nombre_Publications_Doctorants=0
            for pub in self.Dict_Publication.keys():
                ecrit_par_doctorant = False 
                for chaque_auteur in self.Dict_Publication[pub].auteurs:
                    date_publi=self.Dict_Publication[pub].date
                    if date_publi >= Date1 and date_publi<= Date2 and isinstance(self.Dict_Membres[chaque_auteur],Internes):
                        for sonposte in self.Dict_Internes[chaque_auteur].postes_actuels:
                            if sonposte == 'Doctorant':
                                ecrit_par_doctorant = True
                if ecrit_par_doctorant == True :
                    Nombre_Publications_Doctorants+=1
            
            return tk.messagebox.showinfo(title = "Nombre de publication moyen des doctorants sur la période {}:{}".format(self.varDate1.get(),self.varDate2.get()), message = Nombre_Publications_Doctorants/ Nombre_Doctorant)
            
    
    #De générer la liste des revues dans lesquelles le laboratoire publie, par ordre croissant d’article soumis.
    """les revues sont les journaux. Les seules publications concernées sont donc les articles de journaux"""
    def revues_utilisees(self):
        Liste_Revues=[]
        for nomrevue in self.Dict_Revues.keys():
            Liste_Revues.append(self.Dict_Revues[nomrevue])
    
        return tk.messagebox.showinfo(title = "Liste des revues dans lesquelles le labo publie", message = sorted(Liste_Revues, key=lambda revue: revue.nombre_publications_labo))
        
    
    #Le taux d’articles rédigés en collaboration avec des personnels externes
    
    def taux_articles_externes(self):
        Nombre_Articles= len(self.Dict_Publication.keys())
        Nombre_Publi_exterieures = 0
        for pub in self.Dict_Publication.keys():
            ecrit_avec_auteur_exterieur = False 
            
            for chaque_auteur in self.Dict_Publication[pub].auteurs:
                if not chaque_auteur in self.Dict_Internes.keys():
                    ecrit_avec_auteur_exterieur= True
            if ecrit_avec_auteur_exterieur == True:
                Nombre_Publi_exterieures+=1
        
        return tk.messagebox.showinfo(title = "Taux d'articles réalisés en collaboration avec des externes",message = Nombre_Publi_exterieures/Nombre_Articles )
        
    #ainsi que le taux de thèse co-encadrées par des personnels externes.
    
    def taux_theses_externes(self):
        theses_encadrees=0
        for these in self.Dict_Projets_These.keys():
            Nombre_theses= len(self.Dict_Projets_These)
            encadre_par_personnel_externe = False 
            for chaque_auteur in self.Dict_Projets_These[these].encadrant.keys():
                if not chaque_auteur in self.Dict_Internes.keys():
                    encadre_par_personnel_externe= True
            if encadre_par_personnel_externe == True:
                theses_encadrees+=1
       
        return tk.messagebox.showinfo(title = "Taux de thèses réalisées en collaboration avec des externes",message = theses_encadrees/Nombre_theses )
        
    #Le taux moyen de publications rédigées par les doctorants au cours de leur projet de thèse.
    def taux_publication_doctorant(self):
        """Renvoie le taux moyen de publications rédigées par les doctorants au cours de leur projet de thèse."""
        nombre_publications=0
        Nombre_Doctorant=0
        
        self.Dict_membres_statut=self.membres_par_statut2()
        for doctorant in self.Dict_membres_statut['Doctorant']:
            Nombre_Doctorant+=1
            
            
        for these in self.Dict_Projets_These.keys(): #on parcourt toutes les thèses 
            date_debut_these= self.Dict_Projets_These[these].date_lancement
            date_fin_these = self.Dict_Projets_These[these].date_soutenance
            
            if date_fin_these == None: #si la thèse n'est pas terminée ou qu'elle n'a pas de date, on compte jusqu'à aujourd'hui
                date_fin_these= dt.date.today()
            
            for pub in self.Dict_Publication.keys():
                #on vérifie que la publication a été faite durant la thèse 
                if self.Dict_Publication[pub].date > date_debut_these and self.Dict_Publication[pub].date < date_fin_these :
                    for chaque_auteur in self.Dict_Publication[pub].auteurs:
                        if chaque_auteur in self.Dict_membres_statut['Doctorant']:
                            nombre_publications+=1
        
        return tk.messagebox.showinfo(title = "Taux moyen de publications rédigées par les doctorants au cours de leur thèse", message = nombre_publications/Nombre_Doctorant )
        
            
            
    #Durée moyenne des thèses soutenues dans une période donnée
    def duree_these(self):
        """retourne la durée en jours"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
                   
            Liste_duree=[]
            for these in self.Dict_Projets_These.keys():
                date_debut_these= self.Dict_Projets_These[these].date_lancement
                date_fin_these = self.Dict_Projets_These[these].date_soutenance
                if isinstance(date_fin_these, dt.date):
                    if  date_debut_these > Date1 and date_fin_these< Date2:
                        Liste_duree.append((date_fin_these-date_debut_these).days)
           
            return tk.messagebox.showinfo(title = "Durée moyenne des thèses sur la période {}:{}".format(self.varDate1.get(),self.varDate2.get()), message = np.mean(np.array(Liste_duree)))
            
            
    #Taux d’encadrement cumulé de thèse des personnels sur une période donnée
    
    def encadrement_cumule(self):
        """le taux d'encadrement cumulé est la somme des taux d'encadrement des thèses qu'encadre une personne sur la période donnée"""
        """ Par exemple : Une personne qui encadre 2 thèses, l'une à 40% et l'autre à 30% a un taux d'encadrement cumulé de 70%"""
        """les personnels externes sont comptailisés"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
              
            self.Dict_Encadrement_Cumule={}
            
            for chaque_personne in self.Dict_Membres.keys(): #création du dictionnaire avec tous les membres 
                self.Dict_Encadrement_Cumule[chaque_personne]=0.0
            
            for these in self.Dict_Projets_These.keys():
                date_debut_these= self.Dict_Projets_These[these].date_lancement
                date_fin_these = self.Dict_Projets_These[these].date_soutenance
                
                if ( date_debut_these > Date1 and date_debut_these < Date2) or (date_fin_these< Date2 and date_fin_these > Date1) : #si la période de la thèse chavauche l'intervalle donné, elle est comptabilisée  
                    for chaque_encadrant in self.Dict_Projets_These[these].encadrant.keys():
                        self.Dict_Encadrement_Cumule[chaque_encadrant]+=float(self.Dict_Projets_These[these].encadrant[chaque_encadrant])
                    for ledirecteur in self.Dict_Projets_These[these].directeur:
                        self.Dict_Encadrement_Cumule[ledirecteur]+=float(self.Dict_Projets_These[these].directeur[ledirecteur])
            
            return tk.messagebox.showinfo(title = "Taux d'encadrement cumulé sur la période {}:{}".format(self.varDate1.get(),self.varDate2.get()), message = self.Dict_Encadrement_Cumule)
            
    
    #Le montant des projets conclus au cours d’une période donnée par axe de recherche
    """seuls les projets de recherche sont assujetis à un budget"""
    def montant_des_projets(self): 
        """renvoie le montant total des projets par axe de recherche entre les dates 1 et 2 (au format AAAA/MM/JJ)"""
        if len(self.varDate1.get()) == 10 and len(self.varDate2.get())==10:
            Date1 = dt.date(int(self.varDate1.get()[:4]), int(self.varDate1.get()[5:7]), int(self.varDate1.get()[8:10]))
            Date2 = dt.date(int(self.varDate2.get()[:4]), int(self.varDate2.get()[5:7]), int(self.varDate2.get()[8:10]))
              
            self.Dict_Budgets_Axes={}
            for axe in self.Dict_Axes.keys():
                
                self.Dict_Budgets_Axes[axe]=0
                        
            for chaque_projet in self.Dict_Projets_Recherche.keys():
                Liste_Axe_Projet=[]
                date_fin_recherche = self.Dict_Projets_Recherche[chaque_projet].date_cloture
                if isinstance(date_fin_recherche, dt.date):
                    if date_fin_recherche > Date1 and date_fin_recherche < Date2:
                        for chaque_personne in self.Dict_Projets_Recherche[chaque_projet].personnes_impliquees:
                            if chaque_personne in self.Dict_Internes.keys(): #evite les erreurs 
                                for chacun_de_ses_axes in self.Dict_Internes[chaque_personne].taux_appartenance.keys():
                                     if not chacun_de_ses_axes in Liste_Axe_Projet:
                                         Liste_Axe_Projet.append(chacun_de_ses_axes)
                        for unaxe in Liste_Axe_Projet:
                            self.Dict_Budgets_Axes[unaxe]+= self.Dict_Projets_Recherche[chaque_projet].budget
                            
            return tk.messagebox.showinfo(title = "Montant des projets par axe sur la période {}:{}".format(self.varDate1.get(),self.varDate2.get()), message = self.Dict_Budgets_Axes)
            
    
    #La liste des partenaires (industriels ou académiques) ordonné par montant de projet réalisés ensemble
    def partenaires_projets(self):
        """On considère qu'un établissement est un partenaire quand il a un projet commun avec le labo. La liste est triée par ordre croissants"""
        
        Liste_Partenaires=[]
        for nompartenaire in self.Dict_Etablissement.keys():
            if self.Dict_Etablissement[nompartenaire].nombre_projets_communs > 0: #trier les partenaires dans les établissements 
                Liste_Partenaires.append(self.Dict_Etablissement[nompartenaire])
        
        return tk.messagebox.showinfo(title = "La liste des partenaires (industriels ou académiques) ordonné par montant de projet réalisés ensemble", message = sorted(Liste_Partenaires, key=lambda partenaire: partenaire.budget_projets_communs))
        
    
    
    #Liste et nombre de projets qui ont été réalisés par la collaboration des membres de plusieurs axes du laboratoire.
    def projets_multi_axes(self):
        """donne la liste des projets et le nombre de projets réalisés en colaboration avec des membres de plusieurs axes"""
        bibliographie_projets=[]
        Nombre_Projets_Colab=0
    
        for chaque_projet in self.Dict_Projets.keys():
            Liste_Axes_Projet=[]
            if isinstance(self.Dict_Projets[chaque_projet],Projet_recherche): #si c'est un projet de recherche on a direct la liste des encadrants 
                    
                for chaque_personne in self.Dict_Projets[chaque_projet].personnes_impliquees:
                    if chaque_personne in self.Dict_Internes.keys(): #on vérifie que les personnes impliquées sont des internes pour avoir leur axe de recherche 
                        for chaque_axe in self.Dict_Axes.keys():
                            if self.Dict_Internes[chaque_personne] in self.Dict_Axes[chaque_axe].personnel: #on vérifie l'appartenance des internes à chacun des axes 
                                
                                if not self.Dict_Axes[chaque_axe] in Liste_Axes_Projet : #on ajoute qu'une seule fois un axe à la liste des axes 
                                    Liste_Axes_Projet.append(self.Dict_Axes[chaque_axe])
            
            if isinstance(self.Dict_Projets[chaque_projet], Projet_these): 
               
                Liste_Gens_Impliques=[] #on crée une liste avec tout le monde pour éviter d'écrire pleins de cas 
                Liste_Gens_Impliques+= self.Dict_Projets_These[chaque_projet].directeur #ajout du directeur de thèse
                Liste_Gens_Impliques+= self.Dict_Projets_These[chaque_projet].encadrant #ajout des encadrants de thèse
                
                for chaque_personne in Liste_Gens_Impliques:
                   
                    if chaque_personne in self.Dict_Internes.keys(): #on vérifie que les personnes impliquées sont des internes pour avoir leur axe de recherche 
                            
                        for chaque_axe in self.Dict_Axes.keys():
                            if self.Dict_Internes[chaque_personne] in self.Dict_Axes[chaque_axe].personnel: #on vérifie l'appartenance des internes à chacun des axes 
                                
                                if not self.Dict_Axes[chaque_axe] in Liste_Axes_Projet : #on ajoute qu'une seule fois un axe à la liste des axes 
                                    Liste_Axes_Projet.append(self.Dict_Axes[chaque_axe])             
                                   
            if len(Liste_Axes_Projet)> 1:
                Nombre_Projets_Colab+=1
                bibliographie_projets.append(self.Dict_Projets[chaque_projet])
        
        return tk.messagebox.showinfo(title = "Liste et nombre de projets qui ont été réalisés par la collaboration des membres de plusieurs axes du laboratoire", message = "Projets : {}, Nombre : {}".format( bibliographie_projets, Nombre_Projets_Colab))
            
    
    #Liste et nombre de publications qui ont été réalisées par la collaboration des membres de plusieurs axes du laboratoire.
    def publications_multi_axes(self):
        bibliographie=[]
        Nombre_Publications_Colab=0
        
        for chaque_publication in self.Dict_Publication.keys():
            
            Liste_Axes_Publication=[]
            
            for chaque_personne in self.Dict_Publication[chaque_publication].auteurs:
                
                if chaque_personne in self.Dict_Internes.keys(): #on vérifie que les personnes impliquées sont des internes pour avoir leur axe de recherche 
                    for chaque_axe in self.Dict_Axes.keys():
                        if self.Dict_Internes[chaque_personne] in self.Dict_Axes[chaque_axe].personnel: #on vérifie l'appartenance des internes à chacun des axes 
                            if not self.Dict_Axes[chaque_axe] in Liste_Axes_Publication : #on ajoute qu'une seule fois un axe à la liste des axes 
                                Liste_Axes_Publication.append(self.Dict_Axes[chaque_axe])
    
            if len(Liste_Axes_Publication)> 1:
                Nombre_Publications_Colab+=1
                bibliographie.append(self.Dict_Publication[chaque_publication])
       
        return tk.messagebox.showinfo(title = "Liste et nombre de publication qui ont été réalisés par la collaboration des membres de plusieurs axes du laboratoire", message = "Publication : {}, Nombre : {}".format( bibliographie, Nombre_Publications_Colab))
              
        
    """__________________enregistrement du xml__________________"""
        
    def enregistrerXML(self):
        #Enregistrement des données dans un nouveau fichier xml 
        Tronc = ET.Element('Laboratory', {'Name': 'LCFC - EA4495'})
        
        #Enregistrement de Organization 
        OrgaXML=ET.Element('Organization',{'Laboratory_Head_Name' : 'SIADAT'})
        ET.SubElement(OrgaXML, 'University', {'Name': "Université Nationale Supérieure d'Arts et Métiers"})
        ET.SubElement(OrgaXML, 'University', {'Name': "Université de Lorraine"})
        #Erreur de cett implémentation dans le xml, par conséquent, nous avons dû changer la rédaction de cet enregistrement 
        # for orgaPOO in list(self.Dict_Organisation.values()):
            # ET.SubElement(OrgaXML, 'University',{'Name': orgaPOO.universite})
        # #     print(self.Dict_Axes.values())
        # for axe in list(self.Dict_Axes.values()):
        # #         print(axe)
        #     ET.SubElement(OrgaXML, 'Research Team', {'Name' : axe.nom_axe, 'Head' : str(axe.responsable)})
        Tronc.append(OrgaXML)
    
        
        # Enregistrement Internes
        InterneXML=ET.Element('Members')
        for internPOO in list(self.Dict_Internes.values()):
            
            InterXML=ET.SubElement(InterneXML,'Member',{'Name': internPOO.nom, 'Office': internPOO.bureau_occupe ,'Country': internPOO.pays_de_naissance , 'BD': str(internPOO.date_de_naissance), 'Gender': internPOO.sexe, 'FirstName': internPOO.prenom})
        
            for chaqueposte in internPOO.historique_carriere:
               
                ET.SubElement(InterXML, 'Position', {'Name' : str(chaqueposte.intitule), 'Start': str(chaqueposte.date_debut), 'End':str(chaqueposte.date_fin) })
               
            for chaque_taux in internPOO.taux_appartenance:
                ET.SubElement(InterXML, 'Research_Team', {'Name' : chaque_taux , 'Rate': internPOO.taux_appartenance[chaque_taux] })
           
            
            
            
        # Enregistrement Externes 
        for externPOO in list(self.Dict_Externes.values()):
            exterXML=ET.SubElement(InterneXML,'External_Member',{'Name': externPOO.nom ,'Country': externPOO.pays_de_naissance, 'Gender': externPOO.sexe, 'FirstName': externPOO.prenom, 'Company' : externPOO.etablissement_actuel})
        
            for invit in externPOO.invitations:
                    ET.SubElement(exterXML, 'Stay', {'Start' : invit[0], 'End' : invit[1]})
               
           
        Tronc.append(InterneXML)
        
        #Enregistrement projets
        """ATTENTION : Problème de sérialisation non résolu pour l'enregistrement des projets. principalement pour l'enregistrement des projets de recherche """
        
        """
        projetXML = ET.Element('Projects')
        self.Dict_Projets = {**self.Dict_Projets_Recherche, **self.Dict_Projets_These}
        for project in list(self.Dict_Projets_These.values()):
            proj_theseXML = ET.SubElement(projetXML, 'PhD', {'Name': project.titre, 'Start': str(project.date_lancement), 'Place': project.etablissement, 'Defense Date': str(project.date_soutenance), 'Candidate' : str(project.doctorant)})
            for direct in project.directeur.keys():
                
                ET.SubElement(proj_theseXML, 'PhD_Director', {'Name':direct, 'Rate': project.directeur[direct]})
            for encadr in project.encadrant.keys():
                
                ET.SubElement(proj_theseXML, 'Supervisor', {'Name':encadr, 'Rate': project.encadrant[encadr]})
            Jury = ET.SubElement(proj_theseXML, 'Jury_Members')
            for jur in project.jury_soutenance.keys():
                
                ET.SubElement(Jury, 'Member', {'Name':encadr, 'Rate': project.jury_soutenance[jur]})
                ET.SubElement(proj_theseXML, 'Production', {'Ref':project.reference})
                
        for project in list(self.Dict_Projets_Recherche.values()):
            proj_rechercheXML = ET.SubElement(projetXML, 'Project', {'Name': project.titre, 'Head': project.pilote_projet_recherche , 'Short': project.acronyme, 'Expected End': project.date_previsionnelle})
            for membre in project.personnes_impliquees:
                print(membre)
                ET.SubElement(proj_rechercheXML, 'Member', {'Name': membre})
            for societe in project.etablissement_realisation.keys():
                ET.SubElement(proj_rechercheXML, 'Company_Involved', {'Name': societe, 'Funding' : project.etablissement_realisation[societe]})
            ET.SubElement(proj_rechercheXML, 'Production', {'Ref':'Rapport expérimentation chaire Industrielle'})
        Tronc.append(projetXML)
        """
        
            
        # Enregistrement dans un arbre XML et enregistrement du fichier associé
        Nouvelarbre = ET.ElementTree(Tronc)
        
        cheminenregistrement = TKFD.asksaveasfilename(title = "Enregistrer les étudiants en XMl..." , defaultextension = ".xml", filetypes = [("XML","*.xml")])
        if cheminenregistrement != "":
            Nouvelarbre.write(cheminenregistrement)
            print("Ecriture du fichier XML réalisée au chemin précisé : {}".format(cheminenregistrement))
            
        del(Nouvelarbre)
        
    """ATTENTION : Cette partie n'est pas implémentée dans l'interface. Cependant les chemins d'accès sont les bons
    Nous avons eu beaucoup de difficulté à enregistrer le xml car la fonction ouvrir fichier de l'interface ne permet pas de faire du tronc une variable globale
    Nous avons donc totalement changé notre méthode d'enregistrement en cours de route"""
    
    def enregistrerExterne(self, lenom, leprenom, lesexe,ledate_de_naissance, lepays_de_naissance, leposte_actuel, leetablissement_actuel, leinvitations):
        """ lenom : str / leprenom : str / lesexe : M ou F / ledate_de_naissance : str(2008/09/01) / lepays_de_naissance : str / leposte_actuel : / leetablissement_actuel : / leinvitations : """
        NewMember = ET.Element('External_Member',{'Name': lenom, 'Country': lepays_de_naissance, 'gender':lesexe, 'FirstName':leprenom , 'Company':leetablissement_actuel, 'Job' : leposte_actuel })
         
        #leinvitations
        for chaque_invitation in leinvitations:
            ET.SubElement(NewMember,'Stay',{'Start':chaque_invitation[0], 'End' : chaque_invitation [1]})
         
        tronc[1].append(NewMember)
        
    def enregistrerProjet_recherhce(self,letitre, leetablissement_realisation, leacronyme, Dict_investisseur, lepersonnes_impliquees, lepilote_projet_recherche, lefin_projet):
        
        NewProject = ET.Element('Project',{'Name': letitre, 'Head':lepilote_projet_recherche, 'Short': leacronyme, 'Expected_End' : lefin_projet})
         
        #personnes impliquées 
        for chaque_participant in lepersonnes_impliquees:
            ET.SubElement(NewProject,'Member',{'Name':chaque_participant }) 
        
        #entreprises et budgets
        for chaque_entreprise in Dict_investisseur:
             ET.SubElement(NewProject, 'Company_Involved',{ 'Name': chaque_entreprise, 'Funding': Dict_investisseur[chaque_entreprise]})
    
        tronc[2].append(NewProject)
    
    def enregistrerProjet_these(self,letitre, leetablissement_realisation,ledate_lancement, lejury_soutenance,ledoctorant,ledirecteur,leencadrant, ledate_fin_these,DOI):
        
        NewProject = ET.Element('PhD',{'Name': letitre, 'Start':ledate_lancement, 'Place':leetablissement_realisation, 'Defense_Date':ledate_fin_these, 'Candidate':ledoctorant})
         
        #directeur 
        for chaque_directeur in ledirecteur:
            ET.SubElement(NewProject,'Supervisor',{'Name':chaque_directeur, 'Rate': ledirecteur[chaque_directeur]}) 
        
        #Superviseur
        for chaque_encadrant in leencadrant:
             ET.SubElement(NewProject, 'Supervisor',{ 'Name': chaque_encadrant, 'Rate': leencadrant[chaque_encadrant]})
        
        #Membres du jury 
        Jury_Members=ET.Element('Jury_Members',{})
        for chaque_jury in lejury_soutenance:
             ET.SubElement(Jury_Members, 'Member',{ 'Name': chaque_jury, 'Role': lejury_soutenance[chaque_jury]})
        NewProject.append(Jury_Members)
        
        #reference
        ET.SubElement(NewProject, 'Production',{ 'Ref': DOI})
    
        tronc[2].append(NewProject)   
        
    
    def enregistrerArticle_journal(self,ledate, leauteurs, letitre, lelien, lenom_revue):
        
        NewPaper = ET.Element('Journal_paper',{'DOI':lelien, 'Available':ledate, 'Journal':lenom_revue, 'Title':letitre})
         
        #Auteurs
        for chaque_auteur in leauteurs:
             ET.SubElement(NewPaper, 'Author',{ 'Name': chaque_auteur})
        
        tronc[3].append(NewPaper)   
        
    
    def enregistrerArticle_conference(self,ledate, leauteurs, letitre, lelien, lenom_conference, ledate_conference, lelieu_conference):
        
        NewPaper = ET.Element('Conference',{'Place': lelieu_conference,'DOI':lelien, 'Available':ledate,'Dates':ledate_conference,'Conference_Name':lenom_conference})
         
        #Auteurs
        for chaque_auteur in leauteurs:
             ET.SubElement(NewPaper, 'Author',{ 'Name': chaque_auteur})
        
        tronc[3].append(NewPaper)  
        
    def enregistrerRapport_technique(self,ledate, leauteurs, letitre, lelien):
        
        NewPaper = ET.Element('Report',{'Available':ledate, 'Title': letitre, 'DOI': lelien })
         
        #Auteurs
        for chaque_auteur in leauteurs:
             ET.SubElement(NewPaper, 'Author',{ 'Name': chaque_auteur})
        
        tronc[3].append(NewPaper)  
        
    
Interface()

"""Fonctions qui auraient servies plus tard dans le projet"""

# def corriger_date(unedate):
        #     if isinstance(unedate, dt.date):
        #         Annee= str(unedate.year)
                
        #         if len(str(unedate.month))<2:
        #             Mois='0'+str(unedate.month)
        #         else:
        #             Mois= str(unedate.month)
        #         if len(str(unedate.day)) <2:
        #             Jour = '0'+str(unedate.day)
        #         else:
        #             Jour = str(unedate.day)
        #         return(Annee+'/'+Mois+'/'+Jour)
        
        
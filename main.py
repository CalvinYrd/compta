##################################################
#################### IMPORTS #####################
##################################################

from time import time as time
from time import strftime as time_strftime
from time import mktime as time_mktime
from time import localtime as time_localtime

from os.path import exists as os_path_exists
from os import remove as os_remove
from os import system as os_system
from os import name as os_name
from os import listdir, mkdir

from re import match as re_match
from re import sub as re_sub

from datetime import datetime

from colorama import Fore, Back ############# REPLACE RGB

##################################################
################## PREPARATION ###################
##################################################

if (os_name == "nt"): clearCmd = "cls"
else: clearCmd = "clear"
sep = ":"
curCtx = None

##################################################
################### FONCTIONS ####################
##################################################

def rm_if_exists(p):
	if (os_path_exists(p)): os_remove(p)

def isNumber(string):
    pattern = r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$'
    return bool(re_match(pattern, string))

def folderNameIsValid(folder):
    pattern = r'^[a-zA-Z0-9-_]+$'
    return bool(re_match(pattern, folder))

# créé un fichier si il n'existe pas
def createFileIfNotExist(name, base = None):
	if (not os_path_exists(name)):
		with open(name, "w", encoding = "utf8") as f:
			if (base): f.write(base)

# fonction pour lire un fichier
def readFile(path, createObject = False, startIndex = 0):
	with open(path, "r", encoding = "utf-8") as f:
		lines = f.read().split("\n")[startIndex:]

	res = []
	for i in range(len(lines)):
		if (lines[i].strip() and not lines[i].startswith("#")):
			res.append(lines[i].split(sep))

	if (createObject):
		obj = {}
		for dat in res:
			if (dat[1].isdigit()): dat[1] = int(dat[1])
			obj[dat[0]] = dat[1]
		res = obj

	return res

# efface l'écran en ré-affichant un contenu si nécessaire
def clear(txt = None):
	global clearCmd
	os_system(clearCmd)
	if (txt != None): print(txt)

# supprime une chaine de caractères dans une autre
strRemove = lambda toRm, text: text.replace(toRm, "")

# colorise un texte formaté
def colorize(text):
	global config

	color_codes = {
		"@@RED": Back.RED,
		"@@GRN": Back.GREEN,
		"@@BLU": Back.BLUE,
		"@@BLK": Back.BLACK,
		"@@WHT": Back.WHITE,
		"@@CYN": Back.CYAN,
		"@@MGT": Back.MAGENTA,
		"@@YLW": Back.YELLOW,
		"@@LRED": Back.LIGHTRED_EX,
		"@@LGRN": Back.LIGHTGREEN_EX,
		"@@LBLU": Back.LIGHTBLUE_EX,
		"@@LBLK": Back.LIGHTBLACK_EX,
		"@@LWHT": Back.LIGHTWHITE_EX,
		"@@LCYN": Back.LIGHTCYAN_EX,
		"@@LMGT": Back.LIGHTMAGENTA_EX,
		"@@LYLW": Back.LIGHTYELLOW_EX,
		"@@RST": Back.RESET,
		"@RED": Fore.RED,
		"@GRN": Fore.GREEN,
		"@BLU": Fore.BLUE,
		"@BLK": Fore.BLACK,
		"@WHT": Fore.WHITE,
		"@CYN": Fore.CYAN,
		"@MGT": Fore.MAGENTA,
		"@YLW": Fore.YELLOW,
		"@LRED": Fore.LIGHTRED_EX,
		"@LGRN": Fore.LIGHTGREEN_EX,
		"@LBLU": Fore.LIGHTBLUE_EX,
		"@LBLK": Fore.LIGHTBLACK_EX,
		"@LWHT": Fore.LIGHTWHITE_EX,
		"@LCYN": Fore.LIGHTCYAN_EX,
		"@LMGT": Fore.LIGHTMAGENTA_EX,
		"@LYLW": Fore.LIGHTYELLOW_EX,
		"@RST": Fore.RESET
	}
	bg = config["background_color"]
	color_codes["@@RST"] = color_codes["@@"+bg]

	for code, color in color_codes.items():
		text = text.replace(code, color)

	return text

# supprime les formateur de texte de couleur
def cancelColor(text):
	for color in ("@@RED", "@@GRN", "@@BLU", "@@BLK", "@@WHT", "@@CYN", "@@MGT", "@@YLW", "@@LRED", "@@LGRN", "@@LBLU", "@@LBLK", "@@LWHT", "@@LCYN", "@@LMGT", "@@LYLW", "@@RST", "@RED", "@GRN", "@BLU", "@BLK", "@WHT", "@CYN", "@MGT", "@YLW", "@LRED", "@LGRN", "@LBLU", "@LBLK", "@LWHT", "@LCYN", "@LMGT", "@LYLW", "@RST"):
		text = strRemove(color, text)

	return text

rmMultipleSpaces = lambda data: re_sub(r"\s+", " ", data)
days = (
	("monday", "lundi"),
	("tuesday", "mardi"),
	("wednesday", "mercredi"),
	("thursday", "jeudi"),
	("friday", "vendredi"),
	("saturday", "samedi"),
	("sunday", "dimanche")
)
months = (
	("september", "septembre"),
	("october", "octobre"),
	("november", "novembre"),
	("december", "décembre"),
	("january", "janvier"),
	("february", "février"),
	("march", "mars"),
	("april", "avril"),
	("may", "mai"),
	("juily", "juillet"),
	("august", "août")
)

# récupère la chaine de caractères d'une date avec un timestamp fourni
def getDate(timestamp):
	global config
	# gestion du timestamp
	timestamp = float(timestamp)
	timestamp = time_localtime(timestamp)

	# gestion du jour
	day = time_strftime("%e", timestamp)
	day = day.strip()
	day = ["1er" if day == "1" else day][0]

	# le reste
	date = time_strftime("Le %A "+day+" %B %Y à %R:%S", timestamp)
	# enlever doublons espaces
	date = rmMultipleSpaces(date).lower()

	# traduction en français
	for var in ("days", "months"):
		for string in globals()[var]:
			date = date.replace(string[0], string[1].capitalize())

	return date

# récupère ma chaine de caractères d'une somme avec son symbole
def getSum(symbol = None, sumn = None, isSold = False):
	global config
	# si la somme est définie
	if (None not in (symbol, sumn)):
		# arrondir à 3 chiffres après la virgule
		if (type(sumn) == float or (type(sumn) == str and "." in sumn)):
			sumn = round(float(sumn), 3)

		sumn = str(sumn)
		# cas du symbole "-" à retirer
		if (sumn.startswith("-")): sumn = sumn.lstrip("-")

		# couleur selon le symbole de la somme (+ ou -)
		color = [config["positive_color"] if symbol == "+" else config["negative_color"]][0]

		# récupération du nombre de décimales dans la somme
		decimals = str(sumn)
		decimals = decimals.split(".")
		decimals = decimals[0]
		decimals = int(decimals)

		# type d'endroit de la couleur selon la somme
		if (symbol == "+"):
			if (isSold): n = config["min_glowing_positive_sold"]
			else: n = config["min_glowing_positive_sumn"]
			colorType = ["@@" if decimals >= n else "@"][0]

		else:
			colorType = ["@@" if decimals >= config["min_glowing_negative_sumn"] else "@"][0]

		# formatage du prix
		price = symbol+sumn+" €"
		price = price.replace(".", ",")

		# cas de la somme surlignée en vert
		if (colorType == "@@" and symbol == "+"):
			price = "@BLK"+price+"@RST" # écrit en blanc

		# formatage de la somme
		res = colorType+color+price+colorType+"RST"

	# si un des paramètres n'est pas défini
	else: res = getUnnamed()
	return res

# retourne un message du style "Inconnu" si la valeur donnée est nulle
getUnnamed = lambda data = None, lib = "Inconnu": ["@LBLK"+lib+"@RST" if (data in (None, False)) or (type(data) == str and not data.strip().strip("\n")) else data][0]

# retourne une liste des données de comptabilité
def getData(sep = sep, sumn = 0):
	global curCtx
	data = readFile("ctx/"+curCtx+"/data")
	spent = 0

	for i in range(len(data)):
		# cas de la somme finale
		# ajout à la liste
		operator = data[i][0]
		money = float(data[i][1].replace(",", "."))

		if (operator == "+"): sumn += money
		else: sumn -= money

		symbol = ["-" if sumn < 0 else "+"][0]
		data[i].append(getSum(symbol, sumn, True))

		if (operator == "-"): spent += money
		data[i].append(str(round(spent, 3)))

		# sécurité anti doublons espaces
		for index in range(len(data[i])):
			data[i][index] = rmMultipleSpaces(data[i][index])

	return data

# retourne une liste des données de comptabilité séparé par mois
def getSplitedData():
	global config
	res = []
	lastXName = None
	spliter = config["table_split_mode"]
	data = getData()
	reduc = 0

	if (spliter == "day"): spliter = "A"
	if (spliter == "month"): spliter = "B"
	if (spliter == "hour"): spliter = "H"

	for i in range(len(data)):
		X = float(data[i][4])
		X = time_strftime("%"+spliter, time_localtime(X))

		# si le mois diffère : nouvelle liste
		if (X != lastXName):
			res.append([])
			lastXName = X

			# adaptation dépenses mensuelle
			if (len(res) > 1): reduc += float(res[-2][-1][6])

		data[i][6] = float(data[i][6]) - reduc
		data[i][6] = round(data[i][6], 2)
		data[i][6] = str(data[i][6])

		res[-1].append(data[i])
	return res

# retourne la liste des données de comptabilité formaté visuellement
def getDataText():
	res = []
	for data in getSplitedData():
		for i in range(len(data)):
			dat = data[i]
			# symbole de la somme (+ ou -)
			dat[1] = getSum(dat[0], dat[1])
			# suppression du symbole de la somme (+ ou -)
			del dat[0]

			# libelle + organisation
			dat[1] = getUnnamed(dat[1])
			dat[2] = getUnnamed(dat[2])
			# date
			dat[3] = getDate(dat[3])
			dat[5] = "@YLW"+dat[5]+" €@RST"

		res.append(data)
	return res

# créé la ligne d'une rangée d'un tableau
def drawRowLine(src, widths, borderColor, dir = "up", line = ""):
	if (dir == "down"): a, b, c = "╔", "╦", "╗"
	elif (dir == "mid"): a, b, c = "╠", "╬", "╣"
	else: a, b, c = "╚", "╩", "╝"

	for i in range(len(src)):
		if (i == 0): sep = a
		else: sep = b
		line += sep+"═"*(len(src[i])+2)

	line += c
	line = colorize("@"+borderColor+line+"@RST")
	return line

# transforme une couleur écrit en français en code couleur utilisable dans colorize()
def getCol(col):
	col = col.strip().lower()

	if (col == "rouge"): res = "RED"
	elif (col == "vert"): res = "GRN"
	elif (col == "bleu"): res = "BLU"
	elif (col == "noir"): res = "BLK"
	elif (col == "blanc"): res = "WHT"
	elif (col == "cyan" or col == "aqua" or col == "bleu clair" or col == "bleu ciel"): res = "CYN"
	elif (col == "magenta" or col == "violet" or col == "rose"): res = "MGT"
	elif (col == "jaune" or col == "orange"): res = "YLW"
	else: res = "RST"

	return res

# créé le contenu d'un tableau
def drawRowContent(data, widths = None, colors = None, color = None, sep = " "):
	# cas des valeurs des colonnes avec espaces nécessaires
	if (widths):
		for i in range(len(data)):
			w = int(widths[i])
			w -= len(cancelColor(data[i]))
			w *= sep
			data[i] += w

	for col in colors:
		c = data[1].strip().lower()

		if (not ".." in c and col[0] in c):
			data[1] = str("@@"+getCol(col[1])+data[1]+"@@RST")

	# si il y a une couleur définie on l'applique sinon non
	glue = ["@RST ║ @"+color if color else " ║ "][0]
	line = glue.join(data).strip("\n")
	# si il y a une couleur définie on l'applique sinon non
	line = ["@RST║ @"+color+line+"@RST ║" if color else "║ "+line+" ║"][0]
	return line

def getWidths(data):
	# applatir la liste de listes en une liste de listes
	newData = []

	for lst in data:
		# si la liste contient une ou plusieurs listes
		if (type(lst[0]) in (list, tuple)):
			for l in lst:
				newData.append(l)
		else:
			newData.append(lst)

	data = newData
	widths = [0]*len(data[0])

	for lst in data:
		for i in range(len(lst)):
			x = cancelColor(lst[i])
			if (len(x) > widths[i]):
				widths[i] = len(x)

	return widths

# créé le tableau ascii
def drawTable(heading, dat, colors, color = "CYN", borderColor = "LBLK"):
	colsWidth = getWidths([heading]+dat)
	tables = ""

	for data in dat:
		# traitements visuels interne
		# EN-TÊTE
		table = drawRowContent(heading, colsWidth, colors, color, ".")

		table = "\n"+drawRowLine(heading, colsWidth, borderColor, "down")+"\n"+table
		table += "\n"+drawRowLine(heading, colsWidth, borderColor, "mid")

		# DEBUT DU CONTENU
		for line in data:
			table += "\n"+drawRowContent(line, colsWidth, colors)

		# FIN DU CONTENU
		table += "\n"+drawRowLine(heading, colsWidth, borderColor)

		# TRAITEMENTS FINAUX
		table = table.replace("║", "@"+borderColor+"║@RST")
		table = colorize(table)
		tables += table
	
	return tables

# input amélioré
def ask(msg, keepDisplay = None, regex = None, end = ":\n> "):
	while True:
		res = input(msg+end).strip()

		if (regex):
			if (re_match(regex, res)): break
			else:
				clear(keepDisplay)
				print(colorize("@REDLa valeur saisie est incorrecte, merci de reessayer:\n\n@RST"))

		else: break

	clear(keepDisplay)
	return res

##################################################
################### VARIABLES ####################
##################################################

heading = ["Somme", "Libelle", "Organisation", "Date et heure", "Solde", "Dépenses"]

##################################################
################# CODE PRINCIPAL #################
##################################################

if (not os_path_exists("ctx")): mkdir("ctx")
if (os_path_exists("last_context")):
	# on essaye de récupérer le dernier contexte utilisé s'il y en a un
	with open("last_context", "r", encoding = "utf-8") as f:
		curCtx = f.read().strip()
		displayMainMenu = False
else:
	displayMainMenu = True

# choix du contexte
while True:
	if (displayMainMenu):
		# affichage, création et sélection du contexte
		clear()
		rm_if_exists("last_context")
		ctx = listdir("ctx")
		curCtx = None

		if (len(ctx) > 0):
			msg = "Saisissez un nombre pour choisir un contexte :\n\n"

			for i in range(len(ctx)):
				msg += str(i+1)+": "+ctx[i]+".\n"
		else:
			msg = "Aucun contexte disponible.\n"
		
		msg += "\nFaites q pour quitter l'app\nFaites + pour créer un contexte.\n> "
		response = input(msg)

		if (response == "+"):
			while True:
				clear()
				newCtxName = input("Saisissez le nom du nouveau contexte :\n> ")
				p = "ctx/"+newCtxName

				if (folderNameIsValid(newCtxName) and not os_path_exists(p)):
					mkdir(p)
					curCtx = newCtxName
					break

		elif (isNumber(response) and int(response)-1 in range(len(ctx))):
			curCtx = ctx[int(response)-1]
		elif (response == "q"):
			break
		else:
			continue

	else: displayMainMenu = True

	# création des fichiers
	createFileIfNotExist("ctx/"+curCtx+"/config", """# valeur minimale pour que le solde soit en surbrillance lorsqu'il est positif
# par défaut : 1000

min_glowing_positive_sold:1000

# valeur minimale pour que la somme soit en surbrillance lorsqu'elle est positive
# par défaut : 100

min_glowing_positive_sumn:100

# valeur minimale pour que la somme soit en surbrillance lorsqu'elle est négative
# par défaut : 30

min_glowing_negative_sumn:30

# mode de séparation du tableau en d'autres tableaux, voici les valeurs possibles :
# hour (toutes les heures)
# day (quotidien)
# month (mensuel)
# par défaut : day

table_split_mode:day

# les couleurs utilisables sont les suivantes :
# RED (rouge), GRN (vert), BLU (bleu), BLK (noir), WHT (blanc), CYN (cyan),
# MGT (magenta), YLW (jaune), LRED (rouge clair), LGRN (vert clair),
# LBLU (bleu clair) , LBLK (gris fonçé), LWHT (gris clair), LCYN (cyan clair),
# LMGT (magenta clair), LYLW (jaune clair)

# couleur de fond
# par défaut : BLK

background_color:BLK

# couleur lorsqu'une valeur transactionnelle est positive
# par défaut : GRN

positive_color:GRN

# couleur lorsqu'une valeur transactionnelle est négative
# par défaut : RED

negative_color:RED\n""")

	createFileIfNotExist("ctx/"+curCtx+"/data")
	createFileIfNotExist("ctx/"+curCtx+"/colors", """# Accentue chaque occurrence d'un libelle spécifique.
# Syntaxe : <libelle>:<couleur>, ex : extra:violet\n""")
	config = readFile("ctx/"+curCtx+"/config", True) # récupération de la config
	colors = readFile("ctx/"+curCtx+"/colors") # récupération des couleurs

	# sauvegarder le dernier contexte ouvert
	with open("last_context", "w", encoding = "utf-8") as f:
		f.write(curCtx)

	# intéractions avec les transactions
	while True:
		clear()
		dataText = getDataText()
		table = drawTable(heading, dataText, colors)
		print(table)
		purchaseMode = ask("""Faites + pour ajouter une transaction
Faites - pour supprimer la dernière transaction
Faites q pour quitter le contexte""", table)

		if (purchaseMode == "+"):
			purchase = [None]*5
			purchase[0] = ask(
				"De quel type est la transaction ?\n+ : virement\n- : achat",
				table, r'^[+-]$'
			)
			purchase[1] = ask(
				"Saisissez la somme",
				table, r'^[+-]?\d+([.,]\d+)?$'
			)
			purchase[2] = ask("Saisissez le libelle", table)
			purchase[3] = ask("Saisissez l'organisation", table)

			while True:
				try:
					dateAndHour = ask(
						"Saisissez la date et l'heure sous le format JJ-MM-AAAA HH:MM:SS (ne rien écrire pour mettre la date actuelle)",
						table, r'^(?:\d{2}-\d{2}-\d{4}(?: \d{2}:\d{2}:\d{2})?|)$'
					)

					if (dateAndHour):
						if (not ":" in dateAndHour): dateAndHour += " 00:00:00"
						dateAndHour = datetime.strptime(dateAndHour, "%d-%m-%Y %H:%M:%S")
						dateAndHour = time_mktime(dateAndHour.timetuple())
						dateAndHour = str(dateAndHour)
						purchase[4] = dateAndHour

					else: purchase[4] = str(time())
					break

				except (OverflowError, ValueError):
					print(colorize("@REDLa date saisie est trop grande ou trop petite, merci de la modifier:\n\n@RST"))

			purchase = sep.join(purchase)+"\n"

			with open("ctx/"+curCtx+"/data", "a", encoding = "utf8") as file:
				file.write(purchase)

		elif (purchaseMode == "-" and dataText):
			confirm = (ask("Êtes-vous sur de vouloir supprimer la dernière transaction (oui, yes)").lower() in ("oui", "o", "yes", "y"))

			if (confirm):
				with open("ctx/"+curCtx+"/data", "r", encoding = "utf8") as file:
					lines = file.readlines()

				lines.pop()
				with open("ctx/"+curCtx+"/data", "w", encoding = "utf8") as file:
					file.writelines(lines)

		if (purchaseMode == "q"): break



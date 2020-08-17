Ja...

Was kanns? Wie benutzt ichs? usw. sollen hier beantwortet werden:

Starten:

 - Einfach vectorDisplayDatei doppelklicken/ausführen!
 - (Hierzu muss pygame vorhanden sein)

Bedienung:

Q = Verändert Zoomstufe zws. 1, 10 und 100 Einheiten Achsenlänge

W = Schaltet zws. 2D und 3D Modus um

A, Y = Vektorliste hoch und runter scrollen (A hoch, Y runter)

D = (Für Testzwecke) Neuen Vektor hinzufügen. Öffnet Eingabe für x-, y- und z-werte (nacheinander) in der Commandzeile 
	d. h. nicht in der grafischen Oberfläche, sondern im eigentlichen Python Fenster... (für 2D z=0 eingeben)

S = Speichert eine XML-Datei der angezeigten Vektoren unter "saves"; Titel ist Nummer: JJJJMMTTHHMM...


Was kanns:

1) Bunt aussehen
2) Schwer lesbarer Code
3) Alle oben beschriebenen Funktionen (mehr folgt irgendwann...)
4) Unsauber programmiert
5)...


Was ist sonst noch so zu beachten:
 - Code größtenteils auf Englisch (da python/info ja irgendwie auf englisch basiert...); Anmerkungen nicht
 - Kaum Änderungen an Vektorklassen (Bennis) deswegen ist nicht alles sonderlich einheitlich
 - Funktionen haben teilweise keine Docstrings... )-: folgt bestimmt auch noch...
 - Code hält sich nicht an irgentwelche Formatierungsrichtlinien...
 - Geschrieben und getestet mit Python 3.8.3 und Pygame 1.9.6
 - Aufgrund des Problems 3 dimensionale Dinge in 2 Dimensionen darzustellen, sind diese Vektoren 
	nie sehr genau eingezeichnet. 
 - Im reinen 2D-Raum sollten die Vektoren um +/- 2 pixel genau sein. (Das ist im 3D-Raum nicht immer so...)
 - Vectoren im 3D-Raum sind sehr schwer abzulesen. D.h. 2 sehr vers. Vektoren können beinahe identisch aussehen...
# Projekt mit gutem Namen
## Urls:

### / 
--> Liste der offenen Bestellungen
### /order
hier können Bestellungen aufgegeben werden. <br />
man braucht einen "store" als url parameter z.B. ?store="Blau"

### /all
liste aller Bestellungen 

### /done/\<int:id\> 
enpoint um Bestellungen von unerledigt zu erledigt zu ändern 
### /cancel/\<int:id>
endpoint um Bestellungen abzubrechen
### /accept/\<int:id>
endpoint um Bestellungen an zu nehmen und den Status zu ändern

### /getOrders
fetch api  die die tabelle der aktuellen bestellungen zurückgibt
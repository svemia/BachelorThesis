### _PBooster_ - model za anonimizaciju povijesti pretraživanja web-preglednika

_PBooster_ predstavlja anonimizacijski model kojim se, metodom manipulacije poviješću pretraživanja, štiti privatnost korisnika na Internetu.
U okviru ovog projekta implementiran  je prvi korak agloritma _PBooster_ - odabir broja novih poveznica koje je potrebno dodati u povijest pretraživanja.
Korišten je programski jezik _Python 3.6_ te biblioteke _NumPy_, _SciPy_ (za pomoć pri rješavanju matematičkih izraza) i _MatPlotLib_ (za grafički prikaz rezultata).

Osnovni program nalazi se u PBooster.py. Program se izvodi nad umjetno stvorenim skupom podataka definiranim u data.txt, koji se predaje kao argument komandne linije prilikom pokretanja.

#### Struktura ulaznih podataka
Znak '#' u data.txt predstavlja komentare te se linije koje tim znakom započinju preskaču. 
Vrijednosti parametra lambda označene su retkom koji započinje s 'Lambda'. Vrijednost parametra epsilon nalazi se u retku koji započinje s 'Epilon'.
Retci koji započinju s 'User' označuju podatke o korisnicima te svaki redak označava jednog korisnika. Korisnik je opisan distribucijom poveznica po temama
na način da je svaka tema odvojena zarezom i uz ime sadrži broj poveznica koje su uz nju vezane.

Učitavanje podataka iz vanjske datoteke mora se provesti sukladno opisanoj strukturi, inače učitavanje neće uspjeti. 
Može se provesti izmjena strukture ulaznih podataka - obavlja se izmjenom metode _readData_.

#### Klase 
Klasa _PBooster_ koristi se za stvaranje objekata modela. Konstruktor klase prima argumente _lambda_ i _epsilon_ koji opisuju model.
Klasa _User_ stvara objekte korisnika s atributom _topic_frequency_ (distribucija poveznica po temama), pri čemu se koristi struktura rječnika.

#### Funkcije
Pozivom metode _topicSelection_ ostvaruje se ulazak u algoritam odabira. Metoda kao argument prima objekt klase _User_. Metoda implementira pohlepni
algoritam lokalne potrage za korisnika nad kojim je pozvana. Rezultat je broj poveznica koje je potrebno dodati za svaku od tema (_to_be_added_), u obliku rječnika.

Metoda _calculateFunctionG_ provodi izračun optimizacijske funkcije. Funkcija kao argumente prima _topic_frequency_ i _to_be_added_, a kao rezultat vraća vrijednost optimizacijske
funkcije za ulazne parametre (_float_).

Metode _calculatePrivacy_ i _calculateUtilityLoss_ koriste se za izračun mjera privatnosti i gubitka korisnosti (potrebno za izračun optimizacijske funkcije).
_CalculatePrivacy_ kao argument uzima _topic_frequency_. _CalculateUtilityLoss_ kao argumente prima _topic_frequency_ i _topic_frequency_new_ (dobiven iz _topic_frequency_ i _to_be_added_).
Rezultat metoda je _float_.

_CalculateTopicProbability_ i _historySize_ pomoćne su metode za izračun vjerojatnosti tema i veličine povijesti pretraživanja.

_Main_ provodi učitavanje ulaznih podataka te formiranje strukture podataka koju program koristi.
Također, funkcija ostvaruje poziv topicSelection te nudi grafički prikaz rezultata algoritma.

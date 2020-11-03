// Berechnung der Fakultaet
// Teller 1 haelt das Argument
// Das Resultat erscheint auf Teller 3

// Uwe Naumann, 2012

Hole dir 3 Teller!
// Eingabe des Arguments
Frag mich, 
  wieviele Nudeln auf Teller 1 liegen sollen!
// 0!=1
Lege 1 Nudel auf Teller 3!
// Produktkette
Wiederhole folgendes,
  // Definition der Faktoren Teller 1 und Teller 2
  lege
    soviele Nudeln, wie auf Teller 3 liegen,
  auf Teller 2,
  und
  nimm
    soviele Nudeln, wie auf Teller 2 liegen,
  von Teller 3,
  und
  // Multiplikation Teller 1 * Teller 2
  // Resultat wird zu Teller 3 hinzugefuegt
  wiederhole folgendes,
    lege
      soviele Nudeln, wie auf Teller 1 liegen,
    auf Teller 3,
    und
    nimm 1 Nudel von Teller 2,
  solange Teller 2 nicht leer ist,
  und
  nimm 1 Nudel von Teller 1,
solange Teller 1 nicht leer ist!
// Ausgabe des Resultats
Sag mir,
  wieviele Nudeln auf Teller 3 liegen!
Bis bald!


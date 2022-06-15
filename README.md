# SmartGrid

Een poging tot een optimale SmartGrid oplossing, door Dirk Kuiper (12416657) & Lars Zwaan (12414069).
Onderdeel van Programmeertheorie, Minor Programmeren, UvA. 

## Case

Het probleem is als volgt opgebouwd: er zijn 3 districten, met in elk daarvan 150 huizen en 5 batterijen. 
Elk van deze huizen moet aan een batterij verbonden worden. Elk huis heeft een output en elke batterij
heeft een capaciteit; hierdoor is niet elke combinatie mogelijk. In dit project gaan we op zoek naar een 
optimale oplossing, waarbij optimaal bestaat uit het verkrijgen van een oplossing met een zo kort mogelijke
totale kabellengte. Hierbij mogen huizen die aan dezelfde batterij verbonden zijn kabels delen.

De beste door ons gevonden oplossing is de volgende:
<img src="output/plots/3_all_closest_only houses.png" width="500" heigth="500" alt="SmartGrid - optimale oplossing">

## Gebruik

Bij het runnen van main.py worden voor elk van de 3 districten een aantal algoritme's aangeroepen. 
Als eerst worden de huizen in een random volgorde aan batterijen verbonden. Hierna gebeurt 
deze ordening op volgorde op 2 manieren: kortste naar langste afstand 
tot dichtstbijzijnde batterij, met 150 configuraties: kortste eerst, op-één-na kortste eerst, enzovoort. 
Bij de tweede manier van ordenen wordt dit zelfde principe van ordenen niet alleen op de huizen, 
maar ook op de batterijen toegepast. Dit resulteert in 750 opties. Een uitgebreidere toelichting 
hierop valt te lezen onder het kopje 'Experiment'

Voor elk van deze 3 districten met elk 3 opties worden 2 figuren opgeslagen: een visuele
representatie van de oplossing met de kortste totale kabellengte, en een histogram van de
verdeling van de totale kabellengte van elk van de geldige configuraties. 

## Experiment

In het kader van experiment hebben we nagedacht over verschillende manieren om het algoritme te gebruiken dat huizen over batterijen verdeeld. Naast dat je dit x maal op een willekeurige manier kunt doen en hiermee een deel van de state-space kunt onderzoeken, kan je ook op een meer gestructureerde manier door een deel van de state-space zoeken. 

Elk van de 150 huizen kan aan 5 verschillende batterijen verbonden worden, mits de capaciteit dit toelaat. In ons algoritme gaat het vooral om de volgorde waarin dit gebeurd. Dit kun je in verschillende volgordes doen. Wij hebben deze verschillende mogelijkheden onderzocht en vergeleken. Hierin wordt veel gepraat over de afstand tussen een huis en een batterij, die wij berekenen volgens de manhattan distance. Het is echter belangrijk gedurende het lezen te beseffen dat kabels tussen huizen en batterijen gedeeld mogen worden; dit zorgt ervoor dat het verbinden van ieder huis aan de dichtstbijzijnde batterij niet per se optimaal is; een andere volgorde zou door optimaler kabels te delen voordeliger kunnen zijn. 
Als baseline kun je dit op een willekeurige manier doen. In dit geval verbindt een willekeurig huis eerst aan een willekeurige batterij. Hierna verbindt een willekeurig van de overgebleven 149  huizen aan een willekeurige batterij, mits er capaciteit beschikbaar is, enzovoorts. Als blijkt dat na verloop van tijd er een huis overblijft dat niet meer aan een batterij past vanwege te weinig capaciteit, wordt deze optie afgebroken en begint het proces opnieuw. Dit kun je door laten gaan tot je een x aantal mogelijke configuraties vindt, waarvan wij zowel de configuratie met de kortste totale kabellengte plotten, als de verdeling van de totale kabellengtes van deze configuraties.

De eerste optie naast de baseline is het bepalen van de volgorde van huizen verbinden op basis van de afstand tot de dichtstbijzijnde batterij. Hierbij wordt als eerste het huis met de kortste afstand tot zijn dichtstbijzijnde batterij verbonden aan deze batterij. Vervolgens wordt het huis met de op-één-na kortste afstand tot zijn dichtstbijzijnde batterij verbonden, enzovoort. Als de dichtstbijzijnde batterij van een huis vol is, wordt hij aan de op-één-na dichtstbijzijnde batterij verbonden, of de derde, etc. Dit geheel is de eerste configuratie (let op: dit hoeft niet per se een geldige configuratie qua capaciteit te zijn). De tweede mogelijke configuratie wordt bepaald met een iets andere volgorde: als eerste wordt het huis met de tweede kortste afstand aan de dichtstbijzijnde batterij verbonden, dan de derde, etc, met op het eind de 150ste en als allerlaatste de 1ste. Deze volgordes geïllustreerd met een cijfervoorbeeld, waarbij het nummer staat voor de rangorde van afstand tot de dichtstbijzijnde batterij: 1-2-3-4-5 > 2-3-4-5 > 3-4-5-1-2, etc. Dit geeft dus 150 mogelijke volgordes en dus configuraties, waarvan slechts een deel geldig zal zijn.

Ter uitbreiding van dit experiment hebben we vervolgens ditzelfde principe toegepast, maar dan omgekeerd. Hierbij wordt het huis met de verste afstand tot de verste batterij als eerste verbonden. Hierna de op-één-na verste afstand en zo verder. Dit is interessant om te onderzoeken, omdat het delen van kabels de dynamiek van het verbinden compleet verandert. Als het eerste huis met de verste batterij is verbonden, kun je je voorstellen dat deze initiele kabel hoge kosten heeft, maar dat het wel een goede basis geeft voor andere huizen om op aan te sluiten. Echter, dit idee was leuk, maar het leverde geen verbeterde resultaten op ten opzichte van het bepalen van de volgorde van huizen verbinden op basis van de afstand tot de dichtstbijzijnde batterij.

De tweede optie is een uitbreiding van de eerste. Hierbij wordt niet alleen de volgorde van de huizen aangepast, maar ook die van de batterijen. Ter illustratie nemen we de eerste geprobeerde volgorde uit optie 1. Hier wordt gestart met het huis met de kortste afstand tot de dichtstbijzijnde batterij, etc, maar ieder van deze huizen probeert altijd eerst aan zijn dichtstbijzijnde batterij te verbinden. In deze tweede optie worden ook de andere volgordes (batterij 2 - 3- 4- 5 - 1, bijvoorbeeld) geprobeerd. Dit geeft in totaal 750 mogelijk geldige configuraties.

Uit deze resultaten valt af te leiden dat het toevoegen van configuraties waarbij niet éérst wordt geprobeerd te verbinden aan de dichtstbijzijnde batterij, geen kortere oplossing geven. Dit is de reden dat wij andere volgordes niet hebben onderzocht, zoals volgordes als  bijvoorbeeld 3-1-4-2-5, waarbij de nummers niet opeenvolgend hoeven te zijn. 

## Check50

Deze opdracht wordt normaal gesproken automatisch gecontroleerd met check50. Helaas komt onze oplossing hier niet doorheen; ons programma telt
de gedeelde kabels op een andere manier dan dat check50 dat doet. Dit is een definitie-kwestie die in de opdracht niet wordt gespecificeerd:
worden niet-gedeelde kabels op het zelfde gridsegment enkel of dubbel meegeteld? Dit lijkt zo in het voorbeeld output.json bestand en uit de
code in het check50-bestand. Na overleg met vakassistentie is besloten dit verder niet te veranderen: onze methode werkt, aan de hand van onze 
definities. Het belangrijkste verschil is dat kabels die over hetzelfde stuk grid lopen, maar niet gedeeld zijn omdat ze naar verschillende 
batterijen lopen, ook niet als gedeeld worden geteld. Aangezien het voornamelijk gaat om de vergelijking tussen de resultaten, is dit verder
ook niet van cruciaal belang. 

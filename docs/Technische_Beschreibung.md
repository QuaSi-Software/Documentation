# Technische Beschreibung von Hauptkomponenten

## Wärmepumpe

Abb. 1: Allgemeines Anlagenschema einer Wärmepumpe: \
<img src="fig/WP_overview.png" alt="drawing" width="300"/>

Abb. 2: Energiebilanz der modellierten Wärmepumpe: \
<img src="fig/WP_Energies.png" alt="drawing" width="500"/>

Die Leistungszahl (COP) bestimmt die benötigte elektrische Leistung $$P_{el,WP}$$, um die Temperatur eines Massenstroms von dem Temperaturniveau $T_{WP,Quelle,in}$ auf $T_{WP,Senke,out}$ anzuheben: 

$$\epsilon_{WP} = \frac{\dot{Q}_{WP,ab}}{P_{el,WP}} \quad ( < \frac{1}{\eta_{Carnot}} = \frac{T_{WP,Senke,out}}{T_{WP,Senke,out}-T_{WP,Quelle,in} } )$$

Die Leistungszahl ist dabei immer kleiner als der maximal mögliche Carnot-Wirkungsgrad, der aus der Kondensator-Austritts- und Verdampfer-Eintrittstemperatur berechnet wird. In Quasi II ist ein COP-Kennfeld für verschiedene representative Wärmepumpen gegeben, auf denen die weiteren Berechnungen aufbauen.

Die Energiebilanz (bzw. Leistungsbilanz) der Wärmepumpe lässt sich nach Abbildung 2 aufstellen sowie ein Zusammenhang zwischen zu- und abgeführter Wärmeleistung in Abhängigkeit der Leistungszahl bestimmen: 

$\dot{Q}_{WP,ab} = \frac{\epsilon_{WP}}{\epsilon_{WP} -1} \ \dot{Q}_{WP,zu} \mathrm{\quad mit \quad} \dot{Q}_{WP,ab} = \dot{Q}_{WP,zu} + P_{WP,el}$

Die Leistung des Strombezugs der Wärmepumpe inklusive der Verluste der Leistungselektronik ergibt sich als: 

$P_{el,WP,Bezug} = \frac{P_{el,WP}}{\eta_{WP,LE}}$

**Annahme:** Thermische Verluste der WP sind bereits in Leistungszahl mit einberechnet.

Da auch die bisher nicht betrachteten Temperaturen der ein- und austretenden Wärmeströme in bzw. aus der Wärmepumpe von Relevanz sind, können die Wärmeleistungen anhand des jeweiligen Massenstroms $\dot{m}$ und der physikalischen Eigenschaften des Wärmeträgermediums (spezifische Wärmekapazität $c_{p}$ sowie ggf. der Dichte $\rho$) durch Umstellen der folgenden Gleichung berechnet werden:

$\dot{Q} = \dot{m} \ c_{p} \ (T_{max} - T_{min})$

\
Inputs und Outputs der Wärmepumpe:

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
$\dot{Q}_{WP,zu}$  | Der WP zugeführte Wärmestrom (Wärmequelle)   | [MW]
$\dot{Q}_{WP,ab}$   | Der WP abgeführte Wärmestrom (Wärmesenke)   | [MW]
$P_{el,WP}$   | Elektrische Leistungsaufnahme der WP   | [MW]
$P_{el,WP,Bezug}$   | Elektrische Leistungsaufnahme der WP inkl. Verluste der Leistungselektronik   | [MW]
$T_{WP,Senke,in}$   | Kondensator-Eintrittstemperatur   | [°C]
$T_{WP,Senke,out}$   | Kondensator-Austrittstemperatur   | [°C]
$T_{WP,Quelle,in}$   | Verdampfer-Eintrittstemperatur   | [°C]
$T_{WP,Quelle,out}$   | Verdampfer-Austrittstemperatur   | [°C]

\
Weitere Parameter der Wärmepumpe:
Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
$\epsilon_{WP}$  | Leistungszahl (COP) der Wärmepumpe inkl. thermische Verluste in Abhängigkeit von $T_{WP,Senke,out}$ und $T_{WP,Quelle,in}$ und von Teilllast??? | [-]
$\eta_{Carnot}$  | Carnot-Wirkungsgrad   | [-]
$\eta_{WP,LE}$  | Wirkungsgrad der Leistungselektronik für Wärmepumpe    | [-]
$TL_{WP,min}$  | minimal mögliche Teilllast    | [-]

\
Zustandsvariablen:
Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
$x_{WP}$  | Aktueller Betriebspunkt (an, aus, Teilllast)   | [%]

**ToDo**: Teillastverhalten? getaktet oder Drehzahlgeregelt (Inverter)?
Anpassung des COPs über lineare oder quadratische Funktion? Quadratische Funktion nicht invertierbar --> Iterative Lösung notwendig? Oder lineare Anpassung des Wirkungsgrades in Teillast? Oder konstander Wirkungsgrad in Teillast?

Beispiel für quadratische Teillast: \
<img src="fig/Beispiel_fuer_Teillast.png" alt="drawing" width="300"/> \
Quelle [Wemhöner2020]: https://www.uibk.ac.at/bauphysik/aktuell/news/doc/2020/wp_cw.pdf

## BHKW


## Elektrolyseur


## Brennstoffzelle


## Spitzenlastkessel (Erdgas)


## Pufferspeicher


## Langzeitwärmespeicher


## Wärmequellen 
(Vergleich FutureHeatPump II Projekt)


## Wasserstoffverdichter




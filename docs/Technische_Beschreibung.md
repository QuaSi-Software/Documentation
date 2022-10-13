# Technische Beschreibung von Hauptkomponenten

## Wärmepumpe
Als Wärmepumpe können elektrisch betriebene Kompressor-Wärmepumpen in das Modell eingebunden werden. Deren allgemeines Anlagenschema ist Abbildung 1 zu entnehmen. 

Abb. 1: Allgemeines Anlagenschema einer Wärmepumpe

![Image title](fig/WP_overview.png)

Die Energiebilanz an der Wärmepumpe setzt sich aus dem zugeführten Strom, der zugeführten Wärme auf niedrigem Temperaturniveau sowie dem abgeführten Wärmestrom auf höherem Temperaturniveau zusammen. Der Wirkungsgrad der Wärmepumpe wird dabei definiert über die Leistungszahl (COP) in Abhängigkeit der Kondensator-Austrittstemperatur sowie der Verdampfer-Eintrittstemperatur (vgl. Abbildung 2).

Abb. 2: Energiebilanz der modellierten Wärmepumpe

![Image title](fig/221006_Wärmepumpe_Energiefluss.png)
 
Die Leistungszahl bestimmt die benötigte elektrische Leistung \(P_{el,WP}\), um die Temperatur eines Massenstroms von dem Temperaturniveau \(T_{WP,Quelle,in}\) auf \(T_{WP,Senke,out}\) anzuheben: 

$$\epsilon_{WP} = \frac{\dot{Q}_{WP,ab}}{P_{el,WP}} \quad ( < \frac{1}{\eta_{Carnot}} = \frac{T_{WP,Senke,out}}{T_{WP,Senke,out}-T_{WP,Quelle,in} } )$$

Die Leistungszahl ist dabei immer kleiner als der maximal mögliche Carnot-Wirkungsgrad (\(\eta_{Carnot}\)), der aus der Kondensator-Austritts- und Verdampfer-Eintrittstemperatur berechnet wird. In Quasi II ist ein COP-Kennfeld für verschiedene representative Wärmepumpen gegeben, auf denen die weiteren Berechnungen aufbauen. Beispielhat ist ein Kennfeld einer Hochtemperatur-Wärmepumpe in der folgenden Abbildung als Kurvenschar gezeigt.

Abb. 3: Kennfeld einer Hochtemperaturwärmepumpe als Kurvenschar

![Image title](fig/COP_Kennfeld_Beispiel.png)

Die Energiebilanz (bzw. Leistungsbilanz) der Wärmepumpe lässt sich nach Abbildung 2 aufstellen sowie ein Zusammenhang zwischen zu- und abgeführter Wärmeleistung in Abhängigkeit der Leistungszahl bestimmen: 

$$\dot{Q}_{WP,ab} = \frac{\epsilon_{WP}}{\epsilon_{WP} -1} \ \dot{Q}_{WP,zu} \mathrm{\quad mit \quad} \dot{Q}_{WP,ab} = \dot{Q}_{WP,zu} + P_{WP,el}$$

Die Leistung des Strombezugs der Wärmepumpe inklusive der Verluste der Leistungselektronik ergibt sich als: 

$$P_{el,WP,Bezug} = \frac{P_{el,WP}}{\eta_{WP,LE}}$$

**Annahme:** Thermische Verluste der WP sind bereits in Leistungszahl mit einberechnet. 

Da auch die bisher nicht betrachteten Temperaturen der ein- und austretenden Wärmeströme in bzw. aus der Wärmepumpe von Relevanz sind, können die Wärmeleistungen anhand des jeweiligen Massenstroms \(\dot{m}\) und der physikalischen Eigenschaften des Wärmeträgermediums (spezifische Wärmekapazität \(c_{p}\) sowie ggf. der Dichte \(\rho\)) durch Umstellen der folgenden Gleichung berechnet werden:

$$\dot{Q} = \dot{m} \ c_{p} \ (T_{max} - T_{min})$$

**Inputs und Outputs der Wärmepumpe:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(\dot{Q}_{WP,zu}\)  | Der WP zugeführte Wärmestrom (Wärmequelle)   | [MW]
\(\dot{Q}_{WP,ab}\)   | Der WP abgeführte Wärmestrom (Wärmesenke)   | [MW]
\(P_{el,WP}\)   | Elektrische Leistungsaufnahme der WP   | [MW]
\(P_{el,WP,Bezug}\)   | Elektrische Leistungsaufnahme der WP inkl. Verluste der Leistungselektronik   | [MW]
\(T_{WP,Senke,in}\)   | Kondensator-Eintrittstemperatur   | [°C]
\(T_{WP,Senke,out}\)   | Kondensator-Austrittstemperatur   | [°C]
\(T_{WP,Quelle,in}\)   | Verdampfer-Eintrittstemperatur   | [°C]
\(T_{WP,Quelle,out}\)   | Verdampfer-Austrittstemperatur   | [°C]

**Weitere Parameter der Wärmepumpe:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(\epsilon_{WP}\)  | Leistungszahl (COP) der Wärmepumpe inkl. thermische Verluste in Abhängigkeit von \(T_{WP,Senke,out}\) und \(T_{WP,Quelle,in}\) und von Teilllast??? | [-]
\(\eta_{WP,LE}\)  | Wirkungsgrad der Leistungselektronik für Wärmepumpe    | [-]
\(TL_{WP,min}\)  | minimal mögliche Teilllast der Wärmepume    | [-]
\(MB_{WP}\)  | Mindestbetriebszeit der Wärmepumpe    | [min]

**Zustandsvariablen der Wärmepumpe:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(x_{WP}\)  | Aktueller Betriebspunkt (an, aus, Teilllast)   | [%]

**ToDo**: Teillastverhalten? getaktet oder Drehzahlgeregelt (Inverter)?
Anpassung des COPs über lineare oder quadratische Funktion? Quadratische Funktion nicht invertierbar --> Iterative Lösung notwendig? Oder lineare Anpassung des Wirkungsgrades in Teillast? Oder konstander Wirkungsgrad in Teillast?

Beispiel für quadratische Teillast: 

![Image title](fig/Beispiel_fuer_Teillast.png)
Quelle [Wemhöner2020]: https://www.uibk.ac.at/bauphysik/aktuell/news/doc/2020/wp_cw.pdf


## Elektrolyseur
Der Elektrolyseur verwendet elektrische Energie, um Wasser in die Bestandteile Wasserstoff (\(H_2\)) und Sauerstoff (\(O_2\)) aufzuspalten. Die dabei entstehende Abwärme kann direkt oder über eine Wärmepume nutzbar gemacht werden.

Abb. 3: Energie- und Stoffströme am Elektrolyseur

![Image title](fig/221013_Elektrolyseur.png)


$$\dot{Q}_{Ely,Abwärme} = \eta_{Ely,Wärmeauskopplung} \ (1-\eta_{Ely,H_2}) \ P_{el,Ely} = \eta_{Ely,Wärmeauskopplung} \ (P_{el,Ely} - \dot{E}_{Ely,H_2,out}) $$


$$ \dot{E}_{Ely,H_2,out}=  P_{el,Ely}\eta_{Ely,H_2} $$



**Inputs und Outputs des Elektrolyseurs:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(P_{el,Ely}\)   | Elektrische Leistungsaufnahme des Elektrolyseurs   | [MW]
\(P_{el,Ely,Bezug}\)   | Elektrische Leistungsaufnahme des Elektrolyseurs inkl. Verluste der Leistungselektronik   | [MW]
\(\dot{m}_{Ely,H_2O}\)  | Dem Elektrolyseur zugeführter Wasser-Massenstrom  | [kg/dt]
\(\dot{m}_{Ely,O_2,out}\)  | Dem Elektrolyseur abgeführter Sauerstoff-Massenstrom  | [kg/dt]
\(\dot{m}_{Ely,H_2,out}\)  | Dem Elektrolyseur abgeführter Wasserstoff-Massenstrom  | [kg/dt]
\(\dot{E}_{Ely,H_2,out}\)  | Dem Elektrolyseur abgeführter Wasserstoff-Energiestrom  | [MW]
\(T_{Ely,kühl,in}\)   | Kühlwassereintrittstemperatur Elektrolyseur   | [°C]
\(T_{Ely,kühl,out}\)   | Kühlwasseraustrittstemperatur Elektrolyseur   | [°C]
\(\dot{Q}_{Ely,Abwärme}\)  | Dem Elektrolyseur abgeführte Abwärme  | [MW]
\(\dot{Q}_{Ely,Verlust}\)  | Verluste im Elektrolyseur (ungenutze Abwärme)  | [MW]

**Weitere Parameter des Elektrolyseurs:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(\eta_{Ely,H_2}\)  | Wirkungsgrad der Wasserstoffgewinnung des Elektrolyseurs ( \(\dot{E}_{Ely,H_2,out}\) bezogen auf \(P_{el,Ely}\) )    | [-]
\(\eta_{Ely,Wärmeauskopplung}\)  | Wirkungsgrad der nutzbaren Wärmeauskopplung des Elektrolyseurs (bezogen auf \(1-\eta_{Ely,H_2}\))   | [-]
\(\eta_{Ely,O_2}\)  | Verhältnis von Sauerstoff- zu Wasserstoffgewinnung (Stöchiometrie)   | [-]
\(\eta_{Ely,LE}\)  | Wirkungsgrad der Leistungselektronik des Elektrolyseurs    | [-]
\(TL_{Ely,min}\)  | minimal mögliche Teilllast des Elektrolyseurs    | [-]
\(MB_{Ely}\)  | Mindestbetriebszeit des Elektrolyseurs    | [min]
\(AN_{Ely}\)  | Anlaufdauer des Elektrolyseurs bis zur vollen Wärmeauskopplung (linearer Verlauf)   | [min]


**Zustandsvariablen des Elektrolyseurs:**

Formelzeichen| Beschreibung | Einheit
-------- | -------- | --------
\(x_{Ely}\)  | Aktueller Betriebspunkt (an, aus, Teilllast)   | [%]

## Rückkühlung für Elektrolyseur 


## Brennstoffzelle


## BHKW


## Spitzenlastkessel (Erdgas)


## Pufferspeicher


## Langzeitwärmespeicher


## Wärmequellen 
(Vergleich FutureHeatPump II Projekt)


## Wasserstoffverdichter




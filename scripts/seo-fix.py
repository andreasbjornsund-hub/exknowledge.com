#!/usr/bin/env python3
"""
SEO fix script: 
1. Fix translated titles and descriptions
2. Add FAQ schema to all guide pages
"""

import re
import os
import json
from pathlib import Path

BASE = Path("/tmp/exknowledge")

LANGUAGES = ["de", "no", "es", "nl", "sv", "da", "fi", "pt", "it", "ar"]
GUIDE_PAGES = [
    "atex-directive", "atex-for-beginners", "atex-vs-iecex",
    "cable-glands-hazardous-areas", "compex-certification",
    "dust-explosion-protection", "ex-equipment-selection-guide",
    "explosion-proof-vs-intrinsically-safe", "hazardous-area-classification",
    "how-to-read-atex-nameplate", "hydrogen-explosion-protection"
]

# ========== TASK 1: TITLES AND DESCRIPTIONS ==========
# New native-sounding, click-worthy titles (<60 chars) and descriptions (<155 chars)

TITLES_DESCRIPTIONS = {
    "de": {
        "index": {
            "title": "ATEX & Ex-Schutz Wissensdatenbank – ExKnowledge",
            "desc": "Praxiswissen zu ATEX, IECEx und Explosionsschutz. Zoneneinteilung, Schutzarten, Gerätekategorien und Normen – verständlich erklärt für Ingenieure und Techniker."
        },
        "atex-directive": {
            "title": "ATEX-Richtlinie 2014/34/EU – Alles Wichtige",
            "desc": "Die ATEX-Richtlinie verständlich erklärt: Geltungsbereich, Konformitätsbewertung, CE-Kennzeichnung und Pflichten für Hersteller von Ex-Geräten."
        },
        "atex-for-beginners": {
            "title": "ATEX für Einsteiger – Einfach erklärt",
            "desc": "ATEX-Grundlagen verständlich aufbereitet: Zonen, Gerätekategorien, Ex-Kennzeichnung und Schutzkonzepte. Der ideale Einstieg in den Explosionsschutz."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Unterschiede im Vergleich",
            "desc": "ATEX und IECEx im direkten Vergleich: Geltungsbereich, Rechtsgrundlage, Kennzeichnung und Zertifizierungsverfahren. Welcher Standard wann gilt."
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-Kabelverschraubungen – Typen und Auswahl",
            "desc": "Kabelverschraubungen für Ex-Bereiche: Druckfeste (Ex d), erhöhte Sicherheit (Ex e) und Barriere-Typen. Gewindestandards, IP-Schutz und Montagetipps."
        },
        "compex-certification": {
            "title": "CompEx-Zertifizierung – Module und Karriere",
            "desc": "Alles zur CompEx-Zertifizierung: Module Ex01–Ex14, Schulungsinhalte, Gültigkeitsdauer und berufliche Vorteile für Ex-Fachkräfte."
        },
        "dust-explosion-protection": {
            "title": "Staubexplosionsschutz – Zonen und Maßnahmen",
            "desc": "Schutz vor Staubexplosionen: Brennbare Stäube, Zoneneinteilung 20/21/22, Zündquellen erkennen und geeignete Schutzmaßnahmen nach IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Ex-Geräte richtig auswählen – Praxisleitfaden",
            "desc": "Schritt für Schritt zum richtigen Ex-Gerät: Entscheidungsdiagramme, Zuordnung Zone-Kategorie und Vergleich der Schutzarten für jeden Einsatzbereich."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Druckfest oder eigensicher?",
            "desc": "Druckfeste Kapselung (Ex d) und Eigensicherheit (Ex i) im technischen Vergleich: Funktionsprinzipien, Einsatzbereiche und Entscheidungshilfen."
        },
        "hazardous-area-classification": {
            "title": "Zoneneinteilung explosionsgefährdeter Bereiche",
            "desc": "So werden Ex-Bereiche klassifiziert: Methodik, Freisetzungsquellen, Belüftungsbewertung und Dokumentation nach IEC 60079-10. Praxisnah erklärt."
        },
        "how-to-read-atex-nameplate": {
            "title": "ATEX-Typenschild lesen und verstehen",
            "desc": "ATEX-Typenschilder richtig entschlüsseln: CE-Zeichen, Gerätekategorien, Ex-Kennzeichnung, Temperaturklassen und Sonderbedingungen anhand realer Beispiele."
        },
        "hydrogen-explosion-protection": {
            "title": "Explosionsschutz bei Wasserstoff – IIC-Geräte",
            "desc": "Wasserstoff erfordert besonderen Explosionsschutz: Breiter Zündbereich, niedrige Zündenergie. So wählen Sie IIC-zertifizierte Geräte richtig aus."
        },
        # Non-guide pages
        "certification": {
            "title": "Ex-Zertifizierung – ATEX und IECEx Verfahren",
            "desc": "Überblick über Ex-Zertifizierungsverfahren nach ATEX und IECEx: Prüfstellen, Baumusterprüfung, Qualitätssicherung und Konformitätsbewertung."
        },
        "cheat-sheet": {
            "title": "ATEX-Spickzettel – Schnellreferenz",
            "desc": "ATEX und Ex-Schutz auf einen Blick: Zonen, Kategorien, Temperaturklassen und Schutzarten als praktische Schnellreferenz zum Nachschlagen."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Übersicht",
            "desc": "Equipment Protection Levels (EPL) nach IEC 60079-0 erklärt: Ga/Gb/Gc, Da/Db/Dc und Ma/Mb. Zuordnung zu ATEX-Kategorien und Zonen."
        },
        "ex-markings": {
            "title": "Ex-Kennzeichnung verstehen – Markierungen",
            "desc": "Ex-Kennzeichnungen entschlüsseln: Schutzarten, Gasgruppen, Temperaturklassen und EPL. So lesen Sie die Markierung auf Ex-Geräten richtig."
        },
        "faq": {
            "title": "Häufige Fragen zu ATEX und Explosionsschutz",
            "desc": "Antworten auf die häufigsten Fragen zu ATEX, IECEx, Zoneneinteilung, Schutzarten und Ex-Kennzeichnung. Schnelle Orientierung für Einsteiger."
        },
        "fundamentals": {
            "title": "Grundlagen des Explosionsschutzes",
            "desc": "Die Basis des Explosionsschutzes: Explosionsdreieck, Zündquellen, Schutzprinzipien und Zusammenhang zwischen Zonen, Kategorien und Schutzarten."
        },
        "gas-groups": {
            "title": "Gasgruppen IIA, IIB, IIC – Übersicht",
            "desc": "Gasgruppen im Explosionsschutz erklärt: IIA, IIB und IIC nach IEC 60079-20-1. Einteilung, Grenzspaltweiten, Zündströme und typische Gase."
        },
        "installation-inspection": {
            "title": "Ex-Installation und Inspektion – Leitfaden",
            "desc": "Anforderungen an Installation und Inspektion von Ex-Anlagen: IEC 60079-14/17, Erstprüfung, wiederkehrende Prüfungen und Dokumentation."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Systemvergleich",
            "desc": "Nordamerikanisches NEC 500/505 und europäisches ATEX/IEC-System im Vergleich: Divisions vs. Zonen, Schutzverfahren und gegenseitige Anerkennung."
        },
        "protection-methods": {
            "title": "Ex-Schutzarten – Alle Zündschutzarten",
            "desc": "Alle Ex-Schutzarten im Überblick: Druckfeste Kapselung (d), Eigensicherheit (i), Vergusskapselung (m), Überdruckkapselung (p) und weitere."
        },
        "standards": {
            "title": "Explosionsschutz-Normen – IEC 60079 Serie",
            "desc": "Übersicht der wichtigsten Normen im Explosionsschutz: IEC 60079-Reihe, EN-Normen und deren Anwendungsbereiche für Ex-Geräte und -Anlagen."
        },
        "temperature-classes": {
            "title": "Temperaturklassen T1–T6 im Ex-Schutz",
            "desc": "Temperaturklassen T1 bis T6 erklärt: Maximale Oberflächentemperaturen, Zuordnung zu Gasen und Bedeutung für die Geräteauswahl im Ex-Bereich."
        },
        "zone-classification": {
            "title": "Zonenklassifizierung – Zone 0, 1, 2, 20–22",
            "desc": "Zonenklassifizierung für Gas und Staub: Zone 0/1/2 und Zone 20/21/22 nach IEC 60079-10. Definitionen, Beispiele und Vorgehensweise."
        },
        "atex-equipment-categories": {
            "title": "ATEX-Gerätekategorien 1, 2 und 3",
            "desc": "ATEX-Gerätekategorien M1/M2, 1/2/3 erklärt: Schutzniveaus, erlaubte Zonen und Anforderungen an die Konformitätsbewertung nach 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-Verordnung (UK) – Übersicht",
            "desc": "Die britische DSEAR-Verordnung zum Explosionsschutz: Pflichten des Arbeitgebers, Risikobeurteilung und Unterschiede zur europäischen ATEX 153."
        },
    },
    "no": {
        "index": {
            "title": "ATEX og Ex-vern kunnskapsbase – ExKnowledge",
            "desc": "Praktisk kunnskap om ATEX, IECEx og eksplosjonsvern. Soneklassifisering, vernemetoder, utstyrskategorier og standarder – forklart for ingeniører."
        },
        "atex-directive": {
            "title": "ATEX-direktivet 2014/34/EU forklart",
            "desc": "Alt om ATEX-utstyrsdirektivet: virkeområde, samsvarsvurdering, CE-merking og krav til produsenter av Ex-utstyr."
        },
        "atex-for-beginners": {
            "title": "ATEX for nybegynnere – Enkel innføring",
            "desc": "Grunnleggende om ATEX på norsk: soner, utstyrskategorier, Ex-merking og vernekonsepter. Perfekt startpunkt for deg som er ny i eksplosjonsvern."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Forskjeller forklart",
            "desc": "ATEX og IECEx sammenlignet: geografisk virkeområde, rettsgrunnlag, merkekrav og sertifiseringsprosesser. Finn ut hvilken standard som gjelder."
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-kabelgjennomføringer – Typer og valg",
            "desc": "Kabelgjennomføringer for Ex-områder: flammesikre (Ex d), forhøyet sikkerhet (Ex e) og barrieretyper. Gjengstandarder, IP-klasser og vanlige feil."
        },
        "compex-certification": {
            "title": "CompEx-sertifisering – Moduler og karriere",
            "desc": "Alt om CompEx: moduler Ex01–Ex14, opplæringskrav, gyldighet, fornyelse og karrierefordeler for arbeid i eksplosjonsutsatte områder."
        },
        "dust-explosion-protection": {
            "title": "Støveksplosjonsvern – Soner og tiltak",
            "desc": "Vern mot støveksplosjoner: brennbart støv, soneklassifisering 20/21/22, tennkilder og riktig valg av tiltak etter IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Velge riktig Ex-utstyr – Praktisk guide",
            "desc": "Steg for steg til riktig Ex-utstyr: beslutningsdiagrammer, kobling mellom soner og kategorier, og sammenligning av vernemetoder."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Flammesikker eller egensikker?",
            "desc": "Flammesikker kapsel (Ex d) og egensikkerhet (Ex i) i teknisk sammenligning: virkemåte, bruksområder og valgkriterier for ingeniører."
        },
        "hazardous-area-classification": {
            "title": "Klassifisering av eksplosjonsfarlige områder",
            "desc": "Slik klassifiseres Ex-områder i soner: metode, utslippskilder, ventilasjonsvurdering og dokumentasjonskrav etter IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Lese ATEX-typeskilt – Komplett guide",
            "desc": "Slik avkoder du ATEX-typeskilter: CE-merking, utstyrskategorier, Ex-merking, temperaturklasser og spesialvilkår med reelle eksempler."
        },
        "hydrogen-explosion-protection": {
            "title": "Eksplosjonsvern for hydrogen – IIC-utstyr",
            "desc": "Hydrogen krever spesielt eksplosjonsvern: bredt tennområde og lav tennenergi. Slik velger du riktig IIC-sertifisert utstyr."
        },
        "certification": {
            "title": "Ex-sertifisering – ATEX og IECEx prosesser",
            "desc": "Oversikt over Ex-sertifisering etter ATEX og IECEx: prøveinstitusjoner, typegodkjenning, kvalitetssikring og samsvarsvurdering."
        },
        "cheat-sheet": {
            "title": "ATEX-jukselapp – Hurtigreferanse",
            "desc": "ATEX og Ex-vern på én side: soner, kategorier, temperaturklasser og vernemetoder som praktisk hurtigreferanse."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) forklart",
            "desc": "Equipment Protection Levels etter IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc og Ma/Mb. Kobling til ATEX-kategorier og soner."
        },
        "ex-markings": {
            "title": "Ex-merking – Slik leser du merkingen",
            "desc": "Forstå Ex-merking: vernemetoder, gasgrupper, temperaturklasser og EPL. Slik tolker du merkingen på Ex-utstyr korrekt."
        },
        "faq": {
            "title": "Vanlige spørsmål om ATEX og Ex-vern",
            "desc": "Svar på vanlige spørsmål om ATEX, IECEx, soneinndeling, vernemetoder og Ex-merking. Rask oversikt for nybegynnere og fagfolk."
        },
        "fundamentals": {
            "title": "Grunnleggende om eksplosjonsvern",
            "desc": "Eksplosjonsvern fra grunnen: eksplosjonstrekanten, tennkilder, verneprinsipper og sammenhengen mellom soner, kategorier og vernemetoder."
        },
        "gas-groups": {
            "title": "Gasgrupper IIA, IIB, IIC – Oversikt",
            "desc": "Gasgrupper i eksplosjonsvern: IIA, IIB og IIC etter IEC 60079-20-1. Inndeling, spaltevidder, tennstrømmer og typiske gasser."
        },
        "installation-inspection": {
            "title": "Ex-installasjon og inspeksjon – Veiledning",
            "desc": "Krav til installasjon og inspeksjon av Ex-anlegg: IEC 60079-14/17, førstegangskontroll, periodisk kontroll og dokumentasjon."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Sammenligning",
            "desc": "Nordamerikansk NEC 500/505 og europeisk ATEX/IEC sammenlignet: Divisions vs. soner, vernemetoder og gjensidig anerkjennelse."
        },
        "protection-methods": {
            "title": "Ex-vernemetoder – Komplett oversikt",
            "desc": "Alle Ex-vernemetoder forklart: flammesikker kapsling (d), egensikkerhet (i), støpemasse (m), overtrykk (p) og flere."
        },
        "standards": {
            "title": "Eksplosjonsvern-standarder – IEC 60079",
            "desc": "Oversikt over de viktigste standardene i eksplosjonsvern: IEC 60079-serien, EN-standarder og bruksområder for Ex-utstyr."
        },
        "temperature-classes": {
            "title": "Temperaturklasser T1–T6 i Ex-vern",
            "desc": "Temperaturklasser T1 til T6 forklart: maksimale overflatetemperaturer, tilhørende gasser og betydning for utstyrsvalg."
        },
        "zone-classification": {
            "title": "Soneklassifisering – Sone 0, 1, 2, 20–22",
            "desc": "Soneklassifisering for gass og støv: sone 0/1/2 og sone 20/21/22 etter IEC 60079-10. Definisjoner, eksempler og framgangsmåte."
        },
        "atex-equipment-categories": {
            "title": "ATEX-utstyrskategorier 1, 2 og 3",
            "desc": "ATEX-utstyrskategorier M1/M2, 1/2/3: vernenivåer, tillatte soner og krav til samsvarsvurdering etter 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-forskriften (UK) – Oversikt",
            "desc": "Britisk DSEAR-forskrift for eksplosjonsvern: arbeidsgivers plikter, risikovurdering og forskjeller fra europeisk ATEX 153."
        },
    },
    "es": {
        "index": {
            "title": "Base de conocimiento ATEX y Ex – ExKnowledge",
            "desc": "Conocimiento práctico sobre ATEX, IECEx y protección contra explosiones. Zonas, métodos de protección, categorías de equipos y normativas explicadas."
        },
        "atex-directive": {
            "title": "Directiva ATEX 2014/34/UE – Guía completa",
            "desc": "La directiva ATEX de equipos explicada: alcance, evaluación de conformidad, marcado CE y obligaciones del fabricante de equipos Ex."
        },
        "atex-for-beginners": {
            "title": "ATEX para principiantes – Guía básica",
            "desc": "Conceptos básicos de ATEX en español: zonas, categorías de equipos, marcado Ex y principios de protección. Tu primer paso en seguridad antiexplosión."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Diferencias clave",
            "desc": "ATEX e IECEx comparados: alcance geográfico, base legal, marcado y certificación. Descubre cuándo aplica cada norma de protección antiexplosión."
        },
        "cable-glands-hazardous-areas": {
            "title": "Prensaestopas Ex – Tipos y selección",
            "desc": "Prensaestopas para zonas con riesgo de explosión: antideflagrantes (Ex d), seguridad aumentada (Ex e) y barrera. Roscas, IP y errores frecuentes."
        },
        "compex-certification": {
            "title": "Certificación CompEx – Módulos y carrera",
            "desc": "Todo sobre CompEx: módulos Ex01–Ex14, requisitos de formación, validez, renovación y ventajas profesionales para trabajar en zonas peligrosas."
        },
        "dust-explosion-protection": {
            "title": "Protección contra explosiones de polvo",
            "desc": "Prevención de explosiones de polvo: tipos de polvo combustible, zonas 20/21/22, fuentes de ignición y selección de equipos según IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Selección de equipos Ex – Guía práctica",
            "desc": "Cómo elegir equipos Ex paso a paso: diagramas de decisión, relación zona-categoría, comparación de métodos de protección y recomendaciones."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Antideflagrante o seguridad?",
            "desc": "Envolvente antideflagrante (Ex d) frente a seguridad intrínseca (Ex i): principios, aplicaciones y criterios de selección para ingenieros."
        },
        "hazardous-area-classification": {
            "title": "Clasificación de áreas peligrosas – Guía",
            "desc": "Cómo se clasifican las áreas peligrosas en zonas: metodología, fuentes de emisión, ventilación y documentación según IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Leer una placa ATEX – Guía de decodificación",
            "desc": "Aprende a interpretar placas ATEX paso a paso: marcado CE, categorías, marcado Ex, clases de temperatura y condiciones especiales con ejemplos."
        },
        "hydrogen-explosion-protection": {
            "title": "Protección antiexplosión para hidrógeno",
            "desc": "El hidrógeno exige protección especial: amplio rango de inflamabilidad y baja energía de ignición. Guía para seleccionar equipos IIC correctamente."
        },
        "certification": {
            "title": "Certificación Ex – Procesos ATEX e IECEx",
            "desc": "Procesos de certificación Ex según ATEX e IECEx: organismos notificados, ensayo de tipo, aseguramiento de calidad y evaluación de conformidad."
        },
        "cheat-sheet": {
            "title": "Hoja de referencia ATEX – Consulta rápida",
            "desc": "ATEX y protección Ex en una página: zonas, categorías, clases de temperatura y métodos de protección como referencia rápida."
        },
        "epl": {
            "title": "Nivel de Protección del Equipo (EPL)",
            "desc": "Niveles de protección del equipo según IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc y Ma/Mb. Relación con categorías ATEX y zonas."
        },
        "ex-markings": {
            "title": "Marcado Ex – Cómo interpretarlo",
            "desc": "Entiende el marcado Ex: métodos de protección, grupos de gas, clases de temperatura y EPL. Guía para interpretar marcas en equipos Ex."
        },
        "faq": {
            "title": "Preguntas frecuentes sobre ATEX y Ex",
            "desc": "Respuestas a las preguntas más comunes sobre ATEX, IECEx, clasificación de zonas, métodos de protección y marcado Ex."
        },
        "fundamentals": {
            "title": "Fundamentos de protección contra explosiones",
            "desc": "Bases de la protección antiexplosión: triángulo de explosión, fuentes de ignición, principios de protección y relación zonas-categorías."
        },
        "gas-groups": {
            "title": "Grupos de gas IIA, IIB, IIC – Guía",
            "desc": "Grupos de gas en protección antiexplosión: IIA, IIB e IIC según IEC 60079-20-1. Clasificación, intersticios y gases típicos."
        },
        "installation-inspection": {
            "title": "Instalación e inspección Ex – Requisitos",
            "desc": "Requisitos para instalación e inspección de equipos Ex: IEC 60079-14/17, verificación inicial, inspecciones periódicas y documentación."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Comparación",
            "desc": "Sistema norteamericano NEC 500/505 frente al europeo ATEX/IEC: Divisions vs. zonas, métodos de protección y reconocimiento mutuo."
        },
        "protection-methods": {
            "title": "Métodos de protección Ex – Todos los tipos",
            "desc": "Todos los métodos de protección Ex: envolvente antideflagrante (d), seguridad intrínseca (i), encapsulado (m), presurización (p) y más."
        },
        "standards": {
            "title": "Normas de protección antiexplosión – IEC",
            "desc": "Las normas clave de protección antiexplosión: serie IEC 60079, normas EN y sus ámbitos de aplicación para equipos e instalaciones Ex."
        },
        "temperature-classes": {
            "title": "Clases de temperatura T1–T6 en Ex",
            "desc": "Clases de temperatura T1 a T6 explicadas: temperaturas superficiales máximas, gases asociados y su importancia en la selección de equipos."
        },
        "zone-classification": {
            "title": "Clasificación de zonas – 0, 1, 2, 20–22",
            "desc": "Clasificación de zonas para gas y polvo: zona 0/1/2 y zona 20/21/22 según IEC 60079-10. Definiciones, ejemplos y metodología."
        },
        "atex-equipment-categories": {
            "title": "Categorías de equipos ATEX – 1, 2 y 3",
            "desc": "Categorías ATEX M1/M2, 1/2/3: niveles de protección, zonas permitidas y requisitos de evaluación de conformidad según 2014/34/UE."
        },
        "dsear-regulations-uk": {
            "title": "Reglamento DSEAR (Reino Unido) – Resumen",
            "desc": "Reglamento británico DSEAR sobre protección antiexplosión: obligaciones del empleador, evaluación de riesgos y diferencias con la ATEX 153 europea."
        },
    },
    "nl": {
        "index": {
            "title": "ATEX & Ex-bescherming kennisbank – ExKnowledge",
            "desc": "Praktische kennis over ATEX, IECEx en explosiebeveiliging. Zone-indeling, beschermingsmethoden, apparaatcategorieën en normen helder uitgelegd."
        },
        "atex-directive": {
            "title": "ATEX-richtlijn 2014/34/EU – Uitleg",
            "desc": "De ATEX-richtlijn helder uitgelegd: toepassingsgebied, conformiteitsbeoordeling, CE-markering en verplichtingen voor fabrikanten van Ex-apparatuur."
        },
        "atex-for-beginners": {
            "title": "ATEX voor beginners – Eenvoudig uitgelegd",
            "desc": "ATEX-basiskennis begrijpelijk gemaakt: zones, apparaatcategorieën, Ex-markering en beschermingsconcepten. Het ideale startpunt voor nieuwkomers."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Verschillen vergeleken",
            "desc": "ATEX en IECEx naast elkaar gelegd: toepassingsgebied, wettelijke basis, markering en certificering. Wanneer geldt welke norm?"
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-kabelwartels – Typen en selectie",
            "desc": "Kabelwartels voor Ex-zones: drukvaste (Ex d), verhoogde veiligheid (Ex e) en barrièretypen. Draadstandaarden, IP-klassen en veelgemaakte fouten."
        },
        "compex-certification": {
            "title": "CompEx-certificering – Modules en carrière",
            "desc": "Alles over CompEx: modules Ex01–Ex14, opleidingsvereisten, geldigheid, verlenging en voordelen voor werken in explosiegevaarlijke gebieden."
        },
        "dust-explosion-protection": {
            "title": "Stofexplosiebeveiliging – Zones en maatregelen",
            "desc": "Bescherming tegen stofexplosies: brandbaar stof, zone-indeling 20/21/22, ontstekingsbronnen en juiste maatregelen volgens IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Ex-apparatuur kiezen – Praktische gids",
            "desc": "Stap voor stap de juiste Ex-apparatuur kiezen: beslisschema's, zone-categorie koppeling en vergelijking van beschermingsmethoden."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Drukvast of intrinsiek veilig?",
            "desc": "Drukvaste behuizing (Ex d) en intrinsieke veiligheid (Ex i) technisch vergeleken: werkingsprincipes, toepassingen en keuzecriteria."
        },
        "hazardous-area-classification": {
            "title": "Classificatie van gevaarlijke zones – Gids",
            "desc": "Zo worden Ex-zones ingedeeld: methodiek, emissiebronnen, ventilatiebeoordeling en documentatie-eisen volgens IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "ATEX-typeplaatje lezen – Decodering",
            "desc": "Leer ATEX-typeplaatjes correct lezen: CE-markering, categorieën, Ex-markering, temperatuurklassen en bijzondere voorwaarden met praktijkvoorbeelden."
        },
        "hydrogen-explosion-protection": {
            "title": "Explosiebeveiliging waterstof – IIC-apparatuur",
            "desc": "Waterstof vraagt om bijzondere explosiebeveiliging: breed ontvlambaarheidsgebied en lage ontstekingsenergie. Zo kiest u IIC-apparatuur."
        },
        "certification": {
            "title": "Ex-certificering – ATEX en IECEx procedures",
            "desc": "Overzicht van Ex-certificeringsprocedures volgens ATEX en IECEx: keuringsinstanties, typeonderzoek en conformiteitsbeoordeling."
        },
        "cheat-sheet": {
            "title": "ATEX-spiekbriefje – Snelle referentie",
            "desc": "ATEX en Ex-bescherming op één pagina: zones, categorieën, temperatuurklassen en beschermingsmethoden als handig naslagwerk."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Uitleg",
            "desc": "Equipment Protection Levels volgens IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc en Ma/Mb. Koppeling met ATEX-categorieën en zones."
        },
        "ex-markings": {
            "title": "Ex-markering begrijpen – Handleiding",
            "desc": "Ex-markeringen ontcijferd: beschermingsmethoden, gasgroepen, temperatuurklassen en EPL. Zo leest u de markering op Ex-apparatuur."
        },
        "faq": {
            "title": "Veelgestelde vragen over ATEX en Ex",
            "desc": "Antwoorden op veelgestelde vragen over ATEX, IECEx, zone-indeling, beschermingsmethoden en Ex-markering."
        },
        "fundamentals": {
            "title": "Basisprincipes explosiebeveiliging",
            "desc": "Basis van explosiebeveiliging: explosiedriehoek, ontstekingsbronnen, beschermingsprincipes en samenhang zones-categorieën-methoden."
        },
        "gas-groups": {
            "title": "Gasgroepen IIA, IIB, IIC – Overzicht",
            "desc": "Gasgroepen in explosiebeveiliging: IIA, IIB en IIC volgens IEC 60079-20-1. Indeling, spleetwijdtes en kenmerkende gassen."
        },
        "installation-inspection": {
            "title": "Ex-installatie en inspectie – Eisen",
            "desc": "Eisen aan installatie en inspectie van Ex-installaties: IEC 60079-14/17, initiële inspectie, periodieke controles en documentatie."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Vergelijking",
            "desc": "Noord-Amerikaans NEC 500/505 en Europees ATEX/IEC vergeleken: Divisions vs. zones, beschermingsmethoden en wederzijdse erkenning."
        },
        "protection-methods": {
            "title": "Ex-beschermingsmethoden – Alle types",
            "desc": "Alle Ex-beschermingsmethoden: drukvaste behuizing (d), intrinsieke veiligheid (i), vergietmassa (m), overdruk (p) en meer."
        },
        "standards": {
            "title": "Explosiebeveiliging normen – IEC 60079",
            "desc": "Overzicht van de belangrijkste normen voor explosiebeveiliging: IEC 60079-reeks, EN-normen en toepassingsgebieden."
        },
        "temperature-classes": {
            "title": "Temperatuurklassen T1–T6 in Ex",
            "desc": "Temperatuurklassen T1 tot T6 uitgelegd: maximale oppervlaktetemperaturen, bijbehorende gassen en belang voor apparaatkeuze."
        },
        "zone-classification": {
            "title": "Zone-indeling – Zone 0, 1, 2, 20–22",
            "desc": "Zone-indeling voor gas en stof: zone 0/1/2 en zone 20/21/22 volgens IEC 60079-10. Definities, voorbeelden en werkwijze."
        },
        "atex-equipment-categories": {
            "title": "ATEX-apparaatcategorieën 1, 2 en 3",
            "desc": "ATEX-categorieën M1/M2, 1/2/3: beschermingsniveaus, toegestane zones en eisen aan conformiteitsbeoordeling per 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-regelgeving (VK) – Overzicht",
            "desc": "De Britse DSEAR-regelgeving voor explosiebeveiliging: werkgeversplichten, risicobeoordeling en verschillen met de Europese ATEX 153."
        },
    },
    "sv": {
        "index": {
            "title": "ATEX & Ex-skydd kunskapsbas – ExKnowledge",
            "desc": "Praktisk kunskap om ATEX, IECEx och explosionsskydd. Zonklassificering, skyddsmetoder, utrustningskategorier och standarder tydligt förklarade."
        },
        "atex-directive": {
            "title": "ATEX-direktivet 2014/34/EU – Genomgång",
            "desc": "ATEX-utrustningsdirektivet förklarat: tillämpningsområde, bedömning av överensstämmelse, CE-märkning och skyldigheter för tillverkare."
        },
        "atex-for-beginners": {
            "title": "ATEX för nybörjare – Enkel introduktion",
            "desc": "ATEX-grunder på svenska: zoner, utrustningskategorier, Ex-märkning och skyddskoncept. Det perfekta startskottet för explosionsskydd."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Skillnaderna förklarade",
            "desc": "ATEX och IECEx jämförda: geografiskt tillämpningsområde, rättslig grund, märkningsskillnader och certifieringsprocesser."
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-kabelgenomföringar – Typer och val",
            "desc": "Kabelgenomföringar för Ex-områden: trycksäkra (Ex d), ökad säkerhet (Ex e) och barriärtyper. Gängstandarder, IP-klass och vanliga misstag."
        },
        "compex-certification": {
            "title": "CompEx-certifiering – Moduler och karriär",
            "desc": "Allt om CompEx: moduler Ex01–Ex14, utbildningskrav, giltighet, förnyelse och karriärfördelar för arbete i explosionsfarliga områden."
        },
        "dust-explosion-protection": {
            "title": "Dammexplosionsskydd – Zoner och åtgärder",
            "desc": "Skydd mot dammexplosioner: brännbart damm, zonklassificering 20/21/22, tändkällor och lämpliga åtgärder enligt IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Välja rätt Ex-utrustning – Praktisk guide",
            "desc": "Steg för steg till rätt Ex-utrustning: beslutsdiagram, koppling zon-kategori och jämförelse av skyddsmetoder för varje tillämpning."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Trycksäker eller egensäker?",
            "desc": "Trycksäker kapsling (Ex d) och egensäkerhet (Ex i) i teknisk jämförelse: funktionsprinciper, användningsområden och valkriterier."
        },
        "hazardous-area-classification": {
            "title": "Klassificering av explosionsfarliga områden",
            "desc": "Så klassificeras Ex-områden i zoner: metodik, utsläppskällor, ventilationsbedömning och dokumentationskrav enligt IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Läsa ATEX-typskylt – Komplett guide",
            "desc": "Lär dig avkoda ATEX-typskyltar: CE-märkning, kategorier, Ex-märkning, temperaturklasser och specialvillkor med verkliga exempel."
        },
        "hydrogen-explosion-protection": {
            "title": "Explosionsskydd för vätgas – IIC-utrustning",
            "desc": "Vätgas kräver särskilt explosionsskydd: brett antändningsområde och låg antändningsenergi. Så väljer du rätt IIC-utrustning."
        },
        "certification": {
            "title": "Ex-certifiering – ATEX och IECEx processer",
            "desc": "Översikt av Ex-certifiering enligt ATEX och IECEx: provningsorgan, typprovning, kvalitetssäkring och bedömning av överensstämmelse."
        },
        "cheat-sheet": {
            "title": "ATEX-fusklapp – Snabbreferens",
            "desc": "ATEX och Ex-skydd på en sida: zoner, kategorier, temperaturklasser och skyddsmetoder som praktisk snabbreferens."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Guide",
            "desc": "Equipment Protection Levels enligt IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc och Ma/Mb. Koppling till ATEX-kategorier och zoner."
        },
        "ex-markings": {
            "title": "Ex-märkning – Så tolkar du den",
            "desc": "Förstå Ex-märkning: skyddsmetoder, gasgrupper, temperaturklasser och EPL. Så tolkar du märkningen på Ex-utrustning korrekt."
        },
        "faq": {
            "title": "Vanliga frågor om ATEX och Ex-skydd",
            "desc": "Svar på vanliga frågor om ATEX, IECEx, zonklassificering, skyddsmetoder och Ex-märkning."
        },
        "fundamentals": {
            "title": "Grundläggande om explosionsskydd",
            "desc": "Grunden för explosionsskydd: explosiontriangeln, tändkällor, skyddsprinciper och sambandet mellan zoner, kategorier och skyddsmetoder."
        },
        "gas-groups": {
            "title": "Gasgrupper IIA, IIB, IIC – Översikt",
            "desc": "Gasgrupper inom explosionsskydd: IIA, IIB och IIC enligt IEC 60079-20-1. Indelning, spaltvidder och typiska gaser."
        },
        "installation-inspection": {
            "title": "Ex-installation och inspektion – Krav",
            "desc": "Krav på installation och inspektion av Ex-anläggningar: IEC 60079-14/17, förstagångsinspektion, periodisk kontroll och dokumentation."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Jämförelse",
            "desc": "Nordamerikanskt NEC 500/505 och europeiskt ATEX/IEC jämfört: Divisions vs. zoner, skyddsmetoder och ömsesidigt erkännande."
        },
        "protection-methods": {
            "title": "Ex-skyddsmetoder – Alla typer",
            "desc": "Alla Ex-skyddsmetoder: trycksäker kapsling (d), egensäkerhet (i), gjutmassa (m), övertryck (p) och fler."
        },
        "standards": {
            "title": "Explosionsskyddsstandarder – IEC 60079",
            "desc": "Översikt av de viktigaste standarderna för explosionsskydd: IEC 60079-serien, EN-standarder och tillämpningsområden."
        },
        "temperature-classes": {
            "title": "Temperaturklasser T1–T6 inom Ex-skydd",
            "desc": "Temperaturklasser T1 till T6 förklarade: maximala yttemperaturer, tillhörande gaser och betydelse för utrustningsval."
        },
        "zone-classification": {
            "title": "Zonklassificering – Zon 0, 1, 2, 20–22",
            "desc": "Zonklassificering för gas och damm: zon 0/1/2 och zon 20/21/22 enligt IEC 60079-10. Definitioner, exempel och metodik."
        },
        "atex-equipment-categories": {
            "title": "ATEX-utrustningskategorier 1, 2 och 3",
            "desc": "ATEX-kategorier M1/M2, 1/2/3: skyddsnivåer, tillåtna zoner och krav på bedömning av överensstämmelse enligt 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-regler (UK) – Översikt",
            "desc": "Brittiska DSEAR-regler för explosionsskydd: arbetsgivarens skyldigheter, riskbedömning och skillnader mot europeisk ATEX 153."
        },
    },
    "da": {
        "index": {
            "title": "ATEX & Ex-beskyttelse vidensbase – ExKnowledge",
            "desc": "Praktisk viden om ATEX, IECEx og eksplosionsbeskyttelse. Zoneklassificering, beskyttelsesmetoder, udstyrskategorier og standarder forklaret."
        },
        "atex-directive": {
            "title": "ATEX-direktivet 2014/34/EU forklaret",
            "desc": "ATEX-udstyrsdirektivet forklaret: anvendelsesområde, overensstemmelsesvurdering, CE-mærkning og forpligtelser for producenter af Ex-udstyr."
        },
        "atex-for-beginners": {
            "title": "ATEX for begyndere – Nem introduktion",
            "desc": "Grundlæggende ATEX på dansk: zoner, udstyrskategorier, Ex-mærkning og beskyttelseskoncepter. Det ideelle udgangspunkt for eksplosionsbeskyttelse."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Forskelle forklaret",
            "desc": "ATEX og IECEx sammenlignet: geografisk anvendelse, lovgrundlag, mærkningsforskelle og certificeringsprocesser. Hvornår gælder hvad?"
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-kabelgennemføringer – Typer og valg",
            "desc": "Kabelgennemføringer til Ex-områder: flammesikre (Ex d), forhøjet sikkerhed (Ex e) og barrieretyper. Gevindstandarder, IP-klasse og fejl."
        },
        "compex-certification": {
            "title": "CompEx-certificering – Moduler og karriere",
            "desc": "Alt om CompEx: moduler Ex01–Ex14, uddannelseskrav, gyldighed, fornyelse og karrierefordele for arbejde i eksplosionsfarlige områder."
        },
        "dust-explosion-protection": {
            "title": "Støveksplosionsbeskyttelse – Zoner og tiltag",
            "desc": "Beskyttelse mod støveksplosioner: brændbart støv, zoneklassificering 20/21/22, tændkilder og udstyrvalg efter IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Vælg rigtigt Ex-udstyr – Praktisk guide",
            "desc": "Trin for trin til det rigtige Ex-udstyr: beslutningsdiagrammer, zone-kategori kobling og sammenligning af beskyttelsesmetoder."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Flammesikker eller egensikker?",
            "desc": "Flammesikker kapsel (Ex d) og egensikkerhed (Ex i) teknisk sammenlignet: funktionsprincipper, anvendelser og udvælgelseskriterier."
        },
        "hazardous-area-classification": {
            "title": "Klassificering af farlige områder – Guide",
            "desc": "Sådan klassificeres Ex-områder i zoner: metodik, udslipskilder, ventilationsvurdering og dokumentationskrav efter IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Læs et ATEX-typeskilt – Komplet guide",
            "desc": "Lær at afkode ATEX-typeskilte: CE-mærkning, kategorier, Ex-mærkning, temperaturklasser og særlige betingelser med virkelige eksempler."
        },
        "hydrogen-explosion-protection": {
            "title": "Eksplosionsbeskyttelse for brint – IIC-udstyr",
            "desc": "Brint kræver særlig eksplosionsbeskyttelse: bredt antændelsesområde og lav antændelsesenergi. Sådan vælger du IIC-godkendt udstyr."
        },
        "certification": {
            "title": "Ex-certificering – ATEX og IECEx processer",
            "desc": "Oversigt over Ex-certificering efter ATEX og IECEx: prøvningsinstitutter, typeprøvning, kvalitetssikring og overensstemmelsesvurdering."
        },
        "cheat-sheet": {
            "title": "ATEX-snydeark – Hurtig reference",
            "desc": "ATEX og Ex-beskyttelse på én side: zoner, kategorier, temperaturklasser og beskyttelsesmetoder som praktisk hurtig reference."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) forklaret",
            "desc": "Equipment Protection Levels efter IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc og Ma/Mb. Kobling til ATEX-kategorier og zoner."
        },
        "ex-markings": {
            "title": "Ex-mærkning – Sådan tolker du den",
            "desc": "Forstå Ex-mærkning: beskyttelsesmetoder, gasgrupper, temperaturklasser og EPL. Sådan læser du mærkningen på Ex-udstyr korrekt."
        },
        "faq": {
            "title": "Ofte stillede spørgsmål om ATEX og Ex",
            "desc": "Svar på de mest stillede spørgsmål om ATEX, IECEx, zoneklassificering, beskyttelsesmetoder og Ex-mærkning."
        },
        "fundamentals": {
            "title": "Grundlæggende om eksplosionsbeskyttelse",
            "desc": "Fundamentet for eksplosionsbeskyttelse: explosionstrekanten, tændkilder, beskyttelsesprincipper og sammenhængen zoner-kategorier."
        },
        "gas-groups": {
            "title": "Gasgrupper IIA, IIB, IIC – Oversigt",
            "desc": "Gasgrupper i eksplosionsbeskyttelse: IIA, IIB og IIC efter IEC 60079-20-1. Inddeling, spaltevidder og typiske gasser."
        },
        "installation-inspection": {
            "title": "Ex-installation og inspektion – Krav",
            "desc": "Krav til installation og inspektion af Ex-anlæg: IEC 60079-14/17, førstegangskontrol, periodisk kontrol og dokumentation."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Sammenligning",
            "desc": "Nordamerikansk NEC 500/505 og europæisk ATEX/IEC sammenlignet: Divisions vs. zoner, beskyttelsesmetoder og gensidig anerkendelse."
        },
        "protection-methods": {
            "title": "Ex-beskyttelsesmetoder – Alle typer",
            "desc": "Alle Ex-beskyttelsesmetoder: flammesikker kapsel (d), egensikkerhed (i), støbemasse (m), overtryk (p) og flere."
        },
        "standards": {
            "title": "Eksplosionsbeskyttelse standarder – IEC",
            "desc": "Oversigt over de vigtigste standarder i eksplosionsbeskyttelse: IEC 60079-serien, EN-standarder og anvendelsesområder."
        },
        "temperature-classes": {
            "title": "Temperaturklasser T1–T6 i Ex-beskyttelse",
            "desc": "Temperaturklasser T1 til T6 forklaret: maksimale overfladetemperaturer, tilhørende gasser og betydning for udstyrvalg."
        },
        "zone-classification": {
            "title": "Zoneklassificering – Zone 0, 1, 2, 20–22",
            "desc": "Zoneklassificering for gas og støv: zone 0/1/2 og zone 20/21/22 efter IEC 60079-10. Definitioner, eksempler og metodik."
        },
        "atex-equipment-categories": {
            "title": "ATEX-udstyrskategorier 1, 2 og 3",
            "desc": "ATEX-kategorier M1/M2, 1/2/3: beskyttelsesniveauer, tilladte zoner og krav til overensstemmelsesvurdering efter 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-regler (UK) – Oversigt",
            "desc": "Britisk DSEAR-regulering for eksplosionsbeskyttelse: arbejdsgiverens forpligtelser, risikovurdering og forskelle fra europæisk ATEX 153."
        },
    },
    "fi": {
        "index": {
            "title": "ATEX & Ex-suojaus tietopankki – ExKnowledge",
            "desc": "Käytännön tietoa ATEX:sta, IECEx:stä ja räjähdyssuojauksesta. Vyöhykeluokitus, suojausmenetelmät, laiteluokat ja standardit selkeästi selitettynä."
        },
        "atex-directive": {
            "title": "ATEX-direktiivi 2014/34/EU – Opas",
            "desc": "ATEX-laitedirektiivi selkeästi selitettynä: soveltamisala, vaatimustenmukaisuuden arviointi, CE-merkintä ja valmistajan velvollisuudet."
        },
        "atex-for-beginners": {
            "title": "ATEX aloittelijoille – Selkeä johdanto",
            "desc": "ATEX-perusteet ymmärrettävästi: vyöhykkeet, laiteluokat, Ex-merkinnät ja suojauskonseptit. Täydellinen lähtökohta räjähdyssuojaukseen."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Erot selitettynä",
            "desc": "ATEX ja IECEx vertailussa: maantieteellinen soveltamisala, oikeudellinen perusta, merkintäerot ja sertifiointiprosessit."
        },
        "cable-glands-hazardous-areas": {
            "title": "Ex-kaapeliläpiviennit – Tyypit ja valinta",
            "desc": "Kaapeliläpiviennit Ex-alueille: paineenkestävät (Ex d), korotettu turvallisuus (Ex e) ja estetyypit. Kierrestandardit ja IP-luokat."
        },
        "compex-certification": {
            "title": "CompEx-sertifiointi – Moduulit ja ura",
            "desc": "Kaikki CompEx:stä: moduulit Ex01–Ex14, koulutusvaatimukset, voimassaolo, uusinta ja urahyödyt räjähdysvaarallisten tilojen työhön."
        },
        "dust-explosion-protection": {
            "title": "Pölyräjähdyssuojaus – Vyöhykkeet ja toimet",
            "desc": "Suojautuminen pölyräjähdyksiltä: palavat pölyt, vyöhykeluokitus 20/21/22, syttymislähteet ja laitevalinta IEC 60079-10-2 mukaan."
        },
        "ex-equipment-selection-guide": {
            "title": "Ex-laitteiden valinta – Käytännön opas",
            "desc": "Oikea Ex-laite askel askeleelta: päätöskaaviot, vyöhyke-luokka-yhteys ja suojausmenetelmien vertailu eri käyttökohteisiin."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Paineenkestävä vai luontaisesti turvallinen?",
            "desc": "Paineenkestävä kotelointi (Ex d) ja luontainen turvallisuus (Ex i) teknisessä vertailussa: toimintaperiaatteet ja valintakriteerit."
        },
        "hazardous-area-classification": {
            "title": "Räjähdysvaarallisten tilojen luokitus",
            "desc": "Näin Ex-tilat luokitellaan vyöhykkeisiin: menetelmä, päästölähteet, ilmanvaihtoarviointi ja dokumentointivaatimukset IEC 60079-10 mukaan."
        },
        "how-to-read-atex-nameplate": {
            "title": "ATEX-tyyppikilven lukeminen – Opas",
            "desc": "Opi tulkitsemaan ATEX-tyyppikilpiä: CE-merkintä, laiteluokat, Ex-merkinnät, lämpötilaluokat ja erityisehdot todellisilla esimerkeillä."
        },
        "hydrogen-explosion-protection": {
            "title": "Vetyräjähdyssuojaus – IIC-laitteet",
            "desc": "Vety vaatii erityistä räjähdyssuojausta: laaja syttymisalue ja matala syttymisenergia. Opas IIC-hyväksyttyjen laitteiden valintaan."
        },
        "certification": {
            "title": "Ex-sertifiointi – ATEX ja IECEx prosessit",
            "desc": "Katsaus Ex-sertifiointiin ATEX:n ja IECEx:n mukaan: testauslaitokset, tyyppikoe, laadunvarmistus ja vaatimustenmukaisuuden arviointi."
        },
        "cheat-sheet": {
            "title": "ATEX-muistilista – Pikaopas",
            "desc": "ATEX ja Ex-suojaus yhdellä sivulla: vyöhykkeet, luokat, lämpötilaluokat ja suojausmenetelmät kätevästi pikaoppaana."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Opas",
            "desc": "Equipment Protection Levels IEC 60079-0 mukaan: Ga/Gb/Gc, Da/Db/Dc ja Ma/Mb. Yhteys ATEX-luokkiin ja vyöhykkeisiin."
        },
        "ex-markings": {
            "title": "Ex-merkinnät – Tulkintaopas",
            "desc": "Ymmärrä Ex-merkinnät: suojausmenetelmät, kaasuryhmät, lämpötilaluokat ja EPL. Opas Ex-laitteiden merkintöjen lukemiseen."
        },
        "faq": {
            "title": "Usein kysytyt kysymykset – ATEX ja Ex",
            "desc": "Vastaukset yleisimpiin kysymyksiin ATEX:sta, IECEx:stä, vyöhykeluokituksesta, suojausmenetelmistä ja Ex-merkinnöistä."
        },
        "fundamentals": {
            "title": "Räjähdyssuojauksen perusteet",
            "desc": "Räjähdyssuojauksen perusteet: räjähdyskolmio, syttymislähteet, suojausperiaatteet ja vyöhykkeiden, luokkien ja menetelmien yhteys."
        },
        "gas-groups": {
            "title": "Kaasuryhmät IIA, IIB, IIC – Katsaus",
            "desc": "Kaasuryhmät räjähdyssuojauksessa: IIA, IIB ja IIC IEC 60079-20-1 mukaan. Luokitus, rakoleveydet ja tyypilliset kaasut."
        },
        "installation-inspection": {
            "title": "Ex-asennus ja tarkastus – Vaatimukset",
            "desc": "Vaatimukset Ex-laitteistojen asennukselle ja tarkastukselle: IEC 60079-14/17, alkutarkastus, määräaikaistarkastukset ja dokumentointi."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Vertailu",
            "desc": "Pohjoisamerikkalainen NEC 500/505 ja eurooppalainen ATEX/IEC vertailussa: Divisions vs. vyöhykkeet ja suojausmenetelmät."
        },
        "protection-methods": {
            "title": "Ex-suojausmenetelmät – Kaikki tyypit",
            "desc": "Kaikki Ex-suojausmenetelmät: paineenkestävä kotelointi (d), luontainen turvallisuus (i), valumassa (m), ylipaineistus (p) ja muut."
        },
        "standards": {
            "title": "Räjähdyssuojausstandardit – IEC 60079",
            "desc": "Katsaus räjähdyssuojauksen tärkeimpiin standardeihin: IEC 60079-sarja, EN-standardit ja niiden soveltamisalueet."
        },
        "temperature-classes": {
            "title": "Lämpötilaluokat T1–T6 Ex-suojauksessa",
            "desc": "Lämpötilaluokat T1–T6 selitettynä: pintalämpötilat, kaasut ja merkitys laitevalinnassa räjähdysvaarallisissa tiloissa."
        },
        "zone-classification": {
            "title": "Vyöhykeluokitus – Vyöhyke 0, 1, 2, 20–22",
            "desc": "Vyöhykeluokitus kaasuille ja pölyille: vyöhyke 0/1/2 ja vyöhyke 20/21/22 IEC 60079-10 mukaan. Määritelmät ja esimerkit."
        },
        "atex-equipment-categories": {
            "title": "ATEX-laiteluokat 1, 2 ja 3",
            "desc": "ATEX-laiteluokat M1/M2, 1/2/3: suojaustasot, sallitut vyöhykkeet ja vaatimustenmukaisuuden arviointivaatimukset 2014/34/EU mukaan."
        },
        "dsear-regulations-uk": {
            "title": "DSEAR-sääntely (UK) – Yleiskatsaus",
            "desc": "Iso-Britannian DSEAR-sääntely räjähdyssuojauksessa: työnantajan velvollisuudet, riskinarviointi ja erot eurooppalaiseen ATEX 153."
        },
    },
    "pt": {
        "index": {
            "title": "Base de conhecimento ATEX e Ex – ExKnowledge",
            "desc": "Conhecimento prático sobre ATEX, IECEx e proteção contra explosões. Zonas, métodos de proteção, categorias de equipamentos e normas explicadas."
        },
        "atex-directive": {
            "title": "Diretiva ATEX 2014/34/UE – Guia completo",
            "desc": "A diretiva ATEX de equipamentos explicada: âmbito, avaliação de conformidade, marcação CE e obrigações do fabricante de equipamentos Ex."
        },
        "atex-for-beginners": {
            "title": "ATEX para iniciantes – Guia básico",
            "desc": "Conceitos básicos de ATEX em português: zonas, categorias de equipamentos, marcação Ex e princípios de proteção. Seu primeiro passo."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Diferenças explicadas",
            "desc": "ATEX e IECEx comparados: âmbito geográfico, base legal, diferenças de marcação e processos de certificação. Qual norma se aplica?"
        },
        "cable-glands-hazardous-areas": {
            "title": "Prensa-cabos Ex – Tipos e seleção",
            "desc": "Prensa-cabos para áreas Ex: à prova de explosão (Ex d), segurança aumentada (Ex e) e barreira. Roscas, IP e erros comuns."
        },
        "compex-certification": {
            "title": "Certificação CompEx – Módulos e carreira",
            "desc": "Tudo sobre CompEx: módulos Ex01–Ex14, requisitos de formação, validade, renovação e benefícios profissionais para áreas perigosas."
        },
        "dust-explosion-protection": {
            "title": "Proteção contra explosões de poeira",
            "desc": "Proteção contra explosões de poeira: tipos de poeira combustível, zonas 20/21/22, fontes de ignição e seleção de equipamentos por IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Seleção de equipamentos Ex – Guia prático",
            "desc": "Como escolher equipamentos Ex passo a passo: fluxogramas de decisão, relação zona-categoria e comparação de métodos de proteção."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – À prova de explosão ou seguro?",
            "desc": "Invólucro à prova de explosão (Ex d) e segurança intrínseca (Ex i) em comparação técnica: princípios, aplicações e critérios de escolha."
        },
        "hazardous-area-classification": {
            "title": "Classificação de áreas perigosas – Guia",
            "desc": "Como áreas perigosas são classificadas em zonas: metodologia, fontes de emissão, ventilação e documentação conforme IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Ler placa ATEX – Guia de decodificação",
            "desc": "Aprenda a interpretar placas ATEX: marcação CE, categorias, marcação Ex, classes de temperatura e condições especiais com exemplos."
        },
        "hydrogen-explosion-protection": {
            "title": "Proteção contra explosão de hidrogénio",
            "desc": "O hidrogénio exige proteção especial: ampla faixa de inflamabilidade e baixa energia de ignição. Guia para seleção de equipamentos IIC."
        },
        "certification": {
            "title": "Certificação Ex – Processos ATEX e IECEx",
            "desc": "Visão geral da certificação Ex segundo ATEX e IECEx: organismos de certificação, ensaio de tipo e avaliação da conformidade."
        },
        "cheat-sheet": {
            "title": "Folha de consulta ATEX – Referência rápida",
            "desc": "ATEX e proteção Ex numa página: zonas, categorias, classes de temperatura e métodos de proteção como referência prática."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Guia",
            "desc": "Equipment Protection Levels conforme IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc e Ma/Mb. Relação com categorias ATEX e zonas."
        },
        "ex-markings": {
            "title": "Marcação Ex – Como interpretar",
            "desc": "Entenda a marcação Ex: métodos de proteção, grupos de gás, classes de temperatura e EPL. Como ler a marcação em equipamentos Ex."
        },
        "faq": {
            "title": "Perguntas frequentes sobre ATEX e Ex",
            "desc": "Respostas às perguntas mais comuns sobre ATEX, IECEx, classificação de zonas, métodos de proteção e marcação Ex."
        },
        "fundamentals": {
            "title": "Fundamentos da proteção contra explosões",
            "desc": "Base da proteção contra explosões: triângulo da explosão, fontes de ignição, princípios de proteção e relação zonas-categorias."
        },
        "gas-groups": {
            "title": "Grupos de gás IIA, IIB, IIC – Visão geral",
            "desc": "Grupos de gás na proteção contra explosões: IIA, IIB e IIC conforme IEC 60079-20-1. Classificação, interstícios e gases típicos."
        },
        "installation-inspection": {
            "title": "Instalação e inspeção Ex – Requisitos",
            "desc": "Requisitos para instalação e inspeção de equipamentos Ex: IEC 60079-14/17, verificação inicial, inspeções periódicas e documentação."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Comparação",
            "desc": "Sistema norte-americano NEC 500/505 e europeu ATEX/IEC comparados: Divisions vs. zonas, métodos de proteção e reconhecimento mútuo."
        },
        "protection-methods": {
            "title": "Métodos de proteção Ex – Todos os tipos",
            "desc": "Todos os métodos de proteção Ex: invólucro à prova de explosão (d), segurança intrínseca (i), encapsulamento (m), pressurização (p) e mais."
        },
        "standards": {
            "title": "Normas de proteção contra explosões – IEC",
            "desc": "Visão geral das principais normas de proteção contra explosões: série IEC 60079, normas EN e seus âmbitos de aplicação."
        },
        "temperature-classes": {
            "title": "Classes de temperatura T1–T6 em Ex",
            "desc": "Classes de temperatura T1 a T6 explicadas: temperaturas máximas de superfície, gases associados e importância na seleção de equipamentos."
        },
        "zone-classification": {
            "title": "Classificação de zonas – 0, 1, 2, 20–22",
            "desc": "Classificação de zonas para gás e poeira: zona 0/1/2 e zona 20/21/22 conforme IEC 60079-10. Definições, exemplos e metodologia."
        },
        "atex-equipment-categories": {
            "title": "Categorias de equipamentos ATEX – 1, 2, 3",
            "desc": "Categorias ATEX M1/M2, 1/2/3: níveis de proteção, zonas permitidas e requisitos de avaliação da conformidade per 2014/34/UE."
        },
        "dsear-regulations-uk": {
            "title": "Regulamento DSEAR (Reino Unido) – Resumo",
            "desc": "Regulamento DSEAR britânico para proteção contra explosões: obrigações do empregador, avaliação de riscos e diferenças da ATEX 153."
        },
    },
    "it": {
        "index": {
            "title": "Base di conoscenza ATEX e Ex – ExKnowledge",
            "desc": "Conoscenza pratica su ATEX, IECEx e protezione antiesplosione. Zone, metodi di protezione, categorie di apparecchiature e normative spiegate."
        },
        "atex-directive": {
            "title": "Direttiva ATEX 2014/34/UE – Guida completa",
            "desc": "La direttiva ATEX sulle apparecchiature spiegata: campo di applicazione, valutazione di conformità, marcatura CE e obblighi del fabbricante."
        },
        "atex-for-beginners": {
            "title": "ATEX per principianti – Guida semplice",
            "desc": "Le basi di ATEX in italiano: zone, categorie di apparecchiature, marcatura Ex e concetti di protezione. Il punto di partenza ideale."
        },
        "atex-vs-iecex": {
            "title": "ATEX vs. IECEx – Differenze a confronto",
            "desc": "ATEX e IECEx a confronto: ambito geografico, base giuridica, marcatura e certificazione. Scopri quando si applica ciascuna norma."
        },
        "cable-glands-hazardous-areas": {
            "title": "Pressacavi Ex – Tipologie e scelta",
            "desc": "Pressacavi per zone Ex: antideflagranti (Ex d), sicurezza aumentata (Ex e) e a barriera. Filettature, IP e errori comuni da evitare."
        },
        "compex-certification": {
            "title": "Certificazione CompEx – Moduli e carriera",
            "desc": "Tutto su CompEx: moduli Ex01–Ex14, requisiti di formazione, validità, rinnovo e vantaggi professionali per il lavoro in aree pericolose."
        },
        "dust-explosion-protection": {
            "title": "Protezione esplosioni polveri – Zone e misure",
            "desc": "Protezione contro esplosioni di polveri: polveri combustibili, zone 20/21/22, sorgenti di innesco e scelta apparecchiature per IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "Scelta apparecchiature Ex – Guida pratica",
            "desc": "Come scegliere le apparecchiature Ex passo dopo passo: diagrammi decisionali, rapporto zona-categoria e confronto metodi di protezione."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d vs. Ex i – Antideflagrante o sicurezza?",
            "desc": "Custodia antideflagrante (Ex d) e sicurezza intrinseca (Ex i) a confronto tecnico: principi, applicazioni e criteri di scelta."
        },
        "hazardous-area-classification": {
            "title": "Classificazione aree pericolose – Guida",
            "desc": "Come vengono classificate le aree pericolose in zone: metodologia, sorgenti di emissione, ventilazione e documentazione per IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "Leggere la targhetta ATEX – Guida completa",
            "desc": "Impara a interpretare le targhette ATEX: marcatura CE, categorie, marcatura Ex, classi di temperatura e condizioni speciali con esempi."
        },
        "hydrogen-explosion-protection": {
            "title": "Protezione antiesplosione per idrogeno – IIC",
            "desc": "L'idrogeno richiede protezione speciale: ampio campo di infiammabilità e bassa energia di innesco. Guida alla scelta di apparecchiature IIC."
        },
        "certification": {
            "title": "Certificazione Ex – Processi ATEX e IECEx",
            "desc": "Panoramica della certificazione Ex secondo ATEX e IECEx: enti notificati, esame di tipo, garanzia qualità e valutazione di conformità."
        },
        "cheat-sheet": {
            "title": "Scheda rapida ATEX – Riferimento veloce",
            "desc": "ATEX e protezione Ex in una pagina: zone, categorie, classi di temperatura e metodi di protezione come pratico riferimento rapido."
        },
        "epl": {
            "title": "Equipment Protection Level (EPL) – Guida",
            "desc": "Equipment Protection Levels secondo IEC 60079-0: Ga/Gb/Gc, Da/Db/Dc e Ma/Mb. Relazione con categorie ATEX e zone."
        },
        "ex-markings": {
            "title": "Marcatura Ex – Come interpretarla",
            "desc": "Comprendere la marcatura Ex: metodi di protezione, gruppi gas, classi di temperatura e EPL. Come leggere la marcatura Ex correttamente."
        },
        "faq": {
            "title": "Domande frequenti su ATEX e protezione Ex",
            "desc": "Risposte alle domande più frequenti su ATEX, IECEx, classificazione zone, metodi di protezione e marcatura Ex."
        },
        "fundamentals": {
            "title": "Fondamenti di protezione antiesplosione",
            "desc": "Le basi della protezione antiesplosione: triangolo dell'esplosione, sorgenti di innesco, principi di protezione e relazione zone-categorie."
        },
        "gas-groups": {
            "title": "Gruppi gas IIA, IIB, IIC – Panoramica",
            "desc": "Gruppi gas nella protezione antiesplosione: IIA, IIB e IIC secondo IEC 60079-20-1. Classificazione, interstizi e gas tipici."
        },
        "installation-inspection": {
            "title": "Installazione e ispezione Ex – Requisiti",
            "desc": "Requisiti per installazione e ispezione di impianti Ex: IEC 60079-14/17, verifica iniziale, ispezioni periodiche e documentazione."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 vs. ATEX/IEC – Confronto",
            "desc": "Sistema nordamericano NEC 500/505 e europeo ATEX/IEC a confronto: Divisions vs. zone, metodi di protezione e riconoscimento reciproco."
        },
        "protection-methods": {
            "title": "Metodi di protezione Ex – Tutti i tipi",
            "desc": "Tutti i metodi di protezione Ex: custodia antideflagrante (d), sicurezza intrinseca (i), incapsulamento (m), pressurizzazione (p) e altri."
        },
        "standards": {
            "title": "Norme protezione antiesplosione – IEC 60079",
            "desc": "Panoramica delle principali norme di protezione antiesplosione: serie IEC 60079, norme EN e relativi ambiti di applicazione."
        },
        "temperature-classes": {
            "title": "Classi di temperatura T1–T6 in Ex",
            "desc": "Classi di temperatura T1–T6 spiegate: temperature superficiali massime, gas associati e importanza nella scelta delle apparecchiature."
        },
        "zone-classification": {
            "title": "Classificazione zone – 0, 1, 2, 20–22",
            "desc": "Classificazione zone per gas e polveri: zona 0/1/2 e zona 20/21/22 secondo IEC 60079-10. Definizioni, esempi e metodologia."
        },
        "atex-equipment-categories": {
            "title": "Categorie apparecchiature ATEX – 1, 2, 3",
            "desc": "Categorie ATEX M1/M2, 1/2/3: livelli di protezione, zone ammesse e requisiti di valutazione conformità secondo 2014/34/UE."
        },
        "dsear-regulations-uk": {
            "title": "Normativa DSEAR (UK) – Sintesi",
            "desc": "Normativa britannica DSEAR per la protezione antiesplosione: obblighi del datore di lavoro, valutazione rischi e differenze con ATEX 153."
        },
    },
    "ar": {
        "index": {
            "title": "قاعدة معرفة ATEX والحماية من الانفجار – ExKnowledge",
            "desc": "معرفة عملية حول ATEX وIECEx والحماية من الانفجار. تصنيف المناطق وطرق الحماية وفئات المعدات والمعايير موضحة بشكل مبسط."
        },
        "atex-directive": {
            "title": "توجيه ATEX 2014/34/EU – دليل شامل",
            "desc": "شرح توجيه معدات ATEX: النطاق وتقييم المطابقة وعلامة CE والتزامات المصنّع للمعدات المستخدمة في الأجواء المتفجرة."
        },
        "atex-for-beginners": {
            "title": "ATEX للمبتدئين – مقدمة مبسطة",
            "desc": "أساسيات ATEX بلغة واضحة: المناطق وفئات المعدات وعلامات Ex ومبادئ الحماية. نقطة البداية المثالية في عالم الحماية من الانفجار."
        },
        "atex-vs-iecex": {
            "title": "ATEX مقابل IECEx – أبرز الفروقات",
            "desc": "مقارنة ATEX وIECEx: النطاق الجغرافي والأساس القانوني واختلافات العلامات وعمليات التصديق. متى يُطبَّق كل معيار؟"
        },
        "cable-glands-hazardous-areas": {
            "title": "وصلات الكابلات Ex – الأنواع والاختيار",
            "desc": "وصلات كابلات للمناطق الخطرة: مقاومة اللهب (Ex d) وأمان مُعزَّز (Ex e) وحاجز. معايير اللولب وتصنيف IP والأخطاء الشائعة."
        },
        "compex-certification": {
            "title": "شهادة CompEx – الوحدات والمسار المهني",
            "desc": "كل ما تحتاجه عن CompEx: الوحدات Ex01–Ex14 ومتطلبات التدريب والصلاحية والتجديد والمزايا المهنية للعمل في المناطق الخطرة."
        },
        "dust-explosion-protection": {
            "title": "الحماية من انفجارات الغبار – المناطق والتدابير",
            "desc": "الوقاية من انفجارات الغبار: أنواع الغبار القابل للاشتعال وتصنيف المناطق 20/21/22 ومصادر الاشتعال واختيار المعدات وفق IEC 60079-10-2."
        },
        "ex-equipment-selection-guide": {
            "title": "دليل اختيار معدات Ex – دليل عملي",
            "desc": "اختيار معدات Ex خطوة بخطوة: مخططات القرار وربط المنطقة بالفئة ومقارنة طرق الحماية والتوصيات حسب التطبيق."
        },
        "explosion-proof-vs-intrinsically-safe": {
            "title": "Ex d مقابل Ex i – مقاوم للانفجار أم آمن جوهرياً؟",
            "desc": "الغلاف المقاوم للانفجار (Ex d) والأمان الجوهري (Ex i) في مقارنة تقنية: المبادئ والتطبيقات ومعايير الاختيار."
        },
        "hazardous-area-classification": {
            "title": "تصنيف المناطق الخطرة – دليل شامل",
            "desc": "كيف تُصنَّف المناطق الخطرة إلى مناطق: المنهجية ومصادر الانبعاث وتقييم التهوية ومتطلبات التوثيق وفق IEC 60079-10."
        },
        "how-to-read-atex-nameplate": {
            "title": "قراءة لوحة ATEX – دليل فك الرموز",
            "desc": "تعلَّم قراءة لوحات ATEX خطوة بخطوة: علامة CE والفئات وعلامات Ex ودرجات الحرارة والشروط الخاصة مع أمثلة واقعية."
        },
        "hydrogen-explosion-protection": {
            "title": "حماية انفجار الهيدروجين – معدات IIC",
            "desc": "الهيدروجين يتطلب حماية خاصة: نطاق اشتعال واسع وطاقة إشعال منخفضة. دليل اختيار المعدات المعتمدة IIC."
        },
        "certification": {
            "title": "شهادة Ex – عمليات ATEX وIECEx",
            "desc": "نظرة عامة على شهادات Ex وفق ATEX وIECEx: هيئات التصديق واختبار النوع وضمان الجودة وتقييم المطابقة."
        },
        "cheat-sheet": {
            "title": "ورقة مرجعية ATEX – مرجع سريع",
            "desc": "ATEX والحماية Ex في صفحة واحدة: المناطق والفئات ودرجات الحرارة وطرق الحماية كمرجع سريع عملي."
        },
        "epl": {
            "title": "مستوى حماية المعدات (EPL) – دليل",
            "desc": "مستويات حماية المعدات وفق IEC 60079-0: Ga/Gb/Gc وDa/Db/Dc وMa/Mb. العلاقة مع فئات ATEX والمناطق."
        },
        "ex-markings": {
            "title": "علامات Ex – كيف تفسرها",
            "desc": "فهم علامات Ex: طرق الحماية ومجموعات الغاز ودرجات الحرارة وEPL. دليل قراءة العلامات على معدات Ex."
        },
        "faq": {
            "title": "أسئلة شائعة حول ATEX والحماية Ex",
            "desc": "إجابات على الأسئلة الأكثر شيوعاً حول ATEX وIECEx وتصنيف المناطق وطرق الحماية وعلامات Ex."
        },
        "fundamentals": {
            "title": "أساسيات الحماية من الانفجار",
            "desc": "أسس الحماية من الانفجار: مثلث الانفجار ومصادر الاشتعال ومبادئ الحماية والعلاقة بين المناطق والفئات والطرق."
        },
        "gas-groups": {
            "title": "مجموعات الغاز IIA وIIB وIIC – نظرة عامة",
            "desc": "مجموعات الغاز في الحماية من الانفجار: IIA وIIB وIIC وفق IEC 60079-20-1. التصنيف والفجوات والغازات النموذجية."
        },
        "installation-inspection": {
            "title": "تركيب وفحص Ex – المتطلبات",
            "desc": "متطلبات تركيب وفحص منشآت Ex: IEC 60079-14/17 والفحص الأولي والفحوصات الدورية والتوثيق."
        },
        "nec-500-vs-atex-iec": {
            "title": "NEC 500 مقابل ATEX/IEC – مقارنة",
            "desc": "النظام الأمريكي NEC 500/505 والأوروبي ATEX/IEC مقارنة: التقسيمات مقابل المناطق وطرق الحماية والاعتراف المتبادل."
        },
        "protection-methods": {
            "title": "طرق حماية Ex – جميع الأنواع",
            "desc": "جميع طرق حماية Ex: الغلاف المقاوم للانفجار (d) والأمان الجوهري (i) والتغليف (m) والضغط الزائد (p) وغيرها."
        },
        "standards": {
            "title": "معايير الحماية من الانفجار – IEC 60079",
            "desc": "نظرة عامة على أهم معايير الحماية من الانفجار: سلسلة IEC 60079 ومعايير EN ونطاقات تطبيقها."
        },
        "temperature-classes": {
            "title": "فئات الحرارة T1–T6 في حماية Ex",
            "desc": "فئات الحرارة T1 إلى T6 موضحة: الحرارة السطحية القصوى والغازات المرتبطة وأهميتها في اختيار المعدات."
        },
        "zone-classification": {
            "title": "تصنيف المناطق – 0 و1 و2 و20–22",
            "desc": "تصنيف مناطق الغاز والغبار: منطقة 0/1/2 ومنطقة 20/21/22 وفق IEC 60079-10. التعريفات والأمثلة والمنهجية."
        },
        "atex-equipment-categories": {
            "title": "فئات معدات ATEX – 1 و2 و3",
            "desc": "فئات ATEX M1/M2 و1/2/3: مستويات الحماية والمناطق المسموحة ومتطلبات تقييم المطابقة وفق 2014/34/EU."
        },
        "dsear-regulations-uk": {
            "title": "لوائح DSEAR البريطانية – نظرة عامة",
            "desc": "لوائح DSEAR البريطانية للحماية من الانفجار: التزامات صاحب العمل وتقييم المخاطر والاختلافات عن ATEX 153 الأوروبية."
        },
    },
}


def update_title_desc(filepath, new_title, new_desc):
    """Update title and meta description in an HTML file."""
    content = Path(filepath).read_text(encoding='utf-8')
    
    # Update title
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_title}</title>',
        content,
        count=1
    )
    
    # Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{new_desc}">',
        content,
        count=1
    )
    
    # Also update og:description to match
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{new_desc}">',
        content,
        count=1
    )
    
    Path(filepath).write_text(content, encoding='utf-8')


def apply_title_desc_fixes():
    """Apply all title and description fixes."""
    count = 0
    for lang, pages in TITLES_DESCRIPTIONS.items():
        for page, data in pages.items():
            if page == "index":
                filepath = BASE / lang / "index.html"
            else:
                filepath = BASE / lang / "pages" / f"{page}.html"
            
            if filepath.exists():
                update_title_desc(filepath, data["title"], data["desc"])
                count += 1
            else:
                print(f"  MISSING: {filepath}")
    print(f"Updated {count} title/description pairs")


# ========== TASK 2: FAQ SCHEMA ==========

FAQ_DATA = {
    "en": {
        "atex-directive": [
            ("What is the ATEX Directive 2014/34/EU?", "The ATEX Directive 2014/34/EU is the European regulation governing equipment and protective systems intended for use in potentially explosive atmospheres. It sets out essential health and safety requirements and conformity assessment procedures for manufacturers."),
            ("What products does the ATEX Directive cover?", "The ATEX Directive covers all equipment, protective systems, components, and devices intended for use in potentially explosive atmospheres caused by flammable gases, vapours, mists, or combustible dusts."),
            ("What are the ATEX conformity assessment modules?", "The ATEX Directive uses a modular approach to conformity assessment. The modules range from internal production control (Module A) for Category 3 equipment to full EU-type examination (Module B) combined with production quality assurance for Category 1 equipment."),
            ("Who must comply with the ATEX Directive?", "Manufacturers, authorised representatives, importers, and distributors placing equipment on the EU market for use in explosive atmospheres must comply with the ATEX Directive."),
        ],
        "atex-for-beginners": [
            ("What does ATEX stand for?", "ATEX stands for 'Atmosphères Explosibles', the French term for explosive atmospheres. It refers to the European directives that regulate equipment and workplaces where explosive atmospheres may occur."),
            ("What are hazardous area zones in ATEX?", "ATEX zones classify areas based on the likelihood of an explosive atmosphere being present. Zone 0/20 means continuously present, Zone 1/21 means likely during normal operation, and Zone 2/22 means unlikely but possible."),
            ("What are ATEX equipment categories?", "ATEX equipment categories (1, 2, and 3) indicate the level of protection. Category 1 provides the highest protection for Zone 0/20, Category 2 for Zone 1/21, and Category 3 for Zone 2/22."),
            ("Do I need ATEX certification for all electrical equipment?", "Not all equipment needs ATEX certification. Only equipment intended for use in classified hazardous areas (zones) where explosive atmospheres may occur requires ATEX-certified equipment."),
        ],
        "atex-vs-iecex": [
            ("What is the main difference between ATEX and IECEx?", "ATEX is a European Union regulatory directive with legal force in the EU/EEA, while IECEx is a voluntary international certification system used worldwide. ATEX is mandatory in Europe; IECEx facilitates global market access."),
            ("Can IECEx certification be used instead of ATEX in Europe?", "No. IECEx certification alone is not accepted in the EU. However, an IECEx certificate can simplify the ATEX certification process since both systems are based on the same IEC 60079 standards."),
            ("Which countries accept IECEx certification?", "IECEx certification is accepted in over 30 countries worldwide, including Australia, Brazil, South Korea, Singapore, and many others. Each country's national regulations determine the level of acceptance."),
            ("Do ATEX and IECEx use the same technical standards?", "Yes, both ATEX and IECEx are based on the IEC 60079 series of standards. The technical requirements are essentially the same, but the certification and marking procedures differ."),
        ],
        "cable-glands-hazardous-areas": [
            ("What types of cable glands are used in hazardous areas?", "Three main types are used: flameproof (Ex d) cable glands that contain any internal explosion, increased safety (Ex e) glands that prevent ignition-capable sparks, and barrier glands that maintain zone separation between areas."),
            ("What thread standards are used for Ex cable glands?", "The most common thread standards are M-metric (ISO), NPT (North American), and PG (German, being phased out). Thread compatibility with the enclosure is critical for maintaining the protection concept."),
            ("Why is installation torque important for Ex cable glands?", "Correct installation torque ensures the cable gland maintains its IP rating and explosion protection. Under-tightening can allow gas or dust ingress, while over-tightening can damage the gland or cable."),
            ("Can I mix different cable gland types on one enclosure?", "You can use different gland types on the same enclosure if each entry maintains the required protection level. However, the overall protection concept must remain consistent with the enclosure's certification."),
        ],
        "compex-certification": [
            ("What is CompEx certification?", "CompEx (Competency in Explosive atmospheres) is an internationally recognised training and assessment scheme that validates an individual's competence to work safely with electrical and mechanical equipment in hazardous areas."),
            ("What CompEx modules are available?", "CompEx offers modules Ex01-Ex04 for electrical installations, Ex05-Ex08 for mechanical equipment, Ex09-Ex11 for dust atmospheres, and Ex12-Ex14 for equipment overhaul and repair."),
            ("How long is CompEx certification valid?", "CompEx certification is valid for 5 years. After this period, individuals must complete a refresher course and reassessment to renew their certification."),
            ("Who needs CompEx certification?", "CompEx is typically required for electricians, instrumentation technicians, and engineers who install, inspect, or maintain equipment in explosive atmospheres, particularly in the oil and gas, chemical, and pharmaceutical industries."),
        ],
        "dust-explosion-protection": [
            ("What causes a dust explosion?", "A dust explosion occurs when five elements combine: combustible dust particles, oxygen, an ignition source, dispersion of dust in air forming a cloud, and confinement of the dust cloud. This is known as the dust explosion pentagon."),
            ("What are Zone 20, 21, and 22?", "Zone 20 is where combustible dust clouds are continuously present, Zone 21 is where they are likely during normal operation, and Zone 22 is where they are unlikely but may occur briefly. These zones determine the required equipment protection level."),
            ("What types of dust can cause explosions?", "Many types of dust can cause explosions, including metal dusts (aluminium, magnesium), organic dusts (flour, sugar, wood), chemical dusts (pharmaceuticals, plastics), and even food dusts like coffee and spices."),
            ("How are dust explosions prevented?", "Prevention strategies include eliminating ignition sources, controlling dust concentrations, using proper housekeeping to prevent dust accumulation, employing explosion venting or suppression systems, and selecting appropriate Ex-rated equipment."),
        ],
        "ex-equipment-selection-guide": [
            ("How do I choose the right Ex protection method?", "Start with the zone classification, then identify the equipment category needed. Consider the substance (gas/dust), operating conditions, maintenance requirements, and cost. Each protection concept has strengths for different applications."),
            ("What ATEX category do I need for Zone 1?", "Zone 1 requires at minimum Category 2 equipment. Category 1 equipment can also be used in Zone 1 as it provides a higher level of protection, but it's typically more expensive."),
            ("Can I use Zone 2 equipment in Zone 1?", "No. Category 3 equipment (designed for Zone 2) does not provide sufficient protection for Zone 1. Using equipment in a zone with higher risk than it's rated for is dangerous and non-compliant."),
            ("What factors affect Ex equipment selection?", "Key factors include zone classification, gas group or dust characteristics, temperature class, ambient conditions, IP rating requirements, mechanical strength, maintenance access, and the specific application requirements."),
        ],
        "explosion-proof-vs-intrinsically-safe": [
            ("What is the difference between explosion proof and intrinsically safe?", "Explosion proof (Ex d) works by containing any internal explosion within a robust enclosure and cooling escaping gases. Intrinsically safe (Ex i) works by limiting electrical energy so it can never cause ignition. They are fundamentally different protection philosophies."),
            ("When should I use Ex d (flameproof) equipment?", "Use Ex d equipment for high-power applications like motors, lighting, and junction boxes in Zone 1 or 2 areas. It's suitable when equipment needs significant electrical power that cannot be limited to intrinsically safe levels."),
            ("When should I use Ex i (intrinsically safe) equipment?", "Use Ex i for low-power instrumentation, sensors, and portable devices. It's ideal for Zone 0 applications (Ex ia), live maintenance scenarios, and where lightweight equipment is needed."),
            ("Can I combine Ex d and Ex i in one system?", "Yes, combined protection is common. For example, an intrinsically safe field instrument in a hazardous area can be connected via an IS barrier to standard equipment in the safe area."),
        ],
        "hazardous-area-classification": [
            ("What is hazardous area classification?", "Hazardous area classification is the process of identifying and documenting areas where explosive gas or dust atmospheres may occur, then assigning appropriate zones based on the likelihood and duration of the hazardous atmosphere."),
            ("Who is responsible for hazardous area classification?", "The site operator or employer is responsible for having the classification carried out. It should be performed by competent persons with knowledge of the process, materials, and relevant standards (IEC 60079-10)."),
            ("What determines the extent of a zone?", "Zone extent depends on the source of release characteristics, ventilation conditions (natural or artificial), the properties of the flammable material, and any physical barriers that confine the hazardous atmosphere."),
            ("How often should hazardous area classification be reviewed?", "Classification should be reviewed whenever there are process changes, equipment modifications, ventilation changes, or changes to the materials handled. Regular periodic reviews are also good practice."),
        ],
        "how-to-read-atex-nameplate": [
            ("What information is on an ATEX nameplate?", "An ATEX nameplate shows the CE marking, notified body number, ATEX marking (Ex symbol in hexagon), equipment group and category, gas/dust suitability, protection concept codes, gas group, and temperature class."),
            ("What does the hexagon Ex symbol mean?", "The hexagon with 'Ex' inside (the epsilon-x mark) indicates that the equipment is certified for use in explosive atmospheres. It appears on all ATEX-certified equipment."),
            ("How do I identify the temperature class on a nameplate?", "The temperature class (T1 to T6) appears after the gas group designation. T6 has the lowest maximum surface temperature (85°C) and is suitable for the most sensitive gases, while T1 allows the highest (450°C)."),
            ("What are special conditions marked with 'X' on a nameplate?", "An 'X' suffix on the certificate number indicates special conditions for safe use. These conditions are detailed in the certificate and may include restrictions on installation, ambient temperature, or specific maintenance requirements."),
        ],
        "hydrogen-explosion-protection": [
            ("Why is hydrogen especially dangerous?", "Hydrogen has an extremely wide flammable range (4-75% in air), very low minimum ignition energy (0.017 mJ), high flame speed, and is invisible and odourless. These properties make it exceptionally challenging for explosion protection."),
            ("What equipment rating is needed for hydrogen?", "Hydrogen falls in Gas Group IIC, the most demanding category. Only equipment specifically rated for IIC (or equivalent) should be used. IIA or IIB rated equipment is not suitable for hydrogen atmospheres."),
            ("Can Ex d (flameproof) equipment be used with hydrogen?", "Yes, but it must be specifically certified for IIC gases. IIC flameproof enclosures have tighter flamepath tolerances than IIA or IIB designs. Not all Ex d equipment is suitable for hydrogen."),
            ("What protection methods work best for hydrogen?", "Intrinsic safety (Ex i) with IIC rating is ideal for instrumentation. For higher power, Ex d IIC or Ex p (pressurised) enclosures are used. Increased safety (Ex e) is also used for junction boxes and terminals in hydrogen areas."),
        ],
    },
    "de": {
        "atex-directive": [
            ("Was ist die ATEX-Richtlinie 2014/34/EU?", "Die ATEX-Richtlinie 2014/34/EU ist die europäische Verordnung für Geräte und Schutzsysteme zur Verwendung in explosionsgefährdeten Bereichen. Sie legt Sicherheitsanforderungen und Konformitätsbewertungsverfahren für Hersteller fest."),
            ("Welche Produkte fallen unter die ATEX-Richtlinie?", "Die ATEX-Richtlinie umfasst alle Geräte, Schutzsysteme, Komponenten und Vorrichtungen für den Einsatz in explosionsfähigen Atmosphären durch brennbare Gase, Dämpfe, Nebel oder Stäube."),
            ("Was sind die Konformitätsbewertungsmodule der ATEX-Richtlinie?", "Die ATEX-Richtlinie nutzt einen modularen Ansatz: Von der internen Fertigungskontrolle (Modul A) für Kategorie 3 bis zur EU-Baumusterprüfung (Modul B) mit Qualitätssicherung für Kategorie 1."),
            ("Wer muss die ATEX-Richtlinie einhalten?", "Hersteller, Bevollmächtigte, Importeure und Händler, die Geräte für den Einsatz in explosionsgefährdeten Bereichen auf dem EU-Markt anbieten, müssen die ATEX-Richtlinie einhalten."),
        ],
        "atex-for-beginners": [
            ("Wofür steht ATEX?", "ATEX steht für ‚Atmosphères Explosibles', den französischen Begriff für explosionsfähige Atmosphären. Es bezeichnet die europäischen Richtlinien für Geräte und Arbeitsplätze, an denen explosive Atmosphären auftreten können."),
            ("Was sind die ATEX-Zonen?", "ATEX-Zonen klassifizieren Bereiche nach der Wahrscheinlichkeit einer explosionsfähigen Atmosphäre. Zone 0/20 bedeutet ständig vorhanden, Zone 1/21 gelegentlich im Normalbetrieb, Zone 2/22 selten und kurzzeitig."),
            ("Was sind ATEX-Gerätekategorien?", "ATEX-Gerätekategorien (1, 2 und 3) geben das Schutzniveau an. Kategorie 1 bietet den höchsten Schutz für Zone 0/20, Kategorie 2 für Zone 1/21 und Kategorie 3 für Zone 2/22."),
            ("Braucht jedes elektrische Gerät eine ATEX-Zertifizierung?", "Nein. Nur Geräte, die in klassifizierten explosionsgefährdeten Bereichen (Zonen) eingesetzt werden sollen, benötigen eine ATEX-Zertifizierung."),
        ],
        "atex-vs-iecex": [
            ("Was ist der Hauptunterschied zwischen ATEX und IECEx?", "ATEX ist eine EU-Richtlinie mit Gesetzeskraft im EWR, während IECEx ein freiwilliges internationales Zertifizierungssystem ist. ATEX ist in Europa Pflicht, IECEx erleichtert den weltweiten Marktzugang."),
            ("Kann eine IECEx-Zertifizierung ATEX in Europa ersetzen?", "Nein. Eine IECEx-Zertifizierung allein wird in der EU nicht akzeptiert. Sie kann jedoch den ATEX-Zertifizierungsprozess vereinfachen, da beide auf den gleichen IEC 60079-Normen basieren."),
            ("Verwenden ATEX und IECEx die gleichen Normen?", "Ja, beide basieren auf der IEC 60079-Normenreihe. Die technischen Anforderungen sind praktisch identisch, nur die Zertifizierungs- und Kennzeichnungsverfahren unterscheiden sich."),
            ("Welche Länder akzeptieren IECEx?", "IECEx wird in über 30 Ländern weltweit akzeptiert, darunter Australien, Brasilien, Südkorea und Singapur. Die jeweiligen nationalen Vorschriften bestimmen den Grad der Anerkennung."),
        ],
        "cable-glands-hazardous-areas": [
            ("Welche Kabelverschraubungstypen gibt es für Ex-Bereiche?", "Drei Haupttypen: Druckfeste (Ex d) Verschraubungen, die interne Explosionen einschließen; Verschraubungen mit erhöhter Sicherheit (Ex e), die zündfähige Funken verhindern; und Barriere-Verschraubungen zur Zonentrennung."),
            ("Welche Gewindestandards werden bei Ex-Verschraubungen verwendet?", "Die gängigsten Standards sind M-Metrisch (ISO), NPT (Nordamerika) und PG (deutsch, wird abgelöst). Die Gewindekompatibilität mit dem Gehäuse ist entscheidend für den Explosionsschutz."),
            ("Warum ist das richtige Anzugsdrehmoment wichtig?", "Das korrekte Drehmoment stellt sicher, dass die Verschraubung ihre IP-Schutzart und den Explosionsschutz beibehält. Zu wenig Drehmoment erlaubt Gas- oder Staubeintritt, zu viel beschädigt die Verschraubung."),
        ],
        "compex-certification": [
            ("Was ist die CompEx-Zertifizierung?", "CompEx (Competency in Explosive Atmospheres) ist ein international anerkanntes Schulungs- und Prüfprogramm, das die Kompetenz von Fachkräften für Arbeiten an elektrischen und mechanischen Geräten in explosionsgefährdeten Bereichen nachweist."),
            ("Welche CompEx-Module gibt es?", "CompEx bietet Module Ex01–Ex04 für Elektroinstallationen, Ex05–Ex08 für mechanische Geräte, Ex09–Ex11 für Staubatmosphären und Ex12–Ex14 für Geräteüberholung und -reparatur."),
            ("Wie lange gilt die CompEx-Zertifizierung?", "Die CompEx-Zertifizierung gilt 5 Jahre. Danach muss eine Auffrischungsschulung mit erneuter Prüfung absolviert werden."),
            ("Wer braucht eine CompEx-Zertifizierung?", "CompEx wird typischerweise für Elektriker, Messtechniker und Ingenieure benötigt, die Geräte in explosionsgefährdeten Bereichen installieren, prüfen oder warten – besonders in der Öl-, Gas-, Chemie- und Pharmaindustrie."),
        ],
        "dust-explosion-protection": [
            ("Was verursacht eine Staubexplosion?", "Eine Staubexplosion entsteht, wenn fünf Faktoren zusammentreffen: brennbarer Staub, Sauerstoff, eine Zündquelle, Verteilung des Staubs als Wolke in der Luft und Einschluss der Staubwolke. Dies wird als Staubexplosionsfünfeck bezeichnet."),
            ("Was bedeuten Zone 20, 21 und 22?", "Zone 20: brennbare Staubwolke ständig vorhanden. Zone 21: Staubwolke gelegentlich im Normalbetrieb wahrscheinlich. Zone 22: Staubwolke selten und nur kurzzeitig. Die Zonen bestimmen das erforderliche Schutzniveau der Geräte."),
            ("Welche Staubarten können explodieren?", "Viele Stäube können explodieren: Metallstäube (Aluminium, Magnesium), organische Stäube (Mehl, Zucker, Holz), chemische Stäube (Pharmazeutika, Kunststoffe) und sogar Lebensmittelstäube wie Kaffee und Gewürze."),
            ("Wie werden Staubexplosionen verhindert?", "Prävention umfasst: Zündquellen beseitigen, Staubkonzentrationen kontrollieren, regelmäßige Reinigung, Explosionsdruckentlastung oder -unterdrückung einsetzen und geeignete Ex-Geräte verwenden."),
        ],
        "ex-equipment-selection-guide": [
            ("Wie wähle ich die richtige Ex-Schutzart?", "Beginnen Sie mit der Zoneneinteilung, bestimmen Sie die benötigte Gerätekategorie. Berücksichtigen Sie den Stoff (Gas/Staub), Betriebsbedingungen, Wartungsanforderungen und Kosten. Jede Schutzart hat Stärken für bestimmte Anwendungen."),
            ("Welche ATEX-Kategorie brauche ich für Zone 1?", "Zone 1 erfordert mindestens Kategorie 2. Geräte der Kategorie 1 dürfen ebenfalls in Zone 1 eingesetzt werden, bieten höheren Schutz, sind jedoch in der Regel teurer."),
            ("Darf ich Zone-2-Geräte in Zone 1 verwenden?", "Nein. Geräte der Kategorie 3 (für Zone 2) bieten keinen ausreichenden Schutz für Zone 1. Der Einsatz in einer Zone mit höherem Risiko ist gefährlich und nicht zulässig."),
            ("Welche Faktoren beeinflussen die Ex-Geräteauswahl?", "Entscheidende Faktoren sind: Zoneneinteilung, Gasgruppe oder Staubeigenschaften, Temperaturklasse, Umgebungsbedingungen, IP-Anforderungen, mechanische Festigkeit und anwendungsspezifische Anforderungen."),
        ],
        "explosion-proof-vs-intrinsically-safe": [
            ("Was ist der Unterschied zwischen druckfest und eigensicher?", "Druckfeste Kapselung (Ex d) schließt eine interne Explosion in einem robusten Gehäuse ein und kühlt austretende Gase. Eigensicherheit (Ex i) begrenzt die elektrische Energie so, dass eine Zündung unmöglich ist. Grundverschiedene Schutzphilosophien."),
            ("Wann sollte ich Ex d (druckfest) verwenden?", "Ex d eignet sich für leistungsstarke Anwendungen wie Motoren, Beleuchtung und Anschlusskästen in Zone 1 oder 2. Geeignet wenn die Leistung nicht auf eigensichere Pegel begrenzt werden kann."),
            ("Wann sollte ich Ex i (eigensicher) verwenden?", "Ex i ist ideal für Messtechnik, Sensoren und tragbare Geräte mit geringer Leistung. Besonders geeignet für Zone 0 (Ex ia), Wartung unter Spannung und leichte Geräte."),
            ("Können Ex d und Ex i kombiniert werden?", "Ja, kombinierter Schutz ist üblich. Ein eigensicheres Feldgerät im Ex-Bereich kann über eine IS-Barriere mit Standardgeräten im sicheren Bereich verbunden werden."),
        ],
        "hazardous-area-classification": [
            ("Was ist die Klassifizierung explosionsgefährdeter Bereiche?", "Die Klassifizierung ist der Prozess, Bereiche mit möglichen explosionsfähigen Gas- oder Staubatmosphären zu identifizieren und entsprechende Zonen basierend auf Wahrscheinlichkeit und Dauer zuzuweisen."),
            ("Wer ist für die Zoneneinteilung verantwortlich?", "Der Anlagenbetreiber oder Arbeitgeber ist verantwortlich. Die Klassifizierung sollte von fachkundigen Personen mit Kenntnis der Prozesse, Materialien und relevanten Normen (IEC 60079-10) durchgeführt werden."),
            ("Was bestimmt die Ausdehnung einer Zone?", "Die Zonenausdehnung hängt ab von der Freisetzungsquelle, den Lüftungsbedingungen, den Eigenschaften des brennbaren Stoffs und vorhandenen physischen Barrieren."),
            ("Wie oft muss die Zoneneinteilung überprü
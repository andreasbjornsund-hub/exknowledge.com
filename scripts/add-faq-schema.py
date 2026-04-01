#!/usr/bin/env python3
"""Add FAQ schema (JSON-LD) to ExKnowledge guide pages in all languages."""

import json
import os
import re

SITE_DIR = "/tmp/exknowledge"

LANGUAGES = ["en", "de", "no", "es", "nl", "sv", "da", "fi", "pt", "it", "ar"]

# FAQ data per guide page - questions and answers in English (translated versions below)
# We'll generate language-specific Q&A for each guide
GUIDE_FAQS = {
    "atex-directive": {
        "en": [
            ("What is the ATEX Directive 2014/34/EU?", "The ATEX Directive 2014/34/EU is a European Union directive that regulates equipment and protective systems intended for use in potentially explosive atmospheres. It sets essential health and safety requirements for manufacturers."),
            ("What products does ATEX cover?", "ATEX covers all equipment, protective systems, components, and devices intended for use in explosive atmospheres, including electrical and mechanical equipment used in zones 0, 1, 2 (gas) and zones 20, 21, 22 (dust)."),
            ("What is the difference between ATEX equipment categories?", "ATEX defines three equipment categories: Category 1 for very high protection (zones 0/20), Category 2 for high protection (zones 1/21), and Category 3 for normal protection (zones 2/22). Higher categories require more rigorous conformity assessment."),
            ("Is ATEX certification mandatory in Europe?", "Yes, ATEX certification is mandatory for all equipment placed on the EU market that is intended for use in explosive atmospheres. Products must carry CE marking and meet the essential health and safety requirements of the directive."),
        ],
        "de": [
            ("Was ist die ATEX-Richtlinie 2014/34/EU?", "Die ATEX-Richtlinie 2014/34/EU ist eine EU-Richtlinie, die Geräte und Schutzsysteme für den Einsatz in explosionsgefährdeten Bereichen regelt. Sie legt grundlegende Gesundheits- und Sicherheitsanforderungen für Hersteller fest."),
            ("Welche Produkte fallen unter ATEX?", "ATEX umfasst alle Geräte, Schutzsysteme, Komponenten und Vorrichtungen für den Einsatz in explosionsfähigen Atmosphären – darunter elektrische und mechanische Geräte für die Zonen 0, 1, 2 (Gas) und 20, 21, 22 (Staub)."),
            ("Was sind die ATEX-Gerätekategorien?", "ATEX definiert drei Kategorien: Kategorie 1 für sehr hohen Schutz (Zonen 0/20), Kategorie 2 für hohen Schutz (Zonen 1/21) und Kategorie 3 für normalen Schutz (Zonen 2/22)."),
            ("Ist die ATEX-Zertifizierung in Europa Pflicht?", "Ja, die ATEX-Zertifizierung ist für alle Geräte obligatorisch, die in der EU für den Einsatz in explosionsgefährdeten Bereichen in Verkehr gebracht werden. Sie müssen die CE-Kennzeichnung tragen."),
        ],
        "no": [
            ("Hva er ATEX-direktivet 2014/34/EU?", "ATEX-direktivet 2014/34/EU er et EU-direktiv som regulerer utstyr og beskyttelsessystemer beregnet for bruk i potensielt eksplosive atmosfærer. Det fastsetter grunnleggende helse- og sikkerhetskrav for produsenter."),
            ("Hvilke produkter dekker ATEX?", "ATEX dekker alt utstyr, beskyttelsessystemer, komponenter og innretninger beregnet for bruk i eksplosive atmosfærer, inkludert elektrisk og mekanisk utstyr for sone 0, 1, 2 (gass) og sone 20, 21, 22 (støv)."),
            ("Hva er forskjellen mellom ATEX-utstyrskategorier?", "ATEX definerer tre kategorier: Kategori 1 for svært høy beskyttelse (sone 0/20), Kategori 2 for høy beskyttelse (sone 1/21) og Kategori 3 for normal beskyttelse (sone 2/22)."),
            ("Er ATEX-sertifisering obligatorisk i Europa?", "Ja, ATEX-sertifisering er obligatorisk for alt utstyr som markedsføres i EU for bruk i eksplosive atmosfærer. Produktene må ha CE-merking."),
        ],
        "es": [
            ("¿Qué es la Directiva ATEX 2014/34/UE?", "La Directiva ATEX 2014/34/UE es una directiva de la UE que regula los equipos y sistemas de protección destinados a utilizarse en atmósferas potencialmente explosivas. Establece los requisitos esenciales de salud y seguridad para los fabricantes."),
            ("¿Qué productos cubre ATEX?", "ATEX cubre todos los equipos, sistemas de protección, componentes y dispositivos destinados a utilizarse en atmósferas explosivas, incluidos equipos eléctricos y mecánicos para las zonas 0, 1, 2 (gas) y 20, 21, 22 (polvo)."),
            ("¿Cuáles son las categorías de equipos ATEX?", "ATEX define tres categorías: Categoría 1 para protección muy alta (zonas 0/20), Categoría 2 para protección alta (zonas 1/21) y Categoría 3 para protección normal (zonas 2/22)."),
            ("¿Es obligatoria la certificación ATEX en Europa?", "Sí, la certificación ATEX es obligatoria para todos los equipos comercializados en la UE destinados a atmósferas explosivas. Deben llevar el marcado CE."),
        ],
        "nl": [
            ("Wat is de ATEX-richtlijn 2014/34/EU?", "De ATEX-richtlijn 2014/34/EU is een EU-richtlijn die apparaten en beveiligingssystemen regelt voor gebruik in explosieve omgevingen. Het stelt essentiële gezondheids- en veiligheidseisen vast voor fabrikanten."),
            ("Welke producten vallen onder ATEX?", "ATEX omvat alle apparaten, beveiligingssystemen, componenten en voorzieningen voor gebruik in explosieve atmosferen, waaronder elektrische en mechanische apparatuur voor zone 0, 1, 2 (gas) en 20, 21, 22 (stof)."),
            ("Wat zijn de ATEX-apparaatcategorieën?", "ATEX definieert drie categorieën: Categorie 1 voor zeer hoge bescherming (zones 0/20), Categorie 2 voor hoge bescherming (zones 1/21) en Categorie 3 voor normale bescherming (zones 2/22)."),
            ("Is ATEX-certificering verplicht in Europa?", "Ja, ATEX-certificering is verplicht voor alle apparaten die in de EU worden verkocht voor gebruik in explosieve omgevingen. Ze moeten CE-markering dragen."),
        ],
        "sv": [
            ("Vad är ATEX-direktivet 2014/34/EU?", "ATEX-direktivet 2014/34/EU är ett EU-direktiv som reglerar utrustning och skyddssystem avsedda för användning i potentiellt explosiva atmosfärer. Det fastställer grundläggande hälso- och säkerhetskrav för tillverkare."),
            ("Vilka produkter omfattas av ATEX?", "ATEX omfattar all utrustning, skyddssystem, komponenter och anordningar för användning i explosiva atmosfärer, inklusive elektrisk och mekanisk utrustning för zon 0, 1, 2 (gas) och 20, 21, 22 (damm)."),
            ("Vilka är ATEX-utrustningskategorierna?", "ATEX definierar tre kategorier: Kategori 1 för mycket hög skydd (zon 0/20), Kategori 2 för hög skydd (zon 1/21) och Kategori 3 för normalt skydd (zon 2/22)."),
            ("Är ATEX-certifiering obligatorisk i Europa?", "Ja, ATEX-certifiering är obligatorisk för all utrustning som säljs i EU för användning i explosiva atmosfärer. De måste ha CE-märkning."),
        ],
        "da": [
            ("Hvad er ATEX-direktivet 2014/34/EU?", "ATEX-direktivet 2014/34/EU er et EU-direktiv, der regulerer udstyr og beskyttelsessystemer beregnet til brug i potentielt eksplosive atmosfærer. Det fastsætter væsentlige sundheds- og sikkerhedskrav for producenter."),
            ("Hvilke produkter dækker ATEX?", "ATEX dækker alt udstyr, beskyttelsessystemer, komponenter og anordninger til brug i eksplosive atmosfærer, herunder elektrisk og mekanisk udstyr til zone 0, 1, 2 (gas) og 20, 21, 22 (støv)."),
            ("Hvad er ATEX-udstyrskategorierne?", "ATEX definerer tre kategorier: Kategori 1 for meget høj beskyttelse (zone 0/20), Kategori 2 for høj beskyttelse (zone 1/21) og Kategori 3 for normal beskyttelse (zone 2/22)."),
            ("Er ATEX-certificering obligatorisk i Europa?", "Ja, ATEX-certificering er obligatorisk for alt udstyr, der markedsføres i EU til brug i eksplosive atmosfærer. De skal bære CE-mærkning."),
        ],
        "fi": [
            ("Mikä on ATEX-direktiivi 2014/34/EU?", "ATEX-direktiivi 2014/34/EU on EU-direktiivi, joka säätelee räjähdysvaarallisissa tiloissa käytettäväksi tarkoitettuja laitteita ja suojajärjestelmiä. Se asettaa olennaiset terveys- ja turvallisuusvaatimukset valmistajille."),
            ("Mitä tuotteita ATEX kattaa?", "ATEX kattaa kaikki räjähdysvaarallisissa tiloissa käytettävät laitteet, suojajärjestelmät, komponentit ja välineet, mukaan lukien sähkö- ja mekaaniset laitteet vyöhykkeille 0, 1, 2 (kaasu) ja 20, 21, 22 (pöly)."),
            ("Mitkä ovat ATEX-laiteluokat?", "ATEX määrittelee kolme luokkaa: Luokka 1 erittäin korkeaan suojaukseen (vyöhykkeet 0/20), Luokka 2 korkeaan suojaukseen (vyöhykkeet 1/21) ja Luokka 3 normaaliin suojaukseen (vyöhykkeet 2/22)."),
            ("Onko ATEX-sertifiointi pakollinen Euroopassa?", "Kyllä, ATEX-sertifiointi on pakollinen kaikille EU:n markkinoille saatettaville laitteille, jotka on tarkoitettu räjähdysvaarallisiin tiloihin. Tuotteissa on oltava CE-merkintä."),
        ],
        "pt": [
            ("O que é a Diretiva ATEX 2014/34/UE?", "A Diretiva ATEX 2014/34/UE é uma diretiva da UE que regula equipamentos e sistemas de proteção destinados a utilização em atmosferas potencialmente explosivas. Define requisitos essenciais de saúde e segurança para fabricantes."),
            ("Que produtos a ATEX abrange?", "A ATEX abrange todos os equipamentos, sistemas de proteção, componentes e dispositivos para utilização em atmosferas explosivas, incluindo equipamentos elétricos e mecânicos para as zonas 0, 1, 2 (gás) e 20, 21, 22 (poeira)."),
            ("Quais são as categorias de equipamentos ATEX?", "A ATEX define três categorias: Categoria 1 para proteção muito elevada (zonas 0/20), Categoria 2 para proteção elevada (zonas 1/21) e Categoria 3 para proteção normal (zonas 2/22)."),
            ("A certificação ATEX é obrigatória na Europa?", "Sim, a certificação ATEX é obrigatória para todos os equipamentos comercializados na UE destinados a atmosferas explosivas. Devem ostentar a marcação CE."),
        ],
        "it": [
            ("Cos'è la Direttiva ATEX 2014/34/UE?", "La Direttiva ATEX 2014/34/UE è una direttiva UE che regola le apparecchiature e i sistemi di protezione destinati all'uso in atmosfere potenzialmente esplosive. Stabilisce i requisiti essenziali di salute e sicurezza per i produttori."),
            ("Quali prodotti copre la direttiva ATEX?", "ATEX copre tutte le apparecchiature, i sistemi di protezione, i componenti e i dispositivi destinati all'uso in atmosfere esplosive, incluse le apparecchiature elettriche e meccaniche per le zone 0, 1, 2 (gas) e 20, 21, 22 (polvere)."),
            ("Quali sono le categorie di apparecchiature ATEX?", "ATEX definisce tre categorie: Categoria 1 per protezione molto elevata (zone 0/20), Categoria 2 per protezione elevata (zone 1/21) e Categoria 3 per protezione normale (zone 2/22)."),
            ("La certificazione ATEX è obbligatoria in Europa?", "Sì, la certificazione ATEX è obbligatoria per tutte le apparecchiature immesse sul mercato UE destinate ad atmosfere esplosive. Devono riportare la marcatura CE."),
        ],
        "ar": [
            ("ما هو توجيه ATEX 2014/34/EU؟", "توجيه ATEX 2014/34/EU هو توجيه من الاتحاد الأوروبي ينظم المعدات وأنظمة الحماية المخصصة للاستخدام في الأجواء المتفجرة المحتملة. يحدد متطلبات الصحة والسلامة الأساسية للمصنعين."),
            ("ما المنتجات التي يغطيها ATEX؟", "يغطي ATEX جميع المعدات وأنظمة الحماية والمكونات والأجهزة المخصصة للاستخدام في الأجواء المتفجرة، بما في ذلك المعدات الكهربائية والميكانيكية للمناطق 0 و1 و2 (غاز) و20 و21 و22 (غبار)."),
            ("ما هي فئات معدات ATEX؟", "يحدد ATEX ثلاث فئات: الفئة 1 للحماية العالية جداً (المناطق 0/20)، الفئة 2 للحماية العالية (المناطق 1/21)، والفئة 3 للحماية العادية (المناطق 2/22)."),
            ("هل شهادة ATEX إلزامية في أوروبا؟", "نعم، شهادة ATEX إلزامية لجميع المعدات المطروحة في سوق الاتحاد الأوروبي والمخصصة للأجواء المتفجرة. يجب أن تحمل علامة CE."),
        ],
    },
    "atex-for-beginners": {
        "en": [
            ("What does ATEX stand for?", "ATEX comes from the French 'Atmosphères Explosibles' meaning explosive atmospheres. It refers to EU directives governing equipment and workplaces in areas where explosive gas, dust, or vapor may be present."),
            ("Who needs to comply with ATEX?", "Any business operating in areas with potentially explosive atmospheres must comply with ATEX, including oil and gas, chemical plants, pharmaceutical manufacturing, grain handling, and mining operations."),
            ("What are ATEX zones?", "ATEX zones classify hazardous areas by how often an explosive atmosphere occurs. Zone 0/20 is continuous risk, Zone 1/21 is likely during normal operation, and Zone 2/22 is unlikely but possible."),
        ],
        "de": [
            ("Wofür steht ATEX?", "ATEX stammt vom französischen 'Atmosphères Explosibles' und bedeutet explosionsfähige Atmosphären. Es bezieht sich auf EU-Richtlinien für Geräte und Arbeitsplätze in Bereichen mit explosiven Gasen, Stäuben oder Dämpfen."),
            ("Wer muss ATEX einhalten?", "Jedes Unternehmen, das in Bereichen mit explosionsfähigen Atmosphären arbeitet, muss ATEX einhalten – darunter Öl- und Gasindustrie, Chemieanlagen, Pharmaproduktion, Getreidehandling und Bergbau."),
            ("Was sind ATEX-Zonen?", "ATEX-Zonen klassifizieren gefährdete Bereiche nach der Häufigkeit explosionsfähiger Atmosphären. Zone 0/20 ist dauerhaftes Risiko, Zone 1/21 bei Normalbetrieb wahrscheinlich, Zone 2/22 unwahrscheinlich aber möglich."),
        ],
        "no": [
            ("Hva står ATEX for?", "ATEX kommer fra det franske 'Atmosphères Explosibles' som betyr eksplosive atmosfærer. Det viser til EU-direktiver som regulerer utstyr og arbeidsplasser i områder med eksplosive gasser, støv eller damper."),
            ("Hvem må følge ATEX?", "Alle virksomheter som opererer i områder med potensielt eksplosive atmosfærer må følge ATEX, inkludert olje og gass, kjemiske anlegg, farmasøytisk produksjon, kornhåndtering og gruvedrift."),
            ("Hva er ATEX-soner?", "ATEX-soner klassifiserer farlige områder etter hvor ofte en eksplosiv atmosfære forekommer. Sone 0/20 er kontinuerlig risiko, Sone 1/21 er sannsynlig under normal drift, Sone 2/22 er usannsynlig men mulig."),
        ],
        "es": [
            ("¿Qué significa ATEX?", "ATEX proviene del francés 'Atmosphères Explosibles' que significa atmósferas explosivas. Se refiere a las directivas de la UE que regulan equipos y lugares de trabajo en áreas con gases, polvos o vapores explosivos."),
            ("¿Quién debe cumplir con ATEX?", "Cualquier empresa que opere en áreas con atmósferas potencialmente explosivas debe cumplir con ATEX, incluyendo petróleo y gas, plantas químicas, industria farmacéutica, manejo de granos y operaciones mineras."),
            ("¿Qué son las zonas ATEX?", "Las zonas ATEX clasifican las áreas peligrosas según la frecuencia de atmósferas explosivas. Zona 0/20 es riesgo continuo, Zona 1/21 probable en operación normal, Zona 2/22 improbable pero posible."),
        ],
        "nl": [
            ("Waar staat ATEX voor?", "ATEX komt van het Franse 'Atmosphères Explosibles' en betekent explosieve atmosferen. Het verwijst naar EU-richtlijnen voor apparatuur en werkplekken in gebieden met explosieve gassen, stoffen of dampen."),
            ("Wie moet voldoen aan ATEX?", "Elk bedrijf dat werkt in gebieden met potentieel explosieve atmosferen moet aan ATEX voldoen, waaronder olie en gas, chemische fabrieken, farmaceutische productie, graanverwerking en mijnbouw."),
            ("Wat zijn ATEX-zones?", "ATEX-zones classificeren gevaarlijke gebieden op basis van hoe vaak een explosieve atmosfeer voorkomt. Zone 0/20 is continu risico, Zone 1/21 waarschijnlijk bij normaal bedrijf, Zone 2/22 onwaarschijnlijk maar mogelijk."),
        ],
        "sv": [
            ("Vad står ATEX för?", "ATEX kommer från franskans 'Atmosphères Explosibles' som betyder explosiva atmosfärer. Det hänvisar till EU-direktiv som reglerar utrustning och arbetsplatser i områden med explosiva gaser, damm eller ångor."),
            ("Vem måste följa ATEX?", "Alla företag som arbetar i områden med potentiellt explosiva atmosfärer måste följa ATEX, inklusive olja och gas, kemiska anläggningar, läkemedelstillverkning, spannmålshantering och gruvdrift."),
            ("Vad är ATEX-zoner?", "ATEX-zoner klassificerar farliga områden efter hur ofta en explosiv atmosfär uppstår. Zon 0/20 är kontinuerlig risk, Zon 1/21 sannolik vid normal drift, Zon 2/22 osannolik men möjlig."),
        ],
        "da": [
            ("Hvad står ATEX for?", "ATEX kommer fra det franske 'Atmosphères Explosibles', der betyder eksplosive atmosfærer. Det refererer til EU-direktiver, der regulerer udstyr og arbejdspladser i områder med eksplosive gasser, støv eller dampe."),
            ("Hvem skal overholde ATEX?", "Enhver virksomhed, der opererer i områder med potentielt eksplosive atmosfærer, skal overholde ATEX, herunder olie og gas, kemiske anlæg, farmaceutisk produktion, kornhåndtering og minedrift."),
            ("Hvad er ATEX-zoner?", "ATEX-zoner klassificerer farlige områder efter, hvor ofte en eksplosiv atmosfære forekommer. Zone 0/20 er kontinuerlig risiko, Zone 1/21 sandsynlig under normal drift, Zone 2/22 usandsynlig men mulig."),
        ],
        "fi": [
            ("Mitä ATEX tarkoittaa?", "ATEX tulee ranskankielisestä termistä 'Atmosphères Explosibles' eli räjähdysvaaralliset ilmakehät. Se viittaa EU-direktiiveihin, jotka säätelevät laitteita ja työpaikkoja alueilla, joissa voi esiintyä räjähtäviä kaasuja, pölyjä tai höyryjä."),
            ("Kenen on noudatettava ATEX-säännöksiä?", "Kaikkien räjähdysvaarallisissa tiloissa toimivien yritysten on noudatettava ATEX-säännöksiä, mukaan lukien öljy- ja kaasuteollisuus, kemiantehtaat, lääketeollisuus, viljan käsittely ja kaivostoiminta."),
            ("Mitä ovat ATEX-vyöhykkeet?", "ATEX-vyöhykkeet luokittelevat vaaralliset alueet sen mukaan, kuinka usein räjähdyskelpoinen ilmaseos esiintyy. Vyöhyke 0/20 on jatkuva riski, Vyöhyke 1/21 todennäköinen normaalitoiminnassa, Vyöhyke 2/22 epätodennäköinen mutta mahdollinen."),
        ],
        "pt": [
            ("O que significa ATEX?", "ATEX vem do francês 'Atmosphères Explosibles' que significa atmosferas explosivas. Refere-se às diretivas da UE que regulam equipamentos e locais de trabalho em áreas com gases, poeiras ou vapores explosivos."),
            ("Quem precisa cumprir a ATEX?", "Qualquer empresa que opere em áreas com atmosferas potencialmente explosivas deve cumprir a ATEX, incluindo petróleo e gás, fábricas químicas, indústria farmacêutica, manuseamento de cereais e mineração."),
            ("O que são as zonas ATEX?", "As zonas ATEX classificam as áreas perigosas conforme a frequência de atmosferas explosivas. Zona 0/20 é risco contínuo, Zona 1/21 provável em operação normal, Zona 2/22 improvável mas possível."),
        ],
        "it": [
            ("Cosa significa ATEX?", "ATEX deriva dal francese 'Atmosphères Explosibles' che significa atmosfere esplosive. Si riferisce alle direttive UE che regolano le apparecchiature e i luoghi di lavoro in aree con gas, polveri o vapori esplosivi."),
            ("Chi deve conformarsi all'ATEX?", "Qualsiasi azienda che opera in aree con atmosfere potenzialmente esplosive deve conformarsi all'ATEX, tra cui petrolio e gas, impianti chimici, industria farmaceutica, movimentazione cereali e attività minerarie."),
            ("Cosa sono le zone ATEX?", "Le zone ATEX classificano le aree pericolose in base alla frequenza delle atmosfere esplosive. Zona 0/20 è rischio continuo, Zona 1/21 probabile in funzionamento normale, Zona 2/22 improbabile ma possibile."),
        ],
        "ar": [
            ("ماذا يعني ATEX؟", "ATEX يأتي من الفرنسية 'Atmosphères Explosibles' وتعني الأجواء المتفجرة. يشير إلى توجيهات الاتحاد الأوروبي التي تنظم المعدات وأماكن العمل في المناطق التي قد توجد فيها غازات أو أتربة أو أبخرة متفجرة."),
            ("من يجب أن يمتثل لـ ATEX؟", "يجب على أي شركة تعمل في مناطق بها أجواء متفجرة محتملة الامتثال لـ ATEX، بما في ذلك النفط والغاز والمصانع الكيميائية والصناعات الدوائية ومناولة الحبوب وعمليات التعدين."),
            ("ما هي مناطق ATEX؟", "تصنف مناطق ATEX المناطق الخطرة حسب تكرار حدوث الأجواء المتفجرة. المنطقة 0/20 خطر مستمر، المنطقة 1/21 محتملة أثناء التشغيل العادي، المنطقة 2/22 غير محتملة لكن ممكنة."),
        ],
    },
}

# For guides without specific translations, use English FAQ
GENERIC_GUIDE_FAQS = {
    "atex-vs-iecex": [
        ("What is the difference between ATEX and IECEx?", "ATEX is a European Union directive mandatory for EU markets, while IECEx is an international certification system accepted worldwide. ATEX uses equipment categories (1, 2, 3) while IECEx uses Equipment Protection Levels (EPL)."),
        ("Can a product have both ATEX and IECEx certification?", "Yes, many manufacturers obtain both certifications to sell in EU and international markets. The technical requirements are similar, but the conformity assessment procedures differ."),
        ("Which certification do I need?", "If selling in the EU, ATEX is mandatory. For international markets outside the EU, IECEx is widely accepted. Many companies get both for maximum market access."),
    ],
    "cable-glands-hazardous-areas": [
        ("What are Ex-rated cable glands?", "Ex-rated cable glands are specially certified cable entry devices designed to maintain the explosion protection of enclosures in hazardous areas. They prevent flame propagation and maintain the IP rating of equipment."),
        ("What types of cable glands are used in hazardous areas?", "The main types are flameproof (Ex d) cable glands for Zone 1, increased safety (Ex e) cable glands for Zone 1/2, and general purpose cable glands for Zone 2 only."),
        ("How do I select the right cable gland for a hazardous area?", "Selection depends on the zone classification, protection concept of the equipment (Ex d, Ex e, Ex i), cable type and diameter, environmental conditions, and the required IP rating."),
    ],
    "compex-certification": [
        ("What is CompEx certification?", "CompEx is an internationally recognized competency certification for personnel working with electrical equipment in explosive atmospheres. It validates knowledge of hazardous area classification, equipment selection, and installation practices."),
        ("Who needs CompEx certification?", "Electricians, engineers, and technicians who install, inspect, or maintain electrical equipment in hazardous areas typically need CompEx certification. Many oil and gas companies require it for site access."),
        ("How long is CompEx certification valid?", "CompEx certification is typically valid for 5 years, after which personnel must complete a refresher course and assessment to maintain their certified status."),
    ],
    "dust-explosion-protection": [
        ("What causes dust explosions?", "Dust explosions occur when five conditions are met simultaneously: combustible dust, dust dispersion in air, confinement, an ignition source, and oxygen. This is known as the dust explosion pentagon."),
        ("Which industries are at risk of dust explosions?", "Industries handling fine powders are at risk, including grain and food processing, woodworking, pharmaceutical manufacturing, metal processing, chemical production, and coal handling."),
        ("How are dust explosion hazardous areas classified?", "Dust hazardous areas are classified as Zone 20 (continuous dust cloud), Zone 21 (occasional dust cloud during normal operation), and Zone 22 (dust cloud unlikely but possible during abnormal conditions)."),
    ],
    "ex-equipment-selection-guide": [
        ("How do I select the right Ex equipment?", "Equipment selection depends on the zone classification, gas group or dust group present, temperature class required, environmental conditions, and the specific application. Always match the equipment marking to the area classification."),
        ("What do Ex equipment markings mean?", "Ex markings indicate the protection type (e.g., Ex d for flameproof, Ex i for intrinsic safety), the gas/dust group, and the temperature class. For example, Ex d IIC T6 means flameproof protection suitable for all gas groups up to temperature class T6."),
        ("Can Zone 1 equipment be used in Zone 2?", "Yes, equipment certified for a higher-risk zone can always be used in a lower-risk zone. Zone 1 equipment can be used in Zone 2, and Zone 0 equipment can be used in any gas zone."),
    ],
    "explosion-proof-vs-intrinsically-safe": [
        ("What is the difference between explosion-proof and intrinsically safe?", "Explosion-proof (Ex d) equipment contains any internal explosion within a heavy enclosure, while intrinsically safe (Ex i) equipment limits energy to levels too low to cause ignition. They are fundamentally different approaches to explosion protection."),
        ("Which is better: explosion-proof or intrinsically safe?", "Neither is universally better. Intrinsically safe is preferred for portable instruments and low-power devices as it's lighter and allows maintenance in hazardous areas. Explosion-proof is used for higher-power equipment like motors and lighting."),
        ("Can intrinsically safe devices be used in Zone 0?", "Yes, intrinsically safe devices with Ex ia certification can be used in Zone 0 (the highest risk zone). This is one of very few protection methods approved for continuous explosive atmospheres."),
    ],
    "hazardous-area-classification": [
        ("What is hazardous area classification?", "Hazardous area classification is the process of analyzing a facility to identify locations where explosive gas or dust atmospheres may occur, and assigning zone designations (0, 1, 2 for gas; 20, 21, 22 for dust) based on the likelihood and duration."),
        ("Who is responsible for hazardous area classification?", "The facility owner or operator is responsible for hazardous area classification. It should be performed by competent engineers with knowledge of the process, materials handled, and relevant standards like IEC 60079-10."),
        ("How often should hazardous area classification be reviewed?", "Classification should be reviewed whenever there are process changes, equipment modifications, or at regular intervals (typically every 3-5 years). Any change that could affect the release of flammable materials requires a review."),
    ],
    "how-to-read-atex-nameplate": [
        ("How do I read an ATEX nameplate?", "An ATEX nameplate contains the Ex marking (protection type, gas/dust group, temperature class), the equipment category (1, 2, or 3), the group (I for mining, II for surface), and the CE marking with notified body number."),
        ("What does the epsilon-x symbol mean on a nameplate?", "The epsilon-x (Ex) symbol indicates that equipment is certified for use in explosive atmospheres. It's always followed by letters indicating the specific protection method, such as 'd' for flameproof or 'i' for intrinsic safety."),
        ("What is the temperature class on an ATEX nameplate?", "The temperature class (T1 to T6) indicates the maximum surface temperature of the equipment. T6 (85°C) is the most restrictive, while T1 (450°C) is the least. The class must be lower than the auto-ignition temperature of gases present."),
    ],
    "hydrogen-explosion-protection": [
        ("Why is hydrogen especially dangerous?", "Hydrogen is extremely dangerous because it has the widest flammable range (4-75% in air), very low ignition energy (0.017 mJ), high flame speed, and is invisible and odorless. It also belongs to the most demanding gas group (IIC)."),
        ("What equipment is needed for hydrogen environments?", "Equipment in hydrogen environments must be certified for Gas Group IIC (the most stringent group) and typically requires Temperature Class T1. Common protection methods include intrinsic safety (Ex ia) and flameproof (Ex d IIC)."),
        ("How is hydrogen hazardous area classification different?", "Hydrogen's extreme buoyancy and wide flammable range affect zone classification. Hydrogen rises rapidly and disperses quickly outdoors, which can reduce zone extents. However, in enclosed spaces, it creates larger Zone 0 and Zone 1 areas than heavier gases."),
    ],
}


def build_faq_jsonld(faqs):
    """Build FAQ JSON-LD from list of (question, answer) tuples."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            }
            for q, a in faqs
        ]
    }, ensure_ascii=False, indent=2)


def add_faq_to_file(filepath, faqs):
    """Insert FAQ JSON-LD into an HTML file before </head>."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Skip if already has FAQPage schema
    if '"FAQPage"' in html:
        return False

    jsonld = build_faq_jsonld(faqs)
    script_tag = f'<script type="application/ld+json">\n{jsonld}\n</script>\n'

    # Insert before </head>
    html = html.replace("</head>", script_tag + "</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    total = 0
    skipped = 0

    guides = list(GUIDE_FAQS.keys()) + [g for g in GENERIC_GUIDE_FAQS if g not in GUIDE_FAQS]

    for guide in guides:
        for lang in LANGUAGES:
            if lang == "en":
                filepath = os.path.join(SITE_DIR, "pages", f"{guide}.html")
            else:
                filepath = os.path.join(SITE_DIR, lang, "pages", f"{guide}.html")

            if not os.path.exists(filepath):
                continue

            # Get language-specific FAQs
            if guide in GUIDE_FAQS and lang in GUIDE_FAQS[guide]:
                faqs = GUIDE_FAQS[guide][lang]
            elif guide in GUIDE_FAQS and "en" in GUIDE_FAQS[guide]:
                faqs = GUIDE_FAQS[guide]["en"]
            elif guide in GENERIC_GUIDE_FAQS:
                faqs = GENERIC_GUIDE_FAQS[guide]
            else:
                continue

            if add_faq_to_file(filepath, faqs):
                total += 1
                print(f"  ✓ {lang}/{guide}")
            else:
                skipped += 1

    print(f"\nDone: {total} files updated, {skipped} skipped (already had FAQ schema)")


if __name__ == "__main__":
    main()

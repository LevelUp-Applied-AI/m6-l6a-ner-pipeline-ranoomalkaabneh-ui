
Entity Count Summary
| entity_label   |   Base spaCy |   Ruler Before NER |   Ruler After NER |
|:---------------|-------------:|-------------------:|------------------:|
| AGREEMENT      |            0 |                  6 |                 0 |
| CARDINAL       |          138 |                138 |               138 |
| CLIMATE_EVENT  |            0 |                  5 |                 3 |
| DATE           |          256 |                256 |               256 |
| EVENT          |            8 |                  2 |                 8 |
| FAC            |            9 |                  8 |                 9 |
| GPE            |          165 |                164 |               165 |
| LAW            |            5 |                  5 |                 5 |
| LOC            |           93 |                 93 |                93 |
| MONEY          |           63 |                 63 |                63 |
| NORP           |           21 |                 21 |                21 |
| ORDINAL        |            9 |                  9 |                 9 |
| ORG            |          184 |                183 |               184 |
| PERCENT        |          103 |                103 |               103 |
| PERSON         |           36 |                 36 |                36 |
| POLICY         |            0 |                  2 |                 2 |
| PRODUCT        |            6 |                  6 |                 6 |
| QUANTITY       |           92 |                 69 |                92 |
| REPORT         |            0 |                  2 |                 0 |
| THRESHOLD      |            0 |                 26 |                 0 |
| TIME           |            8 |                  8 |                 8 |
| WORK_OF_ART    |            6 |                  6 |                 6 |
| TOTAL          |         1202 |               1211 |              1207 |

Evaluation on Standard Gold Labels Only
| Metric    |   Base spaCy |   Ruler Before NER |   Ruler After NER |
|:----------|-------------:|-------------------:|------------------:|
| Precision |       0.0492 |             0.0509 |            0.0492 |
| Recall    |       0.6471 |             0.6471 |            0.6471 |
| F1        |       0.0914 |             0.0944 |            0.0914 |

Custom Rule Examples
--------------------

Text ID: 1
Custom entity: Sixth Assessment Report [REPORT]
Text: The IPCC released its Sixth Assessment Report in March 2023, warning that global temperatures could exceed 1.5 degrees Celsius above pre-industrial levels by 2030. The report emphasized the urgent need for immediate and deep emission reductions across all sectors. Secretary-General Antonio Guterres called the findings a code red for humanity and urged world leaders to accelerate the phase-out of fossil fuels before the next COP summit.

Text ID: 1
Custom entity: 1.5 degrees [THRESHOLD]
Text: The IPCC released its Sixth Assessment Report in March 2023, warning that global temperatures could exceed 1.5 degrees Celsius above pre-industrial levels by 2030. The report emphasized the urgent need for immediate and deep emission reductions across all sectors. Secretary-General Antonio Guterres called the findings a code red for humanity and urged world leaders to accelerate the phase-out of fossil fuels before the next COP summit.

Text ID: 2
Custom entity: COP28 [CLIMATE_EVENT]
Text: At COP28 in Dubai, over 190 nations agreed to transition away from fossil fuels in energy systems. The United Arab Emirates presidency brokered the deal after two weeks of intense negotiations. The agreement also called for tripling renewable energy capacity globally by 2030 and doubling the rate of energy efficiency improvements. Environmental groups praised the language but noted the absence of binding enforcement mechanisms.

Text ID: 2
Custom entity: 190 [CARDINAL]
Text: At COP28 in Dubai, over 190 nations agreed to transition away from fossil fuels in energy systems. The United Arab Emirates presidency brokered the deal after two weeks of intense negotiations. The agreement also called for tripling renewable energy capacity globally by 2030 and doubling the rate of energy efficiency improvements. Environmental groups praised the language but noted the absence of binding enforcement mechanisms.

Text ID: 4
Custom entity: 31% [PERCENT]
Text: Jordan's National Climate Change Policy, adopted in 2022, commits the country to reducing greenhouse gas emissions by 31% by 2030 compared to a business-as-usual scenario. The policy outlines investments in solar energy, water efficiency, and sustainable transport. The Ministry of Environment coordinates implementation with support from UNDP and the European Union.

Text ID: 5
Custom entity: Paris Agreement [AGREEMENT]
Text: UNFCCC Executive Secretary Simon Stiell addressed delegates at the Bonn Climate Change Conference in June 2024, emphasizing that current nationally determined contributions fall short of the Paris Agreement targets. He called for enhanced ambition in the next round of NDCs due by February 2025 and stressed the importance of loss and damage financing for developing nations.

Text ID: 5
Custom entity: NDCs [POLICY]
Text: UNFCCC Executive Secretary Simon Stiell addressed delegates at the Bonn Climate Change Conference in June 2024, emphasizing that current nationally determined contributions fall short of the Paris Agreement targets. He called for enhanced ambition in the next round of NDCs due by February 2025 and stressed the importance of loss and damage financing for developing nations.

Text ID: 7
Custom entity: Paris Agreement [AGREEMENT]
Text: In September 2023, the United Nations General Assembly hosted the Climate Ambition Summit in New York, where only nations with credible new climate commitments were invited to speak. The summit highlighted a growing divide between developed and developing nations on the pace of decarbonization and the scale of climate finance required to meet the goals of the Paris Agreement.

Text ID: 8
Custom entity: 735 million [CARDINAL]
Text: FAO published its State of Food and Agriculture 2023 report, dedicating an entire chapter to the intersection of climate change and food security. The report estimates that 735 million people faced chronic hunger in 2022, with climate-related crop failures contributing to food price volatility. FAO Director-General Qu Dongyu called for $4 billion in annual investments to transform agri-food systems toward climate resilience.

Text ID: 10
Custom entity: Paris Agreement [AGREEMENT]
Text: China's Special Envoy for Climate Change Xie Zhenhua met with US Climate Envoy John Kerry in Sunnylands, California in November 2023. The bilateral talks produced a joint statement reaffirming both nations' commitment to the Paris Agreement and announcing cooperative efforts on methane reduction, deforestation, and clean energy deployment. The statement was seen as a positive signal ahead of COP28.

Text ID: 10
Custom entity: COP28 [CLIMATE_EVENT]
Text: China's Special Envoy for Climate Change Xie Zhenhua met with US Climate Envoy John Kerry in Sunnylands, California in November 2023. The bilateral talks produced a joint statement reaffirming both nations' commitment to the Paris Agreement and announcing cooperative efforts on methane reduction, deforestation, and clean energy deployment. The statement was seen as a positive signal ahead of COP28.

Text ID: 11
Custom entity: 1.48 degrees [THRESHOLD]
Text: Researchers at NASA's Goddard Institute for Space Studies confirmed that 2023 was the warmest year on record, with global average temperatures 1.48 degrees Celsius above the 1850-1900 baseline. The El Nino pattern that developed in mid-2023 amplified warming trends, contributing to record-breaking heat across Southern Europe, North Africa, and the Middle East. July 2023 was the hottest month ever recorded.

Saved output CSV files.

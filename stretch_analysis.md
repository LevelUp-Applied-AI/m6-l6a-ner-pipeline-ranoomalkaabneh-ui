# Module 6 Week A Stretch: Custom NER Rules

## Overview

This stretch assignment extends the Lab 6A NER pipeline by adding a custom spaCy EntityRuler for climate-domain terminology. The rules target entities that the base spaCy model often misses or mislabels, such as COP28, Paris Agreement, Sixth Assessment Report, NDCs, and temperature thresholds.

## Custom Entity Types

The custom EntityRuler includes patterns across the following custom labels:

- CLIMATE_EVENT
- AGREEMENT
- REPORT
- THRESHOLD
- POLICY

The rules include more than 10 pattern entries and cover more than 8 distinct climate-domain concepts.

## Before/After Summary

The base spaCy model extracted 1202 total entities. When the EntityRuler was placed before the built-in NER, the pipeline extracted 1211 total entities. When the EntityRuler was placed after the built-in NER, the pipeline extracted 1207 total entities.

The before-NER position created more custom labels, including AGREEMENT, REPORT, and THRESHOLD. The after-NER position preserved more of spaCy’s original entity labels and introduced fewer custom replacements.

## Evaluation on Standard Gold Labels

Evaluation was performed only on overlapping standard labels because the gold standard does not include custom labels.

| Metric | Base spaCy | Ruler Before NER | Ruler After NER |
|---|---:|---:|---:|
| Precision | 0.0492 | 0.0509 | 0.0492 |
| Recall | 0.6471 | 0.6471 | 0.6471 |
| F1 | 0.0914 | 0.0944 | 0.0914 |

## Analysis

The custom EntityRuler improved domain-specific entity coverage by identifying climate concepts that the base spaCy model did not consistently capture. For example, in Text ID 1, the rule correctly labeled “Sixth Assessment Report” as REPORT and “1.5 degrees” as THRESHOLD. In Text ID 2 and Text ID 10, the rule correctly identified “COP28” as CLIMATE_EVENT, and in Text IDs 5, 7, and 10, it identified “Paris Agreement” as AGREEMENT without incorrectly matching “Paris” alone. Placing the EntityRuler before NER slightly improved precision and F1 on standard labels, but recall stayed the same, which suggests that the custom rules mostly changed labels rather than finding additional gold-standard entities. Some noise remained in the qualitative examples because standard numeric entities such as “190”, “31%”, and “735 million” appeared alongside custom-rule examples, so custom-label reporting should be filtered carefully.
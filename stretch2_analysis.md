 Cross-Lingual Embedding Analysis (mBERT)
1. How well does multilingual BERT capture cross-lingual similarity?

The results show that bert-base-multilingual-cased is able to map English and Arabic climate-related texts into a shared embedding space with moderate alignment.

In several cases, semantically similar texts across languages (e.g., articles about climate policy, emissions, or IPCC reports) produced higher cosine similarity scores compared to unrelated pairs. For example, some English-Arabic pairs discussing climate agreements reached similarity scores in the range of 0.45–0.65, which is significantly higher than random cross-language pairs that often fall below 0.3.

However, the alignment is not perfect. Within-language similarities (English-English or Arabic-Arabic) were consistently higher (often above 0.7), showing that the model still encodes language-specific structure more strongly than cross-lingual semantics.

This indicates that while mBERT does learn shared semantic representations, the cross-lingual space is noisier and less tightly clustered than monolingual spaces.

2. What does this mean for bilingual NLP in the MENA region?

These findings suggest that multilingual embeddings can support basic bilingual NLP applications in the MENA region, such as cross-lingual search and topic clustering, without requiring separate models for each language.

However, the performance gap between within-language and cross-language similarity indicates that relying solely on mBERT may lead to reduced precision in high-stakes applications, such as legal or policy retrieval systems.

For production systems, this means:

mBERT is suitable for prototype-level bilingual search engines
But may require fine-tuning or hybrid models for accurate Arabic-English alignment
Domain-specific tuning (e.g., climate or policy data) could significantly improve clustering quality

Overall, multilingual transformers provide a strong baseline for unified NLP systems, but they do not fully eliminate language bias in embedding spaces.


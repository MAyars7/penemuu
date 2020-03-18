# penemuu
Rule-based relationship extraction from biomedical texts using spaCy.

Inspired by the ReVerb pattern (http://reverb.cs.washington.edu/emnlp11.pdf) and similar efforts, this is a WIP tool to identify and extract 
relationships between named entities in a short biomedical abstracts or clinical notes based on generalizable patterns in the grammatical structure of sentences.

### Background

A common desire in biomedical fields is to search existing literature for binary relationships between two entities (mutation:cancer, disease:symptom, organism:habitat, etc).  The main challenge to this task is the size and speed at which Pubmed is growing: it contains 29 million articles, increasing by 1 million annually. 
Simple web-search based techniques are highly scalable but easily confounded: a paper containing two specified entities may not link them at all or may even be denying a link between them.  It is therefore important to incorporate contextual clues into relationship extraction.
The past couple of years have seen amazing breakthroughs in deep learning methods of information extraction (Elmo, BERT, etc.).  These methods are powerful but demand extensive computational resources to train and apply, and can be difficult to interpret in reasoning.
My hypothesis behind this project is that the narrow domain of biomedical abstracts may reduce word and sentence variability to the point where simple heuristics can achieve similar results to more powerful tools.

#### ReVerb Pattern

The ReVerb pattern is a robust part-of-speech (POS) based regular expression pattern for relationship extraction.  Sentences are chunked into noun phrases (https://www.nltk.org/book/ch07.html), and the pattern is applied to the POS tags of words between them.

![reverb pattern](/images/reverb.png)

The limitations of ReVerb noted in the paper were an inability to identify relational phrases that were non-contiguous and relational phrases that were not between entities.

![reverb limitations](/images/reverb_limitations.png)

#### Dependency trees

![dep tree](/images/spacy_dep_pathing.png)

A way of modeling grammatical structure in sentences.

Sentences are organized into 'noun chunks': phrases containing a noun and words describing/modifying it.  These noun chunks are assembled into a tree where every word has a single head.  Every sentence has a single root node (usually a verb) from which every other word descends.

My hope is that by looking at the dependency path between entities and between entities and the root verb of a sentence, it may be possible to identify patterns that are less sensitive to the actual order of words in the sentence.

#### Scientific Abstracts

There are several traits to scientific abstracts that make them simpler to interpret with NLP techniques than a lot of mainstream texts:
* They summarize the major findings of a paper in (usually) no more than a few sentences.
* Facts are expressed in clear and unambiguous terms. 
* Papers are edited for grammar and spelling.
* Sarcasm is almost nonexistant.

They also have traits that complicate things:
* Extensive use of abbreviations.  These can be difficult to normalize and also throw off sentence boundary detection.
* Use of words that are highly domain-specific.  
* Some authors are non-native English speakers and may use common words or grammar in unconventional ways.

**Current State**
  * Downloaded abstracts in medline format are parsed and stored in a PassageCorpus.
  * Abstracts stored in PassageCorpus can be annotated for Named Entities using PassageAnnotator.
  * Relationships between pairs of entities within a single sentence can be extracted using DependencyMapper (very basic rules).

**To-do** 
  * Core functionality:
    * Generate breakdown of common sentence structure patterns (assuming they exist).  Currently exploring clustering some combination of similarity between:
      * Root verb.
      * All verbs in sentence.
      * All lowest common ancestors for entity pairs.
      * Number and type of named entities.
      * Relationship of entities to subject or object(s) of sentence.
      * Order of above features in sentence.
    * Generate deeper rules for infering relationships from identified patterns.    
    * Add handling for inter-sentence relationship extraction (coreference resolution).
    * Add unit tests.
    
  * Usability:
    * Add command-line workflow.
    * Add visualization tools.
    * Add Container for installation.
  

# penemuu
Rule-based relationship extraction from biomedical texts using spaCy.

Inspired by the ReVerb pattern (http://reverb.cs.washington.edu/emnlp11.pdf) and similar efforts, this is a WIP tool to identify and extract 
relationships between named entities in a short biomedical abstracts or clinical notes based on generalizable patterns in sentence structure.

### Background

A common desire in biomedical fields is to search existing literature for binary relationships between two entities (mutation:cancer, disease:symptom, organism:habitat, etc).  This task is made difficult by the size of Pubmed: 29 million articles, increasing by 1 million annually. 
Simple web-search based techniques are highly scalable, but easily confounded: a paper containing two specified terms may not link them at all or may even be denying a link between them.  It is therefore important to extract relationships between entities based on their contextual usage.

#### Dependency trees

![dep tree](/images/spacy_dep_pathing.png)

**Current State**
  * Downloaded abstracts in medline format are parsed and stored in a PassageCorpus.
  * Abstracts stored in PassageCorpus can be annotated for Named Entities using PassageAnnotator.
  * Relationships between pairs of entities within a single sentence can be extracted using DependencyMapper (very basic rules).

**To-do** 
  * Core functionality:
 
    * Generate breakdown of common sentence structures to identify patterns (and better rules for resolving them).  Possibly some combination of:
      * Root verb.
      * All verbs in sentence.
      * All lowest common ancestors for entity pairs.
      * Number and type of named entities.
      * Order of above features in sentence.
        
    * Add handling for inter-sentence relationship extraction (coreference resolution).
    * Add unit tests.
    
  * Usability:
    * Add command-line workflow.
    * Add visualization tools.
    * Add Container for installation.
  

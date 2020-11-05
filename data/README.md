# Directory content

## datasets
Dataset definitions extracted from www.data.gov.cz, used to load
metadata by the web-application.

## evaluation
Definition of evaluation tasks.

## evaluation-reports
User evaluation data are stored here.

## evaluation-reports-archive
Used to archive results for particular evaluations.

## evaluation-reports-graphs
Graph produced for directories in ```evaluation-reports-archive```.

## input
Contains input files almost as provided by the external source. 
* ```wikidata-cs.jsonl``` - Czech titles of wikidata entities.
* ```wikidata-cs-en.jsonl``` - English titles of wikidata entities.
* ```wikidata-hierarchy.jsonl``` - File with all *instanceof* and *subclassof* edges.
* ```2020.04.20-www.data.gov.cz.trig``` - Dump with all relevant datasets metadata.

## mapping
Mapping from datasets to wikidata entities, used by web-application.
Content is copy of something in ```working``` directory.

## similarities
Similarities of datasets by given method, used for user-based evaluation.

## similarities-matrix
Computed similarity matrices, provided by external source. 

## udpipe
Files required to run udpipe.

## working
Temporary working directory, can be deleted to free out some space.

## www.data.gov.cz
Files with information about datasets as extracted from 
```./input/2020.04.20-www.data.gov.cz.trig```.

## www.wikidata.org
Files from wikidata, based on data downloaded by ```download-wikidata-remote-content.sh```.
See ```run_prepare_texts``` script to get details about different
versions.
* ```wikidata-cs.v1.jsonl```
* ```wikidata-cs.v2.jsonl```
* ```wikidata-cs.v3.jsonl```

Following files are used in the SISAP demo, they are extraction of used
labels that are loaded to the server. While for us the labels are in cs
we need en version for the conference.
* ```wikidata-labels-cs.jsonl```
* ```wikidata-labels-en.jsonl```

## dataset-iri-to-file-name.json
File generated only once, store mapping from IRI to dataset file name.
Reason for this file is that IRI can not be used as a file name.  This
file is not generated as we need it to be constant.

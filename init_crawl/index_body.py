index_body = {
    "settings": {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {
                    "tokenizer": "ngram_tokenizer",
                    "filter": ["lowercase"]
                }
            },
            "tokenizer": {
                "ngram_tokenizer": {
                    "type": "ngram",
                    "min_gram": 2,
                    "max_gram": 4
                }
            }
        },
        "index": {
            "max_ngram_diff": 3
        }
    },
    "mappings": {
        "properties": {
            "date": {"type": "date"},
            "time": {"type": "keyword"},
            "airline": {
                "type": "text",
                "analyzer": "ngram_analyzer",
                "fields": {
                    "raw": {"type": "keyword"}
                }
            },
            "aircraft_registration": {"type": "keyword"},
            "accident_type": {"type": "keyword"},
            "description": {"type": "text"},
            "ko_description": {"type": "text"},
            "fatalities": {"type": "integer"},
            "occupants": {"type": "integer"},
            "location": {
                "type": "text",
                "analyzer": "ngram_analyzer"
            },
            "phase": {"type": "keyword"},
            "aircraft_model": {"type": "keyword"},
            "aircraft_status": {"type": "keyword"}
        }
    }
}
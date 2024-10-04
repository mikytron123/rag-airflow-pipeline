/bin/weaviate --host 0.0.0.0 --port 8090 --scheme http &

pid=$!

sleep 5

echo 'creating collection'
wget --header 'content-type: application/json' --post-data '{
    "class": "Documents",
    "properties": [
        {
            "dataType": [
                "text"
            ],
            "indexFilterable": true,
            "indexSearchable": true,
            "name": "file_path",
            "tokenization": "word"
        },
        {
            "dataType": [
                "text"
            ],
            "indexFilterable": true,
            "indexSearchable": true,
            "name": "file_name",
            "tokenization": "word"
        },
        {
            "dataType": [
                "text"
            ],
            "indexFilterable": true,
            "indexSearchable": true,
            "name": "file_type",
            "tokenization": "word"
        },
        {
            "dataType": [
                "int"
            ],
            "indexFilterable": true,
            "indexSearchable": false,
            "name": "file_size"
        },
        {
            "dataType": [
                "date"
            ],
            "indexFilterable": true,
            "indexSearchable": false,
            "name": "creation_date"
        },
        {
            "dataType": [
                "date"
            ],
            "indexFilterable": true,
            "indexSearchable": false,
            "name": "last_modified_date"
        },
        {
            "dataType": [
                "text"
            ],
            "indexFilterable": true,
            "indexSearchable": true,
            "name": "text",
            "tokenization": "word"
        },
        {
            "dataType": [
                "text"
            ],
            "indexFilterable": true,
            "indexSearchable": true,
            "name": "link",
            "tokenization": "word"
        }
    ],
    "vectorIndexConfig": {
        "distance": "cosine"
    },
    "vectorIndexType": "hnsw",
    "vectorizer": "none"
}' http://localhost:8090/v1/schema
echo 'done'

wait $pid
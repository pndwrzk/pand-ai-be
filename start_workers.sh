#!/bin/bash

python3 -m app.workers.content_indexing_worker &
python3 -m app.workers.document_ocr_worker &
python3 -m app.workers.content_vector_delete_worker &
python3 -m app.workers.conversation_title_generation_worker &
wait
#!/bin/bash

pids=()

cleanup() {
    echo "Stopping workers..."
    for pid in "${pids[@]}"; do
        kill -TERM "$pid" 2>/dev/null
    done
    wait
    echo "All workers stopped."
}

trap cleanup SIGINT SIGTERM

python3 -m app.workers.content_indexing_worker &
pids+=($!)

python3 -m app.workers.document_ocr_worker &
pids+=($!)

python3 -m app.workers.content_vector_delete_worker &
pids+=($!)

python3 -m app.workers.conversation_title_generation_worker &
pids+=($!)

wait
# Проверка масштаба 1200/300

Настоящий dense encoder, синтетический корпус, scripted фильтр; это не live качество.

{
  "kind": "synthetic_scale_not_live_quality",
  "status": "FAIL",
  "checks": {
    "documents": true,
    "notes": true,
    "gold_docs": true,
    "gold_note_shortlist": true,
    "gold_note_context": false,
    "no_selected_noise": true,
    "bounded_request": true,
    "shortlist": true
  },
  "documents": 1200,
  "notes": 300,
  "sources": 1545,
  "chunks": 1756,
  "index_seconds": 38.79430619999766,
  "index_cache_hit": false,
  "elapsed_seconds": 54.15127069999289,
  "peak_sampled_memory_bytes": {
    "parent_rss": 137412608,
    "tree_rss": 785301504
  },
  "sampling_interval_seconds": 0.1,
  "serialized_request_bytes": 27585,
  "gold_document_hits": [
    "doc:scale-opportunity",
    "doc:scale-risk"
  ],
  "gold_note_shortlist_hits": [
    "note:scale-negative",
    "note:scale-positive"
  ],
  "gold_note_context_hits": [
    "note:scale-negative"
  ],
  "shown_sources": [
    "doc:doc_007",
    "doc:doc_013",
    "doc:scale-opportunity",
    "doc:scale-risk",
    "note:n_007",
    "note:n_022",
    "note:n_028",
    "note:n_031",
    "note:scale-negative",
    "profile",
    "subtask:t_003:s_009",
    "subtask:t_007:s_020",
    "subtask:t_007:s_022",
    "task:t_001",
    "task:t_003",
    "task:t_005",
    "task:t_010",
    "tasker:inventory"
  ],
  "selected_noise_sources": [],
  "note_selection": {
    "shortlist": [
      "e01486",
      "e01488",
      "e01462",
      "e01477",
      "e01481",
      "e01485",
      "e01468",
      "e01458",
      "e01483",
      "e01472",
      "e01466",
      "e01487",
      "e01479",
      "e01470",
      "e01460",
      "e01474",
      "e01456",
      "e01465",
      "e01464",
      "e01530"
    ],
    "selected": [
      "e01462",
      "e01470",
      "e01477",
      "e01479",
      "e01483",
      "e01486",
      "e01487",
      "e01488"
    ],
    "status": "selected"
  },
  "model_mode": "scripted_filter_fixture",
  "no_paid_calls": true,
  "embedding_config": {
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "revision": "c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
    "max_seq_length": 256,
    "token_limit": 254,
    "normalized": true,
    "chunking": "tokenizer-paragraphs-v1",
    "overlap_tokens": 0,
    "offset_unit": "unicode_characters"
  },
  "encoder_events": [
    {
      "pid": 20712,
      "returncode": 0,
      "elapsed": 36.53258210000058,
      "stopped": true,
      "cancelled": false
    },
    {
      "pid": 24816,
      "returncode": 0,
      "elapsed": 14.673355699997046,
      "stopped": true,
      "cancelled": false
    }
  ],
  "api_calls": 23
}
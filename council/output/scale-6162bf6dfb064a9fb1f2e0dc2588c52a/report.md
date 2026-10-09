# Проверка масштаба 1200/300

Настоящий dense encoder, синтетический корпус, scripted фильтр; это не live качество.

{
  "kind": "synthetic_scale_not_live_quality",
  "status": "FAIL",
  "checks": {
    "documents": true,
    "notes": true,
    "gold_docs": false,
    "gold_note_shortlist": false,
    "gold_note_context": false,
    "no_selected_noise": true,
    "bounded_request": true,
    "shortlist": true
  },
  "documents": 1200,
  "notes": 300,
  "sources": 1544,
  "chunks": 1753,
  "index_seconds": 0.5987927000096533,
  "index_cache": "existing digest-matched cache",
  "elapsed_seconds": 15.05456299999787,
  "peak_sampled_memory_bytes": {
    "parent_rss": 136478720,
    "tree_rss": 651145216
  },
  "sampling_interval_seconds": 0.1,
  "serialized_request_bytes": 28599,
  "gold_document_hits": [
    "doc:scale-risk"
  ],
  "gold_note_shortlist_hits": [
    "note:scale-negative"
  ],
  "gold_note_context_hits": [
    "note:scale-negative"
  ],
  "shown_sources": [
    "doc:doc_002",
    "doc:doc_004",
    "doc:doc_014",
    "doc:scale-risk",
    "note:n_007",
    "note:n_015",
    "note:n_022",
    "note:n_031",
    "note:scale-negative",
    "profile",
    "subtask:t_003:s_009",
    "subtask:t_007:s_020",
    "subtask:t_007:s_022",
    "task:t_001",
    "task:t_003",
    "task:t_005",
    "task:t_009",
    "task:t_010"
  ],
  "selected_noise_sources": [],
  "note_selection": {
    "shortlist": [
      "e01483",
      "e01485",
      "e01465",
      "e01459",
      "e01474",
      "e01478",
      "e01482",
      "e01455",
      "e01467",
      "e01480",
      "e01469",
      "e01457",
      "e01462",
      "e01453",
      "e01463",
      "e01461",
      "e01608",
      "e01586",
      "e01527",
      "e01476"
    ],
    "selected": [
      "e01459",
      "e01467",
      "e01474",
      "e01476",
      "e01480",
      "e01483",
      "e01485"
    ],
    "status": "selected"
  },
  "model_mode": "scripted_filter_fixture",
  "no_paid_calls": true,
  "embedding_config": {
    "chunking": "tokenizer-paragraphs-v1",
    "max_seq_length": 256,
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "normalized": true,
    "offset_unit": "unicode_characters",
    "overlap_tokens": 0,
    "revision": "c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
    "token_limit": 254
  },
  "encoder_events": [
    {
      "pid": 10488,
      "returncode": 0,
      "elapsed": 13.745256800000789,
      "stopped": true,
      "cancelled": false
    }
  ],
  "api_calls": 21
}
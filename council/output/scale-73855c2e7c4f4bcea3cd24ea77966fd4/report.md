# Проверка масштаба 1200/300

Настоящий dense encoder, синтетический корпус, scripted фильтр; это не live качество.

{
  "kind": "synthetic_scale_not_live_quality",
  "status": "PASS",
  "checks": {
    "documents": true,
    "notes": true,
    "gold_docs": true,
    "gold_note_shortlist": true,
    "gold_note_context": true,
    "no_selected_noise": true,
    "bounded_request": true,
    "shortlist": true
  },
  "documents": 1200,
  "notes": 300,
  "sources": 1545,
  "chunks": 1756,
  "index_seconds": 0.5408626999997068,
  "index_cache_hit": true,
  "elapsed_seconds": 14.712688500003424,
  "peak_sampled_memory_bytes": {
    "parent_rss": 135946240,
    "tree_rss": 650575872
  },
  "sampling_interval_seconds": 0.1,
  "serialized_request_bytes": 22906,
  "gold_document_hits": [
    "doc:scale-opportunity",
    "doc:scale-risk"
  ],
  "gold_note_shortlist_hits": [
    "note:scale-negative",
    "note:scale-positive"
  ],
  "gold_note_context_hits": [
    "note:scale-negative",
    "note:scale-positive"
  ],
  "shown_sources": [
    "doc:doc_001",
    "doc:doc_004",
    "doc:doc_006",
    "doc:doc_007",
    "doc:doc_009",
    "doc:doc_012",
    "doc:doc_013",
    "doc:doc_014",
    "doc:scale-opportunity",
    "doc:scale-risk",
    "note:n_007",
    "note:n_015",
    "note:n_022",
    "note:n_024",
    "note:n_028",
    "note:n_031",
    "note:scale-negative",
    "note:scale-positive",
    "profile"
  ],
  "selected_noise_sources": [],
  "note_selection": {
    "shortlist": [
      "e01486",
      "e01481",
      "e01468",
      "e01488",
      "e01477",
      "e01462",
      "e01485",
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
      "pid": 28852,
      "returncode": 0,
      "elapsed": 13.475590200003353,
      "stopped": true,
      "cancelled": false
    }
  ],
  "api_calls": 21
}
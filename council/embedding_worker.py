"""One bounded native encoder process. Only the parent chooses its files/model."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
REVISION = 'c9745ed1d9f207416be6d2e6f8de32d1f16199bf'


def work(request):
    # Import/load occurs inside the managed process, so cancellation also stops native work.
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL, revision=REVISION, device='cpu', cache_folder=request['cache'])
    limit = model.max_seq_length - model.tokenizer.num_special_tokens_to_add(pair=False)
    rows = []
    if request['operation'] == 'index':
        for source in request['sources']:
            text = source['text']
            paragraphs = [(m.start(), m.end()) for m in re.finditer(r'.+?(?:\n\s*\n|\Z)', text, re.S)]
            section = '/'
            # Keep every source character, including whitespace, with exact offsets.
            for para_start, para_end in paragraphs:
                paragraph = text[para_start:para_end]
                if paragraph.lstrip().startswith('#'):
                    section = paragraph.strip().splitlines()[0][:600]
                offsets = model.tokenizer(paragraph, add_special_tokens=False, truncation=False,
                                          return_offsets_mapping=True)['offset_mapping']
                start = para_start
                boundaries = [para_start + offsets[i][0] for i in range(limit, len(offsets), limit)] + [para_end]
                for end in boundaries:
                    while start < end:
                        stop = end
                        while len(text[start:stop].encode('utf-8')) > request['chunk_bytes']:
                            stop = start + max(1, (stop - start) // 2)
                        chunk = text[start:stop]
                        # Bound even odd token/character boundaries rather than silently truncate.
                        while len(model.tokenizer(chunk, add_special_tokens=False)['input_ids']) > limit:
                            stop = start + max(1, (stop - start) // 2)
                            chunk = text[start:stop]
                        rows.append({'source_id': source['source_id'], 'text': chunk, 'start': start, 'end': stop, 'section': section})
                        if len(rows) > request['max_chunks']:
                            raise ValueError('chunk budget')
                        start = stop
        texts = [r['text'] for r in rows]
    else:
        texts = request['texts']
        for text in texts:
            if len(model.tokenizer(text, add_special_tokens=False)['input_ids']) > limit:
                raise ValueError('query exceeds encoder token limit')
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()
    return {'rows': rows, 'vectors': vectors, 'model': MODEL, 'revision': REVISION,
            'max_seq_length': model.max_seq_length, 'token_limit': limit, 'normalized': True,
            'chunking': 'tokenizer-paragraphs-v1', 'overlap_tokens': 0, 'offset_unit': 'unicode_characters'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--request', required=True)
    parser.add_argument('--response', required=True)
    args = parser.parse_args()
    request = json.loads(Path(args.request).read_text(encoding='utf-8'))
    result = work(request)
    Path(args.response).write_text(json.dumps(result, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
    main()

"""Materialize selected native fields; complete originals remain in frozen backup.

The public JSON is a provenance-labelled projection, not full-record byte
identity. Existing full records are accepted only when selected fields match.
"""
from pathlib import Path
import hashlib,json

SHA='b6decc5ffedd121e6b671562151ba8faaa523aa9462e68d460bff92277834eb8'
ROOT=Path(__file__).resolve().parents[1]

def matches_subset(full,selected):
    if isinstance(selected,dict):
        return isinstance(full,dict) and all(k in full and matches_subset(full[k],v) for k,v in selected.items())
    return full==selected

def restore_inputs(root=ROOT):
    root=Path(root);blob=(root/'inputs/PARENT_SCIENCE.json').read_bytes()
    if hashlib.sha256(blob).hexdigest()!=SHA:raise ValueError('HE29_INPUT_ARCHIVE_SHA')
    data=json.loads(blob);count=0
    for name,spec,n,table,results,original_shas in data['rows']:
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('HE29_INPUT_UNSAFE_MEMBER')
        values={'IDENTITY.json':dict(data['shared'],spec=spec,n=n,source_table_nodes=512),
                'RESULT.json':dict(status='SCOPED_NATIVE_COMPLETED',source_table_sha256=table,results=results),
                'TABLE.json':dict(source_table_sha256=table)}
        for filename,selected in values.items():
            out=root/'inputs'/rel/filename
            if out.exists():
                try:valid=matches_subset(json.loads(out.read_text()),selected)
                except (ValueError,UnicodeError):valid=False
                if not valid:raise ValueError('HE29_INPUT_EXISTING_MISMATCH')
            else:
                out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('x') as f:json.dump(selected,f,indent=2,allow_nan=False)
            count+=1
    if count!=21:raise ValueError('HE29_INPUT_MEMBER_COUNT')
    return count

if __name__=='__main__':print('Verified/restored parent selected records:',restore_inputs())

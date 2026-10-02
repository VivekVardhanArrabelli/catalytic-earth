"""Execute the intact pinned public RFD3 load/build/parse API without a model."""
from pathlib import Path
import argparse, hashlib, importlib.metadata, inspect, json, random, sys, traceback

root=Path(__file__).resolve().parent
INPUT_PARSING_SHA256='79baccb07cc65924ffd833615e5de6bcb186eeb1c87eedbc4324777c63f7e9ee'
parser=argparse.ArgumentParser()
parser.add_argument('--input',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--foundry-root',type=Path,default=root/'foundry')
parser.add_argument('--source-receipt',type=Path,default=None)
args=parser.parse_args()
foundry=args.foundry_root.resolve()
sys.path[:0]=[str(foundry/'src'),str(foundry/'models/rfd3/src')]
args.output.mkdir(exist_ok=False)
receipt={'status':'starting','inference':False,'model_weights_loaded':False,
         'source_commit':'0932f1cb165ae7d413c11b1a7acc04ee31758817',
         'input':str(args.input.resolve()),'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
         'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'versions':{},'stages':[]}

def save(name,value):
    p=args.output/name
    p.write_text(json.dumps(value,indent=2,default=lambda x:x.tolist())+'\n')
    return {'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def snapshot(aa):
    return {'annotations':{k:aa.get_annotation(k).tolist() for k in aa.get_annotation_categories()},
            'coordinates':aa.coord.tolist(),'bonds':None if aa.bonds is None else aa.bonds.as_array().tolist()}

try:
    import numpy as np
    import torch
    from rfd3.inference.datasets import ContigJsonDataset
    from rfd3.inference.input_parsing import DesignInputSpecification,ensure_input_is_abspath
    for name in ('torch','pydantic','numpy','atomworks','biotite','rdkit','lightning','hydra-core'):
        receipt['versions'][name]=importlib.metadata.version(name)
    receipt['torch_path']=torch.__file__
    native_path=Path(inspect.getfile(DesignInputSpecification)).resolve()
    receipt['native_api_file']=str(native_path)
    receipt['native_api_sha256']=hashlib.sha256(native_path.read_bytes()).hexdigest()
    assert native_path.is_relative_to(foundry), 'Imported native API is outside the requested Foundry source tree'
    assert receipt['native_api_sha256']==INPUT_PARSING_SHA256, 'Pinned native input API bytes changed'
    source_receipt=args.source_receipt or root/'runtime_source_receipt.json'
    if source_receipt.exists():
        source_manifest=json.loads(source_receipt.read_text())
        expected=next(x['sha256'] for x in source_manifest['extracted_files'] if x['path']=='models/rfd3/src/rfd3/inference/input_parsing.py')
        assert expected==INPUT_PARSING_SHA256
        receipt['source_receipt_sha256']=hashlib.sha256(source_receipt.read_bytes()).hexdigest()
    elif args.source_receipt is not None:
        raise FileNotFoundError(source_receipt)
    random.seed(0); np.random.seed(0); torch.manual_seed(0)
    # Native dataset performs the author's global_args wrapper merge.
    dataset=ContigJsonDataset(data=str(args.input.resolve()),cif_parser_args={},transform=None,
                             name='native_acceptance_only',subset_to_keys=None,eval_every_n=1)
    assert dataset.names==['des']
    # Native helper resolves the relative PDB path exactly as dataset __getitem__ does.
    params=ensure_input_is_abspath(dataset.data['des'],dataset.json_path)
    params['cif_parser_args']={}
    spec=DesignInputSpecification.safe_init(**params)
    receipt['stages'].append({'stage':'native_load_and_annotation',**save('native_loaded_atoms.json',snapshot(spec.atom_array_input))})
    # Entire native de novo build, ligand append, mask application, origin and reparse.
    data=spec.to_pipeline_input(example_id='des')
    receipt['stages'].append({'stage':'native_build_and_pipeline_parse',**save('native_built_atoms.json',snapshot(data['atom_array']))})
    receipt['specification']=data['specification']
    receipt['status']='native_load_build_and_pipeline_parse_completed_pending_chemical_review'
except BaseException:
    receipt['status']='native_acceptance_failed'
    receipt['error']=traceback.format_exc()
    raise
finally:
    save('native_execution_receipt.json',receipt)

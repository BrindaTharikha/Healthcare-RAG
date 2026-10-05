import pathlib



project_root_dir = pathlib.Path(__file__).parent.parent
raw_data_dir = project_root_dir / "data" / "raw"
processed_data_dir = project_root_dir / "data" / "processed" 
index_dir = project_root_dir / "data" / "processed" / "index"
cache_dir = project_root_dir / ".cache"
log_dir = project_root_dir / "logs"

folders_to_create = [processed_data_dir, index_dir, cache_dir, log_dir]

for folder in folders_to_create:
    folder.mkdir(parents=True, exist_ok=True)   


CHUNK_SIZE =1000
CHUNK_OVERLAP = 150
TOPK= 4
LLM_RETRY_COUNT = 2
CACHE_TTL_IN_SECONDS = 7 * 24 * 60 * 60
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
import os 
from langdetect import detect 
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm   


def safe_detect(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"


def count_languages(*datasets, n_workers=None, chunksize=1_000, show_progress=True):
    if n_workers is None:
        try:
            n_workers = len(os.sched_getaffinity(0))
        except AttributeError:
            n_workers = os.cpu_count() or 1

    # sample → text 변환을 미리 수행
    all_texts = (s.get("text", "")          # 문자열만 워커에 전달
                 for ds in datasets
                 for s  in ds)
    total_len = sum(len(ds) for ds in datasets)

    counter = Counter()
    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        iterator = pool.map(safe_detect, all_texts, chunksize=chunksize)
        for lang in tqdm(iterator, total=total_len, disable=not show_progress):
            counter[lang] += 1

    return counter



def filter_non_english_samples_mp(
    data,
    lang: str = "en",
    n_workers: int | None = None,
    chunksize: int = 1000,
    is_tqdm: bool = False,
):
    n_workers = n_workers or len(os.sched_getaffinity(0))

    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        langs = list(
            tqdm(
                pool.map(safe_detect, (s.get("text", "") for s in data), chunksize=chunksize),
                total=len(data),
                disable=not is_tqdm,
            )
        )

    return [sample for sample, l in zip(data, langs) if l == lang]

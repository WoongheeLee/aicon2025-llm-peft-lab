# PEFT 기반 LLM 미세조정 템플릿

PEFT(Parameter-Efficient Fine-Tuning) 기법을 활용한 LLM 미세조정 템플릿

- [미세조정 템플릿 노트북](./notepad/llm-efficient-tune.ipynb)

## 참고

실습 코드는 [AAiCON2025 실용인공지능 컨퍼런스](https://aifrenz.org/allday)의  
**"NVIDIA X Google Cloud End to End LLM Bootcamp"** (강사: NVIDIA 유현곤) 세션 중 LLM 미세조정(파인튜닝) 부분을 정리한 것입니다.

- 데이터 전처리에는 **멀티프로세싱**을 적용하여 빠른 처리 속도를 구현했습니다.
- 추후 다양한 공개 데이터셋과 Huggingface 모델에도 확장 적용 가능합니다.
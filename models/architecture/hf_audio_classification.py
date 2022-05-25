# template-name: Audio Classification Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> AudioClassificationPipeline
import transformers

pipe = transformers.pipeline('audio-classification', model=None)
result = pipe()
# models: https://huggingface.co/models?filter=audio-classification
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.AudioClassificationPipeline

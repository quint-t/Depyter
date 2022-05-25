# template-name: Translation Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> TranslationPipeline
import transformers

pipe = transformers.pipeline('translation', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=translation
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TranslationPipeline

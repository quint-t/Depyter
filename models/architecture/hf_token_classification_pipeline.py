# template-name: Token Classification Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> TokenClassificationPipeline
import transformers

pipe = transformers.pipeline('token-classification', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=token-classification
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TokenClassificationPipeline

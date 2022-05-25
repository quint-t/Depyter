# template-name: Text Classification Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> TextClassificationPipeline
import transformers

pipe = transformers.pipeline('text-classification', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=text-classification
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextClassificationPipeline

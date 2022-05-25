# template-name: Image Classification Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> ImageClassificationPipeline
import transformers

pipe = transformers.pipeline('image-classification', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=image-classification
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.ImageClassificationPipeline

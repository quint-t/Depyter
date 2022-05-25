# template-name: Text Generation Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> TextGenerationPipeline
import transformers

pipe = transformers.pipeline('text-generation', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=text-generation
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.TextGenerationPipeline

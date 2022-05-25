# template-name: Text2Text Generation Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> Text2TextGenerationPipeline
import transformers

pipe = transformers.pipeline('text2text-generation', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=text2text-generation
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.Text2TextGenerationPipeline

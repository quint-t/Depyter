# template-name: Conversational Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> ConversationalPipeline
import transformers

pipe = transformers.pipeline('conversational', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=conversational
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.ConversationalPipeline

# template-name: Summarization Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> SummarizationPipeline
import transformers

pipe = transformers.pipeline('summarization', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=summarization
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.SummarizationPipeline

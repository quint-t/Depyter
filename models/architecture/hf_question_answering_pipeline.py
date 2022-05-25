# template-name: Question Answering Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> QuestionAnsweringPipeline
import transformers

pipe = transformers.pipeline('question-answering', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=question-answering
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.QuestionAnsweringPipeline

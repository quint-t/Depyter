# template-name: Fill Mask Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> FillMaskPipeline
import transformers

pipe = transformers.pipeline('fill-mask', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=fill-mask
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.FillMaskPipeline

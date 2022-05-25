# template-name: Feature Extraction Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> FeatureExtractionPipeline
import transformers

pipe = transformers.pipeline('feature-extraction', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=feature-extraction
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.FeatureExtractionPipeline

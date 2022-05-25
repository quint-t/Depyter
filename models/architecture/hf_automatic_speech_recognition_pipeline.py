# template-name: Automatic Speech Recognition Pipeline
# template-type: Hugging-Face Pipelines
# <code-block> AutomaticSpeechRecognitionPipeline
import transformers

pipe = transformers.pipeline('automatic-speech-recognition', model=None)
result = pipe()
# models: https://huggingface.co/models?pipeline_tag=automatic-speech-recognition
# help: https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline

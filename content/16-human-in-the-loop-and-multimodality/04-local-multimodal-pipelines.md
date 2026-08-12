# Local Multimodal Pipelines

## Learning objectives

- Design an inspectable pipeline for image, audio, and text inputs.
- Run an optional vision-language model locally.
- Preserve modality provenance, transformations, and confidence boundaries.

## Multimodal does not mean one opaque call

A useful pipeline separates acquisition, validation, preprocessing, inference, evidence extraction, and output. For an image, validate MIME type from bytes, dimensions, file size, and decompression limits; remove unnecessary metadata; create a derived preview; then pass the approved derivative to a model. Keep the original hash and transformation record so the result is reproducible.

Vision-language models can describe scenes and answer questions, but small details, text, counts, and spatial relationships are common failure points. OCR, object detection, and metadata are independent evidence channels. When an answer matters, compare channels instead of trusting a fluent caption. Never infer sensitive personal attributes from appearance without a lawful, necessary, reviewed purpose.

For audio, separate decoding, segmentation, transcription, speaker handling, and summarization. A transcript is derived evidence and should include timestamps. Do not claim speaker identity from voice unless the product has a legitimate biometric process and strong controls.

## Free local practice

Choose three images you created or that are openly licensed: a document page, a chart, and an everyday scene. Do not use private faces or documents. Create a manifest with path, SHA-256, license/source, dimensions, and intended test questions.

Use Pillow to validate and normalize images. Reject files above your chosen pixel or byte limit and call `Image.verify()` before decoding. For the document page, run local Tesseract OCR. For the chart, also keep the underlying CSV if available.

Optionally install Ollama and a supported vision model that fits your hardware. Send the normalized image plus a narrowly scoped prompt through the local API. Store model identifier, prompt, image hash, latency, and response. Ask:

- What is directly visible?
- What text was read, with uncertain spans marked?
- What cannot be determined from this image?

Compare the VLM result with OCR and a human observation table. For every factual statement, label the evidence channel: pixels/VLM, OCR, metadata, source data, or human verification. Deliberately crop away critical context and verify that the system reports uncertainty rather than reconstructing it.

## Completion criteria

- Inputs are validated by content and bounded before model decoding.
- Every inference is tied to an original hash, derivative hash, transformation, prompt, and model ID.
- OCR/VLM disagreement is surfaced rather than silently resolved.
- A context-removal test produces an abstention or explicit limitation.

## References

- [Hugging Face image-text-to-text guide](https://huggingface.co/docs/transformers/main/tasks/image_text_to_text) - public VLM concepts and local inference examples.
- [Ollama vision documentation](https://docs.ollama.com/capabilities/vision) - passing images to locally served vision models.
- [Pillow image file formats and limits](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) - image decoding behavior and format support.
- [Tesseract user manual](https://tesseract-ocr.github.io/tessdoc/) - open-source local OCR documentation.
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) - validation, storage, and resource-limit controls.

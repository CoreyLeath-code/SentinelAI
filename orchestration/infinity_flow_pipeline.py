class InfinityFlowPipeline:
    def __init__(self, ingestion, inference, tracking):
        self.ingestion = ingestion
        self.inference = inference
        self.tracking = tracking

    def run(self, input_data):
        processed = self.ingestion.process(input_data)
        result = self.inference(processed)
        self.tracking(result)
        return result

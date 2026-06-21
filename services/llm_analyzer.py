import os
from openai import OpenAI

class SentinelLLMAnalyzer:
    def __init__(self):
        # Initialized with enterprise-grade connection practices
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o" # Using standard production-grade GPT-4 omni

    def analyze_system_incident(self, alert_payload: dict, system_logs: list) -> dict:
        """
        Parses active system anomalies and leverages GPT-4 for automated 
        root-cause isolation and remediation strategy maps.
        """
        system_prompt = (
            "You are an L6 Staff Site Reliability Engineer and MLOps Architect. "
            "Analyze the provided data drift alert and system logs. Provide a structured "
            "Root Cause Analysis (RCA) and explicit, automated mitigation steps."
        )
        
        user_content = f"ALERT METRICS:\n{alert_payload}\n\nRECENT SYSTEM TRACES:\n{system_logs}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2, # Low temperature ensures deterministic, analytical output
                response_format={ "type": "json_object" } # Force structured payload
            )
            return response.choices[0].message.content
        except Exception as e:
            return {"error": f"LLM Telemetry Analysis Engine Failure: {str(e)}"}

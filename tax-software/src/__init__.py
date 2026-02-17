# Add OpenTelemetry tracing setup
from agent_framework.observability import configure_otel_providers
configure_otel_providers(
	vs_code_extension_port=4317,  # AI Toolkit gRPC port
	enable_sensitive_data=True  # Enable capturing prompts and completions
)

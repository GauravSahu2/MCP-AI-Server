# apps/mcp-server/security/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import RESOURCE_ATTRIBUTES, Resource
import os

def setup_tracing(app, service_name):
    # Resource labels
    resource = Resource.create({
        RESOURCE_ATTRIBUTES.SERVICE_NAME: service_name,
        "environment": os.getenv("ENV", "production"),
        "region": os.getenv("REGION", "aws-us-east-1")
    })

    # OTLP Exporter (pointing to Jaeger/Tempo)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
        insecure=True
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

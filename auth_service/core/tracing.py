from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from core.config import settings


def init_tracer(app):
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": settings.jaeger_service_name})
        )
    )

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.jaeger_host,
        agent_port=settings.jaeger_port,
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    FastAPIInstrumentor.instrument_app(app)

    app.add_middleware(OpenTelemetryMiddleware)

    return app

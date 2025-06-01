# Dummy C Extension

This is a minimal Python C extension created specifically to demonstrate build tool requirements in Docker slim images.

## Purpose

This package will **always fail** to install on `python:3.10-slim` images because:
- It contains C source code that needs compilation
- Slim images don't include `gcc` or `python3-dev` headers
- There are no pre-built wheels available (since we control this package)

## What it does

- Contains a simple C function that returns "Hello from C!"
- Minimal setup.py that defines the C extension
- Will trigger compilation during `pip install`
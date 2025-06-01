from setuptools import setup, Extension

# This is a dummy C extension that will fail to build without gcc
dummy_extension = Extension(
    'dummy_c_module',
    sources=['dummy_c_module.c']
)

setup(
    name='dummy-c-extension',
    version='0.1.0',
    description='A dummy C extension to demonstrate build tool requirements',
    ext_modules=[dummy_extension],
    zip_safe=False,
)
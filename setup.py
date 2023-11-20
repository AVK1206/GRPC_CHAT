from setuptools import setup, find_packages

setup(
    name='grpc_chat',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'protobuf',
    ],
    entry_points={
        'console_scripts': [
            'grpc_chat_server=grpc_chat.server:run_server',
            'grpc_chat_client=grpc_chat.client:run_client',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

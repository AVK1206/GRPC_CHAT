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
    description='A simple client-server chat application using gRPC in Python with Etcd3 for message storage.'
                'The server supports operations like retrieving a list of users, sending messages, '
                'and broadcasting new messages to subscribed clients.',
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
    project_urls={
        'Documentation': 'https://grpc.io/docs/languages/python/quickstart/',
        'Source Code': 'https://github.com/AVK1206/GRPC_CHAT',
    },

)

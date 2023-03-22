# Copyright 2021 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC hellostreamingworld.MultiGreeter client."""

import asyncio
import logging
from typing import List

import grpc
import hellostreamingworld_pb2
import hellostreamingworld_pb2_grpc


SERVER_DNS = "greeter"
SERVER_PORT = 50051

async def async_get_response_from_greeter(count: int) -> List[str]:
    async with grpc.aio.insecure_channel(f"{SERVER_DNS}:{SERVER_PORT}") as channel:
        stub = hellostreamingworld_pb2_grpc.MultiGreeterStub(channel)

        # Direct read from the stub
        hello_stream = stub.sayHello(
            hellostreamingworld_pb2.HelloRequest(name="you", num_greetings=f"{count}"))
        responses = []
        while True:
            response = await hello_stream.read()
            if response == grpc.aio.EOF:
                break
            responses.append(response.message)
        return responses


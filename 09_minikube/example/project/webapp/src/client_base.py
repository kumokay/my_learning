import grpc


class ClientBase:
    SERVER_DNS = "localhost"
    SERVER_PORT = 50051

    @classmethod
    def get_channel(cls) -> grpc.aio.Channel:
        target = f"{cls.SERVER_DNS}:{cls.SERVER_PORT}"
        return grpc.aio.insecure_channel(target)
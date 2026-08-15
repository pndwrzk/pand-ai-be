# from qdrant_client import QdrantClient

# from app.core.config import settings


# class Qdrant:

#     def __init__(self):

#         self.client = QdrantClient(
#             host=settings.QDRANT_HOST,
#             port=settings.QDRANT_PORT,
#         )


#     def close(self):

#         self.client.close()


from qdrant_client import QdrantClient

from app.core.config import settings


class Qdrant:

    def __init__(self):
        self.client = QdrantClient(
            url="https://80cc9bc5-33a3-451e-913a-1737f0ab21d1.eu-west-2-0.aws.cloud.qdrant.io",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NTU2NzI0ZTUtNDA2OS00MTUwLWI0ZTEtZDY2MWEwYmE5NDVhIn0.zEgBrHGBiHXlA6Q8P4ned6NDpdJMTWxEYxB1vToC4lM",
        )

    def close(self):
        self.client.close()
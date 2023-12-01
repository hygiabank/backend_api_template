import uvicorn
from .settings import settings

def main():
    uvicorn.run(
        "app:create_app",
        factory=True,
        reload=settings.DEBUG,
        host=settings.API_HOST,
        port=settings.API_PORT
    )

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

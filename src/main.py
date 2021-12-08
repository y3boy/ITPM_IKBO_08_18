import os


def main():
    os.system("uvicorn src.app.api:app --reload --reload-dir app --reload-dir db --reload-dir models --reload-dir repositories --reload-dir routers")


if __name__ == '__main__':
    main()

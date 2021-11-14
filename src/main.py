import os


def main():
    os.system("uvicorn src.app.api:app --reload")


if __name__ == '__main__':
    main()

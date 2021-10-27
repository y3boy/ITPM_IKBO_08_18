import os


def main():
    os.system("uvicorn app.api:app --reload")


if __name__ == '__main__':
    main()

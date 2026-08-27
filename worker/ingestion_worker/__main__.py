import time

if __name__ == '__main__':
    print('Ingestion worker boundary ready; connect Redis/Celery or arq in deployment configuration.')
    while True:
        time.sleep(3600)

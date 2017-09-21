FROM python:3.4-onbuild
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["server.py"]
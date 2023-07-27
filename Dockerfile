FROM python:3.9.1

WORKDIR /amazon_scrape

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]
FROM python:slim
ENV TOKEN=
COPY . .
RUN pip install -r requirements.txt
CMD python tr_bot.py
FROM python:3.9
RUN mkdir /world_cup_chips_pool
WORKDIR /world_cup_chips_pool
ADD . /world_cup_chips_pool/
RUN pip install -r requirements.txt
CMD bash
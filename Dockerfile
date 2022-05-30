FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install python3-pip -y
RUN mkdir /root/contracthacker
WORKDIR /root/contracthacker
COPY requirements.txt /root/contracthacker
RUN pip3 install -r requirements.txt
COPY . /root/contracthacker
RUN chmod +x setup.sh && ./setup.sh
CMD ["python3","run.py"]
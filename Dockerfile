FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main


RUN apt-get update && apt-get -y install \
	python \
	python-pip \
	wget \
	zip \
	mercurial \
	curl \
	unzip \
	libtbb-dev \
	libtbb2 \
	bowtie2

RUN pip install --upgrade pip
RUN pip install grep numpy matplotlib scipy biopython dendropy cmseq phylophlan biom-format metaphlan 



ENV PATH="/metaphlan/bowtie2-2.4.5:$PATH"
ENV PATH="/metaphlan/metaphlan:$PATH"
ENV PATH="/metaphlan/metaphlan:utils:$PATH"
RUN metaphlan --install --bowtie2db /metaphlan/metaphlan_databases

# You can use local data to construct your workflow image.  Here we copy a
# pre-indexed reference to a path that our workflow can reference.


# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root

# PYTHON CONTAINER WITH QUARTO
#
# Install Quarto into a base Python image according to instructions from 
# https://www.r-bloggers.com/2022/07/how-to-set-up-quarto-with-docker-part-1-static-content/.
# 
# Installing pandoc-citeproc fails with "Package 'pandoc-citeproc' has no
# installation candidate", which is addressed in a Stack Overflow question:
# https://stackoverflow.com/questions/64392026/error-running-filter-pandoc-citeproc-could-not-find-executable-pandoc-citeproc
#
# =============================================================================

# Download and install base Python image
FROM --platform=linux/amd64 python:3.11

# Non-root user
ARG USERNAME=jovyan
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && export PATH='/home/jovyan/.local/bin'
    
# Download and install Quarto
USER root
RUN apt-get install -y --no-install-recommends \
    pandoc \
    curl \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
RUN gdebi --non-interactive quarto-linux-amd64.deb
RUN quarto install extension schochastics/academicons --no-prompt

# Copy requirements into container
COPY requirements.txt .

# Update pip and install Python package dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER $USERNAME

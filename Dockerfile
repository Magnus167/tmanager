# Use an official Ubuntu base image
FROM ubuntu:latest

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential git libowfat-dev && \
    rm -rf /var/lib/apt/lists/*

# Clone the opentracker repository
RUN git clone git://erdgeist.org/opentracker

# Compile opentracker
WORKDIR /opentracker
RUN make

# Expose the default port
EXPOSE 9080

# Run opentracker
CMD ["./opentracker", "-p", "9080"]


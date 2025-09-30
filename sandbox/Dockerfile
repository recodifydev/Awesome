FROM ubuntu:24.04

# Install required packages
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-terminal \
    chromium-browser \
    vnc4server \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Create sandbox user
RUN useradd -m -s /bin/bash sandbox
USER sandbox
WORKDIR /home/sandbox

# Set up VNC
RUN mkdir ~/.vnc && \
    echo "password" | vncpasswd -f > ~/.vnc/passwd && \
    chmod 600 ~/.vnc/passwd

# Set up environment variables
ENV DISPLAY=:1 \
    CHROME_PORT=9222 \
    VNC_PORT=5900 \
    HOME=/home/sandbox

# Copy application files
COPY --chown=sandbox:sandbox app/ /app/

# Expose ports
EXPOSE $CHROME_PORT
EXPOSE $VNC_PORT

# Start services
CMD ["sh", "-c", "vncserver :1 -geometry 1280x1024 -depth 24 && tail -f ~/.vnc/*.log"]
FROM ubuntu:22.04

# Update and install OpenSSH server and tmux
RUN apt-get update && \
    apt-get install -y openssh-server tmux sudo vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory for ssh to work
RUN mkdir /var/run/sshd

# Configure SSH to run on port 2222
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Create ctf-player user with restricted permissions
RUN useradd -m -d /home/ctf-player -s /bin/bash ctf-player && \
    echo "ctf-player:password" | chpasswd

# Create challenge directory with proper permissions from the start
RUN mkdir -p /home/ctf-player/challenge && \
    chown root:root /home/ctf-player/challenge && \
    chmod 555 /home/ctf-player/challenge

# Create a temp directory where ctf-player can write
RUN mkdir -p /tmp/ctf-player-writable && \
    chown ctf-player:ctf-player /tmp/ctf-player-writable && \
    chmod 700 /tmp/ctf-player-writable 

# Configure .bashrc with read-only settings
RUN echo 'if [[ -z "$TMUX" && -n "$SSH_CONNECTION" ]]; then' >> /home/ctf-player/.bashrc && \
    echo '    cd /home/ctf-player/challenge' >> /home/ctf-player/.bashrc && \
    echo '    exec /usr/local/bin/tmux_setup.sh' >> /home/ctf-player/.bashrc && \
    echo 'fi' >> /home/ctf-player/.bashrc && \
    echo "export TMPDIR=/tmp/ctf-player-writable" >> /home/ctf-player/.bashrc && \
    echo "set -o noclobber" >> /home/ctf-player/.bashrc && \
    echo "alias rm='rm -i --preserve-root'" >> /home/ctf-player/.bashrc && \
    echo "alias cp='cp -i'" >> /home/ctf-player/.bashrc && \
    echo "alias mv='mv -i'" >> /home/ctf-player/.bashrc && \
    echo "" >> /home/ctf-player/.bashrc && \
    echo "# Block any attempts to start a new shell" >> /home/ctf-player/.bashrc && \
    echo "function bash() { echo 'Sorry, starting a new shell is not allowed'; }" >> /home/ctf-player/.bashrc && \
    echo "function sh() { echo 'Sorry, starting a new shell is not allowed'; }" >> /home/ctf-player/.bashrc && \
    echo "function zsh() { echo 'Sorry, starting a new shell is not allowed'; }" >> /home/ctf-player/.bashrc && \
    echo "function ksh() { echo 'Sorry, starting a new shell is not allowed'; }" >> /home/ctf-player/.bashrc && \
    echo "" >> /home/ctf-player/.bashrc && \
    echo "# Prevent users from attaching to other tmux sessions" >> /home/ctf-player/.bashrc && \
    echo "function tmux() {" >> /home/ctf-player/.bashrc && \
    echo "  # Block attach commands" >> /home/ctf-player/.bashrc && \
    echo "  if [[ \"\$1\" == \"attach\"* || \"\$1\" == \"a\"* || \"\$1\" == \"attach-session\"* || \"\$1\" == \"switchc\"* || \"\$1\" == \"switch-client\"* ]]; then" >> /home/ctf-player/.bashrc && \
    echo "    echo \"Sorry, attaching to other sessions is not allowed\"" >> /home/ctf-player/.bashrc && \
    echo "    return 1" >> /home/ctf-player/.bashrc && \
    echo "  fi" >> /home/ctf-player/.bashrc && \
    echo "  # Block listing sessions" >> /home/ctf-player/.bashrc && \
    echo "  if [[ \"\$1\" == \"ls\"* || \"\$1\" == \"list-sessions\"* ]]; then" >> /home/ctf-player/.bashrc && \
    echo "    echo \"Sorry, listing sessions is not allowed\"" >> /home/ctf-player/.bashrc && \
    echo "    return 1" >> /home/ctf-player/.bashrc && \
    echo "  fi" >> /home/ctf-player/.bashrc && \
    echo "  # Block new-session commands" >> /home/ctf-player/.bashrc && \
    echo "  if [[ \"\$1\" == \"new-session\"* || \"\$1\" == \"new\"* ]]; then" >> /home/ctf-player/.bashrc && \
    echo "    echo \"Sorry, creating new sessions is not allowed\"" >> /home/ctf-player/.bashrc && \
    echo "    return 1" >> /home/ctf-player/.bashrc && \
    echo "  fi" >> /home/ctf-player/.bashrc && \
    echo "  # Block shell-related commands" >> /home/ctf-player/.bashrc && \
    echo "  if [[ \"\$*\" == *\"shell\"* || \"\$*\" == *\"/bin/bash\"* || \"\$*\" == *\"/bin/sh\"* || \"\$*\" == *\"exec\"* || \"\$*\" == *\"spawn\"* ]]; then" >> /home/ctf-player/.bashrc && \
    echo "    echo \"Sorry, executing shell commands directly is not allowed\"" >> /home/ctf-player/.bashrc && \
    echo "    return 1" >> /home/ctf-player/.bashrc && \
    echo "  fi" >> /home/ctf-player/.bashrc && \
    echo "  # Allow other tmux commands" >> /home/ctf-player/.bashrc && \
    echo "  command tmux \"\$@\"" >> /home/ctf-player/.bashrc && \
    echo "}" >> /home/ctf-player/.bashrc

# Copy the configuration files from local directory
COPY .tmux.conf /home/ctf-player/.tmux.conf
COPY .vimrc /home/ctf-player/.vimrc
COPY setup_challenge.sh /usr/local/bin/setup_challenge.sh
COPY tmux_setup.sh /usr/local/bin/tmux_setup.sh

# Set correct permissions for the files
RUN chmod +x /usr/local/bin/setup_challenge.sh /usr/local/bin/tmux_setup.sh && \
    chmod 444 /home/ctf-player/.tmux.conf /home/ctf-player/.vimrc && \
    chown ctf-player:ctf-player /home/ctf-player/.tmux.conf /home/ctf-player/.vimrc

# Run the challenge setup script to create the environment with writable permissions
RUN /usr/local/bin/setup_challenge.sh

# Now restrict permissions on home directory and its contents
RUN chmod -R 555 /home/ctf-player/challenge && \
    chmod 444 /home/ctf-player/.bashrc && \
    chown ctf-player:ctf-player /home/ctf-player/.bashrc

# Expose the SSH port
EXPOSE 2222

# Command to run when starting the container
CMD ["/usr/sbin/sshd", "-D"]

#!/bin/bash

# Create a unique session ID based on client IP and timestamp
CLIENT_IP=$(echo $SSH_CONNECTION | cut -d" " -f1)
SESSION_ID="ssh-${CLIENT_IP}-$(date +%s)"  # Simplified timestamp without nanoseconds

# Set the challenge directory
CHALLENGE_DIR="/home/ctf-player/challenge"
cd $CHALLENGE_DIR

# Set up cleanup function to ensure the tmux session is terminated
cleanup() {
    tmux kill-session -t "$SESSION_ID" 2>/dev/null || true
}

# Register trap to ensure cleanup on exit
trap cleanup EXIT INT TERM

# Start a session with all our windows and panes, using the custom .tmux.conf file
# Set destroy-unattached option to automatically clean up the session when detached
#exec tmux -f /home/ctf-player/.tmux.conf \
#    new-session -s "$SESSION_ID" "cd $CHALLENGE_DIR; exec $SHELL" \; \


# Start a session with all our windows and panes, using the custom .tmux.conf file
exec tmux -f /home/ctf-player/.tmux.conf new-session -s "$SESSION_ID" "cd $CHALLENGE_DIR; exec $SHELL" \; \
    set-option destroy-unattached on \; \
    set-option exit-unattached on \; \
    rename-window "Main" \; \
    send keys "cat $CHALLENGE_DIR/user_welcome.txt" C-m \; \
    split-window -v "cd $CHALLENGE_DIR; exec $SHELL" \; \
    split-window -h "cd $CHALLENGE_DIR; cat $CHALLENGE_DIR/system/tmux_system.txt ; exec $SHELL" \; \
    select-pane -t 1 \; \
    send-keys "clear" C-m \; \
    select-pane -t 2 \; \
    send-keys "clear" C-m \; \
    new-window -n "Game Development" "cd $CHALLENGE_DIR; echo 'dalctf{v1m_4nd_7mux_f7w}' ; vim $CHALLENGE_DIR/file.txt ; exec $SHELL" \; \
    split-window -h "cd $CHALLENGE_DIR; echo 'Using custom tmux configuration'; cat ~/.tmux.conf; exec $SHELL" \; \
    select-pane -t 2 \; \
    resize-pane -Z \; \
    new-window -n "MISC" "cd $CHALLENGE_DIR; echo 'CTF Challenge Info'; exec $SHELL" \; \
    split-window -h "cd $CHALLENGE_DIR; echo 'This setup uses your custom .tmux.conf and .vimrc files'; exec $SHELL" \; \
    select-window -t 0 \; \
    select-pane -t 1


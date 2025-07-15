#!/bin/bash

# Set the challenge directory
CHALLENGE_DIR="/home/ctf-player/challenge"
cd $CHALLENGE_DIR

# Create necessary directories
mkdir -p $CHALLENGE_DIR/system $CHALLENGE_DIR/logs

# Setup initial files we'll need with proper permissions
echo 'I have my Tmux set up with a couple of different bindings, check out .tmux.conf' > $CHALLENGE_DIR/system/tmux_system.txt
echo 'Now really, are you sure you checked all the windows on tmux? Like, all of them? Maybe theres more hidden' > $CHALLENGE_DIR/system/hint.txt
echo 'Welcome! You are logged in as ctf-player. What can you find?' > $CHALLENGE_DIR/user_welcome.txt
echo 'Flag is not here, sorry, go dig a bit more' > $CHALLENGE_DIR/system/sys.txt
echo 'Hmm, you might be close to it... But can you exit vim?' > $CHALLENGE_DIR/file.txt
echo '# Sample .tmux.conf\nset -g prefix C-a\nunbind C-b' > $CHALLENGE_DIR/.tmux.conf

# Set permissions so files can be read but not modified
find $CHALLENGE_DIR -type f -exec chmod 644 {} \;
find $CHALLENGE_DIR -type d -exec chmod 755 {} \;

echo "Challenge environment has been set up successfully."

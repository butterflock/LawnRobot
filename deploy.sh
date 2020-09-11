#!/usr/bin/env bash

rsync -r \
  --exclude=".git*" \
  --exclude=".env" \
  --exclude="img" \
  --exclude="*.jpg" \
  --exclude="*.png" \
  --exclude="deploy.sh" \
  --exclude=".*" \
  . \
  pi@lawn.robot:LawnRobotDeploy

if [ "$1" != "-t" ]; then
  echo "Restart service"
  ssh pi@lawn.robot 'sudo systemctl restart LawnRobot.service'
fi
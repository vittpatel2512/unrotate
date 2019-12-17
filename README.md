# unrotate

To build image clone unrotate repo, cd to unrotate/ directory, run:

docker build . -t [image_name]

windows:
docker run -it --rm -p 6080:80 -v "$pwd/:/root/Desktop" --name cv [image_name]

linux
sudo docker run -it --rm -p 127.0.0.1:6080:80 -v "$(pwd)/:/root/Desktop" --name cv [image_name]

In order to remote desktop to the container running on EC2 you must tunnel to the EC2 on port 6080.

cd to the Desktop of the container and run 

python3 check_panel_rotation.py 



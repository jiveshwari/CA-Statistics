# Computational Argumentation 2022 -- Assignment 1

Running the `main.py` file inside the container.
`shell $ docker run --mount type=bind,src="$(pwd)",dst=/mnt -it registry.webis.de/code-lib/public-images/upb-ca22:1.0 sh -c 'python /mnt/main.py' `

# How to run main.py

Assumption: csv file is inside ./data/

Run the above cmd and inside the container the extracted files should be available inside mnt/ directory.

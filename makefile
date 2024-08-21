.PHONY: setup

setup:
	@echo "Enter your Instagram username: "; \
	read username; \
	echo "Enter your Instagram password: "; \
	read -s password; \
	echo '{' > config.json; \
	echo '  "accounts": [' >> config.json; \
	echo '    {' >> config.json; \
	echo '      "username": "'$$username'",' >> config.json; \
	echo '      "password": "'$$password'"' >> config.json; \
	echo '    }' >> config.json; \
	echo '  ]' >> config.json; \
	echo '}' >> config.json; \
	echo "config.json has been created successfully."
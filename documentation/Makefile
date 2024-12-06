html:
	@sphinx-build -b html source ../docs/documentation
	@echo "Copie des fichiers générés vers docs/"
	@rm -rf ../docs/*
	@cp -r build/html/* ../docs/

SOURCE_DIR = source

BUILD_DIR = build/html

DEST_DIR = ../docs

SPHINX = sphinx-build

.PHONY: html clean

html:
	@echo "Génération de la documentation HTML..."
	$(SPHINX) -b html $(SOURCE_DIR) $(BUILD_DIR)
	@echo "Copie des fichiers générés vers $(DEST_DIR)"
	@rm -rf $(DEST_DIR)/*
	@cp -r $(BUILD_DIR)/* $(DEST_DIR)/

clean:
	@echo "Suppression des fichiers générés..."
	@rm -rf $(BUILD_DIR)


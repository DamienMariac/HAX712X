# Répertoire source de la documentation
SOURCE_DIR = source

# Répertoire de sortie de la documentation générée
BUILD_DIR = build/html

# Répertoire où copier les fichiers générés
DEST_DIR = ../docs

# Commande Sphinx
SPHINX = sphinx-build

# Cible par défaut : Génère la documentation HTML et la copie dans siteweb
.PHONY: html clean

html:
	@echo "Génération de la documentation HTML..."
	$(SPHINX) -b html $(SOURCE_DIR) $(BUILD_DIR)
	@echo "Copie des fichiers générés vers $(DEST_DIR)"
	@rm -rf $(DEST_DIR)/*
	@cp -r $(BUILD_DIR)/* $(DEST_DIR)/

# Nettoyer les fichiers générés
clean:
	@echo "Suppression des fichiers générés..."
	@rm -rf $(BUILD_DIR)


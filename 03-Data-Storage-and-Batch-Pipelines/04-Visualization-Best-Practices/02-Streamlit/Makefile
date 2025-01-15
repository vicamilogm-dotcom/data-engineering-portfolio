.PHONY: install

download-sql-file:
	echo "Downloading datasets"
	curl --output ./database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz

	echo "Unzipping the .gz file"
	gzip -d ./database/init/f1db.sql.gz

	echo "Setup done"

help:
	@echo The following makefile targets are available:
	@echo
	@grep -e '^\w\S\+\:' Makefile | sed 's/://g' | cut -d ' ' -f 1

gui:
	python3 ./scripts/cc-volume.py

install:
	pip install -e .

macos_app:
	rm -rf build dist
	pyinstaller --noconfirm ./cc-volume.spec

create_spec:
	pyinstaller --onedir --windowed --noconfirm ./scripts/cc-volume.py

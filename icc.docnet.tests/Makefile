.PHONY: env dev develop install test edit \
	py pot init-ru update-ru comp-cat \
	upd-cat setup test setup-requs tests \
	run-tests gdb-test clean \
	env dev dev-icc.rdfservice \
	dev-icc.restfuldocs py pot init-ru update-ru comp-cat \
	upd-cat adjust-ini devel serv serve server

LPYTHON=python3
PYTHON=$(LPYTHON)
ROOT=$(PWD)
INI=icc.cellula-test
# LCAT=src/icc/cellula/locales/

#A virtualenv name

SERVER_PORT=8082

setup:
	# $(PYTHON) setup.py build_ext # -L$(LG_LIB_DIR) -R$(LG_LIB_DIR) -I$(LG_HEADERS)
	$(PYTHON) setup.py develop

dev:	pre-dev setup-requs setup # upd-cat

devel:
	python setup.py develop

develop: dev

install: env comp-cat
	$(PYTHON) setup.py install

edit:
	cd src && emacs

setup-requs: requirements.txt
	pip install -r requirements.txt
serv server serve: test

run-tests:
	nosetests -w src/tests

test: adjust-ini
	@ip a | grep 2001 || true
	@ip a | grep 172. || true
	@echo "================================================================"
	@echo "Point Your browser to http://[::1]:$(SERVER_PORT) or http://127.0.0.1:$(SERVER_PORT)"
	@echo "================================================================"
	pserve $(INI).ini --reload
	#cd src && $(PYTHON) app.py

tests:	run-tests

dev-icc.rdfservice:
	make -C ../icc.rdfservice dev

dev-icc.restfuldocs:
	make -C ../icc.restfuldocs dev

gdb-test: setup
	gdb --args $(PYTHON) $(VB)/nosetests -w src/tests

py:
	$(PYTHON)

pot:
	mkdir -p $(LCAT)
	$(VB)/pot-create src -o $(LCAT)/messages.pot || echo "Someting unusual with pot."

init-ru:
	$(PYTHON) setup.py init_catalog -l ru -i $(LCAT)/messages.pot \
                         -d $(LCAT)

update-ru:
	$(PYTHON) setup.py update_catalog -l ru -i $(LCAT)/messages.pot \
                            -d $(LCAT)
comp-cat:
	$(PYTHON) setup.py compile_catalog -d $(LCAT)

upd-cat: pot update-ru comp-cat

clean:
	$(PYTHON) setup.py clean

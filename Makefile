# This file is part of OpenPanel - The Open Source Control Panel
# OpenPanel is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the Free 
# Software Foundation, using version 3 of the License.
#
# Please note that use of the OpenPanel trademark may be subject to additional 
# restrictions. For more information, please visit the Legal Information 
# section of the OpenPanel website on http://www.openpanel.com/

all: module.xml

module.xml: module.def
	mkmodulexml < module.def > module.xml

install:
	mkdir -p ${DESTDIR}/var/openpanel/modules/SpamAssassin.module
	mkdir -p ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/tests
	mkdir -p ${DESTDIR}/var/openpanel/conf/staging/SpamAssassin
	mkdir -p ${DESTDIR}/etc/maildrop.d
	cp 50spamassassin.rc ${DESTDIR}/etc/maildrop.d
	install -m 755 action.py ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/action
	cp     module.xml          ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/module.xml
	install -m 755 verify      ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/verify
	cp     tests/test.py          ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/tests/
	# cp     *.png               ${DESTDIR}/var/openpanel/modules/SpamAssassin.module/
	# cp *.html ${DESTDIR}/var/openpanel/modules/SpamAssassin.module

clean:
	rm -f module.xml

SUFFIXES: .cpp .o
.cpp.o:
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -g $<

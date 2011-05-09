#!/usr/bin/env python
from OpenPanel import authd
from OpenPanel.modapi import panelmodule, panelclass
import sys, os, gdbm

class SpamAssassinModule(panelmodule):
    class Mail(panelclass):
        class SpamAssassin(panelclass):
            def create(self, objectid, object, tree):
                db = gdbm.open('/etc/openpanel/spamassassin/settings.dat', 'c')
		domain=tree['Mail']['id']
		label_at=float(object['label_at'])
		drop_at=int(object['drop_at'])
		db['%s-label' % domain] = str(label_at)
		db['%s-drop' % domain] = str(drop_at)

            def delete(self, objectid, tree):
                db = gdbm.open('/etc/openpanel/spamassassin/settings.dat', 'c')
		domain=tree['Mail']['id']
		del db['%s-label' % domain]
		del db['%s-drop' % domain]

            update = create

SpamAssassinModule().run()

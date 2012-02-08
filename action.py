#!/usr/bin/env python
from OpenPanel import authd
from OpenPanel.modapi import panelmodule, panelclass
import sys, os, gdbm

class SpamAssassinModule(panelmodule):
    def getconfig(self):
        extra = {
            'System:SpamPrefs': {
                'subject':'[SPAM]',
                'reportsafe':'off',
                'contact':'postmaster@localhost'
            }
          }
        
        return extra
        
    def updateok(self, currentversion):
        return True
        
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
            
    class System(panelclass):
        class SpamPrefs(panelclass):
            def create(self, objectid, object, tree):
                f = open ('/var/openpanel/conf/staging/SpamAssassin/local.cf','w')
                f.write ("rewrite_header Subject %s \n" % object["subject"])
                f.write ("report_contact %s\n" %object["contact"])
                if object["reportsafe"] == 'off':
                    f.write ("report_safe 0\n")
                elif object["reportsafe"] == 'mime':
                    f.write ("report_safe 1\n")
                elif object["reportsafe"] == 'plain':
                    f.write ("report_safe 2\n")
                f.close ()
                authd.installfile ("local.cf","/etc/spamassassin")
            
            def delete(self, objectid, tree):
            	return
            
            update = create

SpamAssassinModule().run()

##############################################################################
#                                                                            #
#  Cod4 Rotate Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)          #
#  Copyright (C) 2016 Daniele Pantaleone <fenix@bigbrotherbot.net>           #
#                                                                            #
#  This program is free software; you can redistribute it and/or modify      #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation; either version 2 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with this program; if not, write to the Free Software               #
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA  #
#                                                                            #
##############################################################################


__author__ = 'Daniele Pantaleone'
__version__ = '1.0.1'


from b3.cron import PluginCronTab
from b3.plugin import Plugin
from ConfigParser import NoOptionError


class Cod4RotatePlugin(Plugin):

    ####################################################################################################################
    #                                                                                                                  #
    #   STARTUP                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def __init__(self, *args, **kwargs):
        """
        Build the plugin object.
        """
        Plugin.__init__(self, *args, **kwargs)
        self.crontab = None
        self.last_activity_time = 0
        self.max_idle_time = 180


    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        try:
            self.max_idle_time = self.config.getint('settings', 'max_idle_time')
        except NoOptionError:
            self.warning('missing settings/max_idle_time in configuration file, using default ({})'.format(self.max_idle_time))
        except ValueError:
            self.error('bad value for settings/max_idle_time in configuration file, using default ({})'.format(self.max_idle_time))
        else:
            if self.max_idle_time < 30:
                self.warning('settings/max_idle_time MUST be >= 30')
                self.max_idle_time = 30
            self.debug('using settings/max_idle_time = {}'.format(self.max_idle_time))

    def onStartup(self):
        """
        Startup the plugin.
        """
        events = {
            'EVT_CLIENT_SAY',
            'EVT_CLIENT_TEAM_SAY',
            'EVT_CLIENT_PRIVATE_SAY',
            'EVT_CLIENT_DAMAGE',
            'EVT_CLIENT_DAMAGE_SELF',
            'EVT_CLIENT_DAMAGE_TEAM',
            'EVT_CLIENT_KILL',
            'EVT_CLIENT_KILL_TEAM',
            'EVT_CLIENT_SUICIDE',
            'EVT_CLIENT_ACTION'
        }

        self.debug('registering events...')

        for key in events:
            try:
                event_id = self.eventmanager.getId(key)
            except KeyError:
                pass
            else:
                self.registerEvent(event_id, self.onActivity)

        self.debug('installing crontab...')
        self.console.cron - self.crontab
        self.crontab = PluginCronTab(self, self.cron, 30)
        self.console.cron + self.crontab
        self.debug('plugin started')

    ####################################################################################################################
    #                                                                                                                  #
    #   EVENTS                                                                                                         #
    #                                                                                                                  #
    ####################################################################################################################

    def onActivity(self, _):
        """
        Executed when there is some activity on the server.
        """
        self.last_activity_time = self.console.time()

    ####################################################################################################################
    #                                                                                                                  #
    #   OTHER METHODS                                                                                                  #
    #                                                                                                                  #
    ####################################################################################################################

    def cron(self):
        """
        Scheduled execution.
        """
        self.debug('scheduled activity checking...')
        if self.console.time() - self.last_activity_time > self.max_idle_time:
            self.console.debug('no activity detected in the last {} seconds: rotating map...'.format(self.max_idle_time))
            self.console.write('map_rotate')
        else:
            self.console.debug('last activity detected {} seconds ago: we are good'.format(self.console.time() - self.last_activity_time))

#!/usr/bin/env python
# The MIT License (MIT)
# Copyright (c) 2016 Young Professionals Network

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import httplib2
import time
from apiclient import discovery
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from authorise import get_credentials
#from kivy.uix.recycleview import RecycleView
#from kivy.uix.anchorlayout import AnchorLayout
#from kivy.uix.listview import ListView, ListItemButton
#from kivy.factory import Factory
#from kivy.properties import ListProperty, StringProperty, ObjectProperty
# We'll probably need these later, when we want to modify their logic in the
# Python file.

YPN_ID = 'ypnmuscatine.org_p4tvrgupmk2rg4vimmkct8c4p8'

class YpnApp(App):
    pass

class RootWidget(BoxLayout):
    # nts: this might be kind of weird with the discounts page if the menu
    # button isn't disabled while coupons are open. make sure there's no way
    # for users to "cheat" for multiple uses of coupons.
    def __init__(self):
        super(RootWidget, self).__init__()
        self.name = 'Root'
        self.last_page_open = CalendarPage()
        
    def display_page(self, page):
        self.clear_widgets()
        self.last_page_open = page
        self.add_widget(page)

    # There might be a way to cut down on repeated code here by calling direct from the app class? But then we might want different logic for different pages.
    def display_calendar_page(self):
        self.display_page(CalendarPage())

    def display_discounts_page(self):
        self.display_page(DiscountsPage())
        
    def display_articles_page(self):
        self.display_page(ArticlesPage())
        
    def display_about_us_page(self):
        self.display_page(AboutUsPage())
       
    def display_search_page(self):
        self.display_page(SearchPage())
    
    def display_menu_page(self):
        # don't want to reset last_page here
        self.clear_widgets()
        self.add_widget(MenuPage())

    def display_last_page(self):
        if self.last_page_open:
            self.display_page(self.last_page_open)
        # otherwise do nothing because you done screwed up your programming (still relevant)
        
    #class RVTestDrivePage(RecycleView):
     #   pass

class EventLabel(Label):
    def __init__(self, start_time, end_time, summary):
        super(EventLabel, self).__init__()
        self.size_hint_y = 10
        self.date_input_format = '%Y-%m-%dT%H:%M:%S'
        date = self.get_date_time(start_time, '%A, %d %B')
        start_time = self.get_date_time(start_time, '%H:%M')
        end_time = self.get_date_time(end_time, '%H:%M')
        self.text = '{} {}-{}: {}'.format(date, start_time, end_time, summary)

    def get_date_time(self, date_time_str, date_output_format):
        date_time_str = '-'.join(date_time_str.split('-')[:-1])
        date_struct = time.strptime(date_time_str, self.date_input_format)
        converted_date = time.strftime(date_output_format, date_struct)
        return converted_date

# I feel like these classes really should be OO'd into one class...
# They really are basically all the same
# Leaving separate classes as-is for now - may want to make different in future
class CalendarPage(BoxLayout):
    # I've found that the pages are hard to tell apart without color. Well,
    # some people are colorblind anyway, so maybe we should put a nice header
    # at the top of each page. In place of the search bar, I think, because
    # search really should be its own page, accessible via the menu page.
    name = "Event Calendar"
    upcoming_events_count = 5


    def __init__(self):
        super(BoxLayout, self).__init__()
        self.upcoming_events()
        
    def upcoming_events(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z' 
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId = YPN_ID + '@group.calendar.google.com',
            timeMin=now, maxResults=self.upcoming_events_count,
            singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            print('No upcoming events found.')
        event_dict = {}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            self.add_widget(EventLabel(start, end, event['summary']))
        
class DiscountsPage(BoxLayout):
    name = "Member Discounts"
    def search_button(self, search_bar):
        # May want to put this in root if there's a lot of common logic
        print search_bar.ids['search_input'].text
        # do some searching with this
        
class ArticlesPage(BoxLayout):
    name = "Newsletter"

class AboutUsPage(BoxLayout):
    name = "About Us"

class SearchPage(BoxLayout):
    name = "Search"
    
class MenuPage(BoxLayout):
    name = "Menu"

    

# This is the code that actually runs the app.
if __name__ == '__main__':
    YpnApp().run()

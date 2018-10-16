# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

# Mycroft_family_learning

# Mycroft libraries

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_handler
from os.path import dirname, exists, join

import requests
import json

__author__ = 'henridbr' # hd@uip

LOGGER = getLogger(__name__)


class FamilyLearningSkill(MycroftSkill):

    def __init__(self):
        super(FamilyLearningSkill, self).__init__(name="FamilyLearningSkill")
        
    @intent_handler(IntentBuilder("FamilyLearningIntent").require("FamilyLearningKeyword"))
    def handle_family_learning_intent(self, message):
        self.speak_dialog("save.it.memory")

### Find who is my ?        
    @intent_handler(IntentBuilder("FamilyMemberIntent").require("FamilyMemberKeyword"))
    def handle_family_member_intent(self, message):

        family_rank = message.data.get("FamilyMemberKeyword")
#       print(family_rank)
        
        with open(join(self._dir, 'familybook.json'), "r") as read_file:
            family = json.load(read_file)

        membersname = family['family_dictionary']['members']
        
        namelist = []
        namegroup = ""
          
        i=0
        while i< len(membersname):
            if (membersname[i]['rank'] == family_rank):
                namelist.append(membersname[i]['first_name'])
            i = i+1
        i=1
        if len(namelist) ==0 :
            self.speak_dialog('you have no {}'.format(family_rank))
        elif len(namelist) ==1 :
            self.speak_dialog('{} is your {}'.format(namelist[0],family_rank))            
        else:
            namegroup = namelist[0]
            while i< len(namelist):
                namegroup = namegroup +" and " + namelist[i]
                i = i+1
            self.speak_dialog('{} are your {}'.format(namegroup,family_rank))
             
        

#### Find Living Place of someone
    @intent_handler(IntentBuilder("LivingPlaceIntent").require("LivingPlaceKeyword").require("FamilyFirstName"))
    def handle_living_place(self, message):
  
        member = message.data.get('FamilyFirstName')
               
        with open(join(self._dir, 'familybook.json'), "r") as read_file:
            family = json.load(read_file)

        membersname = family['family_dictionary']['members']

        memberslivingplace ={}

        i=0
        foundit = ""
        while i< len(membersname):
            if (member.find(membersname[i]['first_name'].lower())>=0):
                member = membersname[i]['first_name']
                foundit = "found"
            i=i+1
            
        if (foundit==""):
            self.speak('Sorry, I missed something')
        else:
            print(member)
            i=0
            while i< len(membersname):
                who = membersname[i]['first_name']
                where = membersname[i]['location']
                memberslivingplace[who] = where
                i=i+1

            livingplace = memberslivingplace[member]
 
            self.speak('{} is from {}'.format(member, livingplace))
      
       
#### Find Age of someone
    @intent_handler(IntentBuilder("SomeOneAgeIntent").require("SomeOneAgeKeyword").require("FamilyFirstName"))
    def handle_someone_age(self, message):
  
        member = message.data.get('FamilyFirstName')
               
        with open(join(self._dir, 'familybook.json'), "r") as read_file:
            family = json.load(read_file)

        membersname = family['family_dictionary']['members']

        membersage ={}
        foundit = ""

        i=0
        while i< len(membersname):
            if (member.find(membersname[i]['first_name'].lower())>=0):
                member = membersname[i]['first_name']
                foundit = "found"
            i=i+1
        if (foundit==""):
            self.speak('Sorry, I missed something')
        else:
            print(member)
            i=0
            while i< len(membersname):
                who = membersname[i]['first_name']
                so_age = membersname[i]['age']
                membersage[who] = so_age
                i=i+1

            member_age = membersage[member]
            if (member_age == "dead"):
                self.speak('{} is {}'.format(member, member_age))
            else:
                self.speak('{} is {} old'.format(member, member_age))
  

#### Find feature of someone
    @intent_handler(IntentBuilder("SomeOneFeatureIntent").require("SomeOneFeatureKeyword").require("FamilyFirstName"))
    def handle_someone_feature(self, message):
  
        member = message.data.get('FamilyFirstName')
               
        with open(join(self._dir, 'familybook.json'), "r") as read_file:
            family = json.load(read_file)

        membersname = family['family_dictionary']['members']

        membersfeature ={}
        foundit = ""

        i=0
        while i< len(membersname):
            if (member.find(membersname[i]['first_name'].lower())>=0):
                member = membersname[i]['first_name']
                foundit = "found"
            i=i+1
        if (foundit==""):
            self.speak('Sorry, I missed something')
        else:
            print(member)
            i=0
            while i< len(membersname):
                who = membersname[i]['first_name']
                so_feature = membersname[i]['feature']
                membersfeature[who] = so_feature
                i=i+1

            member_feature = membersfeature[member]
            if (member_feature == ""):
                self.speak('Sorry, I don\'t  know more on {}'.format(member))
            else:
                self.speak('{} is really {}'.format(member, member_feature))

#### Add first name of someone                
    @intent_handler(IntentBuilder("NewFamilyMemberIntent").require("NewFamilyMemberKeyword").require("NewMemberFirstName"))
    def handle_someone_feature(self, message):
  
        newfirstname = message.data.get('NewMemberFirstName')
    
    print(newfirstname)
    self.speak(newfirstname)         
                
    
    def stop(self):
        pass

def create_skill():
    return FamilyLearningSkill()

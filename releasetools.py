# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2018 The MoKee Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

def FullOTA_Assertions(info):
  AddModemAssertion(info)
  return

def FullOTA_InstallBegin(info):
  KillMagisk(info)
  return

def IncrementalOTA_Assertions(info):
  AddModemAssertion(info)
  return

def AddModemAssertion(info):
  android_info = info.input_zip.read("OTA/android-info.txt").decode('UTF-8')
  m = re.search(r'require\s+version-modem\s*=\s*(.+)', android_info)
  if m:
    version = m.group(1).rstrip()
    if len(version) and '*' not in version:
      cmd = 'assert(smartisan.verify_modem("' + version + '") == "1");'
      info.script.AppendExtra(cmd)
  return

def KillMagisk(info):
  info.script.Mount("/system")
  info.script.AppendExtra('delete("/system/system/addon.d/99-magisk.sh");')
  info.script.Unmount("/system")

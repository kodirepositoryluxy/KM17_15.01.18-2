import xbmc,xbmcgui,os
mode = 'killkodi'
# Cancel out line 10 for a prompt
################################
###     Kill Kodi ask prompt
################################
def killkodi():
    dialog = xbmcgui.Dialog()
    choice = 1
    #choice = xbmcgui.Dialog().yesno('Close Kodi?', 'Yes to force close Kodi (faster).', 'No to close Normally (saves skin settings).', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')
        #xbmc.executebuiltin('Quit')
        return
    elif choice == 1:
        pass
    log_path = xbmc.translatePath('special://logpath')
    #
    #################################
    # Windows and Pulsar and Quasar
    #################################
    if xbmc.getCondVisibility('system.platform.windows'):
        pulsar_path = xbmc.translatePath('special://home/addons/plugin.video.pulsar')
        if os.path.exists(pulsar_path)==True: os.system('start TASKKILL /im pulsar.exe /f');os.system('tskill pulsar.exe')
        #
        quasar_path = xbmc.translatePath('special://home/addons/plugin.video.quasar')
        if os.path.exists(quasar_path)==True: os.system('start TASKKILL /im quasar.exe /f');os.system('tskill quasar.exe')
        #
        xbmc_log_path = os.path.join(log_path, 'kodi.log')
        if os.path.exists(xbmc_log_path)==True: os.system('start TASKKILL /im kodi.exe /f');os.system('tskill Kodi.exe')         
        #               
        xbmc_log_path = os.path.join(log_path, 'smc.log')
        if os.path.exists(xbmc_log_path)==True: os.system('start TASKKILL /im SMC.exe /f');os.system('tskill SMC.exe')
        #    
        xbmc_log_path = os.path.join(log_path, 'xbmc.log')
        if os.path.exists(xbmc_log_path)==True: os.system('start TASKKILL /im xbmc.exe /f');os.system('tskill xbmc.exe')
        #
        xbmc_log_path = os.path.join(log_path, 'tvmc.log')
        if os.path.exists(xbmc_log_path)==True: os.system('start TASKKILL /im TVMC.exe /f');os.system('tskill TVMC.exe')
        #    

    if xbmc.getCondVisibility('system.platform.android'):
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass     
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass  
        try: os.system('adb shell am force-stop org.smc')
        except: pass   
        try: os.system('adb shell am force-stop org.tvmc')
        except: pass             
        #

    if xbmc.getCondVisibility('system.platform.linux'):
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall SMC')
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 SMC.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.osx'):
        try: os.system('killall -9 Kodi')
        except: pass
        try: os.system('killall -9 SMC')
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        #
    if xbmc.getCondVisibility('system.platform.ios'):
        print 'ios'
        #
    if xbmc.getCondVisibility('system.platform.atv2'):
        try: os.system('killall AppleTV')
        except: pass
        #
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass
        #
    else:
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass

        #
    #dialog.ok("WARNING", "Force Close was unsuccessful.","Closing Kodi normally...",'')
    #xbmc.executebuiltin('Quit')
    xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')
    #
if mode == 'killkodi': killkodi()
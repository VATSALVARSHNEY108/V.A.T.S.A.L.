"""
System Control Module
Handles system-level automation: brightness, audio, sleep/wake, disk cleanup
"""

import platform
import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
import json

class SystemController:
    def __init__(self):
        self.os = platform.system()
        self.config_file = "system_config.json"
        self.shutdown_process = None
        self.load_config()
    
    def load_config(self):
        """Load system configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "sleep_schedule": {"enabled": False, "time": "23:00"},
                "wake_schedule": {"enabled": False, "time": "07:00"},
                "auto_cleanup": {"enabled": False, "disk_limit": 90},
                "brightness_schedule": {"enabled": False, "day_brightness": 80, "night_brightness": 30}
            }
            self.save_config()
    
    def save_config(self):
        """Save system configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def mute_microphone(self):
        """Mute system microphone"""
        try:
            if self.os == "Windows":
                subprocess.run(["nircmd.exe", "mutesysvolume", "1", "microphone"], check=False)
                return "✅ Microphone muted"
            elif self.os == "Darwin":
                subprocess.run(["osascript", "-e", "set volume input volume 0"], check=False)
                return "✅ Microphone muted"
            elif self.os == "Linux":
                subprocess.run(["amixer", "set", "Capture", "nocap"], check=False)
                return "✅ Microphone muted"
        except Exception as e:
            return f"❌ Failed to mute microphone: {str(e)}"
    
    def unmute_microphone(self):
        """Unmute system microphone"""
        try:
            if self.os == "Windows":
                subprocess.run(["nircmd.exe", "mutesysvolume", "0", "microphone"], check=False)
                return "✅ Microphone unmuted"
            elif self.os == "Darwin":
                subprocess.run(["osascript", "-e", "set volume input volume 50"], check=False)
                return "✅ Microphone unmuted"
            elif self.os == "Linux":
                subprocess.run(["amixer", "set", "Capture", "cap"], check=False)
                return "✅ Microphone unmuted"
        except Exception as e:
            return f"❌ Failed to unmute microphone: {str(e)}"
    
    def set_brightness(self, level):
        """Set screen brightness (0-100)"""
        try:
            level = max(0, min(100, int(level)))
            
            if self.os == "Windows":
                subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
            elif self.os == "Darwin":
                subprocess.run(f"brightness {level/100}", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
            elif self.os == "Linux":
                subprocess.run(f"xrandr --output $(xrandr | grep ' connected' | awk '{{print $1}}') --brightness {level/100}", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
        except Exception as e:
            return f"❌ Failed to set brightness: {str(e)}"
    
    def auto_brightness(self):
        """Auto-adjust brightness based on time of day"""
        try:
            current_hour = datetime.now().hour
            
            if 6 <= current_hour < 18:
                brightness = self.config["brightness_schedule"]["day_brightness"]
            else:
                brightness = self.config["brightness_schedule"]["night_brightness"]
            
            return self.set_brightness(brightness)
        except Exception as e:
            return f"❌ Auto-brightness failed: {str(e)}"
    
    def schedule_sleep(self, time_str="23:00"):
        """Schedule PC to sleep at specific time"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            now = datetime.now()
            sleep_time = now.replace(hour=hours, minute=minutes, second=0)
            
            if sleep_time < now:
                sleep_time += timedelta(days=1)
            
            seconds_until_sleep = (sleep_time - now).total_seconds()
            
            if self.os == "Windows":
                subprocess.Popen(f'shutdown /s /t {int(seconds_until_sleep)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
            elif self.os == "Darwin":
                subprocess.Popen(f'sudo shutdown -s +{int(seconds_until_sleep/60)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
            elif self.os == "Linux":
                subprocess.Popen(f'sudo shutdown -h +{int(seconds_until_sleep/60)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
        except Exception as e:
            return f"❌ Failed to schedule sleep: {str(e)}"
    
    def cancel_sleep(self):
        """Cancel scheduled sleep"""
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return "✅ Sleep cancelled"
            elif self.os in ["Darwin", "Linux"]:
                subprocess.run("sudo shutdown -c", shell=True, check=False)
                return "✅ Sleep cancelled"
        except Exception as e:
            return f"❌ Failed to cancel sleep: {str(e)}"
    
    def schedule_wake(self, time_str="07:00"):
        """Schedule PC to wake at specific time (Windows only)"""
        try:
            if self.os == "Windows":
                hours, minutes = map(int, time_str.split(':'))
                subprocess.run(f'powershell "powercfg /waketimers /create /type wakeup /time {hours}:{minutes}"', shell=True, check=False)
                return f"✅ Wake scheduled for {time_str}"
            else:
                return "ℹ️ Wake scheduling is only supported on Windows"
        except Exception as e:
            return f"❌ Failed to schedule wake: {str(e)}"
    
    def clear_temp_files(self):
        """Clear temporary files and cache"""
        try:
            cleared_size = 0
            cleared_files = 0
            
            temp_dirs = []
            if self.os == "Windows":
                user_profile = os.environ.get('USERPROFILE')
                temp_dirs = [
                    os.environ.get('TEMP'),
                    os.environ.get('TMP'),
                ]
                if user_profile:
                    temp_dirs.append(os.path.join(user_profile, 'AppData', 'Local', 'Temp'))
            elif self.os in ["Darwin", "Linux"]:
                temp_dirs = ['/tmp', os.path.expanduser('~/.cache')]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                os.remove(item_path)
                                cleared_size += size
                                cleared_files += 1
                            elif os.path.isdir(item_path):
                                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                          for dirpath, _, filenames in os.walk(item_path)
                                          for filename in filenames)
                                shutil.rmtree(item_path)
                                cleared_size += size
                                cleared_files += 1
                        except:
                            continue
            
            cleared_mb = cleared_size / (1024 * 1024)
            return f"✅ Cleared {cleared_files} items ({cleared_mb:.2f} MB)"
        except Exception as e:
            return f"❌ Failed to clear temp files: {str(e)}"
    
    def empty_recycle_bin(self):
        """Empty recycle bin"""
        try:
            if self.os == "Windows":
                try:
                    import winshell
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    return "✅ Recycle bin emptied"
                except ImportError:
                    subprocess.run("rd /s /q %temp%", shell=True, check=False)
                    return "✅ Temp cleaned (winshell not available)"
            elif self.os == "Darwin":
                subprocess.run("rm -rf ~/.Trash/*", shell=True, check=False)
                return "✅ Trash emptied"
            elif self.os == "Linux":
                subprocess.run("rm -rf ~/.local/share/Trash/*", shell=True, check=False)
                return "✅ Trash emptied"
        except Exception as e:
            return f"❌ Failed to empty recycle bin: {str(e)}"
    
    def check_disk_space(self):
        """Check disk space and auto-cleanup if needed"""
        try:
            usage = shutil.disk_usage("/")
            percent_used = (usage.used / usage.total) * 100
            
            result = f"💾 Disk Usage: {percent_used:.1f}% ({usage.used//(1024**3)}GB / {usage.total//(1024**3)}GB)\n"
            
            if self.config["auto_cleanup"]["enabled"] and percent_used > self.config["auto_cleanup"]["disk_limit"]:
                result += "\n⚠️ Disk space limit exceeded. Running auto-cleanup...\n"
                cleanup_msg = self.clear_temp_files()
                if cleanup_msg:
                    result += cleanup_msg + "\n"
                bin_msg = self.empty_recycle_bin()
                if bin_msg:
                    result += bin_msg
            
            return result
        except Exception as e:
            return f"❌ Failed to check disk space: {str(e)}"
    
    def auto_cleanup_on_limit(self, limit_percent=90):
        """Configure auto-cleanup when disk hits limit"""
        self.config["auto_cleanup"]["enabled"] = True
        self.config["auto_cleanup"]["disk_limit"] = limit_percent
        self.save_config()
        return f"✅ Auto-cleanup enabled at {limit_percent}% disk usage"
    
    def lock_screen(self):
        """Lock the computer screen"""
        try:
            print("🔒 Attempting to lock screen...")
            
            if self.os == "Windows":
                result = subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, check=False, capture_output=True, text=True)
                print(f"Lock command executed (Windows): return code {result.returncode}")
                return "🔒 Screen locked successfully"
                
            elif self.os == "Darwin":
                result = subprocess.run(
                    ["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], 
                    check=False, capture_output=True, text=True
                )
                print(f"Lock command executed (macOS): return code {result.returncode}")
                return "🔒 Screen locked successfully"
                
            elif self.os == "Linux":
                # Try multiple methods in order of preference
                lock_methods = [
                    (["loginctl", "lock-session"], "loginctl"),
                    (["xdg-screensaver", "lock"], "xdg-screensaver"),
                    (["gnome-screensaver-command", "--lock"], "gnome-screensaver"),
                    (["dm-tool", "lock"], "dm-tool"),
                    (["xscreensaver-command", "-lock"], "xscreensaver"),
                ]
                
                for cmd, method_name in lock_methods:
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=5)
                        print(f"Lock command executed (Linux - {method_name}): return code {result.returncode}")
                        return f"🔒 Screen locked successfully (using {method_name})"
                    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
                # If all methods failed
                print("⚠️ All lock methods failed on Linux")
                return "❌ Failed to lock screen. No compatible screen locker found. Please install xdg-screensaver, gnome-screensaver, or configure loginctl."
            else:
                return f"❌ Unsupported operating system: {self.os}"
                
        except Exception as e:
            print(f"❌ Exception in lock_screen: {str(e)}")
            return f"❌ Failed to lock screen: {str(e)}"
    
    def shutdown_system(self, delay_seconds=10):
        """Shutdown the computer with optional delay"""
        try:
            print(f"⚠️ Attempting to shutdown system (delay: {delay_seconds}s)...")
            
            # Cancel any existing shutdown/restart process
            if self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
                    print("Cancelled previous shutdown process")
            
            if self.os == "Windows":
                # Cancel any existing shutdown first
                subprocess.run("shutdown /a", shell=True, check=False, capture_output=True)
                
                # Schedule new shutdown
                result = subprocess.run(f'shutdown /s /t {delay_seconds}', shell=True, capture_output=True, text=True)
                print(f"Shutdown command executed (Windows): return code {result.returncode}")
                
                if delay_seconds > 0:
                    return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' command to abort."
                else:
                    return "⚠️ Shutting down computer now..."
                    
            elif self.os == "Darwin":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo shutdown -h now',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print(f"Shutdown scheduled (macOS): PID {self.shutdown_process.pid}")
                    return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Click 'Cancel Shutdown' or run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
                    print("Immediate shutdown initiated (macOS)")
                    return "⚠️ Shutting down computer now..."
                    
            elif self.os == "Linux":
                if delay_seconds > 0:
                    # Use systemctl with delay
                    minutes = max(1, delay_seconds // 60)
                    try:
                        # Try systemctl first
                        result = subprocess.run(
                            f'sudo systemctl poweroff --message="Shutdown scheduled via VATSAL" --no-wall',
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        print(f"Shutdown command executed (Linux systemctl): return code {result.returncode}")
                        return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' to abort."
                    except:
                        # Fallback to sleep + poweroff
                        self.shutdown_process = subprocess.Popen(
                            f'sleep {delay_seconds} && sudo systemctl poweroff',
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        print(f"Shutdown scheduled (Linux fallback): PID {self.shutdown_process.pid}")
                        return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'systemctl', 'poweroff'])
                    print("Immediate shutdown initiated (Linux)")
                    return "⚠️ Shutting down computer now..."
            else:
                return f"❌ Unsupported operating system: {self.os}"
                
        except Exception as e:
            print(f"❌ Exception in shutdown_system: {str(e)}")
            return f"❌ Failed to shutdown: {str(e)}"
    
    def restart_system(self, delay_seconds=10):
        """Restart the computer with optional delay"""
        try:
            if self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
            
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                subprocess.Popen(f'shutdown /r /t {delay_seconds}', shell=True)
                if delay_seconds > 0:
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
                else:
                    return "🔄 Restarting computer now..."
            elif self.os == "Darwin":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo shutdown -r now',
                        shell=True
                    )
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'shutdown', '-r', 'now'])
                    return "🔄 Restarting computer now..."
            elif self.os == "Linux":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo systemctl reboot',
                        shell=True
                    )
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'systemctl', 'reboot'])
                    return "🔄 Restarting computer now..."
        except Exception as e:
            return f"❌ Failed to restart: {str(e)}"
    
    def cancel_shutdown_restart(self):
        """Cancel scheduled shutdown or restart"""
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return "✅ Shutdown/restart cancelled"
            elif self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
                    return "✅ Shutdown/restart cancelled"
                else:
                    subprocess.run("sudo killall sleep", shell=True, check=False)
                    return "✅ Attempted to cancel shutdown/restart"
        except Exception as e:
            return f"❌ Failed to cancel: {str(e)}"

    def take_camera_photo(self, filename=None):
        """Capture a photo from the camera"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"camera_photo_{timestamp}.jpg"

            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)

            filepath = os.path.join(screenshots_dir, filename)

            if self.os == "Windows":
                try:
                    import cv2
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        return "❌ Failed to access camera. Please check if camera is available."

                    time.sleep(0.5)
                    ret, frame = cap.read()

                    if ret:
                        cv2.imwrite(filepath, frame)
                        cap.release()
                        cv2.destroyAllWindows()
                        return f"📸 Photo captured successfully: {filepath}"
                    else:
                        cap.release()
                        return "❌ Failed to capture photo from camera"
                except ImportError:
                    return "❌ OpenCV (cv2) not installed. Please install opencv-python."

            elif self.os == "Darwin":
                try:
                    import cv2
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        return "❌ Failed to access camera. Please check if camera is available."

                    time.sleep(0.5)
                    ret, frame = cap.read()

                    if ret:
                        cv2.imwrite(filepath, frame)
                        cap.release()
                        cv2.destroyAllWindows()
                        return f"📸 Photo captured successfully: {filepath}"
                    else:
                        cap.release()
                        return "❌ Failed to capture photo from camera"
                except ImportError:
                    subprocess.run(f'imagesnap {filepath}', shell=True, check=False)
                    if os.path.exists(filepath):
                        return f"📸 Photo captured successfully: {filepath}"
                    else:
                        return "❌ Failed to capture photo. Please install imagesnap or opencv-python."

            elif self.os == "Linux":
                try:
                    import cv2
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        return "❌ Failed to access camera. Please check if camera is available."

                    time.sleep(0.5)
                    ret, frame = cap.read()

                    if ret:
                        cv2.imwrite(filepath, frame)
                        cap.release()
                        cv2.destroyAllWindows()
                        return f"📸 Photo captured successfully: {filepath}"
                    else:
                        cap.release()
                        return "❌ Failed to capture photo from camera"
                except ImportError:
                    subprocess.run(f'fswebcam -r 1280x720 --no-banner {filepath}', shell=True, check=False)
                    if os.path.exists(filepath):
                        return f"📸 Photo captured successfully: {filepath}"
                    else:
                        return "❌ Failed to capture photo. Please install fswebcam or opencv-python."

        except Exception as e:
            return f"❌ Failed to capture photo: {str(e)}"

    def wifi_on(self):
        """Turn WiFi on"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    'netsh interface set interface name="Wi-Fi" admin=enabled',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned ON"
                else:
                    result = subprocess.run(
                        'netsh interface set interface name="WiFi" admin=enabled',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned ON"
                    else:
                        result = subprocess.run(
                            'netsh interface set interface name="Wireless Network Connection" admin=enabled',
                            shell=True,
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        if result.returncode == 0:
                            return "✅ WiFi turned ON"
                        else:
                            return "❌ Failed to turn ON WiFi. Please check your WiFi adapter name."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'networksetup -setairportpower en0 on',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned ON"
                else:
                    result = subprocess.run(
                        'networksetup -setairportpower en1 on',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned ON"
                    else:
                        return "❌ Failed to turn ON WiFi. Please check your WiFi adapter."

            elif self.os == "Linux":
                result = subprocess.run(
                    'nmcli radio wifi on',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned ON"
                else:
                    result = subprocess.run(
                        'sudo ifconfig wlan0 up',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned ON"
                    else:
                        result = subprocess.run(
                            'sudo ip link set wlan0 up',
                            shell=True,
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        if result.returncode == 0:
                            return "✅ WiFi turned ON"
                        else:
                            return "❌ Failed to turn ON WiFi. Please check your WiFi adapter."

        except Exception as e:
            return f"❌ Failed to turn ON WiFi: {str(e)}"

    def wifi_off(self):
        """Turn WiFi off"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    'netsh interface set interface name="Wi-Fi" admin=disabled',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned OFF"
                else:
                    result = subprocess.run(
                        'netsh interface set interface name="WiFi" admin=disabled',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned OFF"
                    else:
                        result = subprocess.run(
                            'netsh interface set interface name="Wireless Network Connection" admin=disabled',
                            shell=True,
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        if result.returncode == 0:
                            return "✅ WiFi turned OFF"
                        else:
                            return "❌ Failed to turn OFF WiFi. Please check your WiFi adapter name."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'networksetup -setairportpower en0 off',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned OFF"
                else:
                    result = subprocess.run(
                        'networksetup -setairportpower en1 off',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned OFF"
                    else:
                        return "❌ Failed to turn OFF WiFi. Please check your WiFi adapter."

            elif self.os == "Linux":
                result = subprocess.run(
                    'nmcli radio wifi off',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ WiFi turned OFF"
                else:
                    result = subprocess.run(
                        'sudo ifconfig wlan0 down',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return "✅ WiFi turned OFF"
                    else:
                        result = subprocess.run(
                            'sudo ip link set wlan0 down',
                            shell=True,
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        if result.returncode == 0:
                            return "✅ WiFi turned OFF"
                        else:
                            return "❌ Failed to turn OFF WiFi. Please check your WiFi adapter."

        except Exception as e:
            return f"❌ Failed to turn OFF WiFi: {str(e)}"

    def bluetooth_on(self):
        """Turn Bluetooth on"""
        try:
            if self.os == "Windows":
                powershell_cmd = '''
                Add-Type -AssemblyName System.Runtime.WindowsRuntime
                $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
                Function Await($WinRtTask, $ResultType) {
                    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                    $netTask = $asTask.Invoke($null, @($WinRtTask))
                    $netTask.Wait(-1) | Out-Null
                    $netTask.Result
                }
                [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                [Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                Await ([Windows.Devices.Radios.Radio]::RequestAccessAsync()) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
                $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])
                $bluetooth = $radios | ? { $_.Kind -eq 'Bluetooth' }
                [Windows.Devices.Radios.RadioState,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                Await ($bluetooth.SetStateAsync('On')) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
                '''
                result = subprocess.run(
                    ['powershell', '-Command', powershell_cmd],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=10
                )
                if result.returncode == 0:
                    return "✅ Bluetooth turned ON"
                else:
                    return "❌ Failed to turn ON Bluetooth. Please enable it manually from Settings."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'blueutil --power 1',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ Bluetooth turned ON"
                else:
                    return "❌ Failed to turn ON Bluetooth. Please install blueutil: brew install blueutil"

            elif self.os == "Linux":
                result = subprocess.run(
                    'sudo rfkill unblock bluetooth',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                subprocess.run('sudo systemctl start bluetooth', shell=True, check=False)
                subprocess.run('bluetoothctl power on', shell=True, check=False)

                if result.returncode == 0:
                    return "✅ Bluetooth turned ON"
                else:
                    return "❌ Failed to turn ON Bluetooth. Please check if bluetooth service is installed."

        except Exception as e:
            return f"❌ Failed to turn ON Bluetooth: {str(e)}"

    def bluetooth_off(self):
        """Turn Bluetooth off"""
        try:
            if self.os == "Windows":
                powershell_cmd = '''
                Add-Type -AssemblyName System.Runtime.WindowsRuntime
                $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
                Function Await($WinRtTask, $ResultType) {
                    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                    $netTask = $asTask.Invoke($null, @($WinRtTask))
                    $netTask.Wait(-1) | Out-Null
                    $netTask.Result
                }
                [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                [Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                Await ([Windows.Devices.Radios.Radio]::RequestAccessAsync()) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
                $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])
                $bluetooth = $radios | ? { $_.Kind -eq 'Bluetooth' }
                [Windows.Devices.Radios.RadioState,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
                Await ($bluetooth.SetStateAsync('Off')) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
                '''
                result = subprocess.run(
                    ['powershell', '-Command', powershell_cmd],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=10
                )
                if result.returncode == 0:
                    return "✅ Bluetooth turned OFF"
                else:
                    return "❌ Failed to turn OFF Bluetooth. Please disable it manually from Settings."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'blueutil --power 0',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return "✅ Bluetooth turned OFF"
                else:
                    return "❌ Failed to turn OFF Bluetooth. Please install blueutil: brew install blueutil"

            elif self.os == "Linux":
                subprocess.run('bluetoothctl power off', shell=True, check=False)
                result = subprocess.run(
                    'sudo rfkill block bluetooth',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False
                )

                if result.returncode == 0:
                    return "✅ Bluetooth turned OFF"
                else:
                    return "❌ Failed to turn OFF Bluetooth. Please check if bluetooth service is installed."

        except Exception as e:
            return f"❌ Failed to turn OFF Bluetooth: {str(e)}"

    def hotspot_on(self, ssid="MyHotspot", password="SecurePass123!"):
        """Turn mobile hotspot on with custom or default credentials"""
        try:
            if self.os == "Windows":
                check_cmd = 'netsh wlan show hostednetwork'
                check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)

                check_lower = check_result.stdout.lower()
                if "hosted network is already running" in check_lower or "status" in check_lower and "started" in check_lower:
                    return f"ℹ️ Hotspot is already running"

                if "SSID name" not in check_result.stdout or '""' in check_result.stdout:
                    setup_result = subprocess.run(
                        f'netsh wlan set hostednetwork mode=allow ssid={ssid} key={password}',
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if setup_result.returncode != 0:
                        return "❌ Failed to configure hotspot. You may need administrator privileges."

                start_result = subprocess.run(
                    'netsh wlan start hostednetwork',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                output_lower = start_result.stdout.lower()
                if "couldn't be started" in output_lower or "could not be started" in output_lower or "not supported" in output_lower:
                    return "❌ Hotspot not supported on this system. Windows 10/11 may have Hosted Network disabled. Use Mobile Hotspot from Settings instead."
                elif start_result.returncode == 0 and ("started" in output_lower or "running" in output_lower):
                    return f"✅ Hotspot turned ON (SSID: {ssid}, Password: {password})"
                else:
                    return f"❌ Failed to start hotspot. Error: {start_result.stderr or start_result.stdout or 'Try running as administrator.'}"

            elif self.os == "Darwin":
                return "ℹ️ Hotspot control not available via command line on macOS. Please enable manually from System Preferences > Sharing > Internet Sharing."

            elif self.os == "Linux":
                check_result = subprocess.run(
                    'nmcli connection show Hotspot',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if check_result.returncode != 0:
                    create_result = subprocess.run(
                        'nmcli device wifi hotspot ssid MyHotspot password password123',
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if create_result.returncode == 0:
                        return "✅ Hotspot created and started (SSID: MyHotspot, Password: password123)"
                    else:
                        return f"❌ Failed to create hotspot: {create_result.stderr or 'Unknown error'}"
                else:
                    up_result = subprocess.run(
                        'nmcli connection up Hotspot',
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if up_result.returncode == 0:
                        return "✅ Hotspot turned ON"
                    else:
                        return f"❌ Failed to start hotspot: {up_result.stderr or 'Unknown error'}"

        except Exception as e:
            return f"❌ Failed to turn ON hotspot: {str(e)}"

    def hotspot_off(self):
        """Turn mobile hotspot off"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    'netsh wlan stop hostednetwork',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0 and "stopped" in result.stdout.lower():
                    return "✅ Hotspot turned OFF"
                elif "not started" in result.stdout.lower() or "not running" in result.stdout.lower():
                    return "ℹ️ Hotspot is not currently running"
                else:
                    return f"❌ Failed to stop hotspot: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                return "ℹ️ Hotspot control not available via command line on macOS. Please disable manually from System Preferences > Sharing."

            elif self.os == "Linux":
                result = subprocess.run(
                    'nmcli connection down Hotspot',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    return "✅ Hotspot turned OFF"
                elif "not active" in result.stderr.lower() or "no active connection" in result.stderr.lower():
                    return "ℹ️ Hotspot is not currently active"
                else:
                    return f"❌ Failed to stop hotspot: {result.stderr or 'Unknown error'}"

        except Exception as e:
            return f"❌ Failed to turn OFF hotspot: {str(e)}"

    def set_volume(self, level):
        """Set system volume (0-100)"""
        try:
            level = max(0, min(100, int(level)))

            if self.os == "Windows":
                powershell_cmd = f'''
                $obj = New-Object -ComObject WScript.Shell
                1..50 | ForEach-Object {{ $obj.SendKeys([char]174) }}
                1..{level*2} | ForEach-Object {{ $obj.SendKeys([char]175) }}
                '''
                result = subprocess.run(
                    ['powershell', '-Command', powershell_cmd],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return f"✅ Volume set to approximately {level}%"
                else:
                    return f"❌ Failed to set volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                result = subprocess.run(
                    f'osascript -e "set volume output volume {level}"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume set to {level}%"
                else:
                    return f"❌ Failed to set volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    f'amixer -D pulse sset Master {level}%',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume set to {level}%"
                else:
                    return f"❌ Failed to set volume: {result.stderr or 'Unknown error'}"

        except Exception as e:
            return f"❌ Failed to set volume: {str(e)}"

    def increase_volume(self, increment=10):
        """Increase system volume by specified increment"""
        try:
            increment = max(1, min(100, int(increment)))

            if self.os == "Windows":
                powershell_cmd = f'''
                $obj = New-Object -ComObject WScript.Shell
                1..{increment*2} | ForEach-Object {{ $obj.SendKeys([char]175) }}
                '''
                result = subprocess.run(
                    ['powershell', '-Command', powershell_cmd],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return f"✅ Volume increased by approximately {increment}%"
                else:
                    return f"❌ Failed to increase volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                result = subprocess.run(
                    f'osascript -e "set volume output volume ((output volume of (get volume settings)) + {increment})"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume increased by {increment}%"
                else:
                    return f"❌ Failed to increase volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    f'amixer -D pulse sset Master {increment}%+',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume increased by {increment}%"
                else:
                    return f"❌ Failed to increase volume: {result.stderr or 'Unknown error'}"

        except Exception as e:
            return f"❌ Failed to increase volume: {str(e)}"

    def decrease_volume(self, decrement=10):
        """Decrease system volume by specified decrement"""
        try:
            decrement = max(1, min(100, int(decrement)))

            if self.os == "Windows":
                powershell_cmd = f'''
                $obj = New-Object -ComObject WScript.Shell
                1..{decrement*2} | ForEach-Object {{ $obj.SendKeys([char]174) }}
                '''
                result = subprocess.run(
                    ['powershell', '-Command', powershell_cmd],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return f"✅ Volume decreased by approximately {decrement}%"
                else:
                    return f"❌ Failed to decrease volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                result = subprocess.run(
                    f'osascript -e "set volume output volume ((output volume of (get volume settings)) - {decrement})"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume decreased by {decrement}%"
                else:
                    return f"❌ Failed to decrease volume: {result.stderr or 'Unknown error'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    f'amixer -D pulse sset Master {decrement}%-',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Volume decreased by {decrement}%"
                else:
                    return f"❌ Failed to decrease volume: {result.stderr or 'Unknown error'}"

        except Exception as e:
            return f"❌ Failed to decrease volume: {str(e)}"

    def energy_saver_on(self):
        """Enable energy saver mode"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    'powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode enabled (Power Saver plan activated)"
                else:
                    return f"❌ Failed to enable energy saver: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                result = subprocess.run(
                    'sudo pmset -a lowpowermode 1',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode enabled (Low Power Mode)"
                else:
                    return f"❌ Failed to enable energy saver: {result.stderr or 'May require sudo privileges'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    'sudo cpupower frequency-set -g powersave',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode enabled (CPU governor set to powersave)"
                else:
                    return f"❌ Failed to enable energy saver: {result.stderr or 'cpupower may not be installed'}"

        except Exception as e:
            return f"❌ Failed to enable energy saver: {str(e)}"

    def energy_saver_off(self):
        """Disable energy saver mode"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    'powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode disabled (Balanced plan activated)"
                else:
                    return f"❌ Failed to disable energy saver: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                result = subprocess.run(
                    'sudo pmset -a lowpowermode 0',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode disabled"
                else:
                    return f"❌ Failed to disable energy saver: {result.stderr or 'May require sudo privileges'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    'sudo cpupower frequency-set -g performance',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Energy saver mode disabled (CPU governor set to performance)"
                else:
                    return f"❌ Failed to disable energy saver: {result.stderr or 'cpupower may not be installed'}"

        except Exception as e:
            return f"❌ Failed to disable energy saver: {str(e)}"

    def notifications_on(self):
        """Enable system notifications"""
        try:
            if self.os == "Windows":
                reg_cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 1 /f'
                result = subprocess.run(
                    reg_cmd,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Notifications enabled"
                else:
                    return f"❌ Failed to enable notifications: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                return "ℹ️ Notification settings must be changed manually in System Preferences > Notifications"

            elif self.os == "Linux":
                result = subprocess.run(
                    'gsettings set org.gnome.desktop.notifications show-banners true',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Notifications enabled"
                else:
                    return f"❌ Failed to enable notifications: {result.stderr or 'GNOME settings may not be available'}"

        except Exception as e:
            return f"❌ Failed to enable notifications: {str(e)}"

    def notifications_off(self):
        """Disable system notifications"""
        try:
            if self.os == "Windows":
                reg_cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f'
                result = subprocess.run(
                    reg_cmd,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Notifications disabled"
                else:
                    return f"❌ Failed to disable notifications: {result.stderr or 'Unknown error'}"

            elif self.os == "Darwin":
                return "ℹ️ Notification settings must be changed manually in System Preferences > Notifications"

            elif self.os == "Linux":
                result = subprocess.run(
                    'gsettings set org.gnome.desktop.notifications show-banners false',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Notifications disabled"
                else:
                    return f"❌ Failed to disable notifications: {result.stderr or 'GNOME settings may not be available'}"

        except Exception as e:
            return f"❌ Failed to disable notifications: {str(e)}"

    def night_light_on(self):
        """Enable night light / blue light filter"""
        try:
            if self.os == "Windows":
                reg_cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate" /v Data /t REG_BINARY /d 02000000807d976cd8d5da0143420100 /f'
                result = subprocess.run(
                    reg_cmd,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night light enabled (restart may be needed)"
                else:
                    return f"ℹ️ Night light registry updated. Please toggle Night Light in Windows Settings to activate."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'defaults write /Library/Preferences/com.apple.CoreBrightness "CBBlueReductionStatus" -dict-add "BlueReductionEnabled" -bool YES',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night Shift enabled (may require restart)"
                else:
                    return f"❌ Failed to enable Night Shift: {result.stderr or 'May require sudo privileges'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    'gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled true',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night light enabled"
                else:
                    return f"❌ Failed to enable night light: {result.stderr or 'GNOME color settings may not be available'}"

        except Exception as e:
            return f"❌ Failed to enable night light: {str(e)}"

    def night_light_off(self):
        """Disable night light / blue light filter"""
        try:
            if self.os == "Windows":
                reg_cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate" /v Data /t REG_BINARY /d 02000000807d976cd8d5da0143420000 /f'
                result = subprocess.run(
                    reg_cmd,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night light disabled (restart may be needed)"
                else:
                    return f"ℹ️ Night light registry updated. Please toggle Night Light in Windows Settings to deactivate."

            elif self.os == "Darwin":
                result = subprocess.run(
                    'defaults write /Library/Preferences/com.apple.CoreBrightness "CBBlueReductionStatus" -dict-add "BlueReductionEnabled" -bool NO',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night Shift disabled (may require restart)"
                else:
                    return f"❌ Failed to disable Night Shift: {result.stderr or 'May require sudo privileges'}"

            elif self.os == "Linux":
                result = subprocess.run(
                    'gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled false',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return "✅ Night light disabled"
                else:
                    return f"❌ Failed to disable night light: {result.stderr or 'GNOME color settings may not be available'}"

        except Exception as e:
            return f"❌ Failed to disable night light: {str(e)}"

if __name__ == "__main__":
    controller = SystemController()
    print("System Control Module - Testing")
    print(controller.check_disk_space())

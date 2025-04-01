#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import argparse
from datetime import datetime
import platform
import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# إعداد السجل (logging)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class AdvancedOSINTTool:
    def __init__(self, email=None, username=None):
        self.email = email
        self.username = username if username else (email.split('@')[0] if email else None)
        self.results = {
            "meta": {
                "email": email,
                "username": self.username,
                "timestamp": str(datetime.now()),
                "tools_used": []
            },
            "results": {}
        }
        self.tools_dir = os.path.join(os.path.dirname(__file__), "True.Sys.OSintMaster_tools")
        self.results_dir = os.path.join(os.path.dirname(__file__), "True.Sys.OSintMaster_results")
        self.config = self.load_config()

    def load_config(self):
        """تحميل إعدادات الأدوات من ملف config"""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        default_config = {
            "tools": {
                "sherlock": {"enabled": True, "timeout": 15},
                "maigret": {"enabled": True, "timeout": 15},
                "holehe": {"enabled": True, "timeout": 10},
                "ghunt": {"enabled": True, "docker_required": True},
                "whatsmyname": {"enabled": True, "web_archive": True},
                "blackbird": {"enabled": True, "api_key": ""},
                "email2phone": {"enabled": False, "api_key": ""},
                "darksearch": {"enabled": False, "api_key": ""}
            },
            "proxy": {
                "enabled": False,
                "list": []
            }
        }
        
        try:
            with open(config_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return default_config

    def setup_environment(self):
        """إعداد البيئة وتثبيت المتطلبات"""
        logging.info("[+] إعداد البيئة...")
        
        # إنشاء المجلدات اللازمة
        os.makedirs(self.tools_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
        # تثبيت المتطلبات الأساسية
        self.install_base_requirements()
        
        # تنزيل وتثبيت الأدوات
        self.clone_and_setup_tools()

    def install_base_requirements(self):
        """تثبيت المتطلبات الأساسية للنظام"""
        requirements = {
            "Linux": ["git", "python3", "pip", "docker.io", "libcurl4-openssl-dev"],
            "Windows": ["git", "python", "docker-desktop"]
        }
        
        current_os = platform.system()
        
        if current_os == "Linux":
            if os.geteuid() != 0:
                logging.error("يجب تشغيل الأداة بصلاحيات root/sudo")
                sys.exit(1)
                
            subprocess.run(["apt", "update"], check=True)
            subprocess.run(["apt", "install", "-y"] + requirements[current_os], check=True)
        
        # تثبيت متطلبات Python
        py_requirements = [
            "requests", "bs4", "selenium", "lxml", "python-whois",
            "dnspython", "pandas", "tqdm", "pycurl", "urllib3"
        ]
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install"] + py_requirements, check=True)

    def clone_and_setup_tools(self):
        """تنزيل وتثبيت جميع أدوات OSINT"""
        tools = {
            "sherlock": "https://github.com/sherlock-project/sherlock.git",
            "maigret": "https://github.com/soxoj/maigret.git",
            "holehe": "https://github.com/megadose/holehe.git",
            "ghunt": "https://github.com/mxrch/GHunt.git",
            "whatsmyname": "https://github.com/WebBreacher/WhatsMyName.git",
            "blackbird": "https://github.com/p1ngul1n0/blackbird.git",
            "email2phone": "https://github.com/martinvigo/email2phonenumber.git"
        }
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            for tool, url in tools.items():
                if self.config["tools"].get(tool, {}).get("enabled", False):
                    executor.submit(self.install_tool, tool, url)

    def install_tool(self, tool_name, repo_url):
        """تنزيل وتثبيت أداة معينة"""
        tool_path = os.path.join(self.tools_dir, tool_name)
        
        if not os.path.exists(tool_path):
            logging.info(f"[+] جاري تنزيل {tool_name}...")
            subprocess.run(["git", "clone", repo_url, tool_path], check=True)
        
        # تثبيت متطلبات الأداة
        req_file = os.path.join(tool_path, "requirements.txt")
        if os.path.exists(req_file):
            logging.info(f"[+] جاري تثبيت متطلبات {tool_name}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], 
                         cwd=tool_path, check=True)
            
        # إعدادات خاصة لكل أداة
        if tool_name == "blackbird" and self.config["tools"]["blackbird"]["api_key"]:
            self.setup_blackbird_api(tool_path)

    def setup_blackbird_api(self, tool_path):
        """تكوين مفتاح API لـ Blackbird"""
        config_path = os.path.join(tool_path, "config.json")
        config = {
            "api_key": self.config["tools"]["blackbird"]["api_key"],
            "save_output": True,
            "output_dir": self.results_dir
        }
        with open(config_path, 'w') as f:
            json.dump(config, f)

    def run_tools(self):
        """تشغيل جميع الأدوات الممكنة"""
        tool_functions = {
            "sherlock": self.run_sherlock,
            "maigret": self.run_maigret,
            "holehe": self.run_holehe,
            "ghunt": self.run_ghunt,
            "whatsmyname": self.run_whatsmyname,
            "blackbird": self.run_blackbird,
            "email2phone": self.run_email2phone,
            "darksearch": self.run_darksearch
        }
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            for tool, func in tool_functions.items():
                if self.config["tools"].get(tool, {}).get("enabled", False):
                    executor.submit(func)
                    self.results["meta"]["tools_used"].append(tool)
                    time.sleep(1)  # تجنب حمل زائد على النظام

    # [الوظائف الخاصة بكل أداة...]
    # يمكنك إضافة الوظائف المحددة لكل أداة هنا
    # مثل run_sherlock(), run_maigret() وغيرها
    
    def save_results(self):
        """حفظ النتائج بطرق متعددة"""
        json_file = os.path.join(self.results_dir, "combined_results.json")
        csv_file = os.path.join(self.results_dir, "combined_results.csv")
        
        # حفظ كـ JSON
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        # حفظ كـ CSV (اختياري)
        try:
            import pandas as pd
            flat_data = []
            for tool, results in self.results["results"].items():
                if isinstance(results, dict):
                    for site, data in results.items():
                        flat_data.append({
                            "tool": tool,
                            "site": site,
                            "data": str(data)
                        })
            
            df = pd.DataFrame(flat_data)
            df.to_csv(csv_file, index=False)
        except ImportError:
            pass
            
        logging.info(f"[+] تم حفظ النتائج في: {json_file}")
        if os.path.exists(csv_file):
            logging.info(f"    - CSV: {csv_file}")

    def run(self):
        """تشغيل العملية الكاملة"""
        try:
            self.setup_environment()
            self.run_tools()
            self.save_results()
        except KeyboardInterrupt:
            logging.info("\n[!] تم إيقاف العملية بواسطة المستخدم")
            sys.exit(1)
        except Exception as e:
            logging.error(f"[!] حدث خطأ: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="أداة OSINT متقدمة")
    parser.add_argument("-e", "--email", help="البريد الإلكتروني للبحث")
    parser.add_argument("-u", "--username", help="اسم المستخدم للبحث")
    parser.add_argument("-c", "--config", help="ملف الإعدادات المخصص")
    
    args = parser.parse_args()
    
    if not args.email and not args.username:
        parser.print_help()
        sys.exit(1)
        
    tool = AdvancedOSINTTool(email=args.email, username=args.username)
    tool.run()

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
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tools_dir = os.path.join(base_dir, "True.Sys.OSintMaster_tools")
        self.results_dir = os.path.join(base_dir, "True.Sys.OSintMaster_results")
        self.venv_dir = os.path.join(base_dir, "venv")
        self.config = self.load_config()

    def load_config(self):
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
            "proxy": {"enabled": False, "list": []}
        }
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return default_config

    def setup_environment(self):
        logging.info("[+] إعداد البيئة...")
        os.makedirs(self.tools_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        self.create_virtualenv()
        self.install_base_requirements()
        self.clone_and_setup_tools()

    def create_virtualenv(self):
        if not os.path.exists(self.venv_dir):
            logging.info("[+] إنشاء بيئة افتراضية...")
            subprocess.run([sys.executable, "-m", "venv", self.venv_dir], check=True)

        os.environ["VIRTUAL_ENV"] = self.venv_dir
        os.environ["PATH"] = f"{os.path.join(self.venv_dir, 'bin')}:{os.environ['PATH']}"
        logging.info("[+] تم تفعيل البيئة الافتراضية.")

    def install_base_requirements(self):
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

        py_requirements = [
            "requests", "beautifulsoup4", "selenium", "lxml", "python-whois",
            "dnspython", "pandas", "tqdm", "pycurl", "urllib3"
        ]
        subprocess.run([os.path.join(self.venv_dir, "bin", "pip"), "install", "--upgrade", "pip"], check=True)
        subprocess.run([os.path.join(self.venv_dir, "bin", "pip"), "install"] + py_requirements, check=True)

    def clone_and_setup_tools(self):
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
        tool_path = os.path.join(self.tools_dir, tool_name)
        if not os.path.exists(tool_path):
            logging.info(f"[+] جاري تنزيل {tool_name}...")
            subprocess.run(["git", "clone", repo_url, tool_path], check=True)
        req_file = os.path.join(tool_path, "requirements.txt")
        if os.path.exists(req_file):
            logging.info(f"[+] جاري تثبيت متطلبات {tool_name}...")
            subprocess.run([os.path.join(self.venv_dir, "bin", "pip"), "install", "-r", req_file], cwd=tool_path, check=True)

    def run(self):
        try:
            self.setup_environment()
            logging.info("[+] تم إكمال الإعداد بنجاح!")
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
    args = parser.parse_args()
    if not args.email and not args.username:
        parser.print_help()
        sys.exit(1)
    tool = AdvancedOSINTTool(email=args.email, username=args.username)
    tool.run()
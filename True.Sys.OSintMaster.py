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
                "tool_name": "True.Sys.OSintMaster",
                "version": "1.0",
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
        self.venv_dir = os.path.join(os.path.dirname(__file__), "venv")

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(config_path) as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("[!] لم يتم العثور على ملف التكوين، يرجى التحقق من المسار.")
            sys.exit(1)

    def setup_environment(self):
        logging.info("[+] إعداد البيئة...")
        os.makedirs(self.tools_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

        if not os.path.exists(self.venv_dir):
            logging.info("[+] البيئة الافتراضية غير موجودة، جاري إنشائها...")
            subprocess.run([sys.executable, "-m", "venv", self.venv_dir], check=True)

        self.activate_venv_and_install_requirements()

    def activate_venv_and_install_requirements(self):
        # تفعيل البيئة الافتراضية وتثبيت المكتبات
        venv_python = os.path.join(self.venv_dir, "bin", "python") if platform.system() != "Windows" else os.path.join(self.venv_dir, "Scripts", "python.exe")
        venv_pip = os.path.join(self.venv_dir, "bin", "pip") if platform.system() != "Windows" else os.path.join(self.venv_dir, "Scripts", "pip.exe")

        if not os.path.exists(venv_python):
            logging.error("[!] لم يتم العثور على Python داخل البيئة الافتراضية")
            sys.exit(1)

        # تثبيت المكتبات المطلوبة مباشرة
        logging.info("[+] تثبيت المكتبات المطلوبة...")

        subprocess.run([venv_pip, "install", "spacy", "requests"], check=True)

    def install_tool(self, tool_name, repo_url):
        tool_path = os.path.join(self.tools_dir, tool_name)
        if not os.path.exists(tool_path):
            logging.info(f"[+] جاري تنزيل {tool_name}...")
            subprocess.run(["git", "clone", repo_url, tool_path], check=True)

    def run_tools(self):
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
        with ThreadPoolExecutor(max_workers=5) as executor:
            for tool, func in tool_functions.items():
                if self.config["tools"].get(tool, {}).get("enabled", False):
                    executor.submit(func)
                    self.results["meta"]["tools_used"].append(tool)

    def run_sherlock(self):
        logging.info("[+] تشغيل Sherlock...")
        tool_path = os.path.join(self.tools_dir, "sherlock")
        subprocess.run([sys.executable, "sherlock.py", self.username], cwd=tool_path, check=True)
    
    def run_maigret(self):
        logging.info("[+] تشغيل Maigret...")
        subprocess.run(["maigret", self.username], check=True)
    
    def run_holehe(self):
        logging.info("[+] تشغيل Holehe...")
        subprocess.run(["holehe", self.email], check=True)
    
    def run_blackbird(self):
        logging.info("[+] تشغيل Blackbird...")
        tool_path = os.path.join(self.tools_dir, "blackbird")
        subprocess.run([sys.executable, "blackbird.py", "-u", self.username], cwd=tool_path, check=True)

    def run_email2phone(self):
        logging.info("[+] تشغيل Email2Phone...")
        tool_path = os.path.join(self.tools_dir, "email2phonenumber")
        subprocess.run([sys.executable, "email2phonenumber.py", "-e", self.email], cwd=tool_path, check=True)

    def run_darksearch(self):
        logging.info("[+] البحث في DarkSearch API...")
        api_key = self.config["tools"]["darksearch"].get("api_key", "")
        if not api_key:
            logging.error("[!] مفتاح API لـ DarkSearch غير متوفر")
            return
        response = requests.get("https://darksearch.io/api/search", params={"query": self.username or self.email}, headers={"Authorization": f"Bearer {api_key}"} )
        if response.status_code == 200:
            self.results["results"]["darksearch"] = response.json()

    def run_whatsmyname(self):
        logging.info("[+] تشغيل WhatsMyName...")
        tool_path = os.path.join(self.tools_dir, "whatsmyname")
        subprocess.run([sys.executable, "whatsmyname.py", "-u", self.username], cwd=tool_path, check=True)

    def save_results(self):
        results_path = os.path.join(self.results_dir, "osint_results.json")
        with open(results_path, "w") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        logging.info(f"[+] تم حفظ النتائج في {results_path}")

    def run_ghunt(self):
        logging.info("[+] تشغيل GHunt...")
        tool_path = os.path.join(self.tools_dir, "ghunt")
        if not os.path.exists(tool_path):
            logging.error("[!] GHunt غير مثبت. يرجى التأكد من تنزيله")
            return
        # تحقق من أن Docker مفعل إذا كانت أداة GHunt تتطلب ذلك
        docker_required = self.config["tools"]["ghunt"].get("docker_required", False)
        if docker_required:
            subprocess.run(["docker", "run", "--rm", "-v", f"{tool_path}:/ghunt", "ghunt"], check=True)
        else:
            subprocess.run([sys.executable, "ghunt.py", "-u", self.username], cwd=tool_path, check=True)

    def run(self):
        self.setup_environment()
        self.run_tools()
        self.save_results()

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

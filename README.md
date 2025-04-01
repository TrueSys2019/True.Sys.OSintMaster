# **True.Sys.OSintMaster - Advanced OSINT Data Collection and Analysis Tool**

## **Description:**

True.Sys.OSintMaster is a powerful and comprehensive tool designed to enable cybersecurity professionals and analysts to gather and analyze data using OSINT (Open Source Intelligence) techniques. This tool provides a flexible and robust interface for retrieving a wide range of sensitive information from various online sources, including social networks, email platforms, websites, and other open databases.

## **Key Features:**

- **Multiple Tool Support:** Integrates with several popular OSINT tools such as Sherlock, Maigret, Holehe, GHunt, and WhatsMyName, allowing you to search for information related to email addresses or usernames across the internet.
  
- **API Integration:** Integrates with advanced tools like Blackbird and Email2Phone via APIs, providing deep and accurate results for email or phone number analysis.

- **Flexible Configuration:** Offers various customization options, such as retry attempts for failed searches and proxy settings to keep your identity private.

- **Results Storage:** Supports saving results in multiple formats (JSON and CSV), making it easy to analyze and document findings.

- **Complete Control Over Tools:** Allows you to activate or deactivate specific OSINT tools as needed via a configuration file.

## **How to Install and Use:**

### **1. Clone the repository:**

First, download the source code of the tool from GitHub:

```bash
git clone https://github.com/your-repository/True.Sys.OSintMaster.git
cd True.Sys.OSintMaster
```

### **2. Run the tool:**

The tool will automatically create the virtual environment and install all required dependencies when you run the main script. Simply run the tool using the following command:

```bash
python3 True.Sys.OSintMaster.py -e "email@example.com" -u "username"
```

Where:

- `-e`: The email address you want to search for.
- `-u`: The username you want to search for.

### **3. View Results:**

Once the process completes, the tool will store the results in the `results` folder. The results will be available in both **JSON** and **CSV** formats, which you can analyze or document as needed.

### **4. Customize Search Tools:**

You can adjust retry attempts and the wait time between retries in case some tools fail by modifying the `config.json` file.

For example, if you want to increase the retry attempts for Sherlock, you can change the `"retry"` value in the config file.

### **5. Enable Logging:**

You can enable logging through the `config.json` settings to keep track of the tool’s activities in a log file for audit and analysis purposes.

## **Example Usage:**

To analyze information related to the email `example@example.com`:

```bash
python3 True.Sys.OSintMaster.py -e "example@example.com"
```

To analyze information related to the username `username123`:

```bash
python3 True.Sys.OSintMaster.py -u "username123"
```

If you need to use specific settings or enable certain tools, simply modify the `config.json` file to activate the tools you need.

## **Requirements:**

- Python 3
- Git
- Required Python libraries such as `requests`, `spacy`, etc., which will be automatically installed when the script is run.

## **Conclusion:**

True.Sys.OSintMaster is a robust and flexible tool for collecting and analyzing data using OSINT techniques. With an easy-to-use interface and various customization options, this tool helps cybersecurity researchers and enthusiasts gather and analyze information from a wide range of online sources quickly and efficiently. Whether you're gathering intelligence on email addresses, usernames, or related data, this tool offers everything you need for thorough online investigation.

---

### **Notes:**

- Once you run the main script, the tool will handle everything automatically, including creating the virtual environment and installing the required tools and libraries.
- If everything is set up correctly, you can begin using the tool right away.

---

This version emphasizes that the script handles the environment setup and tool installations automatically when running, and no additional setup steps are required.

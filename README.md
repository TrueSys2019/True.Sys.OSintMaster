# True.Sys.OSintMaster
 
True.Sys.OSintMaster - Advanced OSINT Data Collection and Analysis Tool

Description:

True.Sys.OSintMaster is a powerful and comprehensive tool designed to enable cybersecurity professionals and analysts to gather and analyze data using OSINT (Open Source Intelligence) techniques. This tool provides a flexible and robust interface for retrieving a wide range of sensitive information from various online sources, including social networks, email platforms, websites, and other open databases.

Key Features:

Multiple Tool Support: Integrates with several popular OSINT tools such as Sherlock, Maigret, Holehe, GHunt, and WhatsMyName, allowing you to search for information related to email addresses or usernames across the internet.

API Integration: Integrates with advanced tools like Blackbird and Email2Phone via APIs, providing deep and accurate results for email or phone number analysis.

Flexible Configuration: Offers various customization options, such as retry attempts for failed searches and proxy settings to keep your identity private.

Results Storage: Supports saving results in multiple formats (JSON and CSV), making it easy to analyze and document findings.

Complete Control Over Tools: Allows you to activate or deactivate specific OSINT tools as needed via a configuration file.

How to Use:

Set Up the Environment:

Install necessary tools on your system using the integrated setup commands.

Ensure that required tools like git, python3, and pip are installed on your machine.

Configure the Tool:

Open the config.json file to customize which tools you want to use. You can enable or disable tools such as Sherlock, Maigret, and Blackbird, and enter any required API keys for specific services.

Optionally, configure proxy settings to maintain anonymity during the OSINT process.

Run the Tool:

Once configured, you can run the tool from the command line using the following syntax:

bash
Copy
Edit
python3 True.Sys.OSintMaster.py -e "email@example.com" -u "username"
Where:

-e: The email address you want to search for.

-u: The username you want to search for.

View Results:

Once the process completes, the tool will store the results in the results folder.

You can find the results in JSON and CSV formats within this folder, which you can analyze or report as needed.

Customize Search Tools:

You can adjust the retry attempts and the wait time between retries in case some tools fail by modifying the config.json file.

For example, if you want to increase the retry attempts for Sherlock, you can change the "retry" value in the config file.

Logging:

Enable logging through the config.json settings to keep track of the tool’s activities in a log file for audit and analysis purposes.

Example Usage:

To analyze information related to the email example@example.com:

bash
Copy
Edit
python3 True.Sys.OSintMaster.py -e "example@example.com"
To analyze information related to the username username123:

bash
Copy
Edit
python3 True.Sys.OSintMaster.py -u "username123"
If you need to use specific settings or enable certain tools, simply modify the config.json file to activate the tools you need.

Requirements:

Python 3

Git

Required Python libraries such as requests, bs4, selenium, lxml, and pandas, which will be automatically installed by the script.

Conclusion: True.Sys.OSintMaster is a robust and flexible tool for collecting and analyzing data using OSINT techniques. With an easy-to-use interface and various customization options, this tool helps cybersecurity researchers and enthusiasts gather and analyze information from a wide range of online sources quickly and efficiently. Whether you're gathering intelligence on email addresses, usernames, or related data, this tool offers everything you need for thorough online investigation.

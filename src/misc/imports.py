
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException

import random
import pandas as pd
import time

from fake_useragent import UserAgent
import requests

import sys
import os

import requests
from requests.auth import HTTPProxyAuth

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from ttkwidgets.autocomplete import AutocompleteEntry
import json

import tkinter as tk
from tkinter import ttk
import os
import time
import importlib
import interface

import tkinter as tk
from interface import InterfaceFrame
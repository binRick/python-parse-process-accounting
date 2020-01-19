#!/usr/bin/env python3
import os, sys, json, parse_process_accounting

print(json.dumps(parse_process_accounting.getStats()))

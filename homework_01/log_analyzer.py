#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gzip
import heapq
import json
import logging
import os
from collections import defaultdict

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./",
    "LOG_DIR": "./",
    "LOGGING_PATH": None,
    "ERRORS_THRESHOLD": 0.1
}


def setup_logging(log_path=None):
    logging.basicConfig(filename=log_path, level=logging.INFO, format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')


def parse_config(config_path):
    try:
        with open(config_path, 'r') as f:
            custom_config = json.load(f)
            config.update(custom_config)
    except FileNotFoundError:
        logging.error("Config file not found.")
        raise
    except json.JSONDecodeError:
        logging.error("Invalid config file format.")
        raise


def get_latest_log_file(log_dir):
    log_files = [f for f in os.listdir(log_dir) if f.startswith("nginx-access-ui.log")]
    if not log_files:
        logging.error("No log files found.")
        return None
    return max(log_files)


def read_log_file(log_file):
    logs = []
    with open(log_file, 'rb') as f:
        if log_file.endswith('.gz'):
            f = gzip.open(log_file, 'rt')
        for line in f:
            logs.append(line)
    return logs


def parse_log_line(line):
    parts = line.split(' ')
    return {
        'url': parts[7],
        'request_time': float(parts[-1])
    }


def process_logs(logs):
    statistics = defaultdict(list)
    total_time = 0
    errors_count = 0
    for log in logs:
        try:
            parsed_log = parse_log_line(log)
            statistics[parsed_log['url']].append(parsed_log['request_time'])
            total_time += parsed_log['request_time']
        except Exception as e:
            logging.error(f"Error parsing log line: {e}")
            errors_count += 1
    if errors_count / len(logs) > config['ERRORS_THRESHOLD']:
        logging.error("Too many errors parsing log lines. Exiting.")
        raise RuntimeError("Too many errors parsing log lines.")
    return statistics, total_time


def generate_report(statistics, total_time, report_size):
    sorted_stats = heapq.nlargest(report_size, statistics.items(), key=lambda x: sum(x[1]))
    report_data = []
    for url, times in sorted_stats:
        url_stats = {
            'url': url,
            'count': len(times),
            'count_perc': len(times) / len(statistics),
            'time_sum': sum(times),
            'time_perc': sum(times) / total_time,
            'time_avg': sum(times) / len(times),
            'time_max': max(times),
            'time_med': sorted(times)[len(times) // 2]
        }
        report_data.append(url_stats)
    return report_data


def save_report(report_data, report_path):
    with open(report_path, 'w') as f:
        json.dump(report_data, f)


def main():
    parser = argparse.ArgumentParser(description='Log Analyzer')
    parser.add_argument('--config', help='Path to the config file')
    args = parser.parse_args()

    if args.config:
        parse_config(args.config)

    setup_logging(config['LOGGING_PATH'])

    latest_log_file = get_latest_log_file(config["LOG_DIR"])
    if not latest_log_file:
        logging.error("No log files found. Exiting.")
        return

    log_path = os.path.join(config["LOG_DIR"], latest_log_file)
    logs = read_log_file(log_path)
    statistics, total_time = process_logs(logs)
    report_data = generate_report(statistics, total_time, config["REPORT_SIZE"])
    report_filename = os.path.join(config["REPORT_DIR"], f"report-{latest_log_file[17:27]}.html")
    save_report(report_data, report_filename)


if __name__ == "__main__":
    main()

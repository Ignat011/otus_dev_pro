import unittest


class TestLogAnalyzer(unittest.TestCase):

    def test_get_latest_log_file(self):
        # log_dir = "./log"
        # os.makedirs(log_dir, exist_ok=True)
        # log_files = ["nginx-access-ui.log-20170630.gz", "nginx-access-ui.log-20170701.gz"]
        # for log_file in log_files:
        #     with open(os.path.join(log_dir, log_file), 'w') as f:
        #         f.write("test")
        # latest_log_file = get_latest_log_file(log_dir)
        # self.assertEqual(latest_log_file, "nginx-access-ui.log-20170701.gz")
        # os.rmdir(log_dir)
        pass

    def test_parse_config(self):
        # config_path = "./test_config.json"
        # config_data = {
        #     "REPORT_SIZE": 100,
        #     "REPORT_DIR": "./test_reports",
        #     "LOG_DIR": "./test_logs",
        #     "ERRORS_THRESHOLD": 0.2
        # }
        # with open(config_path, 'w') as f:
        #     json.dump(config_data, f)
        # self.assertEqual(config["REPORT_SIZE"], 100)
        # self.assertEqual(config["REPORT_DIR"], "./reports")
        # self.assertEqual(config["LOG_DIR"], "./log")
        # self.assertEqual(config["ERRORS_THRESHOLD"], 0.2)
        # os.remove(config_path)
        pass


if __name__ == "__main__":
    unittest.main()


import requests
import json
import datetime
import time

from st2actions.runners.pythonrunner import Action


class ArteriaAnalysisServiceAction(Action):

    START_COMMAND = "start"
    POLL_COMMAND = "poll"

    COMMANDS = [START_COMMAND, POLL_COMMAND]

    def _verify_command_valid(self, cmd):
        return cmd in self.COMMANDS

    def run(self, cmd, url, analysis_body=None, status_url=None, sleep=None):

        if not self._verify_command_valid(cmd):
            self.logger.error("Command: {} is not valid. Valid commands are: {}".format(cmd, self.COMMANDS))
            return False, ""

        if cmd == self.START_COMMAND:
            return self.start_analysis(url, analysis_body)
        else:
            pass
            #return self.poll_analysis_instance(status_url, sleep)

    def start_analysis(self, url, analysis_body):
        if not url:
            self.logger.error("You have to specify a url to start!")
            return False, ""

        start_url = "{}/api/1.0/start".format(url)

        if analysis_body:
            analysis_body = json.loads(analysis_body)
        else:
            analysis_body = ""

        response = requests.post(start_url, data=json.dumps(analysis_body))
        #print(response.json())
        return False, response.text

"""     def poll_analysis_instance(self, status_url, sleep):

        retry_attempts = 0
        max_retries = 3
        state = "started"

        while state == "started" or state == "pending" or not state:
            current_time = datetime.datetime.now()

            resp = requests.get(status_url)
            json_resp = resp.json()
            state = json_resp["state"]

            if state == "started" or state == "pending":
                self.logger.info("{0} -- {1} returned state {2}. Sleeping {3}m until retrying again...".format(current_time,
                                                                                                               status_url,
                                                                                                               state,
                                                                                                               sleep))
                time.sleep(sleep)
            elif state == "done":
                self.logger.info("{0} -- {1} returned state {2}. Will now stop polling the status.".format(current_time,
                                                                                                           status_url,
                                                                                                           state))

                return True, json_resp
            elif state in ["error", "none", "cancelled"]:
                self.logger.warning("{0} -- {1} returned state {2}. Will now stop polling the status.".format(current_time,
                                                                                                              status_url,
                                                                                                              state))
                return False, json_resp

            elif not state and retry_attempts < max_retries:
                retry_attempts += 1
                self.logger.warning("{0} -- {1} did not report state. "
                                    "Probably due to a connection error, "
                                    "will retry. Attempt {2} of {3}.".format(current_time,
                                                                             status_url,
                                                                             retry_attempts,
                                                                             max_retries))
                time.sleep(sleep)
            else:
                self.logger.error("{0} -- {1} returned state unknown state {2}. "
                                  "Will now stop polling the status.".format(current_time, status_url, state))
                return False, json_resp """


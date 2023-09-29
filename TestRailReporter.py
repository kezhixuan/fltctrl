import re
import os
import pymsteams

from robot.api import ResultVisitor, ExecutionResult
from robot import rebot
from testrail import APIClient, APIError
from datetime import datetime

login_via_sims = os.getenv('LOGIN_VIA_SIMS', default="false")
job_path_dir = os.getenv('JOB_PATH')
plan_id = os.getenv('TEST_PLAN_ID')
stage_name = os.getenv('STAGE_NAME')
branch_name = os.getenv('FEATURE_BRANCH_NAME')
output_file = f"{job_path_dir}/bulk_report.xml"
root_folder = f"{job_path_dir}/"
job_status = os.getenv('CI_JOB_STATUS')
record_videos = os.getenv('RECORD_VIDEO_OF_TEST_CASE')
report_to_test_rail = os.getenv('REPORT_TO_TEST_RAIL')
job_triggerer_user_id = os.getenv('GITLAB_USER_NAME')
log_file_template = 'testcaseid='
old_bug_tag = "[OLD BUG]"
in_maintenance_tag = "[IN MAINTENANCE]"


def _get_star_version(file_name):
    with open(file_name) as f:
        version_number = ''
        for line in f:
            match_string = re.search(r"\{STAR_VERSION_LABEL\}\s=\sStar\s+(\d+\.?)+", line)
            if match_string is not None:
                string_result = match_string.group()
                version_number = re.search(r"(\d+\.?)+", string_result).group()
                break
    return version_number


fetched_star_version = _get_star_version(output_file)
if fetched_star_version == "":
    star_version = "No info"
else:
    star_version = fetched_star_version


class TestResult:
    def __init__(self, testcase_id, test_status, message, test_name, tag_for_separate_section, duplicate_test_name, jira_id):
        self.testcase_id = testcase_id
        self.test_status = test_status
        self.message = message
        self.test_name = test_name
        self.tag_for_separate_section = tag_for_separate_section
        self.duplicate_test_name = duplicate_test_name
        self.jira_id = jira_id


class ResultForTeams:
    total_counter = 0
    test_count = 0
    fail_counter = 0
    separate_section_counter = 0
    passed_tests_section_counter = 0
    # comments_section_counter = 0
    fail_message_body = ""
    separate_section_message_body = ""
    passed_tests_section_message_body = ""
    # comments_section_message_body = ""
    warning_message = "  \n**Over 100 Test Cases Failed, not all are printed in this message**  \n  "
    
    def __init__(self):
        pass

    def increase_test_count(self, number):
        self.test_count += number

    def increase_fail_counter(self, number):
        self.fail_counter += number
    
    def increase_counter_separate_section(self, number):
        self.separate_section_counter += number

    def increase_counter_passed_tests_section(self, number):
        self.passed_tests_section_counter += number

    # def increase_counter_comments_section(self, number):
    #    self.comments_section_counter += number

    def get_pass_percentage(self):
        total_counter = self.fail_counter + self.separate_section_counter
        return 100 - total_counter / self.test_count * 100
    
    def append_fail_message_body(self, test_result):
        if self.total_counter <= 100:
            self.fail_message_body += f'{self.fail_counter}. {test_result.test_name}\r'
    
    def get_fail_message_body(self):
        return self.fail_message_body

    def append_separate_section_message_body(self, test_result):
         self.separate_section_message_body += f'{self.separate_section_counter}. {test_result.tag_for_separate_section} - [{test_result.jira_id}] - {test_result.test_name}\r'

    def get_separate_section_message_body(self):
        return self.separate_section_message_body
    
    def append_passed_tests_section_message_body(self, test_result):
        self.passed_tests_section_message_body += f'{self.passed_tests_section_counter}. [{test_result.jira_id}] - {test_result.test_name} <=> {test_result.duplicate_test_name}\r'
    
    def get_passed_tests_section_message_body(self):
        return self.passed_tests_section_message_body

    # def append_comments_section_message_body(self, test_result):
    #     self.comments_section_message_body += (f"{self.comments_section_counter}. PLEASE NOTE: Test case '{test_result.test_name}', which was failing in previous releases, now passes.<br/>"
    #                                           f"Please re-check the results and (if necessary) adjust the tags in Robot Framework test case code.<br/>"
    #                                           f"Additionally, if available, please remove the corresponding temporary test case from running in the pipeline.\r")

    # def get_comments_section_message_body(self):
    #     return self.comments_section_message_body

    def generate_fail_test_message(self):
        warning_message = ""
        total_counter = self.get_total_counter()
        pass_percentage = self.get_pass_percentage()
        message_body = self.get_fail_message_body()
        if self.total_counter > 100:
            warning_message = self.warning_message
        return f"**Results summary: {self.test_count} tests total, {self.test_count - total_counter} Passed ({pass_percentage:.2f}%)**  \n {warning_message} \n \
              Failed Test Cases:        \n {message_body} \n"
        
    def generate_separate_section_message(self):
        message_body = self.get_separate_section_message_body()
        return f"** ** \n \
              Recurring Fails:       \n {message_body} \n"
    
    def generate_passed_tests_section_message(self):
        message_body = self.get_passed_tests_section_message_body()
        return f"** ** \n \
              Passed Tests That Have 'OLD BUG' Or 'IN MAINTENANCE' Status - please verify if the bug/maintenance issue still occurs and optionally remove tags and temporary test cases accordingly:     \n {message_body} \n"
        
    # def generate_comments_section_message(self):
    #     message_body = self.get_comments_section_message_body()
    #     return f"** ** \n \
    #          Additional Comments:          \n {message_body} \n \
    #          \n"

    def get_total_counter(self):
        return self.fail_counter + self.separate_section_counter


class TestRailReporter(ResultVisitor):

    def __init__(self):
        self.results = []

    def visit_test(self, test):

        if self.start_test(test) is not False:
            if test.message:
                message = _remove_html_tags(test.message)
                message = _format_message(message)
            else:
                message = ""
            try:
                testcase_id = _get_testcaseid_from_tag(test.tags, test.name)
                if testcase_id is not None:
                    tag_for_separate_section = _get_tag_for_separate_section(test.tags)
                    duplicate_test_name = _get_duplicate_test_name(tag_for_separate_section, test.name)
                    jira_id = _get_jira_id_tag(test.tags)
                    self.results.append(
                        TestResult(testcase_id, test.status, message, test.name, tag_for_separate_section, duplicate_test_name, jira_id))
            except IndexError:
                print(f'Verify TestRail Mapping for test case: {test.name}')
            self.end_test(test)


def _create_run(testplan_id, section_name, name_of_branch, test_ids, app_version):
    curr_date = datetime.today().strftime('%T %d-%m-%Y')
    if login_via_sims == "true":
        run_name = f'{star_version} login via SIMS {curr_date}'
    else:
        run_name = f'{star_version} {curr_date}'
    desc = f'Test Section: {section_name} ' \
           f'\nDate: {curr_date}' \
           f'\nBranch: {name_of_branch}' \
           f'\nSTAR version: {app_version}'
    url = f'add_plan_entry/{testplan_id}'
    print(test_ids)
    result = client.send_post(
        url,
        {'suite_id': 1154, 'description': desc,
         'name': run_name, 'include_all': False,
         'case_ids': test_ids}
    )
    return result['runs'][0]['id']


def _create_bulk_result_and_logs_for_failed_tests(visitor, outputfile_path):
    bulk_result = []
    print(f'available results are {visitor.results}')
    for result in visitor.results:
        if result.test_status == 'PASS':
            if "Old status: FAIL" in result.message:
                bulk_result.append({"status_id": '11',
                                    "case_id": result.testcase_id,
                                    "comment": f"Test passed during re-test, previous test message: {result.message}"})
            else:
                bulk_result.append({"status_id": '1',
                                    "case_id": result.testcase_id,
                                    "comment": "Test case passed, no fails occurred"})

        elif result.test_status == 'FAIL':
            fail_message = f"Test case failed with following message:" \
                           f"{result.message}" \
                           f" For more info please check attached files:"
            bulk_result.append({'status_id': '5',
                                'case_id': result.testcase_id,
                                'comment': fail_message})
            testcase_id_tag = f'{log_file_template}{result.testcase_id}'
            rebot(outputfile_path, outputdir=root_folder, include=testcase_id_tag, log=testcase_id_tag, report=None)
        else:
            bulk_result.append({"status_id": '10',
                                "case_id": result.testcase_id,
                                "comment": 'Test case was skipped/untested'})
    return bulk_result


def _add_results(testrun_id, bulk_result):
    url = f'add_results_for_cases/{testrun_id}'
    result = client.send_post(
        url,
        {"results": bulk_result}
    )
    return result


def _remove_html_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', text)


def _format_message(text):
    text = text.replace("*HTML*", "")
    text = text.replace('New status', "\nNew status")
    text = text.replace('New message', "\nNew message")
    text = text.replace('Old message', "\nOld message")
    text = text.replace('Old status', "\nOld status")
    return text


def _get_testcaseid_from_tag(tag_list, test_case_name):
    for tag in tag_list:
        if "testcaseid" in tag:
            tc_id = tag.replace('testcaseid=', '')
            return tc_id
        else:
            tc_id = None
    if tc_id is None:
        print(f'No test case id found in {test_case_name}')
    return tc_id


def _get_jira_id_tag(tag_list):
    jira_id = "NO_JIRA_ID"
    for tag in tag_list:
        if "jira_id" in tag:
            jira_id = tag.replace('jira_id=', '')
            break
    return jira_id


def _get_tag_for_separate_section(tag_list):
    tag = None
    if "old_bug" in tag_list:
        tag = old_bug_tag
    elif "in_maintenance" in tag_list:
        tag = in_maintenance_tag
    return tag


def _get_duplicate_test_name(tag_for_separate_section, test_name):
    duplicate_test_name = None
    if tag_for_separate_section is not None:
        duplicate_test_name = "Temporary TC For " + test_name
    return duplicate_test_name


def _generate_message():
    teams_result = ResultForTeams()
    message = ""
    for test_result in visitor.results:
        teams_result.increase_test_count(1)
        if test_result.test_status == 'FAIL' and test_result.tag_for_separate_section is None:
            teams_result.increase_fail_counter(1)
            teams_result.append_fail_message_body(test_result)
        elif test_result.test_status == 'FAIL' and test_result.tag_for_separate_section is not None:
            teams_result.increase_counter_separate_section(1)
            teams_result.append_separate_section_message_body(test_result)
        elif test_result.test_status == 'PASS' and test_result.tag_for_separate_section is not None:
            teams_result.increase_counter_passed_tests_section(1)
            teams_result.append_passed_tests_section_message_body(test_result)
            # teams_result.increase_counter_comments_section(1)
            # teams_result.append_comments_section_message_body(test_result)
    pass_percentage = teams_result.get_pass_percentage()
    fail_tests_message = teams_result.generate_fail_test_message()
    recurring_tests_message = teams_result.generate_separate_section_message()
    pass_recurring_tests_message = teams_result.generate_passed_tests_section_message()
    # additional_comments_message = teams_result.generate_comments_section_message()
    if teams_result.get_fail_message_body() != "":
        message += fail_tests_message
    if teams_result.get_separate_section_message_body() != "":
        message += recurring_tests_message
    if teams_result.get_passed_tests_section_message_body() != "":
        message += pass_recurring_tests_message
    # if teams_result.get_comments_section_message_body() != "":
    #     message += additional_comments_message
    return pass_percentage, message


def _report_to_teams(test_rail_link=False):
    pass_percentage, message = _generate_message()
    teams = pymsteams.cardsection()
    teams.activityText(message)
    teams_connection_card = os.getenv('TEAMS_CONNECTION_CARD')
    card = pymsteams.connectorcard(teams_connection_card)
    print(message)

    if pass_percentage < 90:
        card.color("red")
    elif pass_percentage == 100:
        card.color("00ff00")
    else:
        card.color("ffff00")
    card.addSection(teams)
    ci_pipeline_url = os.getenv('CI_PIPELINE_URL')
    card.addLinkButton("Gitlab", f"{ci_pipeline_url}")
    if test_rail_link:
        try:
            card.addLinkButton("TestRail",
                               f"https://dbschenker.testrail.io/index.php?/runs/view/{test_run_id}")
        except NameError:
            print("Test Rail report was not generated, link not added")
    card.text(
        f"**Triggered by:  {job_triggerer_user_id}  \nStage:  \t{stage_name}  \nBranch:  \t{branch_name}  \nSTAR Version:  \t{star_version}**")
    card.send()


visitor = TestRailReporter()
result = ExecutionResult(output_file)
result.visit(visitor)

if report_to_test_rail == "true":
    client = APIClient('https://dbschenker.testrail.io')
    client.user = os.getenv('TESTRAIL_USER')
    client.password = os.getenv('TESTRAIL_PASSWORD')

    test_run_id = _create_run(plan_id, stage_name, branch_name,
                              [item.testcase_id for item in visitor.results], star_version)
    bulk_result = _create_bulk_result_and_logs_for_failed_tests(visitor, output_file)
    test_rail_results = _add_results(test_run_id, bulk_result)

    print('Sending Attachments')
    result_ids = [[index, result['id']] for index, result in enumerate(test_rail_results) if result['status_id'] != 1]
    print(result_ids)

    for result in result_ids:
        test_id = visitor.results[result[0]].testcase_id
        print(f'Sending attachment for testcase id C{test_id}')
        response = 'No response yet'
        try:
            if os.path.exists(f'{root_folder}/{test_id}.jpeg'):
                response = client.send_post(
                    f'add_attachment_to_result/{result[1]}',
                    f'{root_folder}/{test_id}.jpeg'
                )
            elif os.path.exists(f'{root_folder}/{test_id}.webm'):
                response = client.send_post(
                    f'add_attachment_to_result/{result[1]}',
                    f'{root_folder}/{test_id}.webm'
                )
            response = client.send_post(
                f'add_attachment_to_result/{result[1]}',
                f'{root_folder}/{log_file_template}{test_id}.html'
            )
        except FileNotFoundError:
            print(f'Attachment for testcase id C{test_id} does not exist')
        except APIError:
            print(f"Sending Attachment failed: {response}")
        print(response)

    _report_to_teams(test_rail_link=True)

if report_to_teams == "true":
    _report_to_teams()

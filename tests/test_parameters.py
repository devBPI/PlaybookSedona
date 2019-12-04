import re
import unittest

from yaml import load, SafeLoader

OUTPUT_TEMPLATE = 'templates/project_vars.yml.j2'
SETUP_PLAYBOOK = 'initial_setup.yml'
DEPLOY_PLAYBOOK = 'deploy.yml'
AFTER_UPDATE_TASKS = 'tasks/after_update.yml'


def load_playbook_yaml(playbook_filename: str):
    playbook_file = open(playbook_filename, 'r', encoding='utf-8')
    playbook_yaml = load(playbook_file, Loader=SafeLoader)
    playbook_file.close()
    return playbook_yaml


class CheckParameterListConsistency(unittest.TestCase):
    parameter_list = []

    def setUp(self) -> None:
        super().setUp()
        template_file = open(OUTPUT_TEMPLATE, 'r', encoding='utf-8')
        yaml_template = load(template_file, Loader=SafeLoader)
        self.parameter_list = yaml_template.keys()
        template_file.close()

    def test_setup_playbook(self):
        setup_yaml = load_playbook_yaml(SETUP_PLAYBOOK)
        prompt_list = [var_prompt['name'] for var_prompt in setup_yaml[0]['vars_prompt']]

        self.assertCountEqual(self.parameter_list, sorted(prompt_list))

    def test_deploy_playbook(self):
        deploy_yaml = load_playbook_yaml(DEPLOY_PLAYBOOK)
        assert_list = []
        for task in deploy_yaml[0]['pre_tasks']:
            if task['name'] == 'BPI — Vérification de la configuration':
                assert_list = task['assert']['that']
                break

        vars_list = [one_assert.replace(' is defined', '') for one_assert in assert_list]

        self.assertCountEqual(self.parameter_list, vars_list)

    def test_post_update_tasklist(self):
        after_update_tasks_yaml = load_playbook_yaml(AFTER_UPDATE_TASKS)
        replace_items = []
        for task in after_update_tasks_yaml:
            if task['name'] == 'Fill config values':
                replace_items = task['loop']
                break

        extracted_parameter = []
        for replace_task in replace_items:
            extracted_parameter = extracted_parameter + re.findall(r'app_config_\w+', replace_task['replace'])

        reference_app_parameters = [param for param in self.parameter_list if re.match(r'^app_config', param)]
        self.assertCountEqual(reference_app_parameters, extracted_parameter)


if __name__ == '__main__':
    unittest.main()

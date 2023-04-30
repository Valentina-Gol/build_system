from unittest import TestCase
from build_system import BuildSystem
from io import StringIO
import sys


class TestBuildSystem(TestCase):
    def setUp(self) -> None:
        self.build_system = BuildSystem()

    def test_load_yaml(self):
        file_name = "file"
        with self.assertRaises(OSError) as err:
            data = self.build_system.load_yaml(file_name)
        self.assertEqual("File file not found.", str(err.exception))

        file_name = "./tests/incorrect.yaml"
        data = self.build_system.load_yaml(file_name)
        self.assertEqual(data, None)

        file_name = "./tests/tasks1.yaml"
        data = self.build_system.load_yaml(file_name)
        self.assertEqual(data, {'tasks': [{'name': 'bring_black_leprechauns',
                                           'dependencies': []}]})

    def test_load_resources(self):
        tasks_file_name = "./tests/not_tasks.yaml"
        builds_file_name = "./tests/not_builds.yaml"
        with self.assertRaises(ValueError) as err:
            self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.assertEqual("Incorrect tasks format.", str(err.exception))

        tasks_file_name = "./tests/tasks1.yaml"
        builds_file_name = "./tests/not_builds.yaml"
        with self.assertRaises(ValueError) as err:
            self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.assertEqual("Incorrect builds format.", str(err.exception))

        tasks_file_name = "./tests/tasks1.yaml"
        builds_file_name = "./tests/builds2.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.assertEqual(self.build_system.builds,
                         {'approach_important': ['map_gray_centaurs']})
        self.assertEqual(self.build_system.tasks,
                         {'bring_black_leprechauns': []})

    def test_build_task_graph(self):
        tasks_file_name = "./tests/tasks2.yaml"
        builds_file_name = "./tests/builds1.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.build_system.build_tasks_graph(self.build_system.tasks)
        self.assertEqual(self.build_system.graph.number_of_edges(), 25)
        self.assertEqual(self.build_system.graph.number_of_nodes(), 31)

    def test_find_tasks_sequence(self):
        self.build_system.build_tasks_graph({})
        check = self.build_system.find_tasks_sequence("build_blue_leprechauns")
        true_res = []
        self.assertEqual(check, true_res)

        tasks_file_name = "./tests/tasks2.yaml"
        builds_file_name = "./tests/builds1.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.build_system.build_tasks_graph(self.build_system.tasks)
        check = self.build_system.find_tasks_sequence("build_blue_leprechauns")
        true_res = ['bring_purple_leprechauns', 'build_blue_leprechauns']
        self.assertEqual(check, true_res)

    def test_find_seq(self):
        all_dependencies = {'map_gray_centaurs': ['read_purple_centaurs',
                                                  'train_silver_centaurs'],
                            'train_silver_centaurs': ['design_black_centaurs',
                                                      'upgrade_blue_centaurs']}
        task_name = "map_gray_centaurs"
        true_seq = ['read_purple_centaurs', 'design_black_centaurs',
                    'upgrade_blue_centaurs', 'train_silver_centaurs',
                    'map_gray_centaurs']
        self.assertEqual(self.build_system.find_seq(task_name,
                                                    all_dependencies),
                         true_seq)

        self.assertEqual(self.build_system.find_seq("random_name",
                                                    all_dependencies),
                         ["random_name"])

    def test_list_tasks(self):
        tasks_file_name = "./tests/tasks1.yaml"
        builds_file_name = "./tests/builds2.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.list_tasks()
        sys.stdout = sys.__stdout__
        true_output = "List of available tasks:\n* bring_black_leprechauns\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

    def test_list_builds(self):
        tasks_file_name = "./tests/tasks1.yaml"
        builds_file_name = "./tests/builds2.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.list_builds()
        sys.stdout = sys.__stdout__
        true_output = "List of available builds:\n* approach_important\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

    def test_get_task_info(self):
        tasks_file_name = "./tests/tasks1.yaml"
        builds_file_name = "./tests/builds2.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.get_task_info("task_name")
        sys.stdout = sys.__stdout__
        true_output = "Task task_name is not exist.\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.get_task_info("bring_black_leprechauns")
        sys.stdout = sys.__stdout__
        true_output = "Task info:\n* name: bring_black_leprechauns\n* " \
                      "dependencies: []\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

    def test_get_build_info(self):
        tasks_file_name = "./tests/tasks2.yaml"
        builds_file_name = "./tests/builds1.yaml"
        self.build_system.load_resources(tasks_file_name, builds_file_name)
        self.build_system.build_tasks_graph(self.build_system.tasks)
        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.get_build_info("build_name")
        sys.stdout = sys.__stdout__
        true_output = "Build build_name is not exist.\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

        captured_ouput.close()
        captured_ouput = StringIO()
        sys.stdout = captured_ouput
        self.build_system.get_build_info("approach_important")
        sys.stdout = sys.__stdout__
        true_output = "Build info:\n* name: approach_important\n* tasks: " \
                      "read_purple_centaurs, design_black_centaurs, " \
                      "upgrade_blue_centaurs, train_silver_centaurs, " \
                      "map_gray_centaurs\n"
        self.assertEqual(captured_ouput.getvalue(), true_output)

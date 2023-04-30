import yaml
import os
from typing import Optional, Dict, Any, List
import networkx as nx
import argparse


class BuildSystem:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.builds = {}
        self.tasks = {}

    def load_yaml(self, file_name: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(file_name):
            raise OSError(f"File {file_name} not found.")
        with open(file_name, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                data = None
        return data

    def load_resources(self, tasks_path: str = "tasks.yaml",
                       builds_path: str = "builds.yaml") -> None:
        tasks = self.load_yaml(tasks_path)
        builds = self.load_yaml(builds_path)
        if "tasks" not in tasks:
            raise ValueError("Incorrect tasks format.")
        if "builds" not in builds:
            raise ValueError("Incorrect builds format.")
        self.tasks = {}
        self.builds = {}
        tasks = tasks["tasks"]
        builds = builds["builds"]
        for task in tasks:
            self.tasks[task["name"]] = task["dependencies"]
        for build in builds:
            self.builds[build["name"]] = build["tasks"]

    def build_tasks_graph(self, tasks: Dict[str, list]) -> None:
        for task in tasks:
            name = task
            dependencies = tasks[name]
            if len(dependencies) == 0:
                self.graph.add_node(name)
            else:
                for dep in dependencies:
                    self.graph.add_edge(name, dep)

    def find_tasks_sequence(self, task_name: str) -> List[str]:
        if task_name not in self.graph.nodes:
            return []
        all_dependencies = nx.dfs_successors(self.graph, task_name)
        return self.find_seq(task_name, all_dependencies)

    def find_seq(self, task_name: str,
                 all_dependencies: Dict[str, Any]) -> List[str]:
        task_dep = all_dependencies[task_name] \
            if task_name in all_dependencies else []
        res = []
        for dep in task_dep:
            if dep not in all_dependencies:
                res.append(dep)
            else:
                dep_list = self.find_seq(dep, all_dependencies)
                res.extend(dep_list)
        res.append(task_name)
        return res

    def list_tasks(self) -> None:
        print("List of available tasks:")
        for task in self.tasks:
            print(f"* {task}")

    def list_builds(self) -> None:
        print("List of available builds:")
        for build in self.builds:
            print(f"* {build}")

    def get_task_info(self, task_name: str) -> None:
        if task_name not in self.tasks:
            print(f"Task {task_name} is not exist.")
            return
        print("Task info:")
        print(f"* name: {task_name}")
        dep = ', '.join(self.tasks[task_name]) \
            if len(self.tasks[task_name]) > 0 else "[]"
        print(f"* dependencies: {dep}")

    def get_build_info(self, build_name: str) -> None:
        if build_name not in self.builds:
            print(f"Build {build_name} is not exist.")
            return
        print("Build info:")
        print(f"* name: {build_name}")
        tasks = self.builds[build_name]
        res_tasks = []
        for task in tasks:
            res_tasks.extend(self.find_tasks_sequence(task))
        print(f"* tasks: {', '.join(res_tasks)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", type=str, help="Print list available tasks "
                                                 "or builds. Usage: "
                                                 "build_system.py "
                                                 "--tasks|builds",
                        nargs=1)
    parser.add_argument("--get", type=str, help="Print task or build "
                                                "information. Usage: "
                                                "build_system.py --get "
                                                "task|build "
                                                "<task_name|build_name>",
                        nargs=2)
    parser.add_argument("--dir", type=str, help="Change directory with files."
                                                "Usage: "
                                                "build_system.py --dir "
                                                "<dir_name>",
                        nargs=1, default=".")
    args = parser.parse_args()
    list_ = args.list
    get_ = args.get
    dir_ = args.dir
    build_system = BuildSystem()
    build_system.load_resources(str(os.path.join(dir_, "tasks.yaml")),
                                str(os.path.join(dir_, "builds.yaml")))
    if list_:
        if list_[0] == "tasks":
            build_system.list_tasks()
        elif list_[0] == "builds":
            build_system.list_builds()
    if get_:
        if get_[0] == "task":
            build_system.get_task_info(get_[1])
        elif get_[0] == "build":
            build_system.build_tasks_graph(build_system.tasks)
            build_system.get_build_info(get_[1])

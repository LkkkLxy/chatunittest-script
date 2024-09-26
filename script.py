import os
import subprocess
import logging
import re
import json
from typing import List, Union

# 配置日志
logging.basicConfig(level=logging.INFO, filename='coverage_analyzer.log', filemode='w')
logger = logging.getLogger(__name__)

# JACOCO覆盖率分析器路径，改成自己的jar包位置
JACOCO_COVERAGE_JAR_PATH = "/home/othertest/jacoco_analyzer/target/coverage-1.0-SNAPSHOT.jar"
# 测试执行文件，改成自己的exec文件位置
exec_file_path = "/home/othertest/books/target/jacoco.exec"
# 包含目标类文件的目录路径，改成自己的目录路径
class_file_path = "/home/othertest/books/target/classes"
# 测试文件路径，改成自己的测试文件路径
project_path = "/home/othertest/books"

class CoverageAnalyzer:
    def __init__(self, project_path: str, class_name: str, total_class_name: str,method_name: str,class_file_path: str):
        self.project_path = project_path
        self.class_name = class_name
        self.total_class_name = total_class_name
        self.method_name = method_name
        self.class_file_path = class_file_path
        self.key = "coverage_result"
        self.apt_result = {}

    def run_mvn_chatunitest(self) -> Union[None, str]:
        command = f"mvn chatunitest:method -DselectMethod={self.class_name}#{self.method_name}"
        try:
            logger.info(f"Executing command: {command} in {self.project_path}")
            result = subprocess.run(command, shell=True, cwd=self.project_path, capture_output=True, text=True)
            logger.info(result.stdout)
            if result.stderr:
                logger.error(result.stderr)  # 打印错误输出
            result.check_returncode()  # 检查返回码

            # 执行第二个命令
            copy_command = "mvn chatunitest:copy"
            logger.info(f"Executing command: {copy_command} in {self.project_path}")
            copy_result = subprocess.run(copy_command, shell=True, cwd=self.project_path, capture_output=True, text=True)
            logger.info(copy_result.stdout)
            if copy_result.stderr:
                logger.error(copy_result.stderr)  # 打印错误输出
            copy_result.check_returncode()  # 检查返回码

            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing Maven chatunitest command: {e.stderr}")
            return None

    def run_mvn_test(self, testclass_name: str,method_name: str) -> Union[None, str]:
        command = f"mvn test -Dtest={testclass_name}_{method_name}*"
        try:
            logger.info(f"Executing command: {command} in {self.project_path}")
            result = subprocess.run(command, shell=True, cwd=self.project_path, capture_output=True, text=True)
            logger.info(result.stdout)
            if result.stderr:
                logger.error(result.stderr)  # 打印错误输出
            result.check_returncode()  # 检查返回码
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing Maven command: {e.stderr}")
            return None

    def run_jacoco_coverage_analyzer(self, exec_file_path: str) -> Union[None, dict]:
        try:
            command = [
                "java", "-jar", JACOCO_COVERAGE_JAR_PATH,
                exec_file_path,
                self.class_file_path,
                self.total_class_name,
                self.method_name
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(result.stdout)
            print(result)

            # 假设 result.stdout 是以某种方式格式化的 JSON 字符串
            # return json.loads(result.stdout)  # 将字符串转换为字典

        except subprocess.CalledProcessError as e:
            logger.error(f"Jacoco coverage analysis failed: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    def run_apt_test(self) -> Union[bool, str]:
        # 首先执行 chatunitest 命令
        chatunitest_status = self.run_mvn_chatunitest()
        if chatunitest_status is None:
            return False, "run_mvn_chatunitest error"

        # 尝试执行 mvn test，但不让它影响后续步骤
        try:
            status = self.run_mvn_test(testclass_name=self.class_name, method_name=self.method_name)
            if status is None:
                logger.warning("mvn test failed, proceeding with coverage analysis.")
        except Exception as e:
            logger.error(f"Test failed for class {self.class_name}: {e}")

        # 进行覆盖率分析
        try:
            self.run_jacoco_coverage_analyzer(exec_file_path=exec_file_path)
        except Exception as e:
            logger.error(f"Failed to get coverage for class {self.class_name}: {e}")
            return False, "Coverage analysis failed"

        # logger.info(f"Generated coverage result: {coverage_result}")
        # if coverage_result is None:
        #     return False, "No coverage result found"

        # self.apt_result[self.key] = coverage_result.get(self.method_name, "No coverage data available")
        # return True, "Coverage analysis completed successfully"

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze method coverage using Maven and JaCoCo.")
    parser.add_argument("input", help="Input format: com.aidanwhiteley.books.service.UserService[Optional<User>]createOrUpdateActuatorUser()")

    args = parser.parse_args()

    # 使用正则表达式解析类名和方法名
    match = re.match(r'([^[]+)\[.*?\](\w+)\(\)', args.input)
    if match:
        class_name = match.group(1).split('.')[-1]  # 提取类名，保留最后一个部分
        total_class_name = match.group(1).replace('.', '/')
        method_name = match.group(2)  # 提取方法名

        # 创建 CoverageAnalyzer 实例并运行测试
        analyzer = CoverageAnalyzer(project_path, class_name,total_class_name,method_name,class_file_path)
        result = analyzer.run_apt_test()
    else:
        logger.error("Input format is incorrect. Please use: com.aidanwhiteley.books.service.UserService[Optional<User>]createOrUpdateActuatorUser()")